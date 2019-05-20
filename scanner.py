"""
# Descrizione
lo script permette di generare un database dai file aventi le estensioni specificate
nelle directory selezionate (vedi il file config.json).
essi vengono cercati ed inseriti nel database costruendo uno schema logico tra canzoni, artisti e album
le informazioni non presenti nei metadati vengono completate tramite l'utilizzo delle webapi di last.fm

# Funzionamento
1. inizializzazione
2. scansione cartelle e creazione canzoni grezze
3. creazione artisti
4. creazione album
5. creazione canzoni finali
6. ottenimento biografie e immagini (webapi lastfm)
7. ottenimento cover (webapi lastfm)
8. print dei risultati
"""

#-*- coding: utf-8 -*-

import time
import string
import datetime
import json
import urllib.request
import urllib.error
import traceback
from core import config
from core import common
from core import database



# ############################################################################
# 1. Inizializzazione
# ############################################################################

print("* initialization...")

# configuration intialization
cfg = config.Config("config.json")

# drop old db
common.delete(cfg.getDb())

# apertura connessione al database
db = database.Database(cfg.getDb())

# creazione schema ddl del database
with open(cfg.getSchema()) as sh:
    ddl = sh.read()
db.executeScript(ddl)

# count operazioni
added, errors = 0,0

# timer
start_time = time.time()




# ############################################################################
# 2. Scansione canzoni grezze
# ############################################################################

print("* start directories scanning...")

songs = common.getFiles(cfg.getDirs())

print("* {} songs found".format(len(songs)))

print("* fetching track metadata")

for song in songs:
    try:
        res = common.getEyeD3Tags(song)
        if not res["error"]:
            db.execute(
                "INSERT INTO songs_raw VALUES(?,?,?,?,?,?,?);", 
                res["tags"]["title"], 
                res["tags"]["album"], 
                res["tags"]["artist"],
                res["tags"]["year"],
                res["tags"]["length"],
                res["tags"]["tracknum"],
                song)
            added += 1
        else:
            print(res["message"])
            errors += 1
    except Exception as ex:
        print("errore: ", str(ex))
        errors += 1
db.commit()




# ############################################################################
# 3. ottenimento artisti
# ############################################################################

print("* building artists list...")

# inserimento distinct artisti
# popola la tabella artisti cercando i vari nomi dalla tabella songs_raw
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
# popola la tabella degli album prendendo prendendo i valori dalla tabella delle songs_raw
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
# ottiene i valori delle canzoni leggendoli da songs_raw ed albums
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



if cfg.getFetchMetadata():

    # ############################################################################
    # 6. ottenimento metadati biografia/immagine artisti lastfm [RICHIESTA CONNESSIONE]
    # ############################################################################

    print("* getting artists metadata...")

    selartists = db.select("SELECT * FROM artists;")

    for i in range(len(selartists)):

        artist_name = selartists[i]["NAME"]
        artist_id = selartists[i]["ARTIST_ID"]

        try:

            common.progress(i+1, len(selartists))

            req = urllib.request.urlopen(
                "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={0}&api_key={1}&format=json".format(
                    artist_name.replace(" ","+"), 
                    cfg.getApiKey()
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

            common.progress(i+1, len(selalbums))

            req = urllib.request.urlopen(
                "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist={0}&album={1}&api_key={2}&format=json".format(
                    artist_name.replace(" ","+"),
                    album_title.replace(" ","+"),
                    cfg.getApiKey()
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

print("* script ended in {} secs".format(round(time.time() - start_time,1)))
print("* {} tracks found | {} errors detected".format(added, errors))

# chiusura connessione
db.close()

input("press key to exit")