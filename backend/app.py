import asyncio
import uvicorn
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from muse.processor import MuseProcessor
from muselsl import record, stream, list_muses
from spotify.auth import get_spotify_client
from spotify.recommender import MusicRecommender
import numpy as np
from scipy.signal import welch
from ml.model import load_model, classify_emotion
from random import shuffle
from ml.EEG_feature_extraction import (
    generate_feature_vectors_from_samples,
    matrix_from_csv_file,
    calc_feature_vector,
    get_time_slice,
    feature_mean,
)

app = FastAPI()
muse_processor = MuseProcessor()
recommender = MusicRecommender()

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
    token = get_spotify_client().auth_manager.get_access_token()
    if token:
        return {"access_token": token["access_token"]}
    else:
        return {"error": "Token not found"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    model = load_model()
    try:
        model = load_model()
        print("Model loaded")
        with open("muse_readings.csv", "w") as f:
            pass
        stream_name = "muse_readings.csv"
        # os.remove(stream_name)
        while True:
            cwd = os.getcwd()
            print(cwd)
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
            shuffle(songs)

            if detected_emotion is not None:
                await websocket.send_json(
                    {
                        "emotion": detected_emotion,
                        "song": songs,
                        "timestamp": asyncio.get_event_loop().time(),
                    }
                )
            await asyncio.sleep(songs[0]["duration"] / 1000)
    except WebSocketDisconnect:
        print("Client disconnected")


@app.websocket("/wstest")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(
                {
                    "emotion": {"type": "happy", "confidence": 0.85},
                    "valence": "0.33",
                    "song": {"name": "Test Song", "artist": "Test Artist"},
                    "timestamp": "124345.345678",
                }
            )
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
