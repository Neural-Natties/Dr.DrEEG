from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv()


class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str = "http://localhost:8000/callback"
    GENIUS_CLIENT_ID: str
    GENIUS_ACCESS_TOKEN: str

    WEBSOCKET_HOST: str = "0.0.0.0"
    WEBSOCKET_PORT: int = 8000

    MODEL_PATH: str = "models/emotion_classifier.pkl"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
