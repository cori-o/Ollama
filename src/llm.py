from openai import OpenAI
import torch

class LLMModel():
    def __init__(self, config):
        self.config = config 

    def set_gpu(self, model):
        self.device = torch.device("cuda") if torch.cuda.is_available() else "cpu"    
        model.to(self.device)
    
    def set_generation_config(self, max_tokens=500, temperature=0.9):
        self.gen_config = {
            "max_tokens": max_tokens,
            "temperature": temperature
        }

class LLMOpenAI(LLMModel):
    def __init__(self, config):
        super().__init__(config)
        self.client = OpenAI()

    def set_generation_config(self):
        self.gen_config = {
            "max_tokens": self.config['max_tokens'],
            "temperature": self.config['temperature']
        }

    def create_embeddings(self, emb_model, emb_text):
        response = self.client.embeddings.create(
            model = emb_model, 
            input = emb_text,
            dimensions = 1024
        )
        return response.data[0].embedding

    def set_response_guideline(self):
        self.system_role = """
        너는 메타 데이터를 바탕으로, 입력받은 이미지 설명을 매끄러운 문장으로 다듬어주는 역할을 수행하는 전문가야.
        이미지 설명과 메타 데이터를 잘 조합해서 최종 설명을 한글로 번역해서 반환해줘.
        """
        self.sub_role = """ '이미지에서 텍스트를 찾을 수 없습니다' 같이 이미지가 나타내고 있는 장면과 직접적인 관련이 없는 부분은 제외해줘. 또 이미지 파일이 ~다 라고 직접적인 언급은 하지 말아줘. 
        메타데이터를 참고해서 바탕으로 이미지 설명을 상황에 맞게 일부 수정해서 반환해줘. 메타데이터 중 일부 내용이 영어나 한문으로 되어 있으면, 한국어로 번역해서 진행하면 되고, 메타데이터가 의미 없는 경우 이미지 설명만 잘 다듬어서 반환해줘.
        예시는 다음과 같아. 
        ==============================
        이미지 파일 이름: 2025년 신년 현충원 참배
        이미지 설명: The image shows a man dressed in a formal suit and tie standing at the center. He appears to be in mid-motion, possibly saluting or gesturing with his right hand towards another person who is not fully visible in the frame. The setting suggests an outdoor event of significance, as indicated by the presence of what looks like a memorial monument in the background and other individuals also dressed formally to the left side of the image. There are no texts present on the image.
        ==============================
        반환값: 이 이미지는 2025년 신년을 맞아 현충원에서 열린 참배 행사에서 촬영되었습니다. 정장을 입은 한 남성이 중앙에 서 있으며, 오른손으로 경례를 하거나 다른 사람에게 제스처를 취하는 모습입니다. 배경에는 기념비로 보이는 구조물이 있고, 이미지 왼쪽에는 다른 정장 차림의 인물들이 함께 서 있는 모습이 보입니다. 이 이미지는 중요한 야외 행사에서의 순간을 담고 있습니다.
        """

    def set_prompt_template(self, meta_data, img_description):
        self.img_prompt_template = """
        메타데이터: {meta_data}
        이미지 설명: {img_description} 
        """
        return self.img_prompt_template.format(meta_data=meta_data, img_description=img_description)
                   
    def get_response(self, query, role="", sub_role="", model='gpt-4o'):
        try:
            sub_role = sub_role
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": role},
                    {"role": "system", "content": sub_role},
                    {"role": "user", "content": query},
                ],
                max_tokens=self.gen_config['max_tokens'],
                temperature=self.gen_config['temperature'],
            )
        except Exception as e:
            return f"Error: {str(e)}"
        return response.choices[0].message.content