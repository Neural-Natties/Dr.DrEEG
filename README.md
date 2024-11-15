# Emotion-Based Music Recommender

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
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.template .env  # Fill in your Spotify credentials
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
