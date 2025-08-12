from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import os, json

def parse_srt(srt_string):
    """Parse the SRT string and return a list of (start, end, text) for each subtitle."""
    lines = srt_string.split("\n")
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

def filter_caption_width(caption_mode:str):
    if caption_mode == 'desktop':
        caption_width_ratio = 0.5
        caption_height_ratio = 0.8
    elif caption_mode == 'mobile':
        caption_width_ratio = 0.2
        caption_height_ratio = 0.7
    return caption_width_ratio, caption_height_ratio


def subtitler(video_file: str,
            srt_string: str,
            srt_json: str,
            output_file: str,
            fontsize: int,
            font: str,
            bg_color: str,
            text_color: str,
            highlight_mode: bool,
            highlight_color: str,
            caption_mode: str,
            temp_dir: str
            ):
    """Add subtitles to a video, with optional word-level highlighting."""
    video_file = os.path.abspath(video_file)
    output_file = os.path.abspath(output_file)
    temp_audiofile = os.path.join(temp_dir, "temp_audio_file.mp4")
    clip = VideoFileClip(filename=video_file, target_resolution=None)

    subtitle_clips = []

    caption_width_ratio, caption_height_ratio = filter_caption_width(caption_mode)
    subtitle_y_position = clip.h * caption_height_ratio
    if highlight_mode:
        srt_data = json.loads(json.dumps(eval(srt_json)))
        for line in srt_data.get("lines", []):
            line_start = float(line["start"])
            line_end = float(line["end"])
            line_text = line["text"]

            base_clip = TextClip(line_text, fontsize=fontsize, font=font, color=text_color, bg_color=bg_color, method='label')
            base_clip = base_clip.set_start(line_start).set_end(line_end)

            # Center the full line
            line_width = base_clip.w
            x_center = (clip.w - line_width) // 2
            base_clip = base_clip.set_position((x_center, subtitle_y_position))
            subtitle_clips.append(base_clip)

            # Calculate word-level highlight positions
            current_x = x_center
            for word_info in line["words"]:
                word = word_info["word"]
                word_start = float(word_info["start"])
                word_end = float(word_info["end"])

                # Create a background-only word clip
                word_clip = TextClip(word, fontsize=fontsize, color=text_color, stroke_color=text_color, stroke_width=2, font=font,
                        method='label', bg_color=highlight_color)
                word_clip = word_clip.set_start(word_start).set_end(word_end)
                word_clip = word_clip.set_position((current_x - 7.5, subtitle_y_position))
                subtitle_clips.append(word_clip)

                space_width = TextClip(" ", fontsize=fontsize, font=font, method='label').w
                current_x += word_clip.w + space_width
        video = CompositeVideoClip(size=None, clips=[clip] + subtitle_clips)
        video.set_audio(temp_audiofile)
        video.write_videofile(output_file, codec='libx264', audio_codec='aac', temp_audiofile = temp_audiofile)
        return
    # Normal mode
    subtitles = parse_srt(srt_string)
    subtitle_x_position = 'center'
    subtitle_y_position = clip.h * caption_height_ratio
    text_position = (subtitle_x_position, subtitle_y_position)
    for start, end, text in subtitles:
        txt_clip = TextClip(text,
                            fontsize=fontsize,
                            color=text_color,
                            font=font,
                            method='caption',
                            bg_color=bg_color,
                            align='center',
                            size=(clip.w * caption_width_ratio, None))
        txt_clip = txt_clip.set_start(start).set_end(end).set_position(text_position)
        subtitle_clips.append(txt_clip)
    video = CompositeVideoClip(size=None, clips=[clip] + subtitle_clips)
    video.set_audio(temp_audiofile)
    video.write_videofile(output_file, codec='libx264', audio_codec='aac', temp_audiofile = temp_audiofile)