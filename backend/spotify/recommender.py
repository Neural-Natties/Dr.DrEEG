from typing import Dict, List
import spotipy
import lyricsgenius
from spotify.auth import get_spotify_client
from config.settings import settings


class MusicRecommender:
    def __init__(self):
        self.sp = get_spotify_client()
        self.genius = lyricsgenius.Genius(settings.GENIUS_ACCESS_TOKEN)
        self.emotion_seeds = {
            "sad": {
                "max_valence": 0.3,
                "max_energy": 0.4,
                "target_tempo": 60,
                "target_popularity": 100,
                "genres": ["sad", "acoustic", "piano"],
            },
            "angry": {
                "min_valence": 0.3,
                "min_energy": 0.7,
                "target_tempo": 140,
                "target_popularity": 100,
                "genres": ["metal", "punk", "rock"],
            },
            "stressed": {
                "max_valence": 0.4,
                "max_energy": 0.6,
                "target_tempo": 80,
                "target_popularity": 100,
                "genres": ["ambient", "chill", "sleep"],
            },
            "neutral": {
                "target_valence": 0.5,
                "target_energy": 0.5,
                "target_tempo": 100,
                "target_popularity": 100,
                "genres": ["pop", "indie", "acoustic"],
            },
            "relaxed": {
                "max_valence": 0.5,
                "max_energy": 0.4,
                "target_tempo": 60,
                "target_popularity": 100,
                "genres": ["ambient", "chill", "sleep"],
            },
            "happy": {
                "min_valence": 0.7,
                "min_energy": 0.7,
                "target_tempo": 120,
                "target_popularity": 100,
                "genres": ["pop", "dance", "happy"],
            },
            "joyful": {
                "min_valence": 0.8,
                "min_energy": 0.6,
                "target_tempo": 120,
                "target_popularity": 100,
                "genres": ["pop", "dance", "happy"],
            },
            "excited": {
                "min_valence": 0.8,
                "min_energy": 0.8,
                "target_tempo": 140,
                "target_popularity": 100,
                "genres": ["edm", "party", "rock"],
            },
        }

    def get_recommendations(self, emotion: str, limit: int = 5) -> List[Dict]:
        params = self.emotion_seeds.get(emotion, self.emotion_seeds["relaxed"])

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
