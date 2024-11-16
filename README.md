# Dr. DrEEG: Realtime Emotion-Based Music Recommendation Karaoke System

Real-time EEG-based emotion detection and music recommendation system using Muse S headband.

## Features

- Real-time EEG processing
- Emotion classification
- Spotify integration
- 3D visualization
- WebSocket communication

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.template .env  # Fill in your credentials
```

Terminal 1 (connect to Muse S headband):

```bash
python3 muse/stream.py
```

Terminal 2 (run backend server):

```bash
python3 app.py
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

## Usage

- Connect Muse S headband
- Start backend server
- Launch frontend application
- Experience emotion-based music recommendations
