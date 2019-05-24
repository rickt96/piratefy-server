from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

""" from core import config, CONFIG_PATH
cfg = config.Config(CONFIG_PATH) """


db_connect = create_engine('sqlite:///full2.db')


app = Flask(__name__)
api = Api(app)


class SongsList(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from songs")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    
class Song(Resource):
    def get(self, song_id):
            conn = db_connect.connect()
            query = conn.execute("select * from songs where song_id = %d "  %int(song_id))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(result)


api.add_resource(SongsList, '/songs')
api.add_resource(Song, '/songs/<song_id>')


if __name__ == '__main__':
     app.run(debug=True)
