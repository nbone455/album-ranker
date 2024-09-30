import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
import time
from requests.exceptions import ReadTimeout
import csv
import pickle

def load_liked_songs():
    try:
        with open('liked_songs_cache.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("Error: liked_songs_cache.pkl not found. Please run fetch_liked_songs.py first.")
        exit(1)

def group_by_album(liked_songs):
    album_tracks = defaultdict(list)
    for item in liked_songs:
        track = item['track']
        album_id = track['album']['id']
        album_tracks[album_id].append(track)
    return album_tracks

def is_full_album(album):
    return album['total_tracks'] >= 6

def calculate_album_percentages(album_tracks):
    album_percentages = {}
    for album_id, tracks in album_tracks.items():
        album = tracks[0]['album']  # Use the first track's album info
        
        # Skip singles and very short albums
        if not is_full_album(album):
            continue

        total_tracks = album['total_tracks']
        liked_tracks = len(tracks)
        percentage = (liked_tracks / total_tracks) * 100
        album_percentages[album_id] = {
            'name': album['name'],
            'artist': album['artists'][0]['name'],
            'percentage': percentage,
            'liked_tracks': liked_tracks,
            'total_tracks': total_tracks,
            'album_type': album['album_type']
        }
    
    return album_percentages

def main():
    print("Loading liked songs from cache...")
    liked_songs = load_liked_songs()
    print(f"Loaded {len(liked_songs)} liked songs.")

    print("Grouping songs by album...")
    album_tracks = group_by_album(liked_songs)

    print("Calculating percentages for full albums...")
    album_percentages = calculate_album_percentages(album_tracks)

    print("Ranking albums...")
    ranked_albums = sorted(album_percentages.items(), key=lambda x: x[1]['percentage'], reverse=True)

    print("Writing top 100 albums to CSV file...")
    with open('spotify_top_100_albums.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Rank', 'Album', 'Artist', 'Album Type', 'Liked Tracks', 'Total Tracks', 'Percentage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for rank, (album_id, data) in enumerate(ranked_albums[:100], 1):
            writer.writerow({
                'Rank': rank,
                'Album': data['name'],
                'Artist': data['artist'],
                'Album Type': data['album_type'],
                'Liked Tracks': data['liked_tracks'],
                'Total Tracks': data['total_tracks'],
                'Percentage': f"{data['percentage']:.2f}%"
            })

    print(f"CSV file 'spotify_top_100_albums.csv' has been created with the top 100 album rankings.")

if __name__ == "__main__":
    main()
