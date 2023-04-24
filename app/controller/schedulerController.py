
from fastapi import APIRouter
from fastapi import Request, File, UploadFile
from services.lazykhschduler import scheduler
import json

router = APIRouter(
    responses={404: {"description": "Not found"}},

)


@router.post('/scheduler')
async def schedule_phonemes(transcript: UploadFile = File(...), phonemes: UploadFile = File(...)):

    #  Read the file
    transcript = await transcript.read()
    transcript = transcript.decode('utf-8')

    phonemes= await phonemes.read()
    # phonemes = json.loads(phonemes)

    # Call the scheduler 
    jsonFile= scheduler(transcript,phonemes)

    return  jsonFile
