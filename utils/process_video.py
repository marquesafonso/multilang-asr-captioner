import logging, os
from utils.subtitler import subtitler

def process_video(invideo_file: str,
                srt_string:str,
                srt_json: str,
                fontsize:str,
                font:str,
                bg_color:str,
                text_color:str,
                highlight_mode: bool,
                highlight_color: str,
                caption_mode:str,
                temp_dir: str
                ):
    invideo_path_parts = os.path.normpath(invideo_file).split(os.path.sep)
    VIDEO_NAME = os.path.basename(invideo_file)
    OUTVIDEO_PATH = os.path.join(os.path.normpath('/'.join(invideo_path_parts[:-1])), f"result_{VIDEO_NAME}")
    logging.info("Subtitling...")
    subtitler(invideo_file, srt_string, srt_json, OUTVIDEO_PATH, fontsize, font, bg_color, text_color, highlight_mode, highlight_color, caption_mode, temp_dir)
    return OUTVIDEO_PATH
