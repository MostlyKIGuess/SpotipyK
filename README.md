# Spotify Music Analysis Project

This project uses the Spotify API to analyze a user's music listening habits.

## Project Structure

- `auth_model/`: ~~
- `Dataset/dataset.csv`: This is the dataset used for the project. Will be adding more
- `graphingtables/tables.py`: This generates a panda table with the audio features. Like the one showed in the dataframe.png.
- `meaning.md`: This explains every factor from dataframe.png .
- `photogrid/photogrid.py`: This script generates a 3x3 grid of album covers from the user's top tracks. The grid is saved as 'recentlyplayed.jpg'.
- `recommendation_model/recommend.py`: This script generates song recommendations based on the user's recently played tracks. (Not ready yet)
- `testingout/`: This directory contains scripts for testing out various features. (Not available in github, do  not access)

## Setup

1. Clone the repository.
2. Install the required Python packages: `spotipy`, `requests`, `PIL`.
3. Wherever you see clientid,clientsecret, you can add yours, for this you can go to Spotify's Developers portal and create an app to get your id and secret and you will be able to use the features.

## Usage

1. Run `photogrid/photogrid.py` to generate a grid of album covers from your top tracks.
2. Run `recommendation_model/recommend.py` to get song recommendations based on your recently played tracks. ( still in progrss)
3. Run 'graphingtables/tables.py' to get a table with a lot of information. (kinda useless for humans but wtv, I will try to make more cool representation.)

## Note

This project is still under development. More features will be added in the future.