from utils.transcriber import transcriber
from utils.subtitler import subtitler
from utils.convert_video_to_audio import convert_video_to_audio
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
    invideo_filename = os.path.normpath(invideo_filename)
    invideo_path_parts = invideo_filename.split(os.path.sep)
    VIDEO_NAME = invideo_path_parts[-1]
    OUTVIDEO_PATH = os.path.join(invideo_path_parts[-3], invideo_path_parts[-2], f"result_{VIDEO_NAME}")
    if srt_path:
        subtitler(invideo_filename, srt_path, OUTVIDEO_PATH, fontsize, font, bg_color, text_color)
        return OUTVIDEO_PATH
    logging.info("Converting Video to Audio")
    INAUDIO_PATH = os.path.abspath(f"{invideo_filename.split('.')[0]}.m4a")
    if not os.path.exists(INAUDIO_PATH):
        convert_video_to_audio(invideo_filename, INAUDIO_PATH)
    SRT_PATH = os.path.abspath(f"{invideo_filename.split('.')[0]}.srt") 
    logging.info("Transcribing...")
    if not os.path.exists(SRT_PATH):
        transcriber(INAUDIO_PATH, SRT_PATH, max_words_per_line)
    logging.info("Subtitling...")
    subtitler(invideo_filename, SRT_PATH, OUTVIDEO_PATH, fontsize, font, bg_color, text_color)
    return OUTVIDEO_PATH, SRT_PATH
