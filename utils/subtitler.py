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
            start = timing_str[0]
            end = timing_str[1]
            text = lines[i+2].strip()
            subtitles.append((start, end, text))
            i += 4
        else:
            i += 1
    return subtitles

def filter_caption_width(caption_width:str='desktop'):
    if caption_width == 'desktop':
        caption_width = 0.2
    elif caption_width == 'mobile':
        caption_width = 0.5
    return caption_width

def subtitler(video_file:str,
            srt_path:str,
            output_file:str,
            fontsize:int,
            font: str,
            bg_color:str,
            text_color:str,
            caption_width:str
            ):
    """Add subtitles from an SRT file to a video."""
    video_file = os.path.abspath(video_file)
    srt_path = os.path.abspath(srt_path)
    output_file = os.path.abspath(output_file)
    clip = VideoFileClip(filename=video_file, target_resolution=None)
    subtitles = parse_srt(srt_path)
    subtitle_clips = []
    for start, end, text in subtitles:
        # Create TextClip with specified styling
        # To get a list of possible color and font values run: print(TextClip.list("font"), '\n\n', TextClip.list("color"))
        txt_clip = TextClip(text, fontsize=fontsize, color=text_color, font=font, method='caption',
                            bg_color=bg_color, align='center', size=(clip.w*filter_caption_width(caption_width), None))
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip.duration).set_start(start).set_end(end)
        subtitle_x_position = 'center'
        subtitle_y_position = clip.h * 4 / 5 
        text_position = (subtitle_x_position, subtitle_y_position)                    
        subtitle_clips.append(txt_clip.set_position(text_position))
    video = CompositeVideoClip(size=None, clips=[clip] + subtitle_clips)
    video.write_videofile(output_file, codec='libx264', audio_codec='aac')