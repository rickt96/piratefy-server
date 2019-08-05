
# lo script si occupa di poplare il database che verrà poi utilizzato per fornire i dati al client
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


# TODO
# nuovo flusso creazione libreria:
# ottenimento canzoni grezze
# memorizzazione su json locale (non più db)
# distinct generi
# distinct artists (info da spotify)
# album

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


spotify.getToken()


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

print("* fetching track metadata")

for song in songs:
    try:
        res = tags.getTags(song)
        if not res["error"]:
            db.execute(
                "INSERT INTO songs_raw VALUES(?,?,?,?,?,?,?,?);", 
                res["tags"]["title"], 
                res["tags"]["album"], 
                res["tags"]["artist"],
                res["tags"]["year"],
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




### TODO

print("* building genres list...")

# inserimento distinct generi
# popola la tabella generi cercando i vari nomi dalla tabella songs_raw
db.execute("""
    insert into genres (name)
    select distinct genre
    from songs_raw;
""")
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
# 6. ottenimento metadati biografia/immagine artisti lastfm [RICHIESTA CONNESSIONE]
# ############################################################################
if cfg.fetchArtistsInfo():

    print("* getting artists metadata...")

    selartists = db.select("SELECT * FROM artists;")

    for i in range(len(selartists)):
        artist_name = selartists[i]["NAME"]
        artist_id = selartists[i]["ARTIST_ID"]
        try:
            common.progress(i+1, len(selartists))
            result = spotify.getArtistInfo(artist_name)
            if result["status"]:
                db.execute("update artists set image_url = ?, spotify_id = ?, name = ? where artist_id = ?; ", 
                    result["info"]["image"], 
                    result["info"]["spotify_id"], 
                    result["info"]["name"], 
                    artist_id)
            else:
                print("* {}".format(result["message"]))
        except Exception as e:
            print("* fetch artist info error: {}".format(str(e)))

    db.commit()




# ############################################################################
# 7. ottenimento copertine album lastfm [RICHIESTA CONNESSIONE]
# ############################################################################
if cfg.fetchAlbumsInfo():

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
            cover = lastfm.getAlbumInfo(artist_name, album_title)
            if cover != "":
                db.execute("update albums set cover_url = ? where album_id = ?; ",cover, album_id)
        except Exception as e:
            print("* fetch album info error: {}".format(str(e)))

    db.commit()




# ############################################################################
# 8. chiusura programma
# ############################################################################

print("* script ended in {} secs".format(round(time.time() - start_time,1)))
print("* {} tracks found | {} errors detected".format(added, errors))

# chiusura connessione
db.close()

input("press key to exit")