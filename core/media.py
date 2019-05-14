import eyed3


def getsongtags(self, song_path):
    '''return song metadata'''

    title = album = artist = "" 
    date = trackno = length = 0

    audiofile = eyed3.load(song_path)
    title = audiofile.tag.title
    album = audiofile.tag.album
    artist = audiofile.tag.artist
    #date = audiofile.tag.getBestDate().year # eccezzione del tipo Invalid v2.3 TYER, TDAT, or TIME frame: Invalid date string: 2007--
    trackno = audiofile.tag.track_num[0]
    length = round(audiofile.info.time_secs)

    return title, artist, album, date, trackno, length