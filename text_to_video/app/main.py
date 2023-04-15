from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from text_to_video.app.controller.phonemesController import router as phonemes_router
from text_to_video.app.controller.schedulerController import router as scheduler_router
from text_to_video.app.controller.video_controller import router as video_router


app = FastAPI(
    title="Text_to_video", description="Create a video from text", version="1.0.0"
)

allowed_methods = ["POST", "GET"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=allowed_methods,
    allow_headers=["*"],
)


@app.get("/healthz")
def get_request():
    return PlainTextResponse("Healthy")


routes = [phonemes_router, scheduler_router, video_router]
for route in routes:
    app.include_router(route)
