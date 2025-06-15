from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from app.schemas import TranscriptionResponse, TextToSpeechRequest
from app.audio_processor import AudioProcessor
from app.dependencies import get_audio_processor
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
import os


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
    file: UploadFile = File(...),
    processor: AudioProcessor = Depends(get_audio_processor),
):
    print(f"Received file: {file.filename}")
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only WAV files are supported")

    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Process audio and transcribe
        enhanced_path = processor.enhance_audio(temp_path)
        transcription = processor.transcribe_audio(enhanced_path)

        # Clean up
        os.remove(temp_path)
        os.remove(enhanced_path)

        return TranscriptionResponse(transcription=transcription)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/text-to-speech")
async def text_to_speech(
    request: TextToSpeechRequest,
    processor: AudioProcessor = Depends(get_audio_processor),
):
    try:
        # Generate speech and save to temporary file
        output_path = processor.text_to_speech(request.text)

        # Return the audio file
        response = FileResponse(
            path=output_path, media_type="audio/mpeg", filename="output.mp3"
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
