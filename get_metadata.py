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


# configuration intialization
cfg = config.Config(CONFIG_PATH)

# istanza db
db = database.Database(cfg.getDb())
db.open()

# count operazioni
added, errors = 0,0

# timer
start_time = time.time()




# ############################################################################
# 6. ottenimento metadati biografia/immagine artisti lastfm
# ############################################################################

if cfg.fetchArtistsInfo():
    print()
    print("* getting artists metadata...")
    artists = db.select("SELECT * FROM artists;")
    for i in range(len(artists)):
        artist_name = artists[i]["NAME"]
        artist_id = artists[i]["ARTIST_ID"]
        try:
            common.progress(i+1, len(artists))
            result = spotify.getArtistInfo(artist_name)
            if result["status"]:
                db.execute("update artists set image_url = ?, spotify_id = ?, name = ? where artist_id = ?; ", 
                    result["info"]["image"], 
                    result["info"]["spotify_id"], 
                    result["info"]["name"], 
                    artist_id)
            else:
                print()
                print("* {}".format(result["message"]))
        except Exception as e:
            print()
            print("* fetch artist info error: {}".format(str(e)))
    db.commit()




# ############################################################################
# 7. ottenimento copertine album lastfm [RICHIESTA CONNESSIONE]
# ############################################################################
'''
TODO da testare con lo schema logico nuovo
ho messo date al posto di year

if cfg.fetchAlbumsInfo():
    print()
    print("* getting albums metadata...")
    albums = db.select("""
                    SELECT al.ALBUM_ID, al.TITLE, ar.name as "ARTIST_NAME" 
                    FROM albums as al 
                    inner join artists as ar on al.artist_id = ar.artist_id;
                """)
    for i in range(len(albums)):
        album_id = albums[i]["ALBUM_ID"]
        album_title = albums[i]["TITLE"]
        artist_name = albums[i]["ARTIST_NAME"]
        try:
            common.progress(i+1, len(albums))
            cover = lastfm.getAlbumInfo(artist_name, album_title)
            if cover != "":
                db.execute("update albums set cover_url = ? where album_id = ?; ",cover, album_id)
        except Exception as e:
            print()
            print("* fetch album info error: {}".format(str(e)))
    db.commit()

'''


# ############################################################################
# 8. chiusura programma
# ############################################################################

print()
print("* script ended in {} secs".format(round(time.time() - start_time,1)))
print("* {} tracks found | {} errors detected".format(added, errors))   #TODO print result artists e album

db.close()

input("press key to exit")