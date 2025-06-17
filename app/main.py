from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from app.schemas import (
    TranscriptionRequest,
    TranscriptionResponse,
    TextToSpeechRequest,
    TextToSpeechResponse,
)
from app.audio_processor import AudioProcessor
from app.dependencies import get_audio_processor
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
import os
import base64


app = FastAPI(title="Audio Service")

print("Initializing Audio Service with settings:")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    request: TranscriptionRequest,
    processor: AudioProcessor = Depends(get_audio_processor),
):
    print("Received file")

    try:
        # Convert base64 to bytes
        audio_bytes = base64.b64decode(request.audio_base64)
        print("audio _bytes:", audio_bytes)

        # Process and transcribe
        transcription = await processor.transcribe_audio_bytes(audio_bytes)
        print("Transcription:", transcription)
        return TranscriptionResponse(transcription=transcription)
    except Exception as e:
        import traceback

        traceback.print_exc()

        raise HTTPException(status_code=500, detail=str(e))


@app.post("/text-to-speech")
async def text_to_speech(
    request: TextToSpeechRequest,
    processor: AudioProcessor = Depends(get_audio_processor),
):
    print("inside text to speech")
    print("request to text-speech", request)
    try:
        # Generate speech and get bytes
        audio_bytes = processor.text_to_speech(text=request.text)
        print("audio_bytes", audio_bytes)
        # Convert to base64
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return TextToSpeechResponse(audio_base64=audio_base64)
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
