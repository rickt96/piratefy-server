import sys
import os


def progress(current, total):
    sys.stdout.write("\r  %d/%d analyzed" % (current, total))
    sys.stdout.flush()


def delete(file_path):
    '''delete a file'''
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        return True
    except Exception as ex:
        print("unable to delete file: ", ex)
        return False
