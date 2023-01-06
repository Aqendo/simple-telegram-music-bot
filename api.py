import asyncio
from functools import partial, wraps
import os
import uuid
from fastapi import FastAPI
import yt_dlp
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

app = FastAPI()


def do(name):
    filename = str(uuid.uuid4())
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
        "outtmpl": f"./{filename}.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://youtu.be/{name}"])
        return filename


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


@app.get("/")
async def get_legacy_data(video_id: str, background_tasks: BackgroundTasks):
    filename = await wrap(do)(video_id)
    result = None
    with open(filename + ".m4a", "rb") as f:
        result = f.read()
    assert result is not None
    background_tasks.add_task(os.unlink, filename + ".m4a")
    return FileResponse(filename + ".m4a")
