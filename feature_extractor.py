"""
Extracts features from the music files and stores them in a csv file
"""

import csv
import librosa
import os
import matplotlib.pyplot as plt
import numpy as np
import sqlite3


def beat_track(y, sr):
    """
    Returns the tempo (in beats per minute) and an array of frame numbers

    :param y: audio waveform
    :param sr: sampling rate
    :return: tempo, beats
    """

    # Using a default hop length of 512 samples @ 44100Hz ~= 11.6ms
    hop_length_normalised = 512 / 44100
    hop_length = int(hop_length_normalised * sr)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    return tempo, beats


def scale_key(y, sr):
    """
    Returns the key and minor / major scale of a song

    :param y: audio waveform
    :param sr: sampling rate
    :return: scale
    """
    # Compute chromagram
    chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)

    # Summing up the energy in each chroma bin to get the overall energy for each pitch class
    chroma_energy = np.mean(chromagram, axis=1)

    # Find the key (index of the maximum energy)
    estimated_key = np.argmax(chroma_energy)

    # Define key names
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Determine major or minor
    # Major keys start at index 0 in the key_names list, minor keys start at index 9
    if estimated_key < 9:
        scale = "Major"
        key = key_names[estimated_key]
    else:
        scale = "Minor"
        key = key_names[estimated_key - 9]

    return scale, key


def load_audio(filename):
    """
    Loads the audio file and returns the audio waveform and sampling rate

    :param filename: path to the audio file
    :return: audio waveform, sampling rate
    """

    y, sr = librosa.load(filename)
    return y, sr


def plot_beats(beats, onset_env, y, sr):
    # print(len(y), len(beats), len(onset_env))
    # y = y[:4000]

    hop_length = 512
    fig, ax = plt.subplots(nrows=2, sharex=True)
    times = librosa.times_like(onset_env, sr=sr, hop_length=hop_length)
    M = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length)
    librosa.display.specshow(
        librosa.power_to_db(M, ref=np.max),
        y_axis="mel",
        x_axis="time",
        hop_length=hop_length,
        ax=ax[0],
    )
    ax[0].label_outer()
    ax[0].set(title="Mel spectrogram")
    ax[1].plot(times, librosa.util.normalize(onset_env), label="Onset strength")
    ax[1].vlines(
        times[beats], 0, 1, alpha=0.5, color="r", linestyle="--", label="Beats"
    )
    ax[1].legend()
    fig.savefig("beats.png")
    plt.show()


def connect_to_db():
    """
    Connects to the database and returns the connection and cursor objects

    :return: connection, cursor
    """
    conn = sqlite3.connect("music.sqlite")
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS songs (song_name TEXT PRIMARY KEY, tempo REAL, scale STRING, key SCALE)"""
    )
    conn.commit()
    return conn, cursor


def main():
    folder_path = "audio_files"
    filenames = os.listdir(folder_path)

    # Connect to the database
    conn, cursor = connect_to_db()

    # Define the CSV file name
    out = "output.csv"

    # Check if the file exists to decide on writing the header
    file_exists = os.path.isfile(out)

    for songname in filenames:
        print("Processing song:", songname)

        cursor.execute("SELECT * FROM songs WHERE song_name=?", (songname,))
        if cursor.fetchone():
            print("Song already exists in database, continuing...")
            continue

        y, sr = load_audio(os.path.join(folder_path, songname))
        tempo, _ = beat_track(y, sr)
        scale, key = scale_key(y, sr)

        # Insert song and tempo into the database
        cursor.execute(
            "INSERT INTO songs (song_name, tempo, scale, key) VALUES (?, ?, ?, ?)", (songname, tempo, scale, key)
        )
        conn.commit()

        # After the first write, the file exists, so we don't write the header again
        file_exists = True

    # Close database connection
    conn.close()
    return


if __name__ == "__main__":
    main()
