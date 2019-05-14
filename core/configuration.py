import json
import os


# percorso del file di configurazione
CONFIG_PATH = "config.json"


class config:
    '''json configuration manager'''

    cfg = {}

    def __init__(self, json_path=CONFIG_PATH):
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