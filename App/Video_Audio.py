
# Code for converting the given Video to Audio

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
from pytube import YouTube
import ffmpeg
import requests
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json
import os
import warnings
warnings.filterwarnings('ignore')
from Globals import *


# Checking if the video provided is playable
def is_mp4_playable(file_path):
  try:
      probe = ffmpeg.probe(file_path)
      # Check if the file format is recognized as video
      if 'streams' in probe and any(stream['codec_type'] == 'video' for stream in probe['streams']):
          print("MP4 file is playable.")
          return True
      else:
          print("MP4 file is corrupt or non-playable.")
          return False
  except ffmpeg.Error as e:
      return False
  

# Extracting the audio from the video file
def extract_audio(link, output_file_path):

  if urlparse(link).netloc == "www.youtube.com":
    yt = YouTube(link)
    video_path = yt.streams[0].url

  elif urlparse(link).netloc == "www.linkedin.com":
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    data_linkedin = json.loads(soup.find('script', type='application/ld+json').text)
    if data_linkedin['isAccessibleForFree'] == True:
      video_path = json.loads(soup.video['data-sources'])[0]['src']
    else:
      return False

  elif urlparse(link).netloc == "www.coursera.org":
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    data_coursera = json.loads(soup.find('script', type='application/ld+json').text)
    video_path = data_coursera['@graph'][1]['contentURL']

  elif urlparse(link).netloc not in ["www.youtube.com", "www.linkedin.com", "www.coursera.org"]:
    return False

  else:
    if(is_mp4_playable(link)):
      video_path = link
    else:
      return "Sorry! Can't extract audio. Please make sure the video file exists and is not corrupted."


  audio, err = (
      ffmpeg
      .input(video_path)
      .output("pipe:", format='mp3', acodec='libmp3lame', audio_bitrate='320k')
      .run(capture_stdout=True)
  )


  with open(output_file_path, 'wb') as f:
      f.write(audio)

  return True


