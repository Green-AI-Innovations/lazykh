from fastapi import APIRouter
from fastapi import Request, File, UploadFile
from services.gentelPhonemes import get_phonemes
from services.utils import removeTags

router = APIRouter(
    responses={404: {"description": "Not found"}},

)



@router.post('/phonemes')
async def create_phonemes(request: Request, mp3Audio: UploadFile = File(...), textFile: UploadFile = File(...)):
    # execution time is 15.12s
    mp3Audio = await mp3Audio.read()
    textFile = await textFile.read()
    textFile = textFile.decode('utf-8')
    textFile = removeTags(textFile)
    # Send the audio and text to the gentel container
    phonemes = get_phonemes(mp3Audio, textFile)

    # Return the phonemes
    return phonemes