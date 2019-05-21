import eyed3

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
    result = {
        "error" : True,
        "message" : "",
        "tags" : { }
    }
    try:
        audiofile = eyed3.load(path) # possibile errore nel caricamento
        title = "unknown title" if audiofile.tag.title is None else audiofile.tag.title     # ridondanza di codice, ma se dichiaro tutto nel dizionario legge come tuple
        artist = "unknown artist" if audiofile.tag.artist is None else audiofile.tag.artist
        album = "unknown album" if audiofile.tag.album is None else audiofile.tag.album
        tracknum = 0 if audiofile.tag.track_num[0] is None else audiofile.tag.track_num[0]
        year = 0 if audiofile.tag.getBestDate() is None else audiofile.tag.getBestDate().year
        genre = "unknown genre" if audiofile.tag.genre is None else audiofile.tag.genre.name    # per info sulle proprietà studiare la libreria, si trova in Python\Lib\site-packege\eyed3
        result["tags"]["title"] = title.title()
        result["tags"]["artist"] = sanitizeArtist(artist).title()
        result["tags"]["album"] = album.title()
        result["tags"]["tracknum"] = tracknum
        result["tags"]["year"] = year
        result["tags"]["length"] = round(audiofile.info.time_secs)
        result["tags"]["genre"] = genre.title()
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