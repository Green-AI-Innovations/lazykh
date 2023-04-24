
from fastapi import APIRouter
from fastapi import Request, File, UploadFile
from services.lazykhVideoDrawer import drawer
import json
import subprocess

router = APIRouter(
    responses={404: {"description": "Not found"}},

)


@router.post('/drawFrames')
def draw_frames(scheduler_file,classfied_emotion_file, use_billboards, jiggly_transitions):
    # input_file: scheduler csv and classfied emotion text should be the same name
    command = [
        "python3",
        "text_to_video/lazykh/videoDrawer.py",
        "--scheduler_file",
        scheduler_file,
        "--classfied_emotion_file",
        classfied_emotion_file,
        "--use_billboards",
        use_billboards,
        "--jiggly_transitions",
        jiggly_transitions,
    ]
    subprocess.run(command)