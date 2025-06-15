from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    transcription: str


class TextToSpeechRequest(BaseModel):
    text: str
