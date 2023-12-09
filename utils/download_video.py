from pytube import YouTube

def download_video(input_file, output_path, filename):
    try:
        yt = YouTube(input_file)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video_stream:
            video_stream.download(output_path=output_path,filename=filename)
            video_title = f"{output_path}/{filename}"
            return video_title
        else:
            return "No suitable stream found for this video."
    except Exception as e:
        return f"An error occurred: {str(e)}"