from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from websockets.server import serve
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def websocket_handler(websocket):
    while True:
        # Get EEG data
        eeg_data = await get_muse_data()
        # Predict emotion
        emotion = predict_emotion(eeg_data)
        # Get song recommendation
        song = get_opposite_emotion_song(emotion)
        # Send to frontend
        await websocket.send_json({"emotion": emotion, "song": song})
        await asyncio.sleep(1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
