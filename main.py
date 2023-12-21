from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional
from utils.process_video import process_video
import shutil, os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from multilang-asr-captioner"}

@app.get("/submit_video/")
async def get_form():
    html_content = """
    <html>
        <body>
            <form action="/process_video/" enctype="multipart/form-data" method="post">
                Video File: <input type="file" name="video_file"><br>
                Subtitles File: <input type="file" name="srt_file"><br>
                Max words per line: <input type="number" name="max_words_per_line" value="8"><br>
                Font size: <input type="number" name="fontsize" value="36"><br>
                Font: <input type="text" name="font" value="FuturaPTHeavy"><br>
                Background color: <input type="text" name="bg_color" value="#070a13b3"><br>
                Text color: <input type="text" name="text_color" value="white"><br>
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/process_video/")
async def process_video_api(video_file: UploadFile = File(...),
                            srt_file: Optional[UploadFile] = File(...),
                            max_words_per_line: Optional[int] = Form(8),
                            fontsize: Optional[int] = Form(36),
                            font: Optional[str] = Form("FuturaPTHeavy"),
                            bg_color: Optional[str] = Form("#070a13b3"),
                            text_color: Optional[str] = Form("white")
                            ):
    try:
        if not str(video_file.filename).endswith('.mp4'):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP4 file.")
        # Create temp dir
        temp_dir = os.path.join(os.getcwd(),"temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_input_path = os.path.join(temp_dir, video_file.filename)
        # Copy video UploadFile to the temp_input_path
        with open(temp_input_path, 'wb') as buffer:
            try:
                shutil.copyfileobj(video_file.file, buffer)
            finally:
                video_file.file.close()
        # Copy srt UploadFile to the temp_input_path
        if srt_file.size > 0:
            SRT_PATH = os.path.abspath(f"{temp_input_path.split('.')[0]}.srt")
            with open(SRT_PATH, 'wb') as buffer:
                try:
                    shutil.copyfileobj(srt_file.file, buffer)
                finally:
                    srt_file.file.close()
            # Process the video
            output_path = process_video(temp_input_path, SRT_PATH, max_words_per_line, fontsize, font, bg_color, text_color)
            return FileResponse(output_path, media_type="video/mp4", filename=f"result_{video_file.filename}")
        # Process the video
        output_path = process_video(temp_input_path, None, max_words_per_line, fontsize, font, bg_color, text_color)
        # FileResponse(output_path, media_type="text/srt", filename=f"result_{video_file.filename.split('.')[0]}.srt")
        # Return the processed video file
        return FileResponse(output_path, media_type="video/mp4", filename=f"result_{video_file.filename}")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
