"""
Extracts features from the music files and stores them in a csv file
"""

import librosa








def beat_track(y, sr):
    """
    Returns the tempo (in beats per minute) and an array of frame numbers

    :param y: audio waveform
    :param sr: sampling rate
    :return: tempo, beats
    """

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    return tempo, beats


def load_audio(filename):
    """
    Loads the audio file and returns the audio waveform and sampling rate

    :param filename: path to the audio file
    :return: audio waveform, sampling rate
    """

    y, sr = librosa.load(filename)
    return y, sr


def main():
    
    filename = librosa.example('nutcracker')
    y, sr = load_audio(filename)
    tempo, beats = beat_track(y, sr)
    
    print(tempo)
    print(beats)
    print(y)
    
    
    
    
    
    

if __name__ == "__main__":
    main()