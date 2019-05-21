import sys
import os


# stampa a schermo una progressione del tipo 10/50 analizzati
def progress(current, total):
    '''stampa a schermo una progress bar'''
    sys.stdout.write("\r  %d/%d analyzed" % (current, total))
    sys.stdout.flush()


# cancella un file specifico
def delete(file_path):
    '''elimina un file'''
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True
    except Exception as ex:
        print("unable to delete file: ", ex)
        return False





# restituisce tutti i files mp3 nelle directory indicate
def getFiles(directories=[]):
    files = []
    for directory in directories:           # r=root, d=directories, f=files
        for r, d, f in os.walk(directory):
            for file in f:
                if file.endswith('.mp3'): # tuple(extensions)
                    files.append(os.path.join(r, file))
    return files