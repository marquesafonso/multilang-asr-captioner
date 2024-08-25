from fastapi import FastAPI, UploadFile, HTTPException, Form, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from pydantic import BaseModel, field_validator
from utils.process_video import process_video
from utils.zip_response import zip_response
from utils.api_configs import api_configs
from utils.read_html import read_html
from utils.archiver import archiver
from utils.logger import setup_logger
import shutil, os, logging, uvicorn, secrets

app = FastAPI()
security = HTTPBasic()
api_configs_file = os.path.abspath("api_config.yml")

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, api_configs(api_configs_file)["secrets"]["username"])
    correct_password = secrets.compare_digest(credentials.password, api_configs(api_configs_file)["secrets"]["password"])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

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

class SRTFile(BaseModel):
    srt_file: Optional[UploadFile] = None
    
    @property
    def filename(self):
        return self.srt_file.filename
    @property
    def file(self):
        return self.srt_file.file
    @property
    def size(self):
        return self.srt_file.size

    @field_validator('srt_file')
    def validate_srt_file(cls, v):
        if v.size > 0 and not v.filename.endswith('.srt'):
            raise HTTPException(status_code=422, detail='Invalid subtitle file type. Please upload an SRT file.')
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

@app.post("/process_video/")
async def process_video_api(video_file: MP4Video = Depends(),
                            srt_file: SRTFile = Depends(),
                            task: Optional[str] = Form("transcribe"),
                            max_words_per_line: Optional[int] = Form(6),
                            fontsize: Optional[int] = Form(42),
                            font: Optional[str] = Form("FuturaPTHeavy"),
                            bg_color: Optional[str] = Form("#070a13b3"),
                            text_color: Optional[str] = Form("white"),
                            caption_mode: Optional[str] = Form("desktop"),
                            username: str = Depends(get_current_user)
                            ):
    try:
        logging.info("Creating temporary directories")
        temp_dir = os.path.join(os.getcwd(),"temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_vid_dir = os.path.join(temp_dir,video_file.filename.split('.')[0])
        os.makedirs(temp_vid_dir, exist_ok=True)
        temp_input_path = os.path.join(temp_vid_dir, video_file.filename)
        logging.info("Copying video UploadFile to the temp_input_path")
        with open(temp_input_path, 'wb') as buffer:
            try:
                shutil.copyfileobj(video_file.file, buffer)
            finally:
                video_file.file.close()
        logging.info("Copying SRT UploadFile to the temp_input_path")
        if srt_file.size > 0:
            SRT_PATH = os.path.abspath(f"{temp_input_path.split('.')[0]}.srt")
            with open(SRT_PATH, 'wb') as buffer:
                try:
                    shutil.copyfileobj(srt_file.file, buffer)
                finally:
                    srt_file.file.close()
            logging.info("Processing the video...")
            output_path, _ = process_video(temp_input_path, SRT_PATH, task, max_words_per_line, fontsize, font, bg_color, text_color, caption_mode)
            logging.info("Zipping response...")
            zip_path = zip_response(os.path.join(temp_vid_dir,"archive.zip"), [output_path, SRT_PATH])
            return FileResponse(zip_path, media_type='application/zip', filename=f"result_{video_file.filename.split('.')[0]}.zip")
        logging.info("Processing the video...")
        output_path, srt_path = process_video(temp_input_path, None, task, max_words_per_line, fontsize, font, bg_color, text_color, caption_mode, api_configs_file)
        logging.info("Zipping response...")
        zip_path = zip_response(os.path.join(temp_vid_dir,"archive.zip"), [output_path, srt_path])
        return  FileResponse(zip_path, media_type='application/zip', filename=f"result_{video_file.filename.split('.')[0]}.zip")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    app_logger = setup_logger('appLogger', 'main.log', level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000)