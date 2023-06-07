import subprocess
from dotenv import load_dotenv

from fastapi import APIRouter
from models.tts import text_to_speech
from services.gentlePhonemes import get_phonemes
from services.lazykhVideoFinisher import Videofinisher
from services.subtitle import create_video_with_subtitles
from models.emotion_model import emotion_classfy
from services.utilities import (
    create_randome_name,
    delete_cache,
    get_video_from_file,
)

load_dotenv()

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/textToVideo")
async def text_To_video(transcript: str):

    delete_cache()
    randomeFilename = create_randome_name()

    # Storing files in temporory foder Not: All this files will get deleted after the
    temp_path = "services/temporary/"

    #  Classfy the transcript user inputed and save it
    emotion_classfy(transcript,temp_path,randomeFilename)


    # Get text to voice sound and save it in the temp
    actor = "en-US-GuyNeural"
    await text_to_speech(transcript, temp_path + randomeFilename, actor)
    print("sound saved")

    # get phonemes this will take the audion from the temprory folder
    # it takes name of audio file and the transcript and the path
    get_phonemes(temp_path, randomeFilename)


    # Call the scheduler this will creat a csv file in the temprory folder, it takes name of the file and the path
    scheduler(temp_path+randomeFilename)



    # draw frames
    use_billboards = "F"
    jiggly_transitions = "F"
    draw_frames(temp_path+randomeFilename, use_billboards, jiggly_transitions)

    # finish the video and save it in the temprory folder
    Videofinisher(temp_path,randomeFilename)

    # Add subtitle to the final video 
    video_path = randomeFilename+'_final.mp4'
    json_path =temp_path+randomeFilename+'.json'
    output_path = randomeFilename+'_sub_final.mp4'
    create_video_with_subtitles(video_path, json_path, output_path, randomeFilename)

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
        "../services/lazykhScheduler.py",
        "--input_file",
        file_name,
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error lazykhschduler: {e}")


