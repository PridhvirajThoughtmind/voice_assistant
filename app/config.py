from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VOSK_MODEL_PATH: str = "./vosk-model"
    ELEVENLABS_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
