import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import sys
# Spotify auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='woho',
                                               client_secret='lol',
                                               redirect_uri='http://localhost:5089/',
                                               scope='user-library-read user-top-read user-read-recently-played playlist-read-private'))

# Get user's recently played tracks
try:
    user_recently_played = sp.current_user_recently_played(limit=50)['items']
except spotipy.SpotifyException as e:
    print(f"Error: {e}")
    sys.exit(1)

# Get unique songs from recently played
recently_played_tracks = []
for item in user_recently_played:
    track = item['track']
    if track['id'] not in [t['id'] for t in recently_played_tracks]:
        recently_played_tracks.append(track)
        if len(recently_played_tracks) == 5:  # Limit to 5 seed tracks
            break

# Generate recommendations based on the recently played tracks
seed_tracks = [track['id'] for track in recently_played_tracks]
recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=40)

# Print the recommended songs
for track in recommendations['tracks']:
    print(f"Recommended Song: {track['name']} by {track['artists'][0]['name']}")