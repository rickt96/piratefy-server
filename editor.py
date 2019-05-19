# script per la modifica dei metadati dei file mp3

from core import *


path = sys.argv[1]
source=[]

if os.path.isdir(path):
    print("load files")
    source = getFiles([path])

elif os.path.isfile(path) and path.endswith('.mp3'):
    print("one file")
    source = path

else:
    exit("invalid params")


print(source)

