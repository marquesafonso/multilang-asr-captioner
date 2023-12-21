# Import necessary modules
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
                  srt_path: str,
                  max_words_per_line:int,
                  fontsize:str,
                  font:str,
                  bg_color:str,
                  text_color:str
                  ):
    OUTVIDEO_PATH = os.path.join("temp/", "result.mp4")
    if srt_path:
        subtitler(invideo_filename, srt_path, OUTVIDEO_PATH, fontsize, font, bg_color, text_color)
        return OUTVIDEO_PATH
    SRT_PATH = os.path.abspath(f"{invideo_filename.split('.')[0]}.srt")
    if not os.path.exists(SRT_PATH):
        transcriber(invideo_filename, SRT_PATH, max_words_per_line)
    logging.info("Transcription Complete")
    subtitler(invideo_filename, SRT_PATH, OUTVIDEO_PATH, fontsize, font, bg_color, text_color)
    logging.info("Subtitling Complete")
    return OUTVIDEO_PATH
