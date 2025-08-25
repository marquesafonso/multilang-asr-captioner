import os
from gradio_client import Client, handle_file
from dotenv import load_dotenv

def transcriber(invideo_file:str, 
                max_words_per_line:int,
                task:str,
                model_version:str,
                device_type:str
                ):
        load_dotenv()
        HF_TOKEN = os.getenv("HF_TOKEN")
        HF_SPACE = os.getenv("HF_SPACE")
        client = Client(HF_SPACE, hf_token=HF_TOKEN)
        result = client.predict(
                file_input=handle_file(invideo_file),
                file_type = "video",
                max_words_per_line=max_words_per_line,
                task=task,
                model_version=model_version,
                device_type=device_type,
                api_name="/predict"
        )
        return result[0], result[3]