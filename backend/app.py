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


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             # Get EEG features
#             eeg_features = await muse_processor.get_eeg_features()

#             if eeg_features is not None:
#                 # For now, let's send the raw features
#                 await websocket.send_json(
#                     {
#                         "eeg_data": eeg_features.tolist(),
#                         "timestamp": asyncio.get_event_loop().time(),
#                     }
#                 )

#             await asyncio.sleep(0.1)  # Adjust rate as needed

#     except WebSocketDisconnect:
#         print("Client disconnected")

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
