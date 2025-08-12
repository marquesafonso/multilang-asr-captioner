---
title: Multilang Asr Captioner
sdk: docker
emoji: 📚
colorFrom: red
colorTo: blue
app_file: main.py
pinned: true
license: cc-by-nc-4.0
short_description: Multilingual ASR and video captioning tool
---

## Multilang ASR Captioner

A multilingual automatic speech recognition and video captioning tool using faster whisper. 

Supports real-time translation to english. Runs on consumer grade cpu.

<video width="400" height="300" src="https://github.com/marquesafonso/multilang-asr-captioner/assets/79766107/fcff8ac1-cdfc-4400-821c-f797d84c2d8a"></video>

## Requirements and Instalations

### Docker (preferred)

You'll need to install [docker](https://www.docker.com/products/docker-desktop/).

Then, follow the steps below.

1. clone the repo
```{bash}
git clone git@github.com:marquesafonso/multilang-asr-captioner.git
```
2. Build and run the container using docker-compose
```{bash}
docker compose up
```

Check the [landing page](http://127.0.0.1:8000). 

From there you will see the [submit_video endpoint](http://127.0.0.1:8000/submit_video/) and the [documentation](http://127.0.0.1:8000/docs/)

**Tip**: on Linux or Mac localhost will resolve directly to 0.0.0.0 but on windows you will need to change it to 127.0.0.1 or localhost

### Local

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

## Quick start (local)

### API

A FastAPI API is available. To start the API locally, run:

```
pipenv run python main.py
```

Then check the [landing page](http://127.0.0.1:8000).

From there you will see the [submit_video endpoint](http://127.0.0.1:8000/submit_video/) and the [documentation](http://127.0.0.1:8000/docs/)

**Tip**: on Linux or Mac localhost will resolve directly to 0.0.0.0 but on windows you will need to change it to 127.0.0.1 or localhost