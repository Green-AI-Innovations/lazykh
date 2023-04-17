import logging
import os
import shutil
import traceback

from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import FileResponse

from text_to_video.config import AppConfig
from text_to_video.lazykh.lazykh import (
    run_ffmpeg,
    run_frame_drawer,
    run_gentle_aligner,
    run_gentle_script_writer,
    run_scheduler,
)
from text_to_video.lazykh.tts import text_to_speech

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

_app_config = AppConfig()
_artifact_dir = _app_config.settings.artifact_dir
_artifact_base_name = _app_config.settings.artifact_base_name
vid_base = os.path.join(_artifact_dir, _artifact_base_name)


@router.post("/video")
async def create_video_controller(
    request: Request, text: str = Body(..., media_type="text/plain")
):
    if not text:
        raise HTTPException(status_code=400, detail="Text data is missing")

    if not isinstance(text, str):
        raise HTTPException(
            status_code=400, detail="Invalid request body. Text data must be a string."
        )

    txt_file_path = vid_base + ".txt"

    if os.path.exists(txt_file_path):
        os.remove(txt_file_path)

    # Save the text data to a txt file
    with open(txt_file_path, "w") as f:
        f.write(text)

    if not os.path.exists(txt_file_path):
        error_msg = (
            "Saving your text did not succeed. Cannot proceed to the next "
            "step. Aborting."
        )
        logger.error(error_msg, exc_info=traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    txt_g_path = vid_base + "_g.txt"

    if os.path.exists(txt_g_path):
        os.remove(txt_g_path)

    try:
        run_gentle_script_writer(vid_base)
    except Exception as e:
        logger.exception("An error occurred while running the Gentle script writer")
        raise HTTPException(status_code=500, detail=str(e))

    if not os.path.exists(txt_g_path):
        error_msg = (
            "Cleaning your text for text-to-speech did not succeed. "
            "Cannot proceed to the next step. Aborting."
        )
        logger.error(error_msg, exc_info=traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    wav_file_path = vid_base + ".wav"

    if os.path.exists(wav_file_path):
        os.remove(wav_file_path)

    text_to_speech(text, wav_file_path)

    if not os.path.exists(wav_file_path):
        error_msg = (
            "Creating audio from your text did not succeed. "
            "Cannot proceed to the next step. Aborting."
        )
        logger.error(error_msg, exc_info=traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    json_path = vid_base + ".json"

    if os.path.exists(json_path):
        os.remove(json_path)

    try:
        run_gentle_aligner(vid_base)
    except Exception as e:
        logger.exception("An error occurred while running the Gentle aligner")
        raise HTTPException(status_code=500, detail=str(e))

    if not os.path.exists(json_path):
        error_msg = (
            "Aligning the audio with the audio you provided did not succeed. "
            "Cannot proceed to the next step. Aborting."
        )
        logger.error(error_msg, exc_info=traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    csv_file = vid_base + "_schedule.csv"

    if os.path.exists(csv_file):
        os.remove(csv_file)

    try:
        run_scheduler(vid_base)
    except Exception as e:
        logger.exception("An error occurred while running the Lazykh scheduler")
        raise HTTPException(status_code=500, detail=str(e))

    if not os.path.exists(csv_file):
        error_msg = (
            "Scheduling the poses, mouths, and other things did not succeed. "
            "Cannot proceed to the next step. Aborting."
        )
        logger.error(error_msg, exc_info=traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    frames_dir = vid_base + "_frames"

    if os.path.exists(frames_dir) and os.path.isdir(frames_dir):
        shutil.rmtree(frames_dir)

    try:
        run_frame_drawer(vid_base)
    except Exception as e:
        logger.exception("An error occurred while drawing the video frames")
        raise HTTPException(status_code=500, detail=str(e))

    if (
        not os.path.exists(frames_dir)
        or not os.path.isdir(frames_dir)
        or not os.listdir(frames_dir)
    ):
        error_msg = (
            "Drawing the frames did not succeed, since the frames directory is "
            "empty or does not exist. Cannot proceed to the next step. Aborting."
        )
        logger.error(error_msg, exc_info=traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    mp4_file = vid_base + "_final.mp4"

    if os.path.exists(mp4_file):
        os.remove(mp4_file)

    try:
        run_ffmpeg(vid_base)
    except Exception as e:
        logger.exception("An error occurred while drawing the video frames")
        raise HTTPException(status_code=500, detail=str(e))

    if not os.path.exists(mp4_file):
        error_msg = (
            "Combining audio, frames, and schedule into a video did not succeed. "
            "Cannot proceed to the next step. Aborting."
        )
        logger.error(error_msg, exc_info=traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)

    video_url = request.url_for("get_video_file")
    return {"video_url": str(video_url)}


@router.get("/video")
async def get_video_file():
    mp4_file = vid_base + "_final.mp4"
    full_file_path = mp4_file
    if not os.path.isfile(full_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(full_file_path, media_type="video/mp4")
