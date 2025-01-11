import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

if load_dotenv():
    print("Environment variables loaded successfully.")
else:
    print("Could not load environment variables.")

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')


def spotify_data():
    """
    Read in the spotify dataset.

    Returns:
        spotify_data: spotify dataset
    """

    spotify_data = pd.read_csv('../Dataset/dataset.csv')
    return spotify_data

def spotify_auth():
    """
    Spotify authentication.

    Returns:
        sp: spotify object
    """

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                  client_secret=client_secret,
                                                  redirect_uri='http://localhost:5089/',
                                                  scope='user-library-read user-top-read user-read-recently-played playlist-read-private'))
    return sp


def create_album_outputs(album_name, id_dic, df,sp):
    """
    Pull songs from a specific album.

    Parameters:
        album_name (str): name of the album you'd like to pull from the spotify API
        id_dic (dic): dictionary that maps album_name to album_id
        df (pandas dataframe): spotify dataframe
        sp: spotify object

    Returns:
        album: all songs in the album THAT ARE AVAILABLE IN THE PROVIDED DATASET
    """

    #generate album dataframe
    album = pd.DataFrame()
    for ix, i in enumerate(sp.album(id_dic[album_name])['tracks']['items']):
        album.loc[ix, 'artist'] = i['artists'][0]['name']
        album.loc[ix, 'name'] = i['name']
        album.loc[ix, 'id'] = i['id']
        album.loc[ix, 'url'] = i['album']['images'][1]['url']
        album.loc[ix, 'date_added'] = i['added_at']

    album['date_added'] = pd.to_datetime(album['date_added'])

    album = album[album['id'].isin(df['id'].values)].sort_values('date_added',ascending = False)

    return album


def create_playlist_outputs(playlist_name, id_dic, df, sp):
    """
    Pull songs from a specific playlist.

    Parameters:
        playlist_name (str): name of the playlist you'd like to pull from the spotify API
        id_dic (dic): dictionary that maps playlist_name to playlist_id
        df (pandas dataframe): spotify dataframe
        sp: spotify object

    Returns:
        playlist: all songs in the playlist THAT ARE AVAILABLE IN THE PROVIDED DATASET
    """

    #generate playlist dataframe
    playlist = pd.DataFrame()
    for ix, i in enumerate(sp.playlist(id_dic[playlist_name])['tracks']['items']):
        playlist.loc[ix, 'artist'] = i['track']['artists'][0]['name']
        playlist.loc[ix, 'name'] = i['track']['name']
        playlist.loc[ix, 'id'] = i['track']['id']
        playlist.loc[ix, 'url'] = i['track']['album']['images'][1]['url']
        playlist.loc[ix, 'date_added'] = i['added_at']

    playlist['date_added'] = pd.to_datetime(playlist['date_added'])
    # print('debugging playlist columns')
    # print(playlist.columns)
    # print(df.columns)

    playlist = playlist[playlist['id'].isin(df['track_id'].values)].sort_values('date_added',ascending = False)

    return playlist


def create_playlist_outputs_by_id(playlist_id, df, sp):
    """
    Pull songs from a specific playlist.

    Parameters:
        playlist_id (str): ID of the playlist you'd like to pull from the spotify API
        df (pandas dataframe): spotify dataframe
        sp: spotify object

    Returns:
        playlist: all songs in the playlist THAT ARE AVAILABLE IN THE PROVIDED DATASET
    """

    #generate playlist dataframe
    playlist = pd.DataFrame()

    for ix, i in enumerate(sp.playlist(playlist_id)['tracks']['items']):
        playlist.loc[ix, 'artist'] = i['track']['artists'][0]['name']
        playlist.loc[ix, 'name'] = i['track']['name']
        playlist.loc[ix, 'id'] = i['track']['id']
        playlist.loc[ix, 'url'] = i['track']['album']['images'][1]['url']
        playlist.loc[ix, 'date_added'] = i['added_at']

    playlist['date_added'] = pd.to_datetime(playlist['date_added'])

    playlist = playlist[playlist['id'].isin(df['track_id'].values)].sort_values('date_added',ascending = False)

    return playlist

def create_playlist_outputs_by_link(playlist_link, df, sp):
    """
    Pull songs from a specific playlist.

    Parameters:
        playlist_link (str): Spotify link of the playlist you'd like to pull from the spotify API
        df (pandas dataframe): spotify dataframe
        sp: spotify object

    Returns:
        playlist: all songs in the playlist THAT ARE AVAILABLE IN THE PROVIDED DATASET
    """

    # Extract playlist id from the link
    playlist_id = playlist_link.split('/')[-1].split('?')[0]

    # Generate playlist dataframe
    playlist = pd.DataFrame()

    for ix, i in enumerate(sp.playlist(playlist_id)['tracks']['items']):
        playlist.loc[ix, 'artist'] = i['track']['artists'][0]['name']
        playlist.loc[ix, 'name'] = i['track']['name']
        playlist.loc[ix, 'id'] = i['track']['id']
        playlist.loc[ix, 'url'] = i['track']['album']['images'][1]['url']
        playlist.loc[ix, 'date_added'] = i['added_at']

    playlist['date_added'] = pd.to_datetime(playlist['date_added'])

    playlist = playlist[playlist['id'].isin(df['track_id'].values)].sort_values('date_added',ascending = False)

    return playlist


def generate_playlist_feature(complete_feature_set, playlist_df, weight_factor):
    """
    Summarize a user's playlist into a single vector

    Parameters:
        complete_feature_set (pandas dataframe): Dataframe which includes all of the features for the spotify songs
        playlist_df (pandas dataframe): playlist dataframe
        weight_factor (float): float value that represents the recency bias. The larger the recency bias, the most priority recent songs get. Value should be close to 1.

    Returns:
        playlist_feature_set_weighted_final (pandas series): single feature that summarizes the playlist
        complete_feature_set_nonplaylist (pandas dataframe):
    """
    # Error handling
    if not isinstance(complete_feature_set, pd.DataFrame) or not isinstance(playlist_df, pd.DataFrame):
        raise ValueError("complete_feature_set and playlist_df must be pandas DataFrame objects")
    if not isinstance(weight_factor, (int, float)):
        raise ValueError("weight_factor must be a numeric value")

    complete_feature_set_playlist = complete_feature_set[complete_feature_set['id'].isin(playlist_df['id'].values)]
    complete_feature_set_playlist = complete_feature_set_playlist.merge(playlist_df[['id','date_added']], on = 'id', how = 'inner')
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['id'].isin(playlist_df['id'].values)]

    playlist_feature_set = complete_feature_set_playlist.sort_values('date_added',ascending=False)

    most_recent_date = playlist_feature_set.iloc[0,-1]

    for ix, row in playlist_feature_set.iterrows():
        playlist_feature_set.loc[ix,'months_from_recent'] = int((most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days / 30)

    playlist_feature_set['weight'] = playlist_feature_set['months_from_recent'].apply(lambda x: weight_factor ** (-x))

    playlist_feature_set_weighted = playlist_feature_set.copy()
    playlist_feature_set_weighted.update(playlist_feature_set_weighted.iloc[:,:-4].mul(playlist_feature_set_weighted.weight,0))
    playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-4]

    return playlist_feature_set_weighted_final.sum(axis = 0), complete_feature_set_nonplaylist



def generate_playlist_recommendations(df, features, nonplaylist_features,sp):
    """
    Pull songs from a specific playlist.

    Parameters:
        df (pandas dataframe): spotify dataframe
        features (pandas series): summarized playlist feature
        nonplaylist_features (pandas dataframe): feature set of songs that are not in the selected playlist
        sp: spotify object
    Returns:
        non_playlist_df_top_10: Top 10 recommendations for that playlist
    """

    if 'track_id' not in df.columns:
            raise ValueError("The DataFrame does not contain an 'id' column.")

    non_playlist_df = df[df['track_id'].isin(nonplaylist_features['id'].values)]
    non_playlist_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis = 1).values, features.values.reshape(1, -1))[:,0]
    non_playlist_df_top_30 = non_playlist_df.sort_values('sim',ascending = False).head(30)
    # print("tes tes")
    # print(non_playlist_df.columns)
    non_playlist_df_top_10 = non_playlist_df_top_30.drop_duplicates(subset=['track_id']).head(10)
    non_playlist_df_top_10['url'] = non_playlist_df_top_10['track_id'].apply(lambda x: sp.track(x)['album']['images'][1]['url'])

    return non_playlist_df_top_10