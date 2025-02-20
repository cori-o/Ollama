import os 

class FileProcessor:
    def get_file_list(self, file_path):
        '''
        file_path 내에 있는 img 파일들의 이름을 리스트 형태로 반환
        '''
        file_type = ['jpg', 'png']
        entire_file = os.listdir(file_path)
        file_list = [f for f in entire_file if f.split('.')[-1] in file_type]
        return file_list

class DataProcessor():
    def __init__(self, args):
        self.args = args 
    
    def cleanse_text(self, text):
        '''
        다중 줄바꿈 제거 및 특수 문자 중복 제거
        '''
        import re 
        text = re.sub(r'(\n\s*)+\n+', '\n\n', text)
        text = re.sub(r"\·{1,}", " ", text)
        text = re.sub(r"\.{1,}", ".", text)
        # print('after cleansing: ' + text)
        return text