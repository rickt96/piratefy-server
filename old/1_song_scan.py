
# song_scanner
# lo script si occupa di popolare il database con tutte le canzoni
# esso inizialmente ottiene dai percorsi specificati una lista di file mp3
# sucessivamente questi vengono analizzati, i loro metadati estratti ed inseriti nel database sqlite
# nel quale poi sucessivamente viene costruito lo schema logico realtivo a canzoni, artisti, album e generi
# le informazioni non presenti nei metadati locali possono essere completate interrogando le api di last.fm
# dilatando molto i tempi di esecuzione dello script.
# questa componente al momento non è pienamente funzionante e presenta problemi con le immagini

# 1. inizializzazione: creazione nuovo database ed istanza delle variabili
# 2. scansione: vengono ottenute ed analizzate tutte le tracce mp3 ed i loro metadati inseriti in una prima tabella della songs_raw
# 3. creazione artisti: popola la tabella artists tramite i dinstict ottenuti da songs_raw
# 4. creazione albums: popola la tabella albums tramite i dinstinct da songs_raw ed aggiunge il riferimento all'artista
# 5. creazione canzoni: una volta ottenuti albums ed artists crea le canzoni "clean" attivando le chiavi esterne opportune
# 6. ottenimento metadati artisti: opzionalmente è possibile ottenere i metadati relativi alla biografia ed un'immagine degli artisti
# 7. ottenimento metadati album: procedimento analogo a quanto visto sopra, ma ottiene soltanto la cover dell'album
# 8. chiusura: finalizzazione operazione e log dei risultati

#-*- coding: utf-8 -*-

import os
import time
import string
import datetime
import json
import urllib.request
import urllib.error
import traceback
from core import config, common, database, tags, lastfm, spotify, CONFIG_PATH


# ############################################################################
# 1. Inizializzazione
# ############################################################################

print("* initialization...")

# configuration intialization
cfg = config.Config(CONFIG_PATH)

# drop old db
common.delete(cfg.getDb())

# istanza db
db = database.Database(cfg.getDb())
db.open()

# inizializzazione e caricamento schema logico
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

print("* collecting tracks metadata...")

for song in songs:
    try:
        res = tags.getTags(song)
        if res["error"] == False:
            db.execute(
                "INSERT INTO songs_raw VALUES(?,?,?,?,?,?,?,?);", 
                res["tags"]["title"], 
                res["tags"]["album"], 
                res["tags"]["artist"],
                res["tags"]["date"],
                res["tags"]["length"],
                res["tags"]["tracknum"],
                res["tags"]["genre"],
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

# ERROR
# inserimento distinct degli album
# popola la tabella degli album prendendo i valori dalla tabella delle songs_raw
# (select ROUND(avg(year)) from songs_raw as sr2 where sr2.album = sr.album)
db.execute("""
    insert into albums (title, artist_id)
    select distinct album,
        (select a.artist_id from artists as a where a.name = sr.artist),
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
    insert into songs(title, album_id, length, track_no, genre_id, path)
    select  s.title,
            (select alb.album_id from albums as alb where alb.title = s.album),
            s.length,
            s.track_no,
            (select gen.genre_id from genres as gen where gen.name = s.genre),
            s.path
    from songs_raw as s;
""")
db.commit()




# ############################################################################
# 8. chiusura programma
# ############################################################################

print("* script ended in {} secs".format(round(time.time() - start_time,1)))
print("* {} tracks found | {} errors detected".format(added, errors))

# chiusura connessione
db.close()

input("press key to exit")