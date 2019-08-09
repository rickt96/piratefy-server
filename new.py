import os
import time
import string
import datetime
import json
import urllib.request
import urllib.error
import traceback
from core import config, common, database, tags, lastfm, spotify, CONFIG_PATH


data = [
    ["title", "album", "artist", "date", "length", "tracknum", "genre", "path"]
]


# ############################################################################
# 1. Inizializzazione
# ############################################################################

print("* initialization...")

# configuration intialization
cfg = config.Config(CONFIG_PATH)

# count operazioni
added, errors = 0,0

# timer
start_time = time.time()




# ############################################################################
# 2. Scansione canzoni grezze
# ############################################################################

print("* start directories scanning...")

songs = common.getFiles(["D:\MUSICA\Soulfly"])

print("* {} tracks found".format(len(songs)))

print("* collecting tracks metadata...")

for song in songs:
    try:
        res = tags.getTags(song)
        if res["error"] == False:
            data.append([
                res["tags"]["title"], 
                res["tags"]["album"], 
                res["tags"]["artist"],
                res["tags"]["date"],
                res["tags"]["length"],
                res["tags"]["tracknum"],
                res["tags"]["genre"],
                song
            ])
            added += 1
        else:
            print(res["message"])
            errors += 1
    except Exception as ex:
        print("errore: ", str(ex))
        errors += 1



## save to csv
common.createCsv()


# ############################################################################
# 8. chiusura programma
# ############################################################################

print("* script ended in {} secs".format(round(time.time() - start_time,1)))
print("* {} tracks found | {} errors detected".format(added, errors))


input("press key to exit")




common.createCsv(data=data)