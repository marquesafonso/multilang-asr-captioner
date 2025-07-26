import logging, os
from utils.transcriber import transcriber
from utils.subtitler import subtitler

def process_video(invideo_file: str,
                  task: str,
                  model_version: str,
                  max_words_per_line:int,
                  fontsize:str,
                  font:str,
                  bg_color:str,
                  text_color:str,
                  caption_mode:str,
                  config_file:str
                  ):
    invideo_path_parts = os.path.normpath(invideo_file).split(os.path.sep)
    VIDEO_NAME = os.path.basename(invideo_file)
    OUTVIDEO_PATH = os.path.join(os.path.normpath('/'.join(invideo_path_parts[:-1])), f"result_{VIDEO_NAME}")
    srt_string = transcriber(invideo_file, max_words_per_line, task, model_version, config_file)
    logging.info("Subtitling...")
    subtitler(invideo_file, srt_string, OUTVIDEO_PATH, fontsize, font, bg_color, text_color, caption_mode)
    return OUTVIDEO_PATH, srt_string
