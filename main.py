import shutil, os, logging, uvicorn
from typing import Optional
from uuid import uuid4
from tempfile import TemporaryDirectory

from utils.transcriber import transcriber
from utils.process_video import process_video
from utils.zip_response import zip_response
from utils.read_html import read_html

from fastapi import FastAPI, UploadFile, HTTPException, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.security import HTTPBasic
from pydantic import BaseModel, field_validator
from cachetools import TTLCache

## THIS IS A BREAKING CHANGE. SRT FILE INPUT DEPRECATED.
## DONE: separate transcriber from subtitler logic.
## DONE: improve loading spinner. (redirect)
## DONE: fix tempdir cleanup
## DONE: add transcription preview component + allow for interactive validation of transcription in-browser.
## TODO: add word level highlighting option. WIP (word background margins need to be addressed; mobile mode needs work in json mode)
## TODO: improve UI

app = FastAPI()
security = HTTPBasic()
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=static_dir) 
cache = TTLCache(maxsize=1024, ttl=600)

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

@app.get("/transcribe_video/")
async def get_form():
    html_content = f"""
    {read_html(os.path.join(os.getcwd(),"static/transcribe_video.html"))}
    """
    return HTMLResponse(content=html_content)

async def get_temp_dir():
    dir = TemporaryDirectory(delete=False)
    try:
        yield dir
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe/")
async def transcribe_api(video_file: MP4Video = Depends(),
                        task: str = Form("transcribe"),
                        model_version: str = Form("deepdml/faster-whisper-large-v3-turbo-ct2"),
                        max_words_per_line: int = Form(6),
                        temp_dir: TemporaryDirectory = Depends(get_temp_dir)):
    try:
        video_path = os.path.join(temp_dir.name, video_file.filename)
        with open(video_path, 'wb') as f:
            shutil.copyfileobj(video_file.file, f)

        transcription_text, transcription_json = transcriber(video_path, max_words_per_line, task, model_version)

        uid = str(uuid4())
        cache[uid] = {
            "video_path": video_path,
            "transcription_text": transcription_text,
            "transcription_json": transcription_json,
            "temp_dir_path": temp_dir.name}
        return RedirectResponse(url=f"/process_settings/?uid={uid}", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/process_settings/")
async def process_settings(request: Request, uid: str):
    data = cache.get(uid)
    if not data:
        raise HTTPException(404, "Data not found")
    return templates.TemplateResponse("process_settings.html", {
        "request": request,
        "transcription_text": data["transcription_text"],
        "transcription_json": data["transcription_json"],
        "video_path": data["video_path"],
        "temp_dir_path": data["temp_dir_path"]
    })

@app.post("/process_video/")
async def process_video_api(video_path: str = Form(...),
                            temp_dir_path: str = Form(...),
                            srt_string: str = Form(...),
                            srt_json: str = Form(...),
                            fontsize: Optional[int] = Form(42),
                            font: Optional[str] = Form("Helvetica"),
                            bg_color: Optional[str] = Form("#070a13b3"),
                            text_color: Optional[str] = Form("white"),
                            highlight_mode: Optional[bool] = Form(False),
                            caption_mode: Optional[str] = Form("desktop"),
                            temp_dir: TemporaryDirectory = Depends(get_temp_dir)
                            ):
    try:
        output_path = process_video(video_path, srt_string, srt_json, fontsize, font, bg_color, text_color, highlight_mode, caption_mode)
        with open(os.path.join(temp_dir.name, f"{video_path.split('.')[0]}.srt"), 'w+') as temp_srt_file:
            logging.info("Processing the video...")
            temp_srt_file.write(srt_string)    
            logging.info("Zipping response...")
        with open(os.path.join(temp_dir.name, f"{video_path.split('.')[0]}.zip"), 'w+b') as temp_zip_file:
            zip_file = zip_response(temp_zip_file.name, [output_path, temp_srt_file.name])
        return Response(
            content = zip_file,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(video_path).split('.')[0]}.zip"}
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_dir_path and os.path.exists(temp_dir_path):
            shutil.rmtree(temp_dir_path, ignore_errors=True)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)