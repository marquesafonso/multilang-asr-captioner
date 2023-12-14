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
        srt_path,
        invideo_dir,
        invideo_filename,
        outvideo_path,
        fontsize,
        bg_color):
    with tqdm(total=100, desc="Overall Progress") as pbar:       
        if video_url != None:
            stream_title = download_video(video_url, invideo_dir, filename='video.mp4')
            pbar.update(33.33)
            if not os.path.exists(srt_path):
                transcriber(stream_title, srt_path)
            pbar.update(33.33)
            subtitler(stream_title, srt_path, outvideo_path,fontsize, bg_color)
            pbar.update(33.34)
            return
        if not os.path.exists(srt_path):
            transcriber(os.path.join(invideo_dir,invideo_filename), srt_path)
        pbar.update(66.66)
        subtitler(os.path.join(invideo_dir,invideo_filename), srt_path, outvideo_path, fontsize,bg_color)
        pbar.update(33.34)
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--invideo_dir', required=True, type=str, help='path to the input video dir')
    parser.add_argument('--invideo_filename', required=True, type=str, help='filename and extension of ')
    parser.add_argument('--outvideo_path', required=True, help='path to the output video')
    parser.add_argument('--video_url', required=False, default=None, type=str, help='A video file to be subtitled (Optional)')
    parser.add_argument('--srt_path', required=False, default="data/audio.srt", type=str, help='path to the srt file (default: data/audio.srt)')
    parser.add_argument('--fontsize', required=False, default=32, type=int, help='Font size for captions (int)')
    parser.add_argument('--bg_color', required=False, default="#070a13b3", type=str, help='Hex color value for caption background colour.')
    args = parser.parse_args()
    # Example usage
    main(args.video_url, args.srt_path, args.invideo_dir, args.invideo_filename, args.outvideo_path, args.fontsize, args.bg_color)