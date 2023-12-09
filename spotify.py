import json
from config import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# link = "https://open.spotify.com/track/1D5XNEpnMbP4XCqScrfCPs?si=cfcb48cde8154e45"
# link = "https://open.spotify.com/track/7kE5SGVpogBX5VXiTgYiRg?si=fa236b15e7a24e1d"


# results = spotify.audio_features(link)
# data = json.dumps(results)
# print(data)



def main():
    # Set up Spotify API (Make sure the secrets.py is setup correctly)
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=secrets.SPOTIFY_CLIENT_ID, client_secret=secrets.SPOTIFY_CLIENT_SECRET))



      


if __name__ == "__main__":
    main()
    print(spotify)



