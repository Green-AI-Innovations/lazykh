from fastapi import APIRouter
from fastapi import Request, File, UploadFile
from services.phonemes import get_phonemes


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/phonemes")
async def create_phonemes(
    request: Request, mp3Audio: UploadFile = File(...), textFile: UploadFile = File(...)
):
    # execution time is 15.12s
    mp3Audio = await mp3Audio.read()
    textFile = await textFile.read()
    textFile = textFile.decode("utf-8")
    textFile = removeTags(textFile)
    # Send the audio and text to the gentel container
    phonemes = get_phonemes(mp3Audio, textFile)

    # Return the phonemes
    return phonemes


def removeTags(script):
    TO_REMOVE = ["[", "]", "/"]

    newScript = script.replace("-", " ")
    for charToRemove in TO_REMOVE:
        newScript = newScript.replace(charToRemove, "")

    while "<" in newScript:
        start = newScript.index("<")
        end = newScript.index(">") + 1
        newScript = newScript[:start] + newScript[end:]
    while "  " in newScript:
        newScript = newScript.replace("  ", " ")
    while "\n " in newScript:
        newScript = newScript.replace("\n ", "\n")
    while " \n" in newScript:
        newScript = newScript.replace(" \n", "\n")
    while newScript[0] == " ":
        newScript = newScript[1:]

    return newScript
