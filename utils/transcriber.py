from faster_whisper import WhisperModel
import logging

logging.basicConfig(filename='main.log',
                encoding='utf-8',
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

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
                        start_time = words_in_line[0].start
                        end_time = words_in_line[-1].end
                        line_text = ' '.join([w.word.strip() for w in words_in_line])

                        file.write(f"{line_counter}\n{start_time} --> {end_time}\n{line_text}\n\n")

                        # Reset for the next line and increment line counter
                        line_counter += 1

                    words_in_line = []  # Reset words list for the next line



def transcriber(input_path:str,
                srt_path:str,
                max_words_per_line:int):
    
    model_size = "large-v3"

    # Run on GPU with FP16
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    logging.info("Logging Whisper model...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    logging.info("Starting transcription...")
    segments, info = model.transcribe(
        input_path,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=True
    )

    logging.info("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    logging.info("Writing file...")
    write_srt(segments=segments, srt_path=srt_path, max_words_per_line=max_words_per_line)