"""

# Descrizione:
lo script permette di generare un database dai file aventi le estensioni specificate
nelle directory selezionate (vedi il file config.json).
essi vengono cercati ed inseriti nel database costruendo uno schema logico tra canzoni, artisti e album
le informazioni non presenti nei metadati vengono completate tramite l'utilizzo delle webapi di last.fm


# Funzionamento:
1. inizializzazione
2. scansione cartelle e creazione canzoni grezze
3. creazione artisti
4. creazione album
5. creazione canzoni finali
6. ottenimento biografie e immagini (webapi lastfm)
7. ottenimento cover (webapi lastfm)
8. print dei risultati


# Note:
- sqlite3.connect() crea un file nuovo nel caso non esista quello specificato
- nell'esecuzione della query posso specificare i parametri con il ?
- per recuperare il percorso del file corrente usare os.path.dirname(os.path.abspath(__file__))]


# Chiamate last.fm
- ottenimento artista:      http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist=ARTIST_NAME&api_key=YOUR_API_KEY&format=json
- ottenimento album:        http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=YOUR_API_KEY&artist=ARTIST_NAME&album=ALBUM_NAME&format=json


# Note chiamate
- per le immagini utilizzo l'etichetta extralarge (indice 3)


# Link utili:
- errore pip pytaglib:      https://stackoverflow.com/questions/48511211/pip-installing-pytaglib-error
- guida utilizzo sqlite3:   http://www.sqlitetutorial.net/sqlite-python/creating-database/
                            https://docs.python.org/2/library/sqlite3.html
- documentazione pytaglib:  https://pypi.org/project/pytaglib/1.4.1/
- documentazione api last:  https://www.last.fm/api
- rimozione spazi testo:    http://www.datasciencemadesimple.com/remove-spaces-in-python/
- capitalizzazione testo:   https://stackoverflow.com/questions/1549641/how-to-capitalize-the-first-letter-of-each-word-in-a-string-python
- substring:                https://stackoverflow.com/questions/663171/is-there-a-way-to-substring-a-string
- posizione di un char:     https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python

"""

#-*- coding: utf-8 -*-

import os
import os.path
import sys
import time
import string
import datetime
import json
import urllib.request
import urllib.error
import traceback
from core import *





# ############################################################################
# 1. Inizializzazione
# ############################################################################

print("* initialization...")

# configuration intialization
cfg = Config(CONFIG_PATH)

# drop old db
delete(cfg.getdb())

# apre la connessione al database indicato dal parametro (se il file non esiste lo crea)
db = Database(cfg.getdb())

# creazione schema ddl del database
with open(cfg.getschema()) as sh:
    ddl = sh.read()
db.executescript(ddl)

# count operazioni
added, errors = 0,0

# timer
start_time = time.time()



# check file configurazione
""" if len(cfg.getdirs()) == 0 or len(cfg.getexts()) == 0:
    exit() """


# ############################################################################
# 2. Scansione canzoni grezze
# ############################################################################

print("* start directories scanning...")

sc = Scanner()

""" files = sc.getfiles(cfg.getexts(), cfg.getdirs())       # testare sta funzione nuova!!

for file in files:
    try:
        title, artist, album, date, trackno, length = sc.getsongtags(file)

        db.execute(
            "INSERT INTO songs_raw VALUES(?,?,?,?,?,?, ?);", 
            title, album, artist, date, length, trackno, file
        )
        added += 1
        
    except Exception as ex:
        print(str(ex))
        errors += 1 """


for dir in cfg.getdirs():
    
    print("* searching ",dir)

    for root, dirs, files in os.walk(dir):
        
        for f in files:
            
            fullpath = os.path.join(root, f)
            if os.path.splitext(fullpath)[1] in cfg.getexts():
                
                try:
                    
                    title, artist, album, date, trackno, length = sc.getsongtags_new(fullpath) # nuova funzione con eyed3 da testare!

                    db.execute(
                        "INSERT INTO songs_raw VALUES(?,?,?,?,?,?,?);", 
                        title, album, artist, date, length, trackno, fullpath
                    ) # test se funziona il metodo execute, devo trovare il modo di passarei vari parametri

                    added += 1
                    
                except Exception as ex:
                    print("errore: ", str(ex))
                    errors += 1

