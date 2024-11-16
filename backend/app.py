from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import threading
from muse.processor import MuseProcessor
from ml.features import extract_eeg_features

app = FastAPI()
muse_processor = None


async def init_muse():
    global muse_processor
    muse_processor = MuseProcessor()
    await muse_processor.start_stream()


@app.on_event("startup")
async def startup_event():
    await init_muse()


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if muse_processor:
                eeg_features = await muse_processor.get_eeg_features()
                if eeg_features is not None:
                    await websocket.send_json(
                        {
                            "eeg_data": eeg_features.tolist(),
                            "timestamp": asyncio.get_event_loop().time(),
                        }
                    )
            await asyncio.sleep(0.1)
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
