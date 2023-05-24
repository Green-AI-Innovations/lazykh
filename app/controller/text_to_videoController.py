import json
import subprocess
import requests
import re
from dotenv import load_dotenv

import os
from fastapi import APIRouter
from models.tts import text_to_speech
from services.gentelPhonemes import get_phonemes
from services.lazykhVideoFinisher import Videofinisher

from services.utils import (
    creat_randome_name,
    delete_cache,
    delete_temprory_files,
    get_video_from_file,
)
load_dotenv()
router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/textToVideo")
async def text_To_video(transcript: str):

    delete_cache()
    randomeFilename = creat_randome_name()

    # Storing files in temporory foder Not: All this files will get deleted after the
    temp_path = "services/temporary/"

    #  TODO Classfy the transcript user inputed and save it
    fake_classfy(transcript,temp_path,randomeFilename)


    # Get text to voice sound and save it in the temp
    actor = "en-US-GuyNeural"
    await text_to_speech(transcript, temp_path + randomeFilename, actor)
    print("sound saved")

    # get phonemes this will take the audion from the temprory folder, it takes name
    # of audio file and the transcript and the path
    get_phonemes(temp_path, randomeFilename)


    # Call the scheduler this will creat a csv file in the temprory folder, it takes name of the file and the path
    scheduler(temp_path+randomeFilename)



    # draw frames
    use_billboards = "F"
    jiggly_transitions = "F"
    draw_frames(temp_path+randomeFilename, use_billboards, jiggly_transitions)

    # finish the video and save it in the temprory folder
    Videofinisher(temp_path,randomeFilename)



    return get_video_from_file(randomeFilename)


def draw_frames(file_name, use_billboards, jiggly_transitions):
    command = [
        "python",
        "../services/lazykhVideoDrawer.py",
        "--input_file",
        file_name,
        "--use_billboards",
        use_billboards,
        "--jiggly_transitions",
        jiggly_transitions,
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error drawer: {e}")


def scheduler(file_name):
    command = [
        "python",
        "../services/lazykhschduler.py",
        "--input_file",
        file_name,
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error lazykhschduler: {e}")


def emotion_to_lazykh_tag(emotion):
    """ Map API emotion to lazykh tag. """
    # lazky kh tags explain,happy,sad,angry,confused,rq
    mapping = {
        "explain": "<explain>",
        "happy": "<happy>",
        "sad": "<sad>",
        "angry": "<angry>",
    }
    return mapping[emotion]

def get_emotion(sentence):
    """ Get emotion prediction from API. """
    # url = "www.example.com"
    # payload = {'text': sentence}
    # response = requests.post(url, data=payload)
    return "fear"

def get_emotions(sentences):
    """ Get emotion prediction from API. """
    url = os.getenv('API_URL')
    # Token API
    token = os.getenv('API_HEADER_AUTH')
    auth_header = {'Authorization': f'Bearer {token}'}
    # Create and submit a request using the auth header
    headers = auth_header
    # Add content type header
    headers.update({'Content-Type':'application/json'})
    payload = json.dumps({'data': sentences})
    payload = bytes(payload,encoding = 'utf8')
    response = requests.post(url, payload, headers=headers)
    print(f"response from API is: \n\n {response.json()}")
    return response.json()

def fake_classfy(transcript, temp_path, randomeFilename):
    sentences = re.split(r'[.!?]\s+', transcript)
    classifiedText = ""
    emotions = get_emotions(sentences)
    # for sentence in sentences:
    #     emotion = get_emotion(sentence)
    #     lazykh_tag = emotion_to_lazykh_tag(emotion)
    #     classifiedText += f"{lazykh_tag} {sentence}"
    print(f"This is fake classifier method speaking: \n")
    for sentence, emotion in zip(sentences, emotions):
        print(f"sentence: {sentence}")
        print(f"\n emotion: {emotion}")
        lazykh_tag = emotion_to_lazykh_tag(emotion)
        classifiedText += f"{lazykh_tag} {sentence}. \n"

    with open(temp_path + randomeFilename + '.txt', 'w') as f:
        f.write(classifiedText)

    return classifiedText
