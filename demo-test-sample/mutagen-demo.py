from mutagen.mp3 import MP3
#import mutagen


filename = "C:\\Users\\fastcode\\Stage 2019 ITS - Riccardo Tassinari\\song.mp3"

audio = MP3(filename)
print(audio.info.length)
print(audio.info.bitrate)
print(audio.tags.keys())



""" 
for tag in ['artist', 'album', 'title', 'tracknumber']:
    if tag not in info.keys():
        print(False, '"%s" has no %s tag' % (filename, tag))
    elif info[tag] == [u'']:
        print(False, '"%s" has an empty %s tag' % (filename, tag))
 """

""" print(info["artist"])
print(info.info.length)
print(info.keys()) """
# https://www.programcreek.com/python/example/63675/mutagen.File



""" 
info = mutagen.File(filename, easy=True)
print(info["artist"])
print(info["album"])
print(info.keys()) """

""" from mutagen.easyid3 import EasyID3

audio = EasyID3(filename)
print(audio["title"]) """



frasi = [
    ""]
if 