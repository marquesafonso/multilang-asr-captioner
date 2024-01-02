from fastapi import FastAPI, UploadFile, HTTPException, File, Form, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from utils.process_video import process_video
from utils.zip_response import zip_response
from utils.api_configs import api_configs
from utils.read_html import read_html
import shutil, os, logging, uvicorn, secrets

app = FastAPI()
security = HTTPBasic()
api_configs_file = os.path.abspath("api_config_example.yml")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, api_configs(api_configs_file)["secrets"]["username"])
    correct_password = secrets.compare_digest(credentials.password, api_configs(api_configs_file)["secrets"]["password"])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

logging.basicConfig(filename='main.log',
                encoding='utf-8',
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')

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
async def process_video_api(video_file: UploadFile = File(...),
                            srt_file: Optional[UploadFile] = File(...),
                            max_words_per_line: Optional[int] = Form(8),
                            fontsize: Optional[int] = Form(36),
                            font: Optional[str] = Form("FuturaPTHeavy"),
                            bg_color: Optional[str] = Form("#070a13b3"),
                            text_color: Optional[str] = Form("white"),
                            username: str = Depends(get_current_user)
                            ):
    try:
        if not str(video_file.filename).endswith('.mp4'):
            raise HTTPException(status_code=400, detail="Invalid Video File type. Please upload an MP4 file.")
        if srt_file.size > 0 and not str(srt_file.filename).endswith('.srt'):
            raise HTTPException(status_code=400, detail="Invalid Subtitles File type. Please upload an SRT file.")
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
            output_path, _ = process_video(temp_input_path, SRT_PATH, max_words_per_line, fontsize, font, bg_color, text_color)
            logging.info("Archiving response...")
            zip_path = zip_response(os.path.join(temp_vid_dir,"archive.zip"), [output_path, SRT_PATH])
            return FileResponse(zip_path, media_type='application/zip', filename=f"result_{video_file.filename.split('.')[0]}.zip")
        logging.info("Processing the video...")
        output_path, srt_path = process_video(temp_input_path, None, max_words_per_line, fontsize, font, bg_color, text_color)
        logging.info("Archiving response...")
        zip_path = zip_response(os.path.join(temp_vid_dir,"archive.zip"), [output_path, srt_path])
        return  FileResponse(zip_path, media_type='application/zip', filename=f"result_{video_file.filename.split('.')[0]}.zip")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    # Use Uvicorn to run the application
    uvicorn.run(app, host="127.0.0.1", port=8000)
