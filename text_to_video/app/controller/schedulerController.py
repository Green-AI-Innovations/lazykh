from fastapi import APIRouter
from fastapi import File, UploadFile
from text_to_video.app.services.lazykhschduler import scheduler

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/scheduler")
async def schedule_phonemes(
    transcript: UploadFile = File(...), phonemes: UploadFile = File(...)
):
    #  Read the file
    transcript = await transcript.read()
    transcript = transcript.decode("utf-8")

    phonemes = await phonemes.read()
    # phonemes = json.loads(phonemes)

    # Call the scheduler
    jsonFile = scheduler(transcript, phonemes)

    return jsonFile
