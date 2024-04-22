#File that defines all the paths used in this app
import os
audio_file_path = r"Response\Video_Audio.wav"
text_file_path = r"Response\Audio_Text.txt"

output_video_path = r"video_data"
output_folder = r"mixed_data"
output_audio_path = r"mixed_data\output_audio.wav"

filepath = output_video_path + "\input_vid.mp4"

# Hugging face token needed to downloaded the gated models
hg_token = "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"

#Google API key - for Gemini based RAG
GOOGLE_API_KEY = "AIzaSyDD1M74-7FmtrMAXglgTbMchf3lpedkr3g"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

#Open AI key - for Open AI - Clip model
OPENAI_API_TOKEN = "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"
os.environ["OPENAI_API_KEY"] = OPENAI_API_TOKEN