import json
import sqlite3
import taglib
import os
import sys


CONFIG_PATH = "config.json"


def progress(current, total):
    sys.stdout.write("\r  %d/%d analyzed" % (current, total))
    sys.stdout.flush()


def dict_factory(cursor, row):
    '''convert to dictionary a sqlite results set'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def delete(file_path):
    '''delete a file'''
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True
    except Exception as ex:
        print("unable to delete file: ", ex)
        return False


'''
add description here
'''
class Database:
    '''sqlite3 database connection and operation manager'''

    dbconn = None

    def __init__(self, db_path=""):
        """load a specific sqlite file and open connection"""
        if db_path != "":
            self.dbconn = sqlite3.connect(db_path)
            self.dbconn.row_factory = dict_factory


    def execute(self, query="", *params):
        '''execute a query without return (for insert, update delete)'''
        self.dbconn.execute(query, (params))


    def executescript(self, sqlscript=""):
        self.dbconn.executescript(sqlscript)
        

    def select(self, query=""):
        '''execute select query and return a dictionary'''
        cur = self.dbconn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows


    def fetchone(self, query=""):
        '''execute a query and return a single value'''
        cur = self.dbconn.cursor()
        cur.execute(query)
        row = cur.fetchone()
        return row


    def commit(self):
        self.dbconn.commit()


    def close(self):
        self.dbconn.close()



'''
add description here
'''
class Config:
    '''json configuration manager'''

    cfg = {}

    def __init__(self, json_path=""):
        """load a specific json file"""
        if json_path != "":
            with open(json_path, "r") as jh:
                self.cfg = json.load(jh)

    def getdb(self):
        return self.cfg["db"]

    def getapikey(self):
        return self.cfg["scanner"]["api_key"]

    def getport(self):
        return self.cfg["server"]["service_port"]

    def getexts(self):
        return self.cfg["scanner"]["exts"]

    def getschema(self):
        return self.cfg["scanner"]["ddl"]

    def getdirs(self):
        '''return valid directories from config'''
        raw = self.cfg["scanner"]["dirs"]
        dirs = []
        for d in raw:
            if os.path.isdir(d):
                dirs.append(d)
        return dirs




'''
add description here
'''
class Scanner:
    '''song scan manager'''

    def getsongtags(self, song_path):
        '''return song metadata'''

        def _cleartext(text):
            val = text
            val = val.rstrip()    # rimuove gli spazi vuoti all'inizio
            val = val.title()     # imposta tutte le lettere iniziali maiuscole
            return val

        def _cleartrack(track):
            val = track
            out = track
            index = val.find("/")
            if index > -1:
                out = val[:index]
            return out


        s = taglib.File(song_path)
        title = album = artist = "" 
        date = trackno = 0

        if "TITLE" in s.tags:
            if len(s.tags["TITLE"]) > 0:
                title = s.tags["TITLE"][0] #.replace("\"", "'")
        
        if "ALBUM" in s.tags:
            if len(s.tags["ALBUM"]) > 0:
                album = s.tags["ALBUM"][0] #.replace("\"", "'")
        
        if "ARTIST" in s.tags:
            if len(s.tags["ARTIST"]) > 0:
                artist = s.tags["ARTIST"][0]
                artist = _cleartext(artist)

        if "DATE" in s.tags:
            if len(s.tags["DATE"]) > 0:
                date = s.tags["DATE"][0]

        if "TRACKNUMBER" in s.tags:
            if len(s.tags["TRACKNUMBER"]) > 0:
                trackno = s.tags["TRACKNUMBER"][0]
                trackno = _cleartrack(trackno)

        return title, artist, album, date, trackno, s.length

    def getfiles(self, exts=[], paths=[]):
        '''find and return all files with specified extension in the indicated paths'''

        files = []

        for dir in paths:
            for root, dirs, files in os.walk(dir):
                for f in files:
                    fullpath = os.path.join(root, f)
                    if os.path.splitext(fullpath)[1] in exts:
                        files.append(fullpath)
        
        return files




class Logger:

    log_path = None

    def __init__(self, log_path=""):
        self.log_path = log_path

    def write(self, text):
        with open(self.log_path, "w+") as fh:
            fh.write(text)

