import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from user_playlist_integration import  spotify_auth, create_album_outputs,create_playlist_outputs , generate_playlist_feature , generate_playlist_recommendations, create_playlist_outputs_by_link
from oheprep import OHE, create_feature_set
from visualizing import visualize_songs,visualize_songs_with_trackpre
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

if load_dotenv():
    print("Environment variables loaded successfully.")
else:
    print("Could not load environment variables.")

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")
# from datareading import spotify_data


# Spotify auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                    client_secret=client_secret,
                                                  redirect_uri='http://localhost:5089/',
                                                  scope='user-library-read user-top-read user-read-recently-played playlist-read-private'))


spotify_data = pd.read_csv('../Dataset/dataset.csv')
spotify_data['consolidates_genre_lists'] = spotify_data['track_genre'].apply(lambda x: x.split("|"))
spotify_data['popularity_red'] = pd.qcut(spotify_data['popularity'], q=5, labels=False)
float_cols = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
complete_set = create_feature_set(spotify_data, float_cols= float_cols)
complete_set.head()



print(complete_set.columns)

user_playlists = sp.current_user_playlists()

for playlist in user_playlists['items']:
    print(playlist['name'])
    # photo = sp.playlist_cover_image(playlist['id'])
#     print(photo)

# getting songs from kaggle dataset

playlist_id_name = {}
playlist_photo = {}

# for i in sp.current_user_playlists()['items']:
#     playlist_id_name[i['name']] = i['uri'].split(':')[2]
#     playlist_photo[i['uri'].split(':')[2]] = i['images'][0]['url']

# print(playlist_id_name)
    # print(playlist_id_name['Black'])
    # exit()
# checking = sp.playlist(playlist_id_name['Hozzzzzy'])['tracks']['items']
# print(checking)
"""
    playlist and albums don't work the same!
"""

"""
    This is if the user wants to pull by name, but if this doesn't work, we can pull by link
"""
# playlist_with_kaggle = create_playlist_outputs('Hozzzzzy', playlist_id_name, spotify_data, sp)

playlist_with_kaggle = create_playlist_outputs_by_link('https://open.spotify.com/playlist/3rq6CQM7q1nDf97axF4qSx?si=aN5t1HY0SmCQbQg_4oPBkA&pi=a-0W87Ert7RkOF', spotify_data, sp)

# print(playlist_with_kaggle.url)
# playlist_plot  = visualize_songs(playlist_with_kaggle)
# playlist_plot.show()
# print(playlist_with_kaggle.columns)

complete_playlist_features_hozzy,complete_feature_non_playlist = generate_playlist_feature(complete_set, playlist_with_kaggle, 1.08)
# print(complete_playlist_features_hozzy.shape)
#complete_feature_set_playlist_vector_EDM, complete_feature_set_nonplaylist_EDM = generate_playlist_feature(complete_feature_set, playlist_EDM, 1.09)
# print(spotify_data.columns)

recommendation_for_playlist = generate_playlist_recommendations(spotify_data,complete_playlist_features_hozzy, complete_feature_non_playlist,sp)
# # edm_top40 = generate_playlist_recos(spotify_df, complete_feature_set_playlist_vector_EDM, complete_feature_set_nonplaylist_EDM)
# print(recommendation_for_playlist)
# print(recommendation_for_playlist.columns)
visualize_songs_with_trackpre(recommendation_for_playlist).show()
