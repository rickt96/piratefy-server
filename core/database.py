# Database
# classe di gestione della connessione al db sqlite
# [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]

import os
import sqlite3
from sqlite3 import Error


class Database:
    '''classe di gestione del database sqlite'''

    path = ''
    conn = None
    
    def __init__(self, file_path):
        """carica un file sql ed apre la connessione. se il file non esiste lo crea"""
        self.path = file_path


    def __del__(self):
        pass #self.close()


    def __dictFactory(self, cursor, row):
        '''converte in dizionario un result set del sqlite'''
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def open(self):
        '''apre la connessione al file'''
        try:
            self.conn = sqlite3.connect(self.path, check_same_thread=False) # connect() crea il file se non esiste
            self.conn.row_factory = self.__dictFactory
        except Exception as e:
            print(e)


    def execute(self, query, *params):
        '''esegue una query senza ritorno (insert, update, delete)'''
        try:
            self.conn.execute(query, (params))
            return True
        except Exception as e:
            print(e)


    def executeScript(self, sqlscript):
        '''esegue uno script contenete più di una query'''
        try:
            self.conn.executescript(sqlscript)
        except Exception as e:
            print(e)
        

    def select(self, query):
        '''esegue una select e restituisce un dizionario'''
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(e)


    def fetchOne(self, query):
        '''esegue una query e ritorna un singolo valore'''
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            row = cur.fetchone()
            return row
        except Exception as e:
            print(e)


    def commit(self):
        '''esegue il commit della transazione corrente'''
        self.conn.commit()


    def close(self):
        '''chiude la connessione al file'''
        self.conn.close()