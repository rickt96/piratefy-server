from . import database
from . import config
from . import CONFIG_PATH


LIMIT = 15
PAGE = 0


cfg = config.Config(CONFIG_PATH)
db_conn = database.Database(cfg.getDb())
db_conn.open()


def paginate(limit, page):
    offset = limit * page
    #print(" LIMIT {} OFFSET {} ".format(limit, offset))
    return " LIMIT {} OFFSET {} ".format(limit, offset)


#
# controller canzoni
#
class SongsController:
    
    fields = "s.SONG_ID, s.TITLE, s.ALBUM_ID, s.LENGTH, s.TRACK_NO"

    def getAll(self, limit=LIMIT, page=0):
        '''restituisce tutte le canzoni'''
        q = "SELECT {} FROM SONGS as s {}".format(self.fields, paginate(limit, page))
        data = db_conn.select(q)
        return data

    def getById(self, song_id):
        '''restituisce la canzone con l'id specificato'''
        q = "SELECT {} FROM SONGS as s WHERE SONG_ID = {}".format(self.fields, song_id)
        data = db_conn.select(q)
        return data

    def getByArtist(self, artist_id):
        '''restituisce tutte le canzoni dell'artista specificato'''
        q = """select {}
               FROM SONGS as s
               INNER JOIN ALBUMS AS a ON s.ALBUM_ID = a.ALBUM_ID
               WHERE a.ARTIST_ID = {}
               """.format(self.fields, artist_id)
        data = db_conn.select(q)
        return data

    def getByAlbum(self, album_id):
        '''restituisce tutte le canzoni dell'album specificato'''
        q = "SELECT {} FROM SONGS WHERE ALBUM_ID = {}".format(self.fields, album_id)
        data = db_conn.select(q)
        return data
    
    def getByGenre(self, genre_id):
        '''restituisce tutte le canzoni col genere specificato'''
        q = "SELECT {} FROM SONGS WHERE GENRE_ID = {}".format(self.fields, genre_id)
        data = db_conn.select(q)
        return data

    def getSongPath(self, song_id):
        '''restituisce il percorso della canzone specificata'''
        q = "SELECT PATH FROM SONGS WHERE SONG_ID = {}".format(song_id)
        
        data = db_conn.fetchOne(q) #["PATH"]
        path = data['PATH']
        return path



#
# controller albums
#
class AlbumsController:

    def getAll(self, limit=LIMIT, page=0):
        '''restituisce tutti gli album'''
        q = "SELECT * FROM ALBUMS"+paginate(limit, page)
        data = db_conn.select(q)
        return data
    
    def getById(self, album_id):
        '''restituisce l'album con l'id specificato'''
        q = "SELECT * FROM ALBUMS WHERE ALBUM_ID = {}".format(album_id)
        data = db_conn.select(q)
        return data

    def getByArtist(self, artist_id):
        '''restituisce tutti gli album dell'artista specificato'''
        q = "SELECT * FROM ALBUMS WHERE ARTIST_ID = {}".format(artist_id)
        data = db_conn.select(q)
        return data



#
# controller artisti
#
class ArtistsController:

    def getAll(self, limit=LIMIT, page=0):
        '''restituisce tutti gli artisti'''
        q = "SELECT * FROM ARTISTS"+paginate(limit, page)
        data = db_conn.select(q)
        return data
    
    def getById(self, artist_id):
        '''restituisce l'artista con l'id specificato'''
        q = "SELECT * FROM ARTISTS WHERE ARTIST_ID = {}".format(artist_id)
        data = db_conn.select(q)
        return data