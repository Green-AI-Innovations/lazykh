
from fastapi import APIRouter
from fastapi import  File, UploadFile
from services.lazykhschduler import scheduler
import json
import subprocess
from services.lazykhVideoFinisher import Videofinisher
from services.gentelPhonemes import get_phonemes
from services.utils import timer, creat_randome_name, removeTags, save_audio, delete_temprory_files, get_video_from_file,delete_cache





router = APIRouter(
    responses={404: {"description": "Not found"}},

)






@timer
@router.post('/textToVideo')
async def text_To_video(transcript: UploadFile = File(...), sound: UploadFile = File(...),classfiedText: UploadFile = File(...) ):
# TODO check where each fie is saved
    delete_cache()
    randomeFilename=creat_randome_name()

    #  Read the transcript user inputed
    transcript = await transcript.read()
    transcript = transcript.decode('utf-8')
    transcript = removeTags(transcript)
    print('removeTags from transcript')


    # get sound
    # Save audio file TODO
    sound = await sound.read()
    temp_path = "services/temporary/"
    save_audio(sound, temp_path, randomeFilename)

    print('sound saved')

    # get phonemes
    phonemes = get_phonemes(sound,transcript,randomeFilename)
    phonemes = json.dumps(phonemes)


    # Call the scheduler 
    scheduler(transcript,phonemes,randomeFilename)

    

    # get classfied text TODO
    classfiedText = await classfiedText.read()
    classfiedText = classfiedText.decode('utf-8')
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







