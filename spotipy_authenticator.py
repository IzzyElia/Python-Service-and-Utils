# spotipy_authenticator.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Function to load authentication details from a file
def load_auth_details(auth_file):
    auth_details = {}
    with open(auth_file, 'r') as file:
        for line in file:
            if ':' in line:
                item, value = line.strip().split(':', 1)
                auth_details[item] = value
    return auth_details

# Function to initialize the Spotify client with broad scope
def init_spotipy_client(auth_file='spotify-auth.txt'):
    auth_details = load_auth_details(auth_file)
    try:
        spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=auth_details['client_id'],
            client_secret=auth_details['client_secret'],
            redirect_uri=auth_details['redirect_uri'],
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
            cache_path=auth_details.get('cache_path', '.spotipyoauthcache')
        ))
        return spotify_client
    except KeyError as e:
        raise Exception(f"Missing key in authentication details: {e}")
    except spotipy.SpotifyException as e:
        raise Exception(f"An error occurred with the Spotify API: {e}")

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
