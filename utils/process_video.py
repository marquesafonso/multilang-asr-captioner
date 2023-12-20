# Import necessary modules
from utils.download_video import download_video
from utils.transcriber import transcriber
from utils.subtitler import subtitler
import logging, os

# Set up logging
logging.basicConfig(filename='main.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# API Function
def process_video(invideo_filename:str,
                  fontsize:str,
                  bg_color:str,
                  max_words_per_line:int
                  ):
    SRT_PATH = os.path.abspath(f"{invideo_filename.split('.')[0]}.srt")
    OUTVIDEO_PATH = os.path.join("temp/", f"result.mp4")
    if not os.path.exists(SRT_PATH):
        transcriber(invideo_filename, SRT_PATH, max_words_per_line)
    logging.info("Transcription Complete")
    subtitler(invideo_filename, SRT_PATH, OUTVIDEO_PATH, fontsize, bg_color)
    logging.info("Subtitling Complete")
    return OUTVIDEO_PATH
