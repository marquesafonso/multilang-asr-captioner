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
                <input type="file" name="file"><br>
                Font size: <input type="number" name="fontsize" value="32"><br>
                Background color: <input type="text" name="bg_color" value="#070a13b3"><br>
                Max words per line: <input type="number" name="max_words_per_line" value="8"><br>
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/process_video/")
async def process_video_api(file: UploadFile = File(...),
                            fontsize: Optional[int] = Form(32),
                            bg_color: Optional[str] = Form("#070a13b3"),
                            max_words_per_line: Optional[int] = Form(8)):
    try:
        if not str(file.filename).endswith('.mp4'):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP4 file.")
        # Save the uploaded file to a temporary file
        temp_dir = os.path.join(os.getcwd(),"temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_input_path = os.path.join(temp_dir, file.filename)
        # Copy UploadFile to the temp_input_path
        with open(temp_input_path, 'wb') as buffer:
            try:
                shutil.copyfileobj(file.file, buffer)
            finally:
                file.file.close()
        # Process the video
        output_path = process_video(temp_input_path, fontsize, bg_color, max_words_per_line)
        # Return the processed video file
        return FileResponse(output_path, media_type="video/mp4", filename=f"result_{file.filename}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
