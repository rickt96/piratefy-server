import json
import os


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