# implementazione libreria spotipy per l'ottenimento dei metadati di album e artisti da spotify
# api reference https://developer.spotify.com/documentation/web-api/reference/search/search/
# https://www.urlencoder.io/python/

import spotipy
import spotipy.oauth2 as oauth2

client_id = '0385111ec7b4489d8f14a5043fc2a9da' #os.environ['SPOTIPY_CLIENT_ID']
client_secret = 'bdab4e32063f4404a362c08146533173' #os.environ['SPOTIPY_CLIENT_SECRET']
token = None


def sanitizeAlbumName(albumName):
    if albumName.find('(') != -1:
        index = albumName.find('(')
        return albumName[0:index].strip()

    if albumName.find('[') != -1:
        index = albumName.find('[')
        return albumName[0:index].strip()

    if albumName.find('{') != -1:
        index = albumName.find('{')
        return albumName[0:index].strip()


def getToken():
    global token
    if token is None:
        credentials = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        token = credentials.get_access_token()



def getArtistInfo(artistName=''):
    result = {
        "status" : False,
        "message" : "",
        "info" : { "image":'', "spotify_id":'', "name":'' }
    }
    getToken()
    sp = spotipy.Spotify(auth=token)
    searchResult = sp.search(q=artistName, limit=1, offset=0, type="artist")
    if len(searchResult['artists']['items']) > 0:
        result["status"] = True
        result["info"]['image'] = searchResult['artists']['items'][0]['images'][1]["url"]
        result["info"]['spotify_id'] = searchResult['artists']['items'][0]['id']
        result["info"]['name'] = searchResult['artists']['items'][0]['name']
    else:
        result["status"] = False
        result["message"] = "no info provided for "+artistName
    return result



def getAlbumInfo(albumName="", artistName=""):
    result = {
        "status" : False,
        "message" : "",
        "info" : { "image":'', "spotify_id":'', "date":'' }
    }
    albumName = sanitizeAlbumName(albumName)
    getToken()
    sp = spotipy.Spotify(auth=token)
    searchResult = sp.search(q="album:"+albumName+" artist:"+artistName, limit=1, offset=0, type="album")
    if len(searchResult['albums']['items']) > 0:
        result["status"] = True
        result["info"]['image'] = searchResult['albums']['items'][0]['images'][1]["url"]
        result["info"]["date"] = searchResult['albums']['items'][0]["release_date"]
        result["info"]["spotify_id"] = searchResult['albums']['items'][0]["id"]
    else:
        result["status"] = False
        result["message"] = "no info provided for "+albumName
    return result