#This file contains the UI code for the summarizer app.

#Necessary Imports
from Video_Audio import *
from Audio_Text import *
from Summarizer import *
from Globals import *
from Rag import *
import streamlit as st

# Title of the App
st.title('Video Summarizer and RAG')

#Video to be summarized
video_url = st.text_input('Enter the URL of the Video', '')

# Extract audio from video
if st.button('Extract Audio for this video'):
    # Display a message indicating that the extraction process has started
    progress_bar = st.progress(0)
    with st.spinner('Extracting audio...'):
        video_response = extract_audio(video_url, audio_file_path)
        if video_response:
            st.success('Audio extraction completed!') 
        else:
            st.error("Audio couldn't be processed") 

# Text from Audio

if st.button('Extract Text for this video'):    
    progress_bar = st.progress(0)
    with st.spinner('Extracting Text...'):
        speech_response = convert_audio_text(audio_file_path, text_file_path)
        if speech_response:
            st.success('Text extraction completed!')
        else:
            st.error("Text couldn't be processed") 

#Summarizing the video using the given LLMs
model_options = {
        "BART": "bart",
        "Flan-T5": "flan_t5",
        "LLama-2": "llama_2"
    }

selected_model = st.radio("Summarize the video using:", list(model_options.keys()))
if st.button('Summarize using the above selected model'):
    progress_bar = st.progress(0)
    with st.spinner("Summarizing Text..."):
        summary = summarize_file(text_file_path, model_options[selected_model])
        st.write(f"Here is the summary of the video using {model_options[selected_model]}:")
        st.write(summary)  


# Answering a query based on RAG
query = st.text_input("Try asking a query based on the video")

if st.button('Find the answer'):   
    progress_bar = st.progress(0)
    with st.spinner('Finding the answer...'):
        query_response = process_video_clip(video_url, query)
        st.write("Here is the answer to your query")
        st.write(query_response)              



                                        

