
# https://www.mkyong.com/python/python-how-to-list-all-files-in-a-directory/
# https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python/3964690
# https://stackoverflow.com/questions/18351951/check-if-string-ends-with-one-of-the-strings-from-a-list

""" import os

path = 'D:\\MUSICA\\'
extensions = ['.mp3', '.flac']
files = []

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        #if '.mp3' in file:
        if file.endswith(tuple(extensions)):
            files.append(os.path.join(r, file))

print(files)
print(len(files)) """

from mp3_tagger import MP3File, VERSION_1
from core import *

songs = getFiles(["D:\\MUSICA\\"], [".mp3"])

for song in songs:
    mp3 = MP3File(song)
    mp3.set_version(VERSION_1)
    tags = mp3.get_tags()
    print(tags)