import json
import subprocess

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
    classfiedText = fake_classfy(transcript,temp_path,randomeFilename)


    # Get text to voice sound and save it in the temp
    actor = "en-US-JennyNeural"
    text_to_speech(transcript, temp_path + randomeFilename, actor)
    print("sound saved")

    # get phonemes this will take the audion from the temprory folder, it takes name
    # of audio file and the transcript and the path
    get_phonemes(temp_path, randomeFilename)


    # Call the scheduler this will creat a csv file in the temprory folderit takes name of the file and the path
    scheduler(temp_path+randomeFilename)



    # draw frames
    use_billboards = "F"
    jiggly_transitions = "F"
    draw_frames(temp_path+randomeFilename, use_billboards, jiggly_transitions)

    # finish the video and save it in the temprory folder
    audio_path = temp_path + randomeFilename + ".wav"
    frames_path = randomeFilename + "_frames"
    Videofinisher(temp_path,randomeFilename, audio_path, randomeFilename)

    # Delete temprory files
    delete_temprory_files(temp_path, randomeFilename)

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


def fake_classfy(transcript,temp_path,randomeFilename):
    classifiedText = ""  # initialize the classifiedText variable
    count = 0 # initialize count to keep track of the number of words processed

    # loop through the words and add "<happy>" or "<rq>" after every three words
    for i, word in enumerate(transcript.split()):
        classifiedText += word
        count += 1
        if count % 6 == 0:  # check if we have processed every three words
            if count % 12 == 0:
                classifiedText += " <rq>"
            else:
                classifiedText += " <happy>"

        # add a space after every word (except the last one)
        if i < len(transcript.split()) - 1:
            classifiedText += " "

    # Save classfied text 
    with open(temp_path + randomeFilename + '.txt', 'w') as f:
        f.write(classifiedText)

    return classifiedText