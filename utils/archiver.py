import shutil, os
from datetime import datetime

def archiver(archive:str, timestamp:datetime):
    TEMP_DIR = os.path.abspath("temp/")
    LOG_FILE = os.path.abspath("main.log")
    if os.path.exists(TEMP_DIR):
        shutil.make_archive(os.path.join(archive, f"{timestamp.year:4d}-{timestamp.month:2d}-{timestamp.day:2d}"), 'zip', [TEMP_DIR, LOG_FILE])
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)