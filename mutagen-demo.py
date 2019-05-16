from mutagen.mp3 import MP3

audio = MP3("C:\\Users\\fastcode\\Stage 2019 ITS - Riccardo Tassinari\\song.mp3")
print(audio.info.length)
print(audio.info.bitrate)
print(audio.tags["artist"])

info = mutagen.File("C:\\Users\\fastcode\\Stage 2019 ITS - Riccardo Tassinari\\song.mp3", easy=True)

# https://www.programcreek.com/python/example/63675/mutagen.File