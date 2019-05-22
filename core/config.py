import json
import os
from . import CONFIG_PATH


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

    def fetchArtistsInfo(self):
        return self.cfg["fetch_artists_info"]

    def fetchAlbumsInfo(self):
        return self.cfg["fetch_albums_info"]

    def getDirs(self):
        '''return valid directories from config'''
        raw = self.cfg["dirs"]
        dirs = []
        for d in raw:
            if os.path.isdir(d):
                dirs.append(d)
        return dirs
    
    def createConfig(self, config_path=CONFIG_PATH):
        """TODO crea un file di configurazione vuoto"""
        cfg = """
        {
            "db_path": "db\\db.sqlite",
            "api_key" : "YOUR_API_KEY",
            "db_schema" : "db\\structure.sql",
            "dirs": [ ],
            "fetch_metadata" : false,
            "last_scan" : "",
            "server_port" : 5000
        }
        """
        with open(config_path, "w") as fh:
            fh.write(cfg)