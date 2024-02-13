## Multilang ASR Captioner

A multilingual automatic speech recognition and video captioning tool using faster whisper on cpu.

<video width="400" height="300" src="https://github.com/marquesafonso/multilang-asr-captioner/assets/79766107/fcff8ac1-cdfc-4400-821c-f797d84c2d8a"></video>

## Docker

1. clone the repo
```{bash}
git clone git@github.com:marquesafonso/multilang-asr-captioner.git
```
2. Build and run the container using docker-compose

```{bash}
docker compose up
```
Then check the [landing page](http://127.0.0.1:8000). 

From there you will see the [submit_video endpoint](http://127.0.0.1:8000/submit_video/) and the [documentation](http://127.0.0.1:8000/docs/)

Tip: on Linux or Mac localhost will resolve directly to 0.0.0.0 but on windows you will need to change it to 127.0.0.1

## Local

### Requirements and Instalations

To run this tool locally on your computer you will need the following sofware installed:
+ [ImageMagick](https://imagemagick.org/script/download.php)
+ [Python (3.11)](https://www.python.org/downloads/release/python-3116/)

Once you are at your desired working directory, run the following commands on your terminal:

```{bash}
git clone git@github.com:marquesafonso/multilang-asr-captioner.git

pip install pipenv

pipenv install
```

Note that this assumes a proper Git installation and ssh key configuration. 

### Quick start

#### Command Line Interface

Run the following code to your example using the CLI. The example is based on a youtube video url (optional):

```
pipenv run python cli.py --invideo_filename '<your_file_name>' --video_url 'https://www.youtube.com/watch?v=<your_youtube_video>' --max_words_per_line 8
```

Fontsize, Font, Background Color and Text Color arguments are available:

```
pipenv run python cli.py --invideo_filename '<your_file>' --video_url 'https://www.youtube.com/watch?v=<your_youtube_video>' --max_words_per_line 8 --fontsize 28 --font "Arial-Bold" --bg_color None --text_color 'white'
```

#### API

A FastAPI API is also made available.

To start the API run:

```
pipenv run python main.py
```

Then check the [landing page](http://127.0.0.1:8000). 

From there you will see the [submit_video endpoint](http://127.0.0.1:8000/submit_video/) and the [documentation](http://127.0.0.1:8000/docs/)
