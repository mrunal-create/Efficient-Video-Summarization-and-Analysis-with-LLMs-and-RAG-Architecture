# Answering a query based on RAG

from moviepy.editor import VideoFileClip
from pathlib import Path
import speech_recognition as sr
from pytube import YouTube
from pprint import pprint
import os
from llama_index.core.response.notebook_utils import display_source_node
from llama_index.core.schema import ImageNode
from moviepy.editor import VideoFileClip
from pathlib import Path
import speech_recognition as sr
from pytube import YouTube
from pprint import pprint
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core import SimpleDirectoryReader, StorageContext

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core import SimpleDirectoryReader
import json
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from Globals import *
from PIL import Image
import matplotlib.pyplot as plt
import shutil
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls


# Function to plot images
def plot_images(image_paths):
    images_shown = 0
    plt.figure(figsize=(16, 9))
    for img_path in image_paths:
        if os.path.isfile(img_path):
            image = Image.open(img_path)

            plt.subplot(2, 3, images_shown + 1)
            plt.imshow(image)
            plt.xticks([])
            plt.yticks([])

            images_shown += 1
            if images_shown >= 7:
                break


def download_video(url, output_path):
    """
    Download a video from a given url and save it to the output path.

    Parameters:
    url (str): The url of the video to download.
    output_path (str): The path to save the video to.

    Returns:
    dict: A dictionary containing the metadata of the video.
    """
    yt = YouTube(url)
    metadata = {"Author": yt.author, "Title": yt.title, "Views": yt.views}
    yt.streams.get_highest_resolution().download(
        output_path=output_path, filename="input_vid.mp4"
    )
    return metadata


def video_to_images(video_path, output_folder):
    """
    Convert a video to a sequence of images using VideoFileClip and save them to the output folder.

    Parameters:
    video_path (str): The path to the video file.
    output_folder (str): The path to the folder to save the images to.

    """
    clip = VideoFileClip(video_path)
    clip.write_images_sequence(
        os.path.join(output_folder, "frame%04d.png"), fps=0.2
    )


def video_to_audio(video_path, output_audio_path):
    """
    Convert a video to audio (VideoFileClip ) and save it to the output path.

    Parameters:
    video_path (str): The path to the video file.
    output_audio_path (str): The path to save the audio to.

    """
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio.write_audiofile(output_audio_path)


def audio_to_text(audio_path):
    """
    Convert audio to text using the SpeechRecognition library.

    Parameters:
    audio_path (str): The path to the audio file.

    Returns:
    test (str): The text recognized from the audio.

    """
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)

    with audio as source:
        # Record the audio data
        audio_data = recognizer.record(source)

        try:
            # Recognize the speech
            text = recognizer.recognize_whisper(audio_data)
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from service; {e}")

    return text

def retrieve(retriever_engine, query_str):
    retrieval_results = retriever_engine.retrieve(query_str)

    retrieved_image = []
    retrieved_text = []
    for res_node in retrieval_results:
        if isinstance(res_node.node, ImageNode):
            retrieved_image.append(res_node.node.metadata["file_path"])
        else:
            display_source_node(res_node, source_length=200)
            retrieved_text.append(res_node.text)

    return retrieved_image, retrieved_text

def process_video_clip(url, query):
    try:
        if os.path.exists(output_video_path):
            shutil.rmtree(output_video_path)
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        # Create folders if they don't exist
        os.makedirs(output_video_path, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

        metadata_vid = download_video(url, output_video_path)
        video_to_images(filepath, output_folder)
        video_to_audio(filepath, output_audio_path)
        text_data = audio_to_text(output_audio_path)

        with open(output_folder + "\output_text.txt", "w") as file:
            file.write(text_data)
        print("Text data saved to file")
        file.close()
        os.remove(output_audio_path)
        print("Audio file removed")

    except Exception as e:
        raise e
    
    text_store = LanceDBVectorStore(uri="lancedb", table_name="text_collection")
    image_store = LanceDBVectorStore(uri="lancedb", table_name="image_collection")
    storage_context = StorageContext.from_defaults(vector_store=text_store, image_store=image_store)

    # Create the MultiModal index
    documents = SimpleDirectoryReader(output_folder).load_data()

    index = MultiModalVectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context)

    retriever_engine = index.as_retriever(
        similarity_top_k=5, image_similarity_top_k=5)
    
    metadata_str = json.dumps(metadata_vid)
#   metadata = {"Author": yt.author, "Title": yt.title, "Views": yt.views}
    qa_tmpl_str = (
        "Given the provided information, including relevant images and retrieved context from the video, \
    accurately and precisely answer the query without any additional prior knowledge.\n"
        "Please ensure honesty and responsibility, refraining from any racist or sexist remarks.\n"
        "---------------------\n"
        "Context: {context_str}\n"
        "Metadata for video: {metadata_str} \n"
        "---------------------\n"
        "Query: {query_str}\n"
        "Answer: "
    )

    img, txt = retrieve(retriever_engine=retriever_engine, query_str=query)
    image_documents = SimpleDirectoryReader(
        input_dir=output_folder, input_files=img
    ).load_data()   #return top 5 images which can answer the query -
    context_str = "".join(txt)
    print(context_str)
    plot_images(img)

    from llama_index.multi_modal_llms.openai import OpenAIMultiModal

    openai_mm_llm = OpenAIMultiModal(
        model="gpt-4-vision-preview", api_key=OPENAI_API_TOKEN, max_new_tokens=1500
    )

    response_1 = openai_mm_llm.complete(
        prompt=qa_tmpl_str.format(
            context_str=context_str, query_str=query, metadata_str=metadata_str
        ),
        image_documents=image_documents,
    )

    return response_1.text
    