from faster_whisper import WhisperModel
import logging

logging.basicConfig(filename='main.log',
                encoding='utf-8',
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

def convert_seconds_to_time(seconds):
    # Separate seconds into hours, minutes, and seconds
    seconds = float(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    whole_seconds = int(remainder)
    milliseconds = int((remainder - whole_seconds) * 1000)    
    return f"{int(hours):02}:{int(minutes):02}:{whole_seconds:02},{milliseconds:03}"


def write_srt(segments, srt_path, max_words_per_line):
    """Write segments to an SRT file with a maximum number of words per line."""
    with open(srt_path, "w", encoding='utf-8') as file:
        line_counter = 1
        for _, segment in enumerate(segments):
            words_in_line = []
            for w, word in enumerate(segment.words):
                words_in_line.append(word)
                # Write the line if max words limit reached or it's the last word in the segment
                if len(words_in_line) == max_words_per_line or w == len(segment.words) - 1:
                    if words_in_line:  # Check to avoid writing a line if there are no words
                        start_time = convert_seconds_to_time(words_in_line[0].start)
                        end_time = convert_seconds_to_time(words_in_line[-1].end)
                        line_text = ' '.join([w.word.strip() for w in words_in_line])
                        file.write(f"{line_counter}\n{start_time} --> {end_time}\n{line_text}\n\n")
                        # Reset for the next line and increment line counter
                        line_counter += 1
                    words_in_line = []  # Reset words list for the next line

def transcriber(input_path:str,
                srt_path:str,
                max_words_per_line:int,
                task:str):
    #TODO: model_size = "distil-large-v3" -> need to wait for new pypi version of faster-whisper (pull request already merged)
    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8") #TODO: add condition_on_previous_text=False when using distil-whisper
    segments, info = model.transcribe(
        input_path,
        beam_size=5,
        task=task,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=True
    )
    logging.info("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    write_srt(segments=segments, srt_path=srt_path, max_words_per_line=max_words_per_line)