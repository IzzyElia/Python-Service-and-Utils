#artist_data.py

import spotipy
from spotipy_authenticator import init_spotipy_client

def get_followed_artists_data():
    # Create Spotipy client
    sp = init_spotipy_client()

    # Initialize variables
    followed_artists = []
    after = None

    # Loop to fetch all followed artists
    while True:
        artists = sp.current_user_followed_artists(limit=50, after=after)
        followed_artists.extend(artists['artists']['items'])

        # Check if there are more artists to fetch
        after = artists['artists']['cursors']['after']
        if not after:
            break

    return followed_artists

def get_followed_artists_names():
    # Create Spotipy client
    sp = init_spotipy_client()

    # Fetch all artist data
    followed_artists = get_followed_artists_data()

    # Extract artist names
    artist_names = [artist['name'] for artist in followed_artists]

    return artist_names
