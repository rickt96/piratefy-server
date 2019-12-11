# questo script funge da server rest per il progetto
# gira su modulo flask e gestisce gli endpoint per l'invio dei dati json dei media
# restituisce dati relativi ad artisti, album, canzoni e generi
# inoltre espone un endpoint per lo streaming delle tracce audio
# quest'ultima parte inizialmente era più semplice e risultava funzionante su browser come edge e firefox
# ma su chrome non era consentito il seek delle tracce, questo perchè 
# il browser necessita che il server mandi in streaming il contenuto con supporto ai partial contents.
# per adeguare quindi la funzione ho dovuto utilizzare una soluzione più complessa
# da github https://gist.github.com/lizhiwei/7885684
# vedere le reference sul file README nella categoria flask/media
# parole di ricerca utilizzate: flask streaming chrome, flask mp3 streaming, chrome audio stream not seek


import mimetypes
import os
import re
import flask
from flask import request, send_file, Response, Flask, abort
from flask_cors import CORS
from core import config, controllers, CONFIG_PATH


# setup flask
app = Flask(__name__)
CORS(app) #cors = CORS(app, resources={r"*": {"origins": "*"}})

# configurazione
cfg = config.Config(CONFIG_PATH)
service_port = cfg.getPort()

# api controllers
songsController = controllers.SongsController()
artistsController = controllers.ArtistsController()
albumsController = controllers.AlbumsController()



# ###########################################################################################
# API ARTISTS
# ###########################################################################################


@app.route("/api/artists", methods=["GET"])
def get_artists():
    page = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 15))
    data = artistsController.getAll(limit, page)
    return flask.jsonify(data)


@app.route("/api/artists/<int:artistID>", methods=["GET"])
def get_artist(artistID):
    data = artistsController.getById(artistID)
    return flask.jsonify(data)




# ###########################################################################################
# API ALBUMS
# ###########################################################################################


@app.route("/api/albums", methods=["GET"])
def get_albums():
    page = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 15))
    data = albumsController.getAll(limit, page)
    return flask.jsonify(data)


@app.route("/api/albums/<int:albumID>", methods=["GET"])
def get_album(albumID):
    data = albumsController.getById(albumID)
    return flask.jsonify(data)




# ##########################################################################################
# API SONGS
# ##########################################################################################

'''
per gestire le informazioni più verbose sugli artisti serve questa query
cosi ritorno anche il nome dell'artista e dell'album per ogni song

select 
	s.*, a.title as 'ALBUM_TITLE', a.COVER_URL as 'ALBUM_COVER', ar.ARTIST_ID, ar.name as 'ARTIST_NAME', ar.IMAGE_URL as 'ARTIST_COVER' 
from SONGS as s
join albums as a on s.ALBUM_ID = a.ALBUM_ID
join artists as ar on a.ARTIST_ID = ar.ARTIST_ID
'''

@app.route("/api/songs", methods=["GET"])
def get_songs():
    page = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 15))
    query = str(request.args.get('query', ''))
    asc = bool(request.args.get('asc', True))
    sort = str(request.args.get('sort', ''))
    
    data = songsController.getAll(limit, page, sort, asc, query)
    return flask.jsonify(data)


@app.route("/api/songs/<int:songID>", methods=["GET"])
def get_song(songID):
    data = songsController.getById(songID)
    return flask.jsonify(data)


@app.route("/api/songs/play/<int:songID>", methods=["GET"])
def play_partial(songID):
    path = songsController.getSongPath(songID)

    # verifica il percorso della risorsa
    # NB la label del disco potrebbe cambiare se si avvia il server su un altra macchina
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
"""     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*') """
    




# ##########################################################################################
# AVVIO FLASK
# ##########################################################################################

if __name__ == "__main__":
    app.run(
        debug = True,
        host = "0.0.0.0",
        port = service_port
    )