db.commit()



# ############################################################################
# 3. ottenimento artisti
# ############################################################################

print("* building artists list...")


# inserimento distinct artisti
db.execute("""
insert into artists (name)
select distinct artist
from songs_raw;
""")
db.commit()



# ############################################################################
# 4. ottenimento album
# ############################################################################

print("* building albums list...")

# inserimento distinct degli album
db.execute("""
insert into albums (title, artist_id, year)
select distinct album,
	   (select a.artist_id from artists as a where a.name = sr.artist),
	   (select ROUND(avg(year)) from songs_raw as sr2 where sr2.album = sr.album)
from songs_raw as sr;
""")
db.commit()



# ############################################################################
# 5. creazione canzoni
# ############################################################################

print("* building songs list...")

# inserimento canzoni clean
db.execute("""
insert into songs(title, album_id, length, track_no, path)
select  s.title,
		(select alb.album_id from albums as alb where alb.title = s.album),
		s.length,
		s.track_no,
		s.path
from songs_raw as s;
""")
db.commit()




# ############################################################################
# 6. ottenimento metadati artisti lastfm [RICHIESTA CONNESSIONE]
# ############################################################################

print("* getting artists metadata...")

# ottenimento di tutti gli artisti
selartists = db.select("SELECT * FROM artists;")

for i in range(len(selartists)):

    artist_name = selartists[i]["NAME"]
    artist_id = selartists[i]["ARTIST_ID"]

    try:

        progress(i+1, len(selartists))

        req = urllib.request.urlopen(
            "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={0}&api_key={1}&format=json".format(
                artist_name.replace(" ","+"), 
                cfg.getapikey()
                ).encode('ascii', 'ignore').decode('ascii'))

        html = req.read()
        json_data = json.loads(html)

        if "artist" in json_data:
            artist_bio = json_data["artist"]["bio"]["summary"]
            artist_img = json_data["artist"]["image"][3]["#text"]
            db.execute(
                "update artists set biography = ?, image_url = ? where artist_id = ?; ",
                artist_bio, artist_img, artist_id
            )    

    except Exception as e:
        pass

db.commit()



# ############################################################################
# 7. ottenimento copertine album lastfm [RICHIESTA CONNESSIONE]
# ############################################################################

print("\n* getting albums metadata...")


# ottenimento dell'elenco degli album locali ed iterazione per ottenere i metadati
selalbums = db.select("""
                SELECT al.ALBUM_ID, al.TITLE, ar.name as "ARTIST_NAME" 
                FROM albums as al 
                inner join artists as ar on al.artist_id = ar.artist_id;
            """)

for i in range(len(selalbums)):

    album_id = selalbums[i]["ALBUM_ID"]
    album_title = selalbums[i]["TITLE"]
    artist_name = selalbums[i]["ARTIST_NAME"]

    try:

        progress(i+1, len(selalbums))

        req = urllib.request.urlopen(
            "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist={0}&album={1}&api_key={2}&format=json".format(
                artist_name.replace(" ","+"),
                album_title.replace(" ","+"),
                cfg.getapikey()
                ).encode('ascii', 'ignore').decode('ascii'))

        html = req.read()
        json_data = json.loads(html)
        
        if "album" in json_data:
            album_img = json_data["album"]["image"][3]["#text"]
            db.execute(
                "update albums set cover_url = ? where album_id = ?; ",
                album_img, album_id
            )

    except Exception as e:
        pass

db.commit()



# ############################################################################
# 8. chiusura programma
# ############################################################################

print("\n* script ended in {} secs".format(round(time.time() - start_time,1)))
print("* {} tracks found".format(added))
print("* {} errors detected".format(errors))

# chiusura connessione
db.close()

input("press key to exit") 