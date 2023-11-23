import json
import spotipy_authenticator
import artist_data

def check_new_releases():
    # Step 1: Initialize Spotipy client
    sp = spotipy_authenticator.init_spotipy_client()

    # Step 2: Get followed artists
    followed_artists = artist_data.get_followed_artists_data()

    # Step 3: Read the existing JSON file
    try:
        with open('artist_last_release_log.json', 'r') as file:
            last_releases = json.load(file)
    except FileNotFoundError:
        last_releases = {}

    new_releases = []

    for artist in followed_artists:
        # Step 4: Get the artist's last release from Spotify
        results = sp.artist_albums(artist['id'], album_type='album,single')
        if results['items']:
            latest_release = max(results['items'], key=lambda x: x['release_date'])
            latest_release_date = latest_release['release_date']

            # Step 5: Compare and update
            if (artist['name'] not in last_releases) or (latest_release_date > last_releases[artist['name']]):
                if artist['name'] in last_releases:
                    new_releases.append({'artist': artist['name'], 'album': latest_release['name'], 'date':latest_release_date})
                last_releases[artist['name']] = latest_release_date

    cached_last_release_data = last_releases
    return new_releases


def update_log(new_releases):
    try:
        with open('artist_last_release_log.json', 'r') as file:
            last_releases = json.load(file)
    except FileNotFoundError:
        last_releases = {}

    for release in new_releases:
        artist_name = release['artist']
        release_date = release['date']
        # Update the entry if the artist is already present, otherwise add a new entry
        last_releases[artist_name] = release_date

    # Step 6: Save updated release dates back to the JSON file
    with open('artist_last_release_log.json', 'w') as file:
        json.dump(last_releases, file)


if __name__ == "__main__":
    try:
        new_releases = check_new_releases()
        if new_releases:
            print("New releases found:")
            for release in new_releases:
                print(f"{release['artist']} - {release['album']}")

        else:
            print("No new releases found.")
    except Exception as e:
        print(f"An error occurred: {e}")