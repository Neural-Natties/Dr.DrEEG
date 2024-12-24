import argparse
import asyncio
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ml.EEG_feature_extraction import (
    calc_feature_vector,
    feature_mean,
    generate_feature_vectors_from_samples,
    get_time_slice,
    matrix_from_csv_file,
)
from ml.model import load_model, classify_emotion
from spotify.auth import get_spotify_client
from spotify.recommender import MusicRecommender

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()
debug = args.debug

app = FastAPI()

if debug:
    from muse.processor import MuseProcessor
    from muselsl import record

    muse_processor = MuseProcessor()

recommender = MusicRecommender()
model = load_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "online", "message": "EEG Backend is running!"}


@app.get("/test")
def test_endpoint():
    return {"data": "Connection successful!"}


@app.get("/auth/login")
async def login():
    auth_url = get_spotify_client().get_authorize_url()
    return {"url": auth_url}


@app.get("/auth/callback")
async def callback(code: str):
    token_info = get_spotify_client().get_access_token(code)
    return {"access_token": token_info["access_token"]}


@app.get("/auth/token")
async def get_token():
    token = get_spotify_client().auth_manager.get_cached_token()
    if token:
        return {"access_token": token["access_token"]}
    else:
        return {"error": "Token not found"}


@app.get("/ws")
async def websocket_endpoint():
    global model
    try:
        print("Model loaded")
        with open("muse_readings.csv", "w") as f:
            pass

        stream_name = "muse_readings.csv" if debug else "ml/data/test-data.csv"
        while True:
            cwd = os.getcwd()
            print(cwd)
            if debug:
                record(8, filename=cwd + "/" + stream_name)

            with open(stream_name, "r") as f, open(
                stream_name.replace(".csv", "out.csv"), "w"
            ) as out:
                lines = f.readlines()
                out.writelines(lines[:602])

            detected_emotion = classify_emotion(
                model, stream_name.replace(".csv", "out.csv")
            )
            if detected_emotion:
                print(detected_emotion)
            songs = recommender.get_recommendations(detected_emotion, limit=1)

            if detected_emotion is not None:
                return {
                    "emotion": detected_emotion,
                    "song": songs[0],
                    "timestamp": asyncio.get_event_loop().time(),
                }
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="debug")
