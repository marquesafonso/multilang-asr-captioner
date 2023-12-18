from argparse import ArgumentParser
from utils.download_video import download_video
from utils.transcriber import transcriber
from utils.subtitler import subtitler
import logging, os
from tqdm import tqdm

logging.basicConfig(filename='main.log',
                encoding='utf-8',
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')

def main(video_url,
        invideo_filename,
        fontsize,
        bg_color,
        max_words_per_line
        ):
    INVIDEO_DIR = os.path.join('data/',invideo_filename)
    if not os.path.exists(INVIDEO_DIR):
        os.makedirs(INVIDEO_DIR)
    SRT_PATH = os.path.join(INVIDEO_DIR, f"{invideo_filename}.srt")
    OUTVIDEO_PATH = os.path.join(INVIDEO_DIR, f"result_{invideo_filename}.mp4")
    with tqdm(total=100, desc="Overall Progress") as pbar:       
        if video_url != None:
            stream_title = download_video(video_url, INVIDEO_DIR, invideo_filename)
            pbar.update(33.33)
            if not os.path.exists(SRT_PATH):
                transcriber(stream_title, SRT_PATH, max_words_per_line)
            pbar.update(33.33)
            subtitler(stream_title, SRT_PATH, OUTVIDEO_PATH,fontsize, bg_color)
            pbar.update(33.34)
            return
        INVIDEO_PATH = os.path.join(INVIDEO_DIR, f"{invideo_filename}.mp4")
        if not os.path.exists(SRT_PATH):
            transcriber(INVIDEO_PATH, SRT_PATH, max_words_per_line)
        pbar.update(66.66)
        subtitler(INVIDEO_PATH, SRT_PATH, OUTVIDEO_PATH, fontsize,bg_color)
        pbar.update(33.34)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--invideo_filename', required=True, type=str, help='filename')
    parser.add_argument('--video_url', required=False, default=None, type=str, help='A video file to be subtitled (Optional)')
    parser.add_argument('--fontsize', required=False, default=32, type=int, help='Font size for captions (int)')
    parser.add_argument('--bg_color', required=False, default="#070a13b3", type=str, help='Hex color value for caption background colour.')
    parser.add_argument("--max_words_per_line", type=int, default=None, help="(requires --word_timestamps True, no effect with --max_line_width) the maximum number of words in a segment")
    args = parser.parse_args()
    # Example usage
    main(args.video_url,
        args.invideo_filename,
        args.fontsize,
        args.bg_color,
        args.max_words_per_line,
        )