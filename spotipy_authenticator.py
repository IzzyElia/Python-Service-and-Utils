# spotipy_authenticator.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv




# Function to initialize the Spotify client with broad scope
def init_spotipy_client():
    # Load environment variables from .env file
    load_dotenv()
    try:
        client_secret = os.environ['SPOTIFY_SECRET']
    except KeyError:
        raise KeyError("Environment variable 'SPOTIFY_SECRET' is not set")

    try:
        client_id = os.environ['SPOTIFY_CLIENT_ID']
    except KeyError:
        raise KeyError("Environment variable 'SPOTIFY_CLIENT_ID' is not set")

    # Assuming the redirect URI and cache path are still defined in the 'config.txt' file
    # and using the same function `load_auth_details` to get them
    config_details = load_auth_details('config.txt')

    spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=config_details['redirect_uri'],
        scope=" ".join([
            "ugc-image-upload",
            "user-read-recently-played",
            "user-top-read",
            "user-read-playback-position",
            "user-read-playback-state",
            "user-read-currently-playing",
            "app-remote-control",
            "streaming",
            "playlist-modify-public",
            "playlist-modify-private",
            "playlist-read-private",
            "playlist-read-collaborative",
            "user-follow-modify",
            "user-follow-read",
            "user-library-modify",
            "user-library-read",
            "user-read-email",
            "user-read-private"
        ]),
        cache_path=config_details.get('cache_path', '.spotipyoauthcache')
    ))
    return spotify_client

# Test method to retrieve user data
def test_authentication(spotify_client):
    user_info = spotify_client.me()
    return user_info

# If this module is run directly, it will test the authentication
if __name__ == "__main__":
    try:
        spotify_client = init_spotipy_client()
        user_data = test_authentication(spotify_client)
        print(f"Successfully retrieved user data for {user_data['display_name']}")
    except Exception as e:
        print(f"An error occurred: {e}")
