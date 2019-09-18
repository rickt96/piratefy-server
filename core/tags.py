import eyed3
import os

eyed3.log.setLevel("ERROR")

special_artists_name = ["ac/dc"]

def setTags(path, title='', artist='', album='', track=0, genre='', year=0 ):
    ''' TODO imposta i tag di un file mp3'''
    audiofile = eyed3.load(path)
    audiofile.tag.title = title
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.track_num = track
    audiofile.tag.genre = genre
    audiofile.tag.year = year
    audiofile.tag.save(path)



def getTags(path):
    """restituisce i tag del file mp3"""
    # https://stackoverflow.com/questions/51566381/attributeerror-nonetype-object-has-no-attribute-tag-using-eyed3
    result = {
        "error" : True,
        "message" : "",
        "tags" : { 
            "title": '',
            "artist": '',
            "album": '',
            "tracknum": 0,
            "date": '',
            "length": 0,
            "genre": ''
        }
    }
    try:
        audiofile = eyed3.load(path) # possibile errore nel caricamento
        if audiofile:
            title = "" if audiofile.tag.title is None else audiofile.tag.title     # ridondanza di codice, ma se dichiaro tutto nel dizionario legge come tuple
            artist = "" if audiofile.tag.artist is None else audiofile.tag.artist
            album = "" if audiofile.tag.album is None else audiofile.tag.album
            tracknum = 0 if audiofile.tag.track_num[0] is None else audiofile.tag.track_num[0]
            year = "" if audiofile.tag.getBestDate() is None else audiofile.tag.getBestDate().year
            genre = "" if audiofile.tag.genre is None else audiofile.tag.genre.name    # per info sulle proprietà studiare la libreria, si trova in Python\Lib\site-packege\eyed3
            result["tags"]["title"] = title.title()
            result["tags"]["artist"] = sanitizeArtist(artist).title()
            result["tags"]["album"] = album.title()
            result["tags"]["tracknum"] = tracknum
            result["tags"]["date"] = year
            result["tags"]["length"] = round(audiofile.info.time_secs)
            result["tags"]["genre"] = genre.title()
        else:
            #https://stackoverflow.com/questions/678236/how-to-get-the-filename-without-the-extension-from-a-path-in-python
            base = os.path.basename(path)
            result["tags"]["title"] = os.path.splitext(base)[0]
        result["error"] = False

    except Exception as e:
        result["error"] = True
        result["message"] = "* eyed3 error: {} - {}".format(str(e), path)

    return result



def sanitizeArtist(value):
    """pulisce il nome dell'artista rimuovendo il carattere '/'
    ignorando la procedura se il nome appartiene alla lista degli artisti con nomi speciali
    """
    # https://www.w3schools.com/python/ref_string_rstrip.asp
    if value.lower() not in special_artists_name:
        split = value.split("/")[0]
        clean = split.rstrip()
        return clean
    else:
        return value