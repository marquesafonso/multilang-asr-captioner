import shutil, os
from datetime import datetime

def archiver(timestamp:datetime):
    ARCHIVE = os.path.abspath(f"archive/{timestamp.year:4d}-{timestamp.month:2d}-{timestamp.day:2d}/")
    TEMP_DIR = os.path.abspath("temp/")
    LOG_FILE = os.path.abspath("main.log")
    if os.path.exists(TEMP_DIR):
        shutil.make_archive(os.path.join(ARCHIVE, "files"), 'zip', TEMP_DIR)
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(LOG_FILE):
        shutil.copy(LOG_FILE, os.path.join(ARCHIVE, f"{timestamp.year:4d}-{timestamp.month:2d}-{timestamp.day:2d}.log"))
        os.remove(LOG_FILE)

if __name__ == '__main__':
    archiver(timestamp=datetime.now())