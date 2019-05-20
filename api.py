import mimetypes
import os
import re
import flask
from flask import request, send_file, Response, Flask, abort
from flask_cors import CORS
from core import config
from core import controllers


# setup flask
app = Flask(__name__)
CORS(app)

# configurazione
cfg = config.Config("config.json")
service_port = cfg.getPort()
db_path = cfg.getDb()

# api controllers
songsController = controllers.SongsController()
artistsController = controllers.ArtistsController()
albumsController = controllers.AlbumsController()




# ###########################################################################################
# API ARTISTS
# ###########################################################################################


@app.route("/api/artists", methods=["GET"])
def get_artists():
    data = artistsController.getAll()
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
    data = albumsController.getAll()
    return flask.jsonify(data)


@app.route("/api/albums/<int:albumID>", methods=["GET"])
def get_album(albumID):
    data = albumsController.getById(albumID)
    return flask.jsonify(data)




# ##########################################################################################
# API SONGS
# ##########################################################################################


@app.route("/api/songs")
def get_songs():
    data = songsController.getAll()
    return flask.jsonify({"songs": data})


@app.route("/api/songs/<int:songID>", methods=["GET"])
def get_song(songID):
    data = songsController.getById(songID)
    return flask.jsonify(data)


@app.route("/api/songs/play/<int:songID>", methods=["GET"])
def play_partial(songID):
    path = songsController.getSongPath(songID)

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
        port = service_port
    )
