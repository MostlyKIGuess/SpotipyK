import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import requests
from PIL import Image
import io

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='yourclientid',
                                                client_secret='yourclientsecret',
                                                redirect_uri='http://localhost:5089/',
                                                scope='user-top-read user-read-recently-played',
                                     show_dialog=True))

try:
    user_top_tracks = sp.current_user_top_tracks(limit=9, time_range='short_term')['items']
    user_recently_played = sp.current_user_recently_played(limit=9)['items']
    user_profile = sp.current_user()
    print(f"User: {user_profile['display_name']}")
except spotipy.SpotifyException as e:
    print(f"Error: {e}")
    sys.exit(1)


grid = Image.new('RGB', (900, 900))

x = 0
y = 0
for track in user_top_tracks:
    # track = item['track']
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()

    # Download the cover art
    response = requests.get(track['album']['images'][0]['url'])
    img = Image.open(io.BytesIO(response.content))

    # Resize the image and add it to the grid
    img = img.resize((300, 300))
    grid.paste(img, (x, y))
    # adding name of the song
    # text = track['name']
    # img.paste(text, (x, y))


    x += 300
    if x >= 900:
        x = 0
        y += 300


grid.save('recentlyplayed.jpg')


