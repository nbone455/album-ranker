# album-ranker

This script ranks your liked songs on Spotify by album and generates a CSV file with the top 100 albums based on the percentage of liked tracks. What an "album" is defined as is up to you, currently it is 6 or more songs.

## Prerequisites

- Python 3.x
- `spotipy` library
- Spotify Developer account

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/spotify-album-ranker.git
    cd spotify-album-ranker
    ```

2. **Install the required libraries:**
    ```sh
    pip install spotipy
    ```

3. **Set up Spotify API credentials:**
    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create a new application.
    - Note down the `Client ID` and `Client Secret`.
    - Set the Redirect URI to `http://localhost:8888/callback`.

4. **Create a `.env` file in the project directory and add your Spotify API credentials:**
    ```env
    SPOTIPY_CLIENT_ID='your_client_id'
    SPOTIPY_CLIENT_SECRET='your_client_secret'
    SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
    ```

5. **Fetch your liked songs:**
    - Run the `fetch_liked_songs.py` script to cache your liked songs.
    ```sh
    python fetch_liked_songs.py
    ```
This might take a while but creates a liked songs cache that can be used for other things.

6. **Run the album ranker script:**
    ```sh
    python spotify_album_ranker.py
    ```
## Output

The script will generate a CSV file named `spotify_top_100_albums.csv` with the top 100 albums ranked by the percentage of liked tracks.
