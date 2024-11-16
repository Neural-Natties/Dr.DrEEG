import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from muse.processor import MuseProcessor
from spotify.auth import get_spotify_client
from spotify.recommender import MusicRecommender
import numpy as np
from scipy.signal import welch
from ml.model import load_model, classify_emotion
from ml.EEG_feature_extraction import generate_feature_vectors_from_samples, matrix_from_csv_file, calc_feature_vector,  get_time_slice, generate_features_for_timeslice, feature_mean

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
        # print("Model loaded")
        while True:
            eeg_features = await muse_processor.get_eeg_features()
            eeg_feature_vectors, _ = generate_feature_vectors_from_samples("../test-muse/recordings/test-data.csv", 400, 1, '0', False)

            detected_emotion = classify_emotion(model,eeg_feature_vectors, 0)
            emotion = detected_emotion['emotion']
            songs = recommender.get_recommendations(emotion, limit=2)
            songs.shuffle()
                


            # time = eeg_features[-1][0]
            # print("Time", time)
            # # break
            # for i in range( int(time-eeg_features[0][0])):
            #     # eeg_features[i] = extract_eeg_features(eeg_features[i])
            #     print(f"Getting time slice {i}")
                
            #     time_slice, _ = get_time_slice(eeg_features, i)
            #     print("Time slice shape", time_slice.shape, "\n",time_slice)  
            #     if 0 in time_slice.shape: 
            #         continue
            #     features, _ = generate_features_for_timeslice(time_slice)

            #     time_slice = features
            #     print("Time slice shape", time_slice.shape, "\n",time_slice)
            #     time_slice, _ = feature_mean(time_slice)
            #     print("Time slice shape", time_slice.shape, "\n",time_slice)
            #     classifications.append(classify_emotion(model, time_slice, i))
            
            # for i, classification in enumerate(classifications):
            if detected_emotion is not None:
                # For now, let's send the raw features
                print(f"Sending classification {i}")
                await websocket.send_json(
                    {
                        # "eeg_data": eeg_features.tolist(),
                        "emotion": detected_emotion['emotion'],
                        "valence": detected_emotion['valence'],
                        "song": songs[0],
                        "timestamp": asyncio.get_event_loop().time(),
                    }
                )
                # await asyncio.sleep(1)  
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")


@app.websocket("/wstest")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        model = load_model()
        # print("Model loaded")
        while True:
            eeg_features = await muse_processor.get_eeg_features()
            eeg_feature_vectors, _ = generate_feature_vectors_from_samples("../test-muse/recordings/test-data.csv", 400, 1, '0', False)

            detected_emotion = classify_emotion(model,eeg_feature_vectors, 0)


            # time = eeg_features[-1][0]
            # print("Time", time)
            # # break
            # for i in range( int(time-eeg_features[0][0])):
            #     # eeg_features[i] = extract_eeg_features(eeg_features[i])
            #     print(f"Getting time slice {i}")
                
            #     time_slice, _ = get_time_slice(eeg_features, i)
            #     print("Time slice shape", time_slice.shape, "\n",time_slice)  
            #     if 0 in time_slice.shape: 
            #         continue
            #     features, _ = generate_features_for_timeslice(time_slice)

            #     time_slice = features
            #     print("Time slice shape", time_slice.shape, "\n",time_slice)
            #     time_slice, _ = feature_mean(time_slice)
            #     print("Time slice shape", time_slice.shape, "\n",time_slice)
            #     classifications.append(classify_emotion(model, time_slice, i))
            
            # for i, classification in enumerate(classifications):
            if detected_emotion is not None:
                # For now, let's send the raw features
                print(f"Sending classification {i}")
                await websocket.send_json(
                    {
                        "eeg_data": eeg_features.tolist(),
                        "emotion": detected_emotion['emotion'],
                        "valence": detected_emotion['valence'],
                        "timestamp": asyncio.get_event_loop().time(),
                    }
                )
                await asyncio.sleep(1)  # Adjust rate as needed
            # await websocket.send_json(
            #     {
            #         "emotion": {"type": "happy", "confidence": 0.85},
            #         "song": {"name": "Test Song", "artist": "Test Artist"},
            #     }
            # )
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
