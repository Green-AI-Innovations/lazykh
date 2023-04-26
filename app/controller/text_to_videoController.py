
from fastapi import APIRouter
from fastapi import  File, UploadFile
import json
import subprocess

from services.lazykhschduler import scheduler
from services.lazykhVideoFinisher import Videofinisher
from services.gentelPhonemes import get_phonemes
from services.utils import timer, creat_randome_name, removeTags, save_audio, delete_temprory_files, get_video_from_file,delete_cache

from models.tts import text_to_speech



router = APIRouter(
    responses={404: {"description": "Not found"}},

)






@timer
@router.post('/textToVideo')
async def text_To_video(transcript: str):

    delete_cache()
    randomeFilename=creat_randome_name()
    # Storing files in temporory foder Not: All this files will get deleted after the user get the video
    temp_path = "services/temporary/"


    #  Read the transcript user inputed
 
  
    transcript = removeTags(transcript)
    print('removeTags from transcript')


    # save sound in the temp
    actor='en-US-JennyNeural'
    # https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=tts#text-to-speech
    text_to_speech(transcript,temp_path+randomeFilename,actor)
    print('sound saved')


    # get phonemes this will take the audion from the temprory folder it just need name of audio file and the transcript and the path
    phonemes = get_phonemes(temp_path, transcript,randomeFilename)
    phonemes = json.dumps(phonemes)


    # Call the scheduler this will creat a csv file in the temprory folder
    scheduler(transcript,phonemes,randomeFilename)

    

    # get classfied text TODO this will creat a text file in the temprory folder
    classfiedText = transcript
    with open("services/temporary/"+randomeFilename+'.txt', 'w') as file:
        file.write(classfiedText)
  

    # draw frames
    use_billboards="False"
    jiggly_transitions="False"
    draw_frames(randomeFilename, use_billboards, jiggly_transitions)




    # finish the video and save it in the temprory folder
    audio_path = temp_path + randomeFilename+'.wav'
    frames_path=randomeFilename+'_frames'
    Videofinisher(frames_path,audio_path,randomeFilename)


    
    # Delete temprory files 
    delete_temprory_files(temp_path,randomeFilename)

   
    return  get_video_from_file(randomeFilename)




    
def draw_frames(file_name, use_billboards, jiggly_transitions):
    command = [
        "python",
        "services/lazykhVideoDrawer.py",
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







