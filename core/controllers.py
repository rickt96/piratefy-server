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

    def getAll(self, limit=LIMIT, page=0, sort='', asc=True, query=''):
        '''restituisce tutte le canzoni'''
        #q = "SELECT {} FROM SONGS as s {}".format(self.fields, paginate(limit, page))
        # song_id, title, album_id, length, track_no, path, album_name, album_cover, artist_name, artist_cover, artist_id
        select = """
            select s.*, al.title as 'ALBUM_NAME', al.cover_url as 'ALBUM_COVER', ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_COVER', ar.ARTIST_ID
            from SONGS as s
            join ALBUMS as al on s.album_id = al.album_id
            join ARTISTS as ar on al.artist_id = ar.artist_id
        """ 
        where = ""
        if query != '':
            where = " WHERE s.TITLE LIKE '%{0}%' OR ALBUM_NAME LIKE '%{0}%' OR ARTIST_NAME LIKE '%{0}%' ".format(query)

        orderby = ""
        if sort != '':
            order = "ASC" if asc else "DESC"
            orderby = " ORDER BY '{0}' {1} ".format(sort, order)
        
        limit = paginate(limit, page)

        print(select + where + orderby + limit)
        data = db_conn.select(select + where + orderby + limit)
        return data

    def getById(self, song_id):
        '''restituisce la canzone con l'id specificato'''
        #q = "SELECT {} FROM SONGS as s WHERE SONG_ID = {}".format(self.fields, song_id)
        q = """
            select s.*, al.title as 'ALBUM_NAME', al.cover_url as 'ALBUM_COVER', ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_COVER', ar.ARTIST_ID
            from SONGS as s
            join ALBUMS as al on s.album_id = al.album_id
            join ARTISTS as ar on al.artist_id = ar.artist_id
            where s.song_id = 
        """ + str(song_id)
        data = db_conn.select(q)
        return data

    def getByArtist(self, artist_id):
        '''restituisce tutte le canzoni dell'artista specificato'''
        #TODO
        #q = """select {}
        #       FROM SONGS as s
        #       INNER JOIN ALBUMS AS a ON s.ALBUM_ID = a.ALBUM_ID
        #       WHERE a.ARTIST_ID = {}
        #       """.format(self.fields, artist_id)
        #data = db_conn.select(q)
        #return data

    def getByAlbum(self, album_id):
        '''restituisce tutte le canzoni dell'album specificato'''
        #q = "SELECT {} FROM SONGS WHERE ALBUM_ID = {}".format(self.fields, album_id)
        q = """
            select s.*, al.title as 'ALBUM_NAME', al.cover_url as 'ALBUM_COVER', ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_COVER', ar.ARTIST_ID
            from SONGS as s
            join ALBUMS as al on s.album_id = al.album_id
            join ARTISTS as ar on al.artist_id = ar.artist_id
            where al.album_id = 
        """ + str(album_id)
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

    def getAll(self, limit=LIMIT, page=0, sort=''):
        '''restituisce tutti gli album'''
        #q = "SELECT * FROM ALBUMS"+paginate(limit, page)
        q = """
            select al.*, ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_IMAGE'
            from ALBUMS as al
            join artists as  ar on al.artist_id = ar.artist_id
        """ + paginate(limit, page)
        data = db_conn.select(q)
        return data
    
    def getById(self, album_id):
        '''restituisce l'album con l'id specificato'''
        #q = "SELECT * FROM ALBUMS WHERE ALBUM_ID = {}".format(album_id)
        # album_id, title, artist_id, date, cover_url, spotify_id, artist_name, artist_image
        q = """
            select al.*, ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_IMAGE'
            from ALBUMS as al
            join artists as  ar on al.artist_id = ar.artist_id
            where al.album_id = 
        """ + str(album_id)
        data = db_conn.select(q)
        return data

    def getByArtist(self, artist_id):
        '''restituisce tutti gli album dell'artista specificato'''
        #q = "SELECT * FROM ALBUMS WHERE ARTIST_ID = {}".format(artist_id)
        q = """
            select al.*, ar.name as 'ARTIST_NAME', ar.image_url as 'ARTIST_IMAGE'
            from ALBUMS as al
            join artists as ar on al.artist_id = ar.artist_id
            where ar.artist_id = 
        """ + str(artist_id)
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