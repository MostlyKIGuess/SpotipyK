import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import dataframe_image as dfi
from collections import defaultdict

# spotify auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='yourclientid',
                                                client_secret='yourclientsecret',
                                                redirect_uri='http://localhost:5089/',
                                                scope='user-library-read user-top-read user-read-recently-played playlist-read-private'))
#user data
try:
    user_recently_played = sp.current_user_recently_played(limit=50)['items']
except spotipy.SpotifyException as e:
    print(f"Error: {e}")
    sys.exit(1)


tracks_with_features = []
seen_track_ids = set()
for item in user_recently_played:
    track = item['track']
    track_id = track['id']
    if track_id not in seen_track_ids:
        seen_track_ids.add(track_id)
        audio_features = sp.audio_features([track_id])[0]
        if audio_features:
            track_with_features = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity'],
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'key': audio_features['key'],
                'loudness': audio_features['loudness'],
                'mode': audio_features['mode'],
                'speechiness': audio_features['speechiness'],
                'acousticness': audio_features['acousticness'],
                'instrumentalness': audio_features['instrumentalness'],
                'liveness': audio_features['liveness'],
                'valence': audio_features['valence'],
                'tempo': audio_features['tempo'],
            }
            tracks_with_features.append(track_with_features)
    if len(tracks_with_features) == 30:
        break

# Canda panda
df = pd.DataFrame(tracks_with_features)
df.index += 1
dfi.export(df, 'dataframe.png')

print("DataFrame saved as 'dataframe.png'")
