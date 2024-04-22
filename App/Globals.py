#File that defines all the paths used in this app
import os
audio_file_path = r"Response\Video_Audio.wav"
text_file_path = r"Response\Audio_Text.txt"

output_video_path = r"video_data"
output_folder = r"mixed_data"
output_audio_path = r"mixed_data\output_audio.wav"

filepath = output_video_path + "\input_vid.mp4"

# Hugging face token needed to downloaded the gated models
hg_token = ""

#Google API key - for Gemini based RAG
#To run the app - uncomment the below lines and add the respective keys
# GOOGLE_API_KEY = ""
# os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# #Open AI key - for Open AI - Clip model
# OPENAI_API_TOKEN = ""
# os.environ["OPENAI_API_KEY"] = OPENAI_API_TOKEN