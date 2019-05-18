# http://www.blog.pythonlibrary.org/2010/04/22/parsing-id3-tags-from-mp3s-using-python/
from core import *
import eyed3
import time
 

eyed3.log.setLevel("ERROR")

#file = open("log.txt","w") 
 


#----------------------------------------------------------------------
""" def getEyeD3Tags(path):
    try:
        audiofile = eyed3.load(path)
        title = "no title" if audiofile.tag.title is None else audiofile.tag.title
        artist = "no artist" if audiofile.tag.artist is None else audiofile.tag.artist
        album = "no album" if audiofile.tag.album is None else audiofile.tag.album
        trackno = audiofile.tag.track_num[0]
        year = 0 if audiofile.tag.getBestDate() is None else audiofile.tag.getBestDate().year
        length = round(audiofile.info.time_secs)

        log = "%s - %s - %s - %s - %s - %s" % (year, title, artist, album, trackno, length)
        print(log)
        file.write(log + "\n")
        #return title, artist, album, tracknum, date, length
    except Exception as e:
        print(path, " - ", str(e))
 """


""" start_time = time.time()
songs = getFiles(["D:\\MUSICA\\"])
for song in songs:
    getEyeD3Tags(song)

print(round(time.time() - start_time,1))
print(len(songs)) """

dirs = ["D:\\MUSICA\\Airbourne\\"]
songs = getFiles(dirs)
for song in songs:
    res = getEyeD3Tags(song)
    if res["error"]:
        print(res)

#file.close() 