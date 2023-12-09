import json
from config import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=secrets.SPOTIPY_CLIENT_ID, client_secret=secrets.SPOTIPY_CLIENT_SECRET))

# link = "https://open.spotify.com/track/1D5XNEpnMbP4XCqScrfCPs?si=cfcb48cde8154e45"
link = "https://open.spotify.com/track/7kE5SGVpogBX5VXiTgYiRg?si=fa236b15e7a24e1d"


results = spotify.audio_features(link)
data = json.dumps(results)
print(data)