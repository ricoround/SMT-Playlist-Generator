import json
from config import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Set up Spotify API (Make sure the secrets.py is setup correctly)
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=secrets.SPOTIFY_CLIENT_ID, client_secret=secrets.SPOTIFY_CLIENT_SECRET
    )
)


def get_track_features(track):
    """
    Small helper function to get track features from the Spotify API.

    :param track: Spotify track
    :return: Track features
    """
    track_info = spotify.audio_features(track)
    return track_info[0] if track_info else None


def get_playlist_tracks(playlist_url):
    """
    Get all the song names from a given playlist

    :param playlist_url: Spotify playlist URL
    :return: List of song names
    """
    
    # Get the playlist
    playlist = spotify.playlist(playlist_url)
    
    # Obtain some playlist information
    playlist_name = playlist["name"]
    playlist_description = playlist["description"]
    playlist_owner = playlist["owner"]["display_name"]
    playlist_tracks = playlist["tracks"]["items"]
    playlist_total_tracks = playlist["tracks"]["total"]

    # Print the playlist info
    print("Playlist name:", playlist_name)
    print("Playlist description:", playlist_description)
    print("Playlist owner:", playlist_owner)
    print("Playlist total tracks:", playlist_total_tracks)

    # Loop through the playlist tracks
    song_features = []
    for track in playlist_tracks:
        # Generate title
        title = ""
        for artist in track["track"]["artists"]:
            title += artist["name"] + ", "
        title = title[:-2] + " - " + track["track"]["name"]
        
        # Get and store all track features
        features = get_track_features(track["track"]["id"])
        features["title"] = title
        features["playlist_name"] = playlist_name
        features["playlist_desc"] = playlist_description
        features["playlist_owner"] = playlist_owner
        features["playlist_total_tracks"] = playlist_total_tracks
        song_features.append(features)

    # Collapse to a single dataframe
    df_song_features = pd.DataFrame(song_features)

    # Return the list of song names
    return df_song_features


def main():
    # Add the playlist URLs here
    playlists = [
        #"https://open.spotify.com/playlist/4P4sVCiU21HvonfXg9wvDs",
        #"https://open.spotify.com/playlist/3axoelQG1FrBeeq9MNTBP6",
        "https://open.spotify.com/playlist/4v7hIKEzzsEgIKrjrLghb9"
    ]
    
    # Get all the song features for given playlists
    dfs = []
    for playlist in playlists:
        dfs.append(get_playlist_tracks(playlist))
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv("analysis/data/spotify_data.csv", index=False)
    

if __name__ == "__main__":
    main()
