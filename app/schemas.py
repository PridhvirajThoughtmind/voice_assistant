from pydantic import BaseModel, Field


class TranscriptionRequest(BaseModel):
    audio_base64: str = Field(..., max_length=13_333_333)  # ~10MB raw audio


class TranscriptionResponse(BaseModel):
    transcription: str


class TextToSpeechRequest(BaseModel):
    text: str = Field(..., max_length=13_333_333)  # ~10MB raw audio


class TextToSpeechResponse(BaseModel):
    audio_base64: str
