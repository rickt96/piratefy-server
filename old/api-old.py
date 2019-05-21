'''
# Documentazione script:
  questo script si occupa di mandare in streaming i vari media
  tramite il protocollo http
  facendo questo la pagina web ed il tag <audio> dell'html5 è in grado
  di riprodurre la canzone
  originalmente c'era uno script più semplice
  ma per problemi di compatibilita con chrome ho dovuto usare questa solizione più complessa
  
# Keyword di ricerca utilizzate:
- flask streaming chrome
- flask mp3 streaming
- chrome audio stream not seek

# Note:
- a differenza di edge e firefox chrome necessita che il server che manda in stream il contenuto
  supporti i partial contents, senza di quelli non è in grado di fare il seek sulle canzoni
- play_partial non ho la minima idea di come funzioni, ma funziona (lo snippet originale è nel primo link di github)
'''


import mimetypes
import os, os.path
import re
import sqlite3
import json
import flask
from flask import request, send_file, Response, Flask, abort
from flask_cors import CORS
from core import *
from corenew import config
from corenew import database



# setup flask
app = Flask(__name__)
CORS(app)


# caricamento configurazione
cfg = Config(CONFIG_PATH) 


# ###########################################################################################
# METODI
# * execute(query)        |   apre la conn al db, esegue la query specificata e restituisce un dizionario dei valori
# * fetchOne(query)       |   apre la conn al db, esegue la query specificata e restituisce un singolo valore
# ###########################################################################################


# esecuzione query
def execute(query):
    """dbconn = sqlite3.connect(cfg.getdb())
    dbconn.row_factory = dict_factory
    cur = dbconn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    dbconn.close()
    return data """
    db = Database(cfg.getDb())
    data = db.select(query)
    db.close()
    return data



# ritorno singolo valore
def fetchone(query):
    db = Database(cfg.getDb())
    value = db.fetchOne(query)
    db.close()
    return value



# ottenimento dati artista (albums e canzoni)
def getArtistsData(query):
    artists = execute(query)
    for ar in artists:
        albums = execute("select * from albums where artist_id = " + str(ar["ARTIST_ID"]) + " order by year")
        for al in albums:
            album_songs = execute("select * from songs where album_id = "+str(al["ALBUM_ID"])+" order by track_no")
            al["SONGS"] = album_songs
        ar["ALBUMS"] = albums
    return artists


# ottenimento delle canzoni
def getSongsData(where, offset):
    songs = execute("""
                select song_id, s.title, al.title as 'ALBUM', al.album_id as 'ALBUM_ID', al.cover_url as 'COVER_URL', ar.name as 'ARTIST', ar.image_url as 'ARTIST_IMAGE', length, al.year as 'YEAR' 
                from SONGS as s 
                inner join albums as al on s.album_id = al.album_id 
                inner join artists as ar on al.artist_id = ar.artist_id 
                {0} 
                order by s.title
                {1}""".format(where, offset))
    return songs


# ottenimento album
def getAlbumData(where, orderby, offset):
    albums = execute("""
                select al.album_id as 'ALBUM_ID',
                       al.title as 'TITLE',
                       al.artist_id as 'ARTIST_ID',
                       al.year as 'YEAR',
                       al.cover_url as 'COVER_URL',
                       ar.name as 'ARTIST_NAME'
                from ALBUMS as al
                inner join ARTISTS  as ar on al.artist_id = ar.artist_id 
                {0} 
                {1} 
                {2}""".format(where, orderby, offset))
    for al in albums:
        album_songs = execute("select * from songs where album_id = "+str(al["ALBUM_ID"])+" order by track_no")
        al["SONGS"] = album_songs
    return albums



# ###########################################################################################
# API ARTISTS
# * /api/artists?search=<string>&offset=<int>&limit=<int>
# * /api/artists/<int:id>
# ###########################################################################################

# ricerca artisti
@app.route("/api/artists", methods=["GET"])
def get_artists():
    search = request.args.get('search', "").replace("+","")
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 15)
    
    artists = getArtistsData(
        "select * from artists where name like '%" + search + "%' " +
        "order by name " +
        "limit " + str(offset) + "," + str(limit))

    return flask.jsonify({"artists": artists})


# selezione artista
@app.route("/api/artists/<int:artistID>", methods=["GET"])
def get_artist(artistID):
    artists = getArtistsData("select * from artists where artist_id = " + str(artistID) + " limit 1")
    if len(artists) > 0:
        return flask.jsonify({"artist": artists[0]})
    else:
        abort(404)



# ###########################################################################################
# API ALBUMS
# * /api/albums?search=<string>&offset=<int>&limit=<int>
# * /api/albums/<int:id>
# ###########################################################################################

# ricerca albums
@app.route("/api/albums", methods=["GET"])
def get_albums():
    search = request.args.get('search', "").replace("+","")
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 15)
    
    albums = getAlbumData(
        "where title like '%" + search + "%' ",
        "order by title ",
        "limit " + str(offset) + "," + str(limit))

    return flask.jsonify({"albums": albums})



# selezione album
@app.route("/api/albums/<int:albumID>", methods=["GET"])
def get_album(albumID):
    albums = getAlbumData(
        "where album_id = " + str(albumID) + " ", "", "")
    if len(albums) > 0:
        return flask.jsonify({"album": albums[0]})
    else:
        abort(404)





# ##########################################################################################
# API SONGS
# * /api/songs?search=<string>&offset=<int>&limit=<int>
# * /api/songs/<int:id>
# * /api/songs/play/<int:id>
# ##########################################################################################

# ricerca canzoni
@app.route("/api/songs")
def get_songs():
    search = request.args.get('search', "").replace("+","")
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 15)
    
    songs = getSongsData(
        "where s.title like '%" + search + "%' ",
        "limit "+ str(offset) + "," + str(limit))

    return flask.jsonify({"songs": songs})


# selezione canzone
@app.route("/api/songs/<int:songID>", methods=["GET"])
def get_song(songID):
    songs = getSongsData("where s.song_id = "+str(songID), "")
    if len(songs) > 0:
        return flask.jsonify({"song": songs[0]})
    else:
        abort(404)


# streaming http della canzone
@app.route("/api/songs/play/<int:songID>", methods=["GET"])
def play_partial(songID):

    query = "select path from songs where song_id = "+str(songID)
    path = fetchone(query)["PATH"]
    #print(path)

    if os.path.isfile(path) == False:
        abort(404)
    
    range_header = request.headers.get('Range', None)
    if not range_header: return send_file(path)
    
    size = os.path.getsize(path)    
    byte1, byte2 = 0, None
    
    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()
    
    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1
    
    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, 
        206,
        mimetype=mimetypes.guess_type(path)[0], 
        direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))
    #rv.headers.add('Access-Control-Allow-Origin', '*')
    return rv


@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response




# ****************************************************************************************
# AVVIO FLASK
# ****************************************************************************************

if __name__ == "__main__":
    app.run(
        debug = True,
        host = "0.0.0.0",
        port = int(cfg.getPort())
    )
