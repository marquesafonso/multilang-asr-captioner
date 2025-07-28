import logging, os
from utils.subtitler import subtitler

def process_video(invideo_file: str,
                  srt_string:str,
                  fontsize:str,
                  font:str,
                  bg_color:str,
                  text_color:str,
                  caption_mode:str
                  ):
    invideo_path_parts = os.path.normpath(invideo_file).split(os.path.sep)
    VIDEO_NAME = os.path.basename(invideo_file)
    OUTVIDEO_PATH = os.path.join(os.path.normpath('/'.join(invideo_path_parts[:-1])), f"result_{VIDEO_NAME}")
    logging.info("Subtitling...")
    subtitler(invideo_file, srt_string, OUTVIDEO_PATH, fontsize, font, bg_color, text_color, caption_mode)
    return OUTVIDEO_PATH
