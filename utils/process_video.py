# Import necessary modules
from utils.transcriber import transcriber
from utils.subtitler import subtitler
from utils.convert_mp4_to_mp3 import convert_mp4_to_mp3
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
    VIDEO_NAME = invideo_filename.split('\\')[-1] 
    OUTVIDEO_PATH = os.path.join(invideo_filename.split('\\')[-3], invideo_filename.split('\\')[-2], f"result_{VIDEO_NAME}")
    if srt_path:
        subtitler(invideo_filename, srt_path, OUTVIDEO_PATH, fontsize, font, bg_color, text_color)
        return OUTVIDEO_PATH
    INAUDIO_PATH = os.path.abspath(f"{invideo_filename.split('.')[0]}.mp3")
    convert_mp4_to_mp3(invideo_filename, INAUDIO_PATH)
    SRT_PATH = os.path.abspath(f"{invideo_filename.split('.')[0]}.srt") 
    if not os.path.exists(SRT_PATH):
        transcriber(INAUDIO_PATH, SRT_PATH, max_words_per_line)
    logging.info("Transcription Complete")
    subtitler(invideo_filename, SRT_PATH, OUTVIDEO_PATH, fontsize, font, bg_color, text_color)
    logging.info("Subtitling Complete")
    return OUTVIDEO_PATH
