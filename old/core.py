import datetime
import json
import sqlite3
import eyed3
import os
import sys
import glob

# -*- coding: utf-8 -*-

eyed3.log.setLevel("ERROR")


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

def setEyeD3Tags(path, title='', artist='', album='', track=0, genre='', year=0 ):
    audiofile = eyed3.load(path)
    audiofile.tag.title = title
    audiofile.tag.artist = artist
    audiofile.tag.album = album
    audiofile.tag.track_num = track
    audiofile.tag.genre = genre
    audiofile.tag.year = year
    audiofile.tag.save(path)



def getEyeD3Tags(path):
    """restituisce i tag del file mp3"""
    # https://www.programiz.com/python-programming/methods/built-in/str
    # https://gist.github.com/sinewalker/c636025bfc4bf3cc3e9992f212a40afa
    # https://stackoverflow.com/questions/8948/accessing-mp3-meta-data-with-python
    result = {
        "error" : True,
        "message" : "",
        "tags" : { }
    }

    try:
        audiofile = eyed3.load(path) # test
        if audiofile is not None:
            title = "unknown title" if audiofile.tag.title is None else audiofile.tag.title     # ridondanza di codice, ma se dichiaro tutto nel dizionario legge come tuple
            artist = "unknown artist" if audiofile.tag.artist is None else audiofile.tag.artist
            album = "unknown album" if audiofile.tag.album is None else audiofile.tag.album
            tracknum = 0 if audiofile.tag.track_num[0] is None else audiofile.tag.track_num[0]
            year = 0 if audiofile.tag.getBestDate() is None else audiofile.tag.getBestDate().year
            result["tags"]["title"] = title
            result["tags"]["artist"] = artist
            result["tags"]["album"] = album
            result["tags"]["tracknum"] = tracknum
            result["tags"]["year"] = year
            result["tags"]["length"] = round(audiofile.info.time_secs)
            result["error"] = False
        else:
            result["error"] = True
            result["message"] = "unable to read file - "+path

    except Exception as e:
        result["error"] = True
        result["message"] = str(e) + " - " + path

    return result



def getFiles(directories=[]):
    files = []
    for directory in directories:           # r=root, d=directories, f=files
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
        return self.cfg["server_port"]

    def getExts(self):
        return self.cfg["exts"]

    def getSchema(self):
        return self.cfg["db_schema"]

    def getFetchMetadata(self):
        return self.cfg["fetch_metadata"]

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
