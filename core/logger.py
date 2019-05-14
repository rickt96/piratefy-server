import datetime

LOG_PATH = "log.txt"

def write_log(sender, text):
    log = datetime.datetime.now() + ";" + sender + ";" + text
    with open(LOG_PATH, "w+") as fh:
        fh.write(log)