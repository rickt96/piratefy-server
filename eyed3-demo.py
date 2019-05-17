# http://www.blog.pythonlibrary.org/2010/04/22/parsing-id3-tags-from-mp3s-using-python/
from core import *
import eyed3
import time
 

eyed3.log.setLevel("ERROR")

#----------------------------------------------------------------------
def getEyeD3Tags(path):
    """ottiene i tag del file mp3"""
    try:
        audiofile = eyed3.load(path)
        title = audiofile.tag.title
        artist = audiofile.tag.artist
        album = audiofile.tag.album
        tracknum = audiofile.tag.track_num[0]
        date = audiofile.tag.getBestDate().year # verificare possibili errori qui
        length = round(audiofile.info.time_secs)
        print("%s - %s - %s - %s - %s - %s" % (date, title, artist, album, tracknum, length))
        #return title, artist, album, tracknum, date, length
    except Exception as e:
        print(path, " - ", str(e))



start_time = time.time()
songs = getFiles(["D:\\MUSICA\\"])
for song in songs:
    getEyeD3Tags(song)

print(round(time.time() - start_time,1))
print(len(songs))

""" for song in songs:
    getEyeD3Tags(song) """