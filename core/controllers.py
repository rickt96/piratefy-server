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
    return " LIMIT {} OFFSET {} ".format(limit, offset)


#
# controller canzoni
#
class SongsController:

    select = """
            select 
                s.SONG_ID, s.TITLE, s.ALBUM_ID, s.LENGTH, s.TRACK_NO, al.title as 'ALBUM_NAME', al.cover_url as 'ALBUM_COVER', ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_COVER', ar.ARTIST_ID
            from 
                SONGS as s
                join ALBUMS as al on s.album_id = al.album_id
                join ARTISTS as ar on al.artist_id = ar.artist_id
            """

    def getAll(self, limit=LIMIT, page=PAGE, query=''):
        '''restituisce tutte le canzoni'''
        where = " WHERE s.TITLE LIKE '%{0}%' ".format(query) if query != '' else ""
        limit = paginate(limit, page)
        data = db_conn.select(self.select + where + limit)
        return data


    def getById(self, song_id):
        '''restituisce la canzone con l'id specificato'''
        where = " where s.song_id = " + str(song_id)
        data = db_conn.select(self.select + where)
        return data[0] if len(data)>0 else {}


    def getByArtist(self, artist_id):
        '''restituisce tutte le canzoni dell'artista specificato'''
        where = " WHERE ar.artist_id = " + str(artist_id)
        data = db_conn.select(self.select + where)
        return data


    def getByAlbum(self, album_id):
        '''restituisce tutte le canzoni dell'album specificato'''
        where = " WHERE s.album_id = " + str(album_id)
        print(self.select + where)
        data = db_conn.select(self.select + where)
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

    select = """
            select 
                al.ALBUM_ID, al.TITLE, al.ARTIST_ID, al.DATE, al.COVER_URL, al.SPOTIFY_ID, ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_IMAGE'
            from 
                ALBUMS as al
                join artists as  ar on al.artist_id = ar.artist_id
            """

    def getAll(self, limit=LIMIT, page=PAGE, query=''):
        '''restituisce tutti gli album'''
        where = " WHERE al.TITLE LIKE '%{0}%' ".format(query) if query != '' else ""
        limit = paginate(limit, page)
        data = db_conn.select(self.select + where + limit)
        return data
    

    def getById(self, album_id):
        '''restituisce l'album con l'id specificato'''
        where = " where al.album_id = " + str(album_id)
        data = db_conn.select(self.select + where)
        return data[0] if len(data)>0 else {}


    def getByArtist(self, artist_id):
        '''restituisce tutti gli album dell'artista specificato'''
        where = " where ar.artist_id = " + str(artist_id)
        data = db_conn.select(self.select + where)
        return data



#
# controller artisti
#
class ArtistsController:

    select = "SELECT * FROM ARTISTS"

    def getAll(self, limit=LIMIT, page=PAGE, query=''):
        '''restituisce tutti gli artisti'''
        where = " WHERE NAME LIKE '%{0}%' ".format(query) if query != '' else ""
        limit = paginate(limit, page)
        data = db_conn.select(self.select + where + limit)
        return data
    

    def getById(self, artist_id):
        '''restituisce l'artista con l'id specificato'''
        where = " WHERE ARTIST_ID = " + str(artist_id)
        data = db_conn.select(self.select + where)
        return data[0] if len(data)>0 else {}