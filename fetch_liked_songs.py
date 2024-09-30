import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pickle

def fetch_liked_songs():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

    results = sp.current_user_saved_tracks()
    liked_songs = results['items']

    while results['next']:
        results = sp.next(results)
        liked_songs.extend(results['items'])

    with open('liked_songs_cache.pkl', 'wb') as f:
        pickle.dump(liked_songs, f)

    print(f"Fetched and cached {len(liked_songs)} liked songs.")

if __name__ == "__main__":
    fetch_liked_songs()
