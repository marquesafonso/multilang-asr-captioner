from pytube import YouTube
import logging

def download_audio(video_url, output_path, filename):
    try:
        # Creating YouTube object
        yt = YouTube(video_url)

        # Selecting the audio stream with the highest quality
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Downloading the audio file
        audio_stream.download(output_path=output_path,filename=filename)

        logging.info(f"Audio downloaded successfully at {output_path}/{audio_stream.default_filename}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")
