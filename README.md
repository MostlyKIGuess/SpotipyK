# Spotify Music Analysis Project 

## Overview

The project utilises the spotify API to obtain user's music preferences and analyse the data to learn about the user's music listening trends

## Project Structure


- `Dataset/dataset.csv`: This is the dataset used for the project. Here's a link to it's kaggle https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/data, Will be adding more altho
- `graphingtables/tables.py`: This generates a panda table with the audio features. Like the one showed in the dataframe.png.
- `meaning.md`: This explains every feature from dataframe.png .
- `photogrid/photogrid.py`: This script generates a 3x3 grid of album covers from the user's top tracks. The grid is saved as 'recentlyplayed.jpg'.
- `recommendation_model/recommend.py`: This script generates song recommendations based on the user's recently played tracks. (Not ready yet)

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Functions and snippets](#functions)



## Installation

To run this project, follow these steps:

1. Clone the repository:

`will paste link at last.`

2. Install the requird packages:

    `matplotlib` `spotipy` `pandas` `scikit-image`


3. Replace `client_id` and `client_secret` in `spotify_auth()` and .env file with your own Spotify API credentials. To obtain the credentials go to developer.spotify.com, login and create an app. 

## Usage

1. Run `photogrid/photogrid.py` to generate a grid of album covers from your top tracks.

2. Run recommendation_model/recommend.py to get song recommendations based on your recently played tracks.

3. Run 'graphingtables/tables.py' to get a table with a lot of information. (kinda useless for humans but wtv, I will try to make more cool representation.)

Apart from these these we can write custom codes to utilise functions in user_playlist_integration.py to obtain playlist data of users, generate plylist feature vector, recommend songs from a plyalist. 

We can also display the playlist album covers by using function written in visualising.py

Each of the functions in user_playlist_integration is explained belwo with sample usage and outputs. 

## Functions

### `spotify_data()`

Reads in the Spotify dataset from the specified location.

### `spotify_auth()`

Authenticates and returns a Spotify object (`sp`) using Spotipy and OAuth2.

### `create_album_outputs(album_name, id_dic, df, sp)`

Pulls songs from a specific album on Spotify and returns those available in the provided dataset.



- **Parameters:**
- `album_name` (str): Name of the album to pull songs from.
- `id_dic` (dict): Dictionary mapping album names to album IDs.
- `df` (pandas DataFrame): Spotify dataset.
- `sp`: Spotify object authenticated with `spotify_auth()`.

- **Returns:**
- `album` (pandas DataFrame): DataFrame containing songs from the specified album available in the provided dataset.

#### Note that albums and plylist are different from each other in spotify and the functions to get album and playlist cannot be used interchangeably.

### `create_playlist_outputs(playlist_name, id_dic, df, sp)`

Pulls songs from a specific playlist on Spotify and returns those available in the provided dataset.

- **Parameters:**
- `playlist_name` (str): Name of the playlist to pull songs from.
- `id_dic` (dict): Dictionary mapping playlist names to playlist IDs.
- `df` (pandas DataFrame): Spotify dataset.
- `sp`: Spotify object authenticated with `spotify_auth()`.

- **Returns:**
- `playlist` (pandas DataFrame): DataFrame containing songs from the specified playlist available in the provided dataset.

### `create_playlist_outputs_by_id(playlist_id, df, sp)`

Pulls songs from a specific playlist on Spotify using its ID and returns those available in the provided dataset.

- **Parameters:**
- `playlist_id` (str): ID of the playlist to pull songs from.
- `df` (pandas DataFrame): Spotify dataset.
- `sp`: Spotify object authenticated with `spotify_auth()`.

- **Returns:**
- `playlist` (pandas DataFrame): DataFrame containing songs from the specified playlist available in the provided dataset.

#### Playlist IDs can be obtained either by copying the last part of a playlist link as shown below, or by utilising the Spotipy Module. Below is a snippet to obtain a user's plalist and retrieve the ID's of each of them. 

```
from SpotipyK.recommendation_model.user_playlist_integration import spotify_data,spotify_auth,
#initialising spotify object
sp = spotify_auth()
user_playlists = sp.current_user_playlists()

for playlist in user_playlists['items']:
    print(playlist['name'],playlist['id'])

```

### `create_playlist_outputs_by_link(playlist_link, df, sp)`

Pulls songs from a specific playlist on Spotify using its link and returns those available in the provided dataset.

- **Parameters:**
- `playlist_link` (str): Spotify link of the playlist to pull songs from.
- `df` (pandas DataFrame): Spotify dataset.
- `sp`: Spotify object authenticated with `spotify_auth()`.

- **Returns:**
- `playlist` (pandas DataFrame): DataFrame containing songs from the specified playlist available in the provided dataset.

### Example 
```
from SpotipyK.recommendation_model.user_playlist_integration import spotify_data,spotify_auth,create_playlist_outputs_by_link
import pandas as pd

#importing dataset
df = spotify_data()

#initialising spotify object
sp = spotify_auth()

playlist_link= "https://open.spotify.com/playlist/6P1RtLZFVpGNY3xb9C4HJC?si=2b716aaf5c994275"

#getting playlist dataframe
playlist = create_playlist_outputs_by_link(playlist_link,df,sp)

#printing head of allbum
print(playlist.head())
```

### `generate_playlist_feature(complete_feature_set, playlist_df, weight_factor)`

Summarizes a user's playlist into a single vector and returns the summarized playlist and non playlist features.

- **Parameters:**
- `complete_feature_set` (pandas DataFrame): DataFrame including all features for Spotify songs.
- `playlist_df` (pandas DataFrame): DataFrame of songs in the playlist.
- `weight_factor` (float): Float value representing the recency bias (closer to 1 gives more priority to recent songs).

- **Returns:**
- `playlist_feature_set_weighted_final` (pandas Series): Summarized feature vector representing the playlist.
- `complete_feature_set_nonplaylist` (pandas DataFrame): DataFrame of songs that are not in the selected playlist.

#### To generate feture set after getting the playlist (you can continue the code from the playlist link example)

```

#preprocessing the dataset 
df['consolidates_genre_lists'] = df['track_genre'].apply(lambda x: x.split("|"))
df['popularity_red'] = pd.qcut(df['popularity'], q=5, labels=False)
float_cols = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
complete_set = create_feature_set(df, float_cols= float_cols)

complete_set.head()


#generate feature set of playlist and nonplaylist songs
playlist_weighted,non_playlist = generate_playlist_feature(complete_set,playlist_df,1.4)

print(playlist_weighted.head())
print(non_playlist.head())


```

### `generate_playlist_recommendations(df, features, nonplaylist_features, sp)`

Generates and returns top 10 recommendations for a playlist based on cosine similarity.

- **Parameters:**
- `df` (pandas DataFrame): Spotify dataset.
- `features` (pandas Series): Summarized playlist feature vector.
- `nonplaylist_features` (pandas DataFrame): Feature set of songs that are not in the selected playlist.
- `sp`: Spotify object authenticated with `spotify_auth()`.

- **Returns:**
- `non_playlist_df_top_10` (pandas DataFrame): DataFrame containing top 10 recommendations for the playlist.

#### To generate recommendations using the featureset obtained previously, 

```
recommendation_for_playlist = generate_playlist_recommendations(df,playlist_weighted, non_playlist,sp)
print(recommendation_for_playlist.head())

```
### We can also visualise the recommendations using the fucntion in visualising.py module. Below is the description of the function and example usage. 

### `visualize_songs_with_trackpre(df)`
Visualizes song cover art alongside track names from a given pandas DataFrame (`df`).

**Parameters:**
- `df` (pandas dataframe): DataFrame containing 'url' (cover art URLs) and 'track_name' (track names).

**Returns:**
- `plt` (matplotlib.pyplot object): Matplotlib figure object displaying the cover arts with track names.

```

#import function from SpotipyK.recommendation_model.visualizing
#use
visualize_songs_with_trackpre(recommendation_for_playlist).show()

```

