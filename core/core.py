
import sqlite3
#import taglib #TO REMOVE
#from eyed3 import id3



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
        '''execute a multiple queries witchout return'''
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




class Config:
    '''json configuration manager'''

    cfg = {}

    def __init__(self, json_path=""):
        """load a json file"""
        if json_path != "":
            with open(json_path, "r") as jh:
                self.cfg = json.load(jh)

    def getdb(self):
        return self.cfg["db_path"]

    def getapikey(self):
        return self.cfg["scanner"]["api_key"]

    def getport(self):
        return self.cfg["server"]["service_port"]

    def getexts(self):
        return self.cfg["scanner"]["exts"]

    def getschema(self):
        return self.cfg["scanner"]["db_schema"]

    def getdirs(self):
        '''return valid directories from config'''
        raw = self.cfg["scanner"]["dirs"]
        dirs = []
        for d in raw:
            if os.path.isdir(d):
                dirs.append(d)
        return dirs



