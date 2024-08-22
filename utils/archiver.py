import shutil, os
from datetime import datetime

def archiver(timestamp:datetime=datetime.now()):
    TIME = f"{timestamp.year:4d}-{timestamp.month:02d}-{timestamp.day:02d}_{timestamp.hour:02d}-{timestamp.minute:02d}"
    ARCHIVE = os.path.abspath(f"archive/{TIME}")
    TEMP_DIR = os.path.abspath("temp/")
    LOG_FILE = os.path.abspath("main.log")
    if os.path.exists(TEMP_DIR):
        shutil.make_archive(os.path.join(ARCHIVE, "files"), 'zip', TEMP_DIR)
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(LOG_FILE):
        shutil.copy(LOG_FILE, os.path.join(ARCHIVE, f"{TIME}.log"))
        os.remove(LOG_FILE)

if __name__ == '__main__':
    archiver(timestamp=datetime.now())