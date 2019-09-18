# lo script analizza gli artisti e gli album
# e cerca i metadati tramite le api di spotify
# per gli artists cerca l'immagine
# per gli albums cerca immagine e data

#-*- coding: utf-8 -*-

import time
from core import config, common, database, spotify, CONFIG_PATH


# configuration intialization
cfg = config.Config(CONFIG_PATH)

# istanza db
db = database.Database(cfg.getDb())
db.open()

# count operazioni
added, errors = 0,0

# timer
start_time = time.time()


# get artists metadata
if cfg.fetchArtistsInfo():
    print()
    print("* getting artists metadata...")
    artists = db.select("""
                    SELECT * 
                    FROM artists 
                    where name <> '' AND spotify_id is NULL;
                    """)
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



# get abums metadata
if cfg.fetchAlbumsInfo():
    print()
    print("* getting albums metadata...")
    albums = db.select("""
                SELECT al.ALBUM_ID, al.TITLE, ar.name as "ARTIST_NAME" 
                FROM albums as al 
                inner join artists as ar on al.artist_id = ar.artist_id
                where al.TITLE <> '' AND al.spotify_id is NULL;
                """)
    for i in range(len(albums)):
        album_id = albums[i]["ALBUM_ID"]
        album_title = albums[i]["TITLE"]
        artist_name = albums[i]["ARTIST_NAME"]
        try:
            common.progress(i+1, len(albums))
            result = spotify.getAlbumInfo(album_title, artist_name)
            if result["status"]:
                db.execute("update albums set cover_url = ?, date = ?, spotify_id = ? where album_id = ?; ",
                    result["info"]["image"],
                    result["info"]["date"],
                    result["info"]["spotify_id"], 
                    album_id)
            else:
                print()
                print("* {}".format(result["message"]))
        except Exception as e:
            print()
            print("* fetch album info error: {}".format(str(e)))
    db.commit()


# ending
print()
print("* script ended in {} secs".format(round(time.time() - start_time,1)))

db.close()

input("press key to exit")