# Converting the audio to text

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import json
from Globals import *


# Dividing the audio into chunks
def divide_audio_chunks(audio_file, chunksize = 30000):
    mp3_audio = AudioSegment.from_mp3(audio_file)
    # Split the audio into chunks based on chunksize
    chunks = make_chunks(mp3_audio, chunksize)
    return chunks

# Processing each chunk
def process_chunks(audio_chunks):
    whole_speech = ""
    recognizer = sr.Recognizer()
    for i, chunk in enumerate(audio_chunks):
        audio = chunk.export(format="wav")
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                whole_speech += text
            except sr.UnknownValueError:
                print(f"Chunk {i+1}, Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return whole_speech

def convert_audio_text(input, output=text_file_path):
    audio_chunks = divide_audio_chunks(input)
    speech = process_chunks(audio_chunks)
    print(speech)
    if speech:
        with open(output, 'w',  encoding='utf-8') as f:
            f.write(speech)
            return True
    else:
        return False    