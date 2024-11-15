from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str = "http://localhost:8000/callback"

    WEBSOCKET_HOST: str = "0.0.0.0"
    WEBSOCKET_PORT: int = 8000

    MODEL_PATH: str = "models/emotion_classifier.pkl"

    class Config:
        env_file = ".env"


settings = Settings()
