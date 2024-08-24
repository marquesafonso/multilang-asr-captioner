from gradio_client import Client, handle_file
from utils.api_configs import api_configs

def transcriber(invideo_path:str, srt_path:str,
        max_words_per_line:int, task:str,
        config_file:str):
        
        HF_TOKEN = api_configs(config_file)["secrets"]["hf-token"]
        HF_SPACE = api_configs(config_file)["secrets"]["hf-space"]
        client = Client(HF_SPACE, hf_token=HF_TOKEN)
        result = client.predict(
                video_input=handle_file(invideo_path),
                max_words_per_line=max_words_per_line,
                task=task,
                api_name="/predict"
        )
        with open(srt_path, "w", encoding='utf-8') as file:
                file.write(result[0])
        return srt_path