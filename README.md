# SMT-Playlist-Generator

## Quick links
- [Feature Extraction](#feature-extraction)
- [Playlist Generator](#playlist-generator)
- [Installation](#installation)

## Feature Extraction
The script [`feature_extractor.py`](feature_extractor.py) extracts the features from the audio files and stores them in a csv file. The features are extracted using the [librosa](https://librosa.org/doc/0.10.1/index.html) library (version 0.10.1).

## Spotify Extraction
The script [`spotify.py`](spotify.py) contains the functions to interact with the Spotify API. See the [Spotify API](#spotify-api) section for more information about setting up the Spotify API.

## Playlist Generator
This is a music playlist generator application with the main purpose to generate running playlists.

In short, how it works:
- WIP

## Installation
(This project uses Python 3.8.10)

Best way to install the required packages is to use a virtual environment.

### Install packages

Install the required packages using the following command:
```
pip install -r config/requirements.txt
```

### Database
The feature extractor creates a database with the features of the songs. To quickly check the contents of the database I would recommend using [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer) in VS Code.



### Spotify API
To use the Spotify API, you need to create a Spotify developer account and create an application. You can find more information [here](https://developer.spotify.com/documentation/general/guides/app-settings/).

After creating the application, you need to create a file called [`secrets.py`](config/secrets.py) in the [`config`](config) folder. This file will contain the client id and client secret of your Spotify application. You can find these in the Spotify developer dashboard. Make sure that this file is in the `.gitignore` file, because you don't want to share these secrets.



