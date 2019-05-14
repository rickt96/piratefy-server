### SAMPLE 1

import eyed3

audiofile = eyed3.load("C:\\Users\\fastcode\\Stage 2019 ITS - Riccardo Tassinari\\song.mp3")
title = audiofile.tag.title
album = audiofile.tag.album
artist = audiofile.tag.artist
date = audiofile.tag.getBestDate()          # https://stackoverflow.com/questions/40441007/how-to-access-the-release-date-or-year-from-an-mp3-file-with-eyed3-and-python2-7
trackno = audiofile.tag.track_num[0]        # track_num è una tupla del tipo (traccia/totale)
length = round(audiofile.info.time_secs)    # https://stackoverflow.com/questions/6037826/finding-the-length-of-an-mp3-file

print(artist, album, title, trackno, length, date)


### SAMPLE 2
# https://stackoverflow.com/questions/29702179/how-to-get-detail-title-artist-from-mp3-files-in-python-using-eyed3
""" 
from eyed3 import id3

tag = id3.Tag()
tag.parse("C:\\Users\\fastcode\\Stage 2019 ITS - Riccardo Tassinari\\song.mp3")
print(tag.artist)
print(tag.track_num[0])
"""

""" 
tag = eyed3.Tag()
tag.link("C:\\Users\\fastcode\\Stage 2019 ITS - Riccardo Tassinari\\song.mp3")
print(tag.getArtist())
print(tag.getTitle()) """