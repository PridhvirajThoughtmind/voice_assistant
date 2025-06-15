from fastapi import Depends
from app.config import Settings, settings
from app.audio_processor import AudioProcessor


def get_audio_processor(
    settings: Settings = Depends(lambda: settings),
) -> AudioProcessor:
    print("Creating AudioProcessor with settings:")
    return AudioProcessor(settings)
