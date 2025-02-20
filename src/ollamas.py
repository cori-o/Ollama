import ollama 

class OllamaImg:
    def __init__(self, config):
        self.config = config 

    def get_info_from_image(self, image_file):
        print(f"\nProcessing {image_file}") 
        response = ollama.chat(
            model=f"{self.config['ollama_model']}:{self.config['ollama_param']}",     # llava:13b
            messages=[
                {"role": "system", "content": "Describe the content of the image.", "images": [image_file], "temperature": self.config['temperature']}
            ],
            # stream=True  # 스트리밍 여부 (원하면 True로 설정)
        )
        full_response = response['message']['content']
        # print(full_response, end='\n\n')
        return full_response
