from moviepy.editor import VideoFileClip

def convert_video_to_audio(mp4_file_path, m4a_file_path):
    # Load the video file
    video_clip = VideoFileClip(mp4_file_path)

    # Extract the audio from the video clip
    audio_clip = video_clip.audio

    # Save the audio clip as an m4a file
    audio_clip.write_audiofile(m4a_file_path, codec='aac')

    # Close the clips
    audio_clip.close()
    video_clip.close()
    return m4a_file_path