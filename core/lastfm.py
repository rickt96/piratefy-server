import json
import urllib.request
import urllib.error
import urllib.parse
from. import config, CONFIG_PATH

# https://www.w3schools.com/tags/ref_urlencode.asp
# https://www.urlencoder.io/python/

cfg = config.Config(CONFIG_PATH)
api_key = cfg.getApiKey() #"21dde19ce5f13edddc9e3fea33bddb78"

LASTFM_ALBUM_INFO = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist={0}&album={1}&api_key={2}&format=json"
LASTFM_ARTIST_INFO = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={0}&api_key={1}&format=json"



def getAlbumInfo(artist_name, album_title):
    """esegue la chiamata alle webapi di lastfm ed ottiene le informazioni dell'album"""
    cover = ""
    query = LASTFM_ALBUM_INFO.format(
        urllib.parse.quote_plus(artist_name),
        urllib.parse.quote_plus(album_title),
        api_key
        )
    req = urllib.request.urlopen(query)
    html = req.read()
    json_data = json.loads(html)
    
    if "album" in json_data: #finire qui, alcuni album non hanno il tag wiki
        cover = json_data["album"]["image"][3]["#text"]

    return cover



def getArtistInfo(artist_name):
    """esegue la chiamata alle webapi di lastfm ed ottiene le informazioni dell'artista"""
    info = { "image": "", "summary": "" }
    query = LASTFM_ARTIST_INFO.format(
        urllib.parse.quote_plus(artist_name),
        api_key
        )
    req = urllib.request.urlopen(query)
    html = req.read()
    json_data = json.loads(html)

    if "artist" in json_data:
        info["summary"] = json_data["artist"]["bio"]["content"]
        info["image"] = json_data["artist"]["image"][3]["#text"]

    return info