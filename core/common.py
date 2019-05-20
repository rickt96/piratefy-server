import sys
import eyed3
import os


# stampa a schermo una progressione del tipo 10/50 analizzati
def progress(current, total):
    '''stampa a schermo una progress bar'''
    sys.stdout.write("\r  %d/%d analyzed" % (current, total))
    sys.stdout.flush()


# cancella un file specifico
def delete(file_path):
    '''elimina un file'''
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True
    except Exception as ex:
        print("unable to delete file: ", ex)
        return False


# descrizione da aggiungere
def setEyeD3Tags(path, title='', artist='', album='', track=0, genre='', year=0 ):
    '''imposta i tag di un file mp3'''
    """audiofile = eyed3.load(path)
    audiofile.tag.title = title
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.track_num = track
    audiofile.tag.genre = genre
    audiofile.tag.year = year
    audiofile.tag.save(path) """
    pass



# restituisce i metadati della canzone
def getEyeD3Tags(path):
    """restituisce i tag del file mp3"""
    # https://www.programiz.com/python-programming/methods/built-in/str
    # https://gist.github.com/sinewalker/c636025bfc4bf3cc3e9992f212a40afa
    # https://stackoverflow.com/questions/8948/accessing-mp3-meta-data-with-python
    result = {
        "error" : True,
        "message" : "",
        "tags" : { }
    }

    try:
        audiofile = eyed3.load(path) # test
        if audiofile is not None:
            title = "unknown title" if audiofile.tag.title is None else audiofile.tag.title     # ridondanza di codice, ma se dichiaro tutto nel dizionario legge come tuple
            artist = "unknown artist" if audiofile.tag.artist is None else audiofile.tag.artist
            album = "unknown album" if audiofile.tag.album is None else audiofile.tag.album
            tracknum = 0 if audiofile.tag.track_num[0] is None else audiofile.tag.track_num[0]
            year = 0 if audiofile.tag.getBestDate() is None else audiofile.tag.getBestDate().year
            genre = "unknown genre" if audiofile.tag.genre is None else audiofile.tag.genre
            result["tags"]["title"] = title.title()
            result["tags"]["artist"] = artist.title()
            result["tags"]["album"] = album.title()
            result["tags"]["tracknum"] = tracknum
            result["tags"]["year"] = year
            result["tags"]["length"] = round(audiofile.info.time_secs)
            result["tags"]["genre"] = genre
            result["error"] = False
        else:
            result["error"] = True
            result["message"] = "unable to read file - "+path

    except Exception as e:
        result["error"] = True
        result["message"] = str(e) + " - " + path

    return result



# restituisce tutti i files mp3 nelle directory indicate
def getFiles(directories=[]):
    files = []
    for directory in directories:           # r=root, d=directories, f=files
        for r, d, f in os.walk(directory):
            for file in f:
                if file.endswith('.mp3'): # tuple(extensions)
                    files.append(os.path.join(r, file))
    return files