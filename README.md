## Multilang ASR Captioner

A multilingual automatic speech recognition and video captioning tool using faster whisper on cpu.

## Requirements and Instalations

To run this tool you will need the following sofware installed on your computer:
+ [ImageMagick](https://imagemagick.org/script/download.php)
+ [Python (3.11)](https://www.python.org/downloads/release/python-3116/)

Once you are at your desired working directory, run the following commands on your terminal:

```{bash}
git clone git@github.com:marquesafonso/multilang-asr-captioner.git

pip install pipenv

pipenv install
```

Note that this assumes a proper Git installation and ssh key configuration. 

## Quick start

### Command Line Interface

Run the following code to your example using the CLI. The example is based on a youtube video url (optional):

```
pipenv run python .\cli.py --invideo_filename '<your_file_name>' --video_url 'https://www.youtube.com/watch?v=<your_youtube_video>' --max_words_per_line 8
```

Fontsize, Font, Background Color and Text Color arguments are available:

```
pipenv run python .\cli.py --invideo_filename '<your_file>' --video_url 'https://www.youtube.com/watch?v=<your_youtube_video>' --max_words_per_line 8 --fontsize 28 --font "Arial-Bold" --bg_color None --text_color 'white'
```

### API

A FastAPI API is also made available.

To start the API run:

```
pipenv run python main.py
```

Then check the [landing page](http://127.0.0.1:8000). 

From there you will see the [submit_video endpoint](http://127.0.0.1:8000/submit_video/) and the [documentation](http://127.0.0.1:8000/docs/)
