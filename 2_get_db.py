
#-*- coding: utf-8 -*-

import os
import time
import string
import datetime
import json
import urllib.request
import urllib.error
import traceback
from core import config, common, database, tags, spotify, CONFIG_PATH


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

# creazione schema logico tabelle db
try:
    with open(cfg.getSchema()) as sh:
        ddl = sh.read()
    db.executeScript(ddl)
except Exception as e:
    print("cannot create db schema: ",e)
    db.close()
    exit()


# timer
start_time = time.time()

#https://stackoverflow.com/questions/24441606/how-to-create-a-list-in-python-with-the-unique-values-of-a-csv-file

# load csv data
print("* loading csv file...")
data = common.readCsv(filename="scan/scan-full.csv")


# build raw songs
print("* building raw songs...")
for d in data:
    db.execute(
        "INSERT INTO songs_raw VALUES(?, ?, ?, ?, ?, ?, ?, ?);", 
        d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]
    )
db.commit()


# build artists list
# insert distinct degli artisti
# popola la tabella artisti cercando i vari nomi dalla tabella songs_raw
print("* building artists list...")
db.execute("""
    insert into artists (name)
    select distinct artist
    from songs_raw;
""")
db.commit()


# inserimento distinct degli album
# popola la tabella degli album prendendo i valori dalla tabella delle songs_raw
# (select ROUND(avg(year)) from songs_raw as sr2 where sr2.album = sr.album)
print("* building albums list...")
db.execute("""
    insert into albums (title, artist_id)
    select distinct album, (select a.artist_id from artists as a where a.name = sr.artist)
    from songs_raw as sr;
""")
db.commit()


# build songs list
# inserimento canzoni clean
# ottiene i valori delle canzoni leggendoli da songs_raw ed albums
print("* building songs list...")
db.execute("""
    insert into songs(title, album_id, length, track_no, path) -- , genre_id
    select  s.title,
            (select alb.album_id from albums as alb where alb.title = s.album),
            s.length,
            s.track_no,
            s.path
            --(select gen.genre_id from genres as gen where gen.name = s.genre),
    from songs_raw as s;
""")
db.commit()


# closing
print("* database ", cfg.getDb(), " created")
print("* script ended in {} secs".format(round(time.time() - start_time,1)))

db.close()

input("press key to exit")