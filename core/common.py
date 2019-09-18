import sys
import os
import csv



def progress(current, total):
    """stampa a schermo una progressione"""
    sys.stdout.write("\r  %d/%d analyzed" % (current, total))
    sys.stdout.flush()

    if current == total: # manda a capo alla fine della progressione
        sys.stdout.write('\n')



def delete(file_path):
    '''elimina un file'''
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True
    except Exception as ex:
        print("unable to delete file: ", ex)
        return False



def getFiles(directories=[], extensions=[".mp3"]):
    """ottiene tutti i file nelle cartelle e sottocartelle con l'estensione specificata
    
    "directories" è la lista di cartelle da scansionare ricorsivamente
    "extensions" è la lista di estensioni da cercare, di default accetta solo .mp3

    restituisce un'array di files
    """
    files = []
    for directory in directories:           # r=root, d=directories, f=files
        for r, d, f in os.walk(directory):
            for file in f:
                if file.endswith(tuple(extensions)):
                    files.append(os.path.join(r, file))
    return files



def prompt(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    valid = {
        "yes": True, "y": True, "si": True, "s":True,
        "no": False, "n": False
        }
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")



def createCsv(filename="scan.csv", data=[]):
    #https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
    #https://realpython.com/python-csv/#reading-csv-files-with-csv
    with open(filename, 'w+', newline='',  encoding="utf-16") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL) #, quotechar='|', quoting=csv.QUOTE_MINIMAL
        for row in data:
            writer.writerow(row)



def readCsv(filename="scan.csv", includeHeader=False):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader((line.replace('\0','') for line in f), delimiter=';') #csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data