import pandas as pd


spotify_data = pd.read_csv('../Dataset/dataset.csv')
spotify_data.head()
print(spotify_data.head())

print(spotify_data.dtypes)

genretest =spotify_data['track_genre'].values[0]
print(genretest)
artisttest =spotify_data['artists'].values[0]
print(artisttest)

search = spotify_data[spotify_data['track_name'] == 'No Surprises']
print(search) # test succefully passed

# print(spotify_data.columns)