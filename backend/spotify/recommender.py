from typing import Dict, List
import random
import lyricsgenius
from spotify.auth import get_spotify_client
from config.settings import settings


class MusicRecommender:
    def __init__(self):
        self.sp = get_spotify_client()
        self.genius = lyricsgenius.Genius(settings.GENIUS_ACCESS_TOKEN)

    def generate_emotion_seeds(self, emotion: str) -> Dict:
        seeds = {
            "sad": {
                "target_valence": random.uniform(0.2, 0.4),
                "target_energy": random.uniform(0.3, 0.5),
                "target_tempo": random.randint(40, 80),
                "target_popularity": random.randint(80, 100),
                "genres": ["sad", "acoustic", "piano"],
            },
            "angry": {
                "target_valence": random.uniform(0.2, 0.4),
                "target_energy": random.uniform(0.6, 0.8),
                "target_tempo": random.randint(120, 160),
                "target_popularity": random.randint(80, 100),
                "genres": ["metal", "punk", "rock"],
            },
            "stressed": {
                "target_valence": random.uniform(0.4, 0.5),
                "target_energy": random.uniform(0.4, 0.6),
                "target_tempo": random.randint(60, 100),
                "target_popularity": random.randint(80, 100),
                "genres": ["ambient", "chill", "classical"],
            },
            "happy": {
                "target_valence": random.uniform(0.7, 0.9),
                "target_energy": random.uniform(0.6, 0.8),
                "target_tempo": random.randint(100, 140),
                "target_popularity": random.randint(80, 100),
                "genres": ["pop", "dance", "happy"],
            },
            "excited": {
                "target_valence": random.uniform(0.7, 0.9),
                "target_energy": random.uniform(0.7, 0.9),
                "target_tempo": random.randint(120, 160),
                "target_popularity": random.randint(80, 100),
                "genres": ["edm", "party", "rock"],
            },
        }
        return seeds.get(emotion, seeds["happy"])

    def get_recommendations(self, emotion: str, limit: int = 5) -> List[Dict]:
        params = self.generate_emotion_seeds(emotion)
        print(params)
        recommendations = self.sp.recommendations(
            seed_genres=params["genres"][:2],
            limit=limit,
            **{k: v for k, v in params.items() if k != "genres"}
        )

        tracks = []

        for track in recommendations["tracks"]:
            song = self.genius.search_song(track["name"], track["artists"][0]["name"])
            lyrics = []
            if song and song.lyrics:
                raw_lyrics = song.lyrics.split("\n")
                for line in raw_lyrics:
                    line = line.strip()
                    if line and not line.startswith("[") and not line.endswith("]"):
                        lyrics.append(line)

            tracks.append(
                {
                    "id": track["id"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "url": track["external_urls"]["spotify"],
                    "albumArt": (
                        track["album"]["images"][0]["url"]
                        if track["album"]["images"]
                        else None
                    ),
                    "album": track["album"]["name"],
                    "duration": track["duration_ms"],
                    "emotion": emotion,
                    "lyrics": lyrics,
                }
            )
        return tracks
