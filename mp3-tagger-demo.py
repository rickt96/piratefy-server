from mp3_tagger import MP3File, VERSION_1

# Create MP3File instance.
mp3 = MP3File("C:\\Users\\fastcode\\Stage 2019 ITS - Riccardo Tassinari\\song.mp3")
mp3.set_version(VERSION_1)
tags = mp3.get_tags()
print(tags["song"])
#print(tags)


"""
Allowed tags:

    - artist;
    - album;
    - song;
    - track;
    - comment;
    - year;
    - genre;
"""
