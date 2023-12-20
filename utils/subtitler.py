from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import os

def parse_srt(srt_file):
    """Parse the SRT file and return a list of (start, end, text) for each subtitle."""

    with open(srt_file, "r", encoding='utf-8') as file:
        lines = file.readlines()
    
    i = 0
    subtitles = []
    while i < len(lines):
        if lines[i].strip().isdigit():
            timing_str = lines[i+1].strip().split(" --> ")
            start = timing_str[0].replace(',', '.')
            end = timing_str[1].replace(',', '.')
            text = lines[i+2].strip()
            subtitles.append((start, end, text))
            i += 4
        else:
            i += 1
    return subtitles


def subtitler(video_file:str,
            srt_file:str,
            output_file:str,
            fontsize:int,
            bg_color:str):
    """Add subtitles from an SRT file to a video."""
    video_file = os.path.abspath(video_file)
    srt_file = os.path.abspath(srt_file)
    output_file = os.path.abspath(output_file)
    
    clip = VideoFileClip(video_file)
    subtitles = parse_srt(srt_file)

    subtitle_clips = []
    for start, end, text in subtitles:
        # Create TextClip with specified styling
        txt_clip = TextClip(text, fontsize=fontsize, color='white', font="Arial-Bold", method='caption',
                            bg_color=bg_color, align='center', size=(clip.w*1/2, None))
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip.duration).set_start(start).set_end(end)
        subtitle_x_position = 'center'
        subtitle_y_position = clip.h * 4 / 5 
        text_position = (subtitle_x_position, subtitle_y_position)                    
        subtitle_clips.append(txt_clip.set_position(text_position))
    
    video = CompositeVideoClip([clip] + subtitle_clips)
    video.write_videofile(output_file, codec='libx264', audio_codec='aac')