import spotify_functions as spfunc
import spotipy
import pandas as pd
import argparse
import json
import db
import numpy as np
import logging
from datetime import datetime

# Setup spotify API
spotify = spfunc.get_spotify_client()

# Create a log filename with the current date
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f'logs/log_{current_date}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, required=False, default=np.inf)
    parser.add_argument("--offset", type=int, required=False, default=0)
    parser.add_argument("--query", type=str, required=False, default="running")
    parser.add_argument("--limit", type=int, required=False, default=50)
    # output_path = parser.add_argument("--output", type=str, required=True)

    args = parser.parse_args()
    max_songs = args.max
    offset = args.offset
    query = args.query
    limit = args.limit

    # Connect to database
    conn, cursor = db.connect_to_db_songid()
    
    current = 0
    logging.info(f"----------------------------------\nStarting script with parameters: max_songs={max_songs}, offset={offset}, limit={limit}\n----------------------------------")
    
    while current < max_songs or offset >= 1000:
        print(
            f"Parameters: \noffset={offset}\ncurrent={current}"
        )
        logging.info(f"Parameters: offset={offset}, current={current}")

        search = spotify.search(
            q=query, limit=limit, type="playlist", market="NL", offset=offset
        )

        # First create a list of all playlist ids
        playlists = []
        for playlist in search["playlists"]["items"]:
            # print(f"Getting tracks from playlist: {playlist['name']}")
            playlists.append(playlist["id"])

        # Cycle through all playlists and get all track_ids
        for pid in playlists:
            playlist = spotify.playlist(
                pid, fields="tracks.total,tracks.items(track(id,artists,name))"
            )
            
            print(f'-------------------------\nAdding playlist: {pid, playlist["tracks"]["total"]}')

            for track in playlist["tracks"]["items"]:
                try:
                    id = track["track"]["id"]

                    # Add title to database as well just for visual convenience
                    name = track["track"]["name"]
                    artists = ""
                    for artist in track["track"]["artists"]:
                        artists += artist["name"] + ", "
                    artists = artists[:-2]
                    title = artists + " - " + name

                    # Check if the song is already in the database
                    cursor.execute("SELECT * FROM songid WHERE id = ?", (id,))
                    if cursor.fetchone() is None:
                        cursor.execute(
                            "INSERT INTO songid (id, title) VALUES (?, ?)", (id, title)
                        )
                        conn.commit()

                        current += 1
                        if current >= max_songs:
                            break
                    # else:
                    #     print(f"Record already exists: {id, title}")

                except Exception as e:
                    print(f"ERROR: {e}")
                    logging.error(e)
                    continue
                
            logging.info(f"Finished adding playlist: {pid, playlist['tracks']['total']}")
        offset += limit
    
    logging.info(f"Finished adding {current} songs to the database")

    # Close the database connection
    cursor.close()
