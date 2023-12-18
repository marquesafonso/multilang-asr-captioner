from pytube import YouTube
import os

def download_video(input_file, output_path, filename):
    full_filename = f"{filename}.mp4"
    try:
        yt = YouTube(input_file)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video_stream:
            video_stream.download(output_path=output_path,filename=full_filename)
            video_title = os.path.join(output_path, full_filename)
            return video_title
        else:
            return "No suitable stream found for this video."
    except Exception as e:
        return f"An error occurred: {str(e)}"