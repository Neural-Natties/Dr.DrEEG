import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from muse.processor import MuseProcessor
from spotify.auth import get_spotify_client
from spotify.recommender import MusicRecommender

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
    try:
        # Get recommendations for different emotions
        emotions = ["happy", "calm", "focused", "excited"]
        for emotion in emotions:
            songs = recommender.get_recommendations(emotion, limit=2)
            for song in songs:
                await websocket.send_json({"emotion": emotion, "song": song})
                await asyncio.sleep(10)  # Wait 10 seconds between songs
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
                    "song": {"name": "Test Song", "artist": "Test Artist"},
                }
            )
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
