import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ..config.settings import settings


def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope="user-library-read playlist-modify-public",
        )
    )
