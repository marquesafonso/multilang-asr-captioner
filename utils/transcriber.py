from faster_whisper import WhisperModel
import logging

logging.basicConfig(filename='main.log',
                encoding='utf-8',
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

def write_srt(segments, srt_path):
    """Write segments to an SRT file."""
    with open(srt_path, "w", encoding='utf-8') as file:
        for i, segment in enumerate(segments):
            file.write(f"{i+1}\n{segment.start} --> {segment.end}\n{segment.text}\n\n")

def transcriber(input_path:str, srt_path:str):
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
    )

    logging.info("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    logging.info("Writing file...")
    write_srt(segments=segments, srt_path=srt_path)
