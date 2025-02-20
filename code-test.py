import av
import numpy as np
from transformers import VideoLlavaProcessor, VideoLlavaForConditionalGeneration

def read_video_pyav(container, indices):
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)
    return np.stack([x.to_ndarray(format="rgb24") for x in frames])


model = VideoLlavaForConditionalGeneration.from_pretrained("LanguageBind/Video-LLaVA-7B-hf")
processor = VideoLlavaProcessor.from_pretrained("LanguageBind/Video-LLaVA-7B-hf")

prompt = "USER: <video>Why is this video funny? ASSISTANT:"
video_path = "./testfile/NC060000127222_111-adc-7159.mp4"
container = av.open(video_path)

# sample uniformly 8 frames from the video
total_frames = container.streams.video[0].frames
indices = np.arange(0, total_frames, total_frames / 8).astype(int)
clip = read_video_pyav(container, indices)

inputs = processor(text=prompt, videos=clip, return_tensors="pt")

# Generate
generate_ids = model.generate(**inputs, max_length=2080)
print(processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])