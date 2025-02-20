import ollama

response = ollama.chat(
                model="llava:13b",  # 모델 이름 (llava-13b)
                messages=[
                    {"role": "system", "content": "Describe the content of the image."}
                ],
            )

full_response = response['message']['content']
print(full_response)