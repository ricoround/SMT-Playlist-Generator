import json
from config import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API (Make sure the secrets.py is setup correctly)
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=secrets.SPOTIFY_CLIENT_ID, client_secret=secrets.SPOTIFY_CLIENT_SECRET
    )
)


def get_playlist_tracks(playlist_url):
    """
    Get all the song names from a given playlist

    :param playlist_url: Spotify playlist URL
    :return: List of song names
    """
    
    # # Get the playlist
    playlist = spotify.playlist(playlist_url)
    
    # Get the playlist name
    playlist_name = playlist["name"]
    # Get the playlist description
    playlist_description = playlist["description"]
    # Get the playlist owner
    playlist_owner = playlist["owner"]["display_name"]
    # Get the playlist tracks
    playlist_tracks = playlist["tracks"]["items"]
    # Get the playlist total tracks
    playlist_total_tracks = playlist["tracks"]["total"]

    # Print the playlist info
    print("Playlist name:", playlist_name)
    print("Playlist description:", playlist_description)
    print("Playlist owner:", playlist_owner)
    print("Playlist total tracks:", playlist_total_tracks)

    # List to store the song names
    song_titles = []

    # Loop through the playlist tracks
    for track in playlist_tracks:
        # Generate title
        title = ""
        for artist in track["track"]["artists"]:
            title += artist["name"] + ", "
        title = title[:-2] + " - " + track["track"]["name"]
        
        song_titles.append(title)

    # Return the list of song names
    return song_titles


def main():
    # Add the playlist URLs here
    playlists = [
        # "https://open.spotify.com/playlist/4P4sVCiU21HvonfXg9wvDs",
        # "https://open.spotify.com/playlist/3axoelQG1FrBeeq9MNTBP6",
        "https://open.spotify.com/playlist/4v7hIKEzzsEgIKrjrLghb9"
    ]
    
    # Get all the song titles from a given playlist, so that it can be used to 
    # search for the song for downloading
    song_titles = []
    for playlist in playlists:
        song_titles += get_playlist_tracks(playlist)
        print(song_titles)

    

if __name__ == "__main__":
    main()
