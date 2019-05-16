import datetime
import json
import sqlite3
import eyed3
import os
import sys




################################################################################
# PATHS
################################################################################

CONFIG_PATH = "config.json"
LOG_PATH = "log.txt"




################################################################################
# COMMON
################################################################################

def progress(current, total):
    '''stampa a schermo una progress bar'''
    sys.stdout.write("\r  %d/%d analyzed" % (current, total))
    sys.stdout.flush()


def dict_factory(cursor, row):
    '''converte a dizionario un result set del sqlite'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def delete(file_path):
    '''elimina un file'''
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True
    except Exception as ex:
        print("unable to delete file: ", ex)
        return False

def getSongTags(song_path):
    '''return song metadata'''
    title = album = artist = "" 
    date = trackno = length = 0

    audiofile = eyed3.load(song_path)
    title = audiofile.tag.title
    album = audiofile.tag.album
    artist = audiofile.tag.artist
    #date = audiofile.tag.getBestDate().year # eccezzione del tipo Invalid v2.3 TYER, TDAT, or TIME frame: Invalid date string: 2007--
    trackno = audiofile.tag.track_num[0]
    length = round(audiofile.info.time_secs)

    return title, artist, date, album, trackno, length



def getFiles(directories=[]):
    files = []
    for directory in directories:
        # r=root, d=directories, f = files
        for r, d, f in os.walk(directory):
            for file in f:
                if file.endswith('.mp3'): # tuple(extensions)
                    files.append(os.path.join(r, file))
    return files




################################################################################
# DATABASE
################################################################################

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


    def executeScript(self, sqlscript=""):
        self.dbconn.executescript(sqlscript)
        

    def select(self, query=""):
        '''execute select query and return a dictionary'''
        cur = self.dbconn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows


    def fetchOne(self, query=""):
        '''execute a query and return a single value'''
        cur = self.dbconn.cursor()
        cur.execute(query)
        row = cur.fetchone()
        return row


    def commit(self):
        self.dbconn.commit()


    def close(self):
        self.dbconn.close()




################################################################################
# CONFIGURATION MANAGER
################################################################################

class Config:
    '''json configuration manager'''

    cfg = {}

    def __init__(self, json_path=""):
        """load a specific json file"""
        if json_path != "":
            with open(json_path, "r") as jh:
                self.cfg = json.load(jh)

    def getDb(self):
        return self.cfg["db_path"]

    def getApiKey(self):
        return self.cfg["api_key"]

    def getPort(self):
        return self.cfg["service_port"]

    def getExts(self):
        return self.cfg["exts"]

    def getSchema(self):
        return self.cfg["db_schema"]

    def getDirs(self):
        '''return valid directories from config'''
        raw = self.cfg["dirs"]
        dirs = []
        for d in raw:
            if os.path.isdir(d):
                dirs.append(d)
        return dirs




################################################################################
# LOGGER
################################################################################

class Logger:

    log_path = None

    def __init__(self, log_path=LOG_PATH):
        self.log_path = log_path

    def writeLog(self, sender, text):
        log = datetime.datetime.now() + ";" + sender + ";" + text
        with open(LOG_PATH, "w+") as fh:
            fh.write(log)
