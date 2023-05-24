from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware

from controller.textToVideoController import router as text_to_video



app = FastAPI(
    title="Text_to_video",
    description="Create a video from text",
    version="1.0.0"
)

allowed_methods = ["POST", "GET"]

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=allowed_methods, allow_headers=["*"])


@app.get("/healthz")
def get_request():
    return PlainTextResponse("Healthy")


routes=[text_to_video]
for route in routes:
  app.include_router(route)
