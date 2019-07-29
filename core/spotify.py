import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError


# parametri ruqest api
base_url = 'https://api.spotify.com/v1/'
client_id = '0385111ec7b4489d8f14a5043fc2a9da' #os.environ['SPOTIPY_CLIENT_ID']
client_secret = 'bdab4e32063f4404a362c08146533173' #os.environ['SPOTIPY_CLIENT_SECRET']
username = '21sbnltyv77x7qh3di767nsoy'
redirect_uri = 'http://localhost:8080/callback'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
token = None



def getToken():
    try:
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)


def getArtistInfo(artistName=''):
    info = { "image":'', "spotify_id":'', "name":'' }
    spotifyObject = spotipy.Spotify(auth=token)
    searchResult = spotifyObject.search(artistName,1,0,"artist")
    if len(searchResult['artists']['items']) > 0:
        info['image'] = searchResult['artists']['items'][0]['images'][1]
        info['spotify_id'] = searchResult['artists']['items'][0]['id']
        info['name'] = searchResult['artists']['items'][0]['name']
    return info


def getAlbumInfo(albumName):
    info = { "cover":'', "spotify_id":'', "name":'', "year": 0 }
    pass