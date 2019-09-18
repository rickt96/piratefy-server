import time
from core import config, common, tags, CONFIG_PATH


print("* initialization...")

# configuration intialization
cfg = config.Config(CONFIG_PATH)

# count operazioni
added, errors = 0,0

# csv source path
csvPath = "scan.csv"

# timer
start_time = time.time()

# csv data
data = [
    #["title", "album", "artist", "date", "length", "tracknum", "genre", "path"]
]


# scan directories
print("* start directories scanning...")
songs = common.getFiles(["D:\\MUSICA\\Soulfly"])#cfg.getDirs())
print("* {} tracks found".format(len(songs)))


# population csv source
print("* collecting tracks metadata...")
for song in songs:
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


# writing csv file
common.createCsv(data=data, filename=csvPath)


# closing
print("* file ", csvPath, " created")
print("* script ended in {} secs".format(round(time.time() - start_time,1)))
print("* {} tracks found | {} errors detected".format(added, errors))

input("press key to exit")