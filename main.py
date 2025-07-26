import shutil, os, logging, uvicorn, tempfile
from typing import Optional

from utils.process_video import process_video
from utils.zip_response import zip_response
from utils.read_html import read_html

from fastapi import FastAPI, UploadFile, HTTPException, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi.security import HTTPBasic
from pydantic import BaseModel, field_validator

## THIS IS A BREAKING CHANGE. SRT FILE INPUT DEPRECATED. WIP.
## TODO: add word level highlighting option
## TODO: separate transcriber from subtitler logic + allow for interactive validation of trancription in-browser
## TODO: add video preview component
## TODO: improve loading spinner.

app = FastAPI()
security = HTTPBasic()
api_configs_file = os.path.abspath("api_config.yml")
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class MP4Video(BaseModel):
    video_file: UploadFile
    
    @property
    def filename(self):
        return self.video_file.filename
    @property
    def file(self):
        return self.video_file.file

    @field_validator('video_file')
    def validate_video_file(cls, v):
        if not v.filename.endswith('.mp4'):
            raise HTTPException(status_code=500, detail='Invalid video file type. Please upload an MP4 file.')
        return v

@app.get("/")
async def root():
    html_content = f"""
    {read_html(os.path.join(os.getcwd(),"static/landing_page.html"))}
    """
    return HTMLResponse(content=html_content)


@app.get("/submit_video/")
async def get_form():
    html_content = f"""
    {read_html(os.path.join(os.getcwd(),"static/submit_video.html"))}
    """
    return HTMLResponse(content=html_content)

async def get_temp_dir():
    dir = tempfile.TemporaryDirectory()
    try:
        yield dir.name
    finally:
        del dir

@app.post("/process_video/")
async def process_video_api(video_file: MP4Video = Depends(),
                            task: Optional[str] = Form("transcribe"),
                            model_version: Optional[str] = Form("deepdml/faster-whisper-large-v3-turbo-ct2"),
                            max_words_per_line: Optional[int] = Form(6),
                            fontsize: Optional[int] = Form(42),
                            font: Optional[str] = Form("FuturaPTHeavy"),
                            bg_color: Optional[str] = Form("#070a13b3"),
                            text_color: Optional[str] = Form("white"),
                            caption_mode: Optional[str] = Form("desktop"),
                            temp_dir: str = Depends(get_temp_dir)
                            ):
    try:
        logging.info("Creating temporary directories")
        with open(os.path.join(temp_dir, video_file.filename), 'w+b') as temp_file:
            logging.info("Copying video UploadFile to the temporary directory")
            try:
                shutil.copyfileobj(video_file.file, temp_file)
            finally:
                video_file.file.close()
            logging.info("Copying SRT UploadFile to the temp_input_path")
            with open(os.path.join(temp_dir, f"{video_file.filename.split('.')[0]}.srt"), 'w+') as temp_srt_file:
                logging.info("Processing the video...")
                output_path, srt_string = process_video(temp_file.name, task, model_version, max_words_per_line, fontsize, font, bg_color, text_color, caption_mode, api_configs_file)
                temp_srt_file.write(srt_string)    
            logging.info("Zipping response...")
            with open(os.path.join(temp_dir, f"{video_file.filename.split('.')[0]}.zip"), 'w+b') as temp_zip_file:
                zip_file = zip_response(temp_zip_file.name, [output_path, temp_srt_file.name])
                return Response(
                    content = zip_file,
                    media_type="application/zip",
                    headers={"Content-Disposition": f"attachment; filename={video_file.filename.split('.')[0]}.zip"}
                    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)