from moviepy.editor import VideoFileClip

def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
    # Load the video file
    video_clip = VideoFileClip(mp4_file_path)

    # Extract the audio from the video clip
    audio_clip = video_clip.audio

    # Save the audio clip as an MP3 file
    audio_clip.write_audiofile(mp3_file_path)

    # Close the clips
    audio_clip.close()
    video_clip.close()
    return mp3_file_path