"""
This module contains the endpoints for audio processing.
"""

from fastapi import FastAPI, HTTPException
from app.main import download_audio, transcribe_audio, convert_to_mp3
from pydantic import BaseModel

app = FastAPI()

class URLPayload(BaseModel):
    url: str

@app.get("/")
def root_endpoint():
    """
    Endpoint to test the root.
    """
    return {"message": "Hello World"}

@app.post("/filename/")
def download(payload: URLPayload):
    """
    Endpoint to download youtube audio from a given URL.
    """
    try:
        url = payload.url
        return {"filename": download_audio(url)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/transcribe/")
def transcribe_audio_endpoint(payload: URLPayload):
    """
    Endpoint to transcribe audio from a given URL.
    """
    try:
        url = payload.url
        filename = download_audio(url)
        filename = convert_to_mp3(filename)
        transcription = transcribe_audio(filename)
        return {"transcription": transcription['text']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e