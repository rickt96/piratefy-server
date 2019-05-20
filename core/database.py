# Database
# classe di gestione della connessione al db sqlite


import sqlite3


class Database:
    '''sqlite3 database connection and operation manager'''

    dbconn = None

    def dict_factory(self, cursor, row):
        '''converte in dizionario un result set del sqlite'''
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def __init__(self, db_path=""):
        """load a specific sqlite file and open connection"""
        if db_path != "":
            self.dbconn = sqlite3.connect(db_path, check_same_thread=False) # connect() crea il file se non esiste
            self.dbconn.row_factory = self.dict_factory


    def __del__(self):
        self.close()


    def execute(self, query="", *params):
        '''execute a query without return (for insert, update delete)'''
        self.dbconn.execute(query, (params))


    def executeScript(self, sqlscript=""):
        '''esegue uno script contenete più di una query'''
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
        '''commit della transazione corrente'''
        self.dbconn.commit()


    def close(self):
        '''chiusura connessione al file'''
        self.dbconn.close()