## Multilang ASR Captioner

A multilingual automatic speech recognition and video captioning CLI tool using faster whisper on cpu.

## Requirements and Instalations

To run this tool you will need the following sofware installed on your computer:
+ [ImageMagick](https://imagemagick.org/script/download.php)
+ [Python (3.11)](https://www.python.org/downloads/release/python-3116/)

```{bash}
git clone git@github.com:marquesafonso/resultados_eleitorais_autarquias_76-97.git

pip install pipenv

pipenv install
```

## Quick start

Run the following code to your example. The example is based on a youtube video url (optional):

```
pipenv run python .\main.py --invideo_dir './data/' --invideo_filename '<your_video>.mp4' --outvideo_path './data/<output_video>.mp4' --video_url 'https://www.youtube.com/watch?v=<your_youtube_video>' --srt_path '<your_srt_file>.srt'
```

Fontsize and Background Color arguments are available:

```
pipenv run python .\main.py --invideo_dir './data/' --invideo_filename '<your_video>.mp4' --outvideo_path './data/<output_video>.mp4' --video_url 'https://www.youtube.com/watch?v=<your_youtube_video>' --srt_path '<your_srt_file>.srt' --fontsize 28 --bg_color None
```
