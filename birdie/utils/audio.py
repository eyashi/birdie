import os
import csv

import pathlib
import psutil
import random

import librosa
import numpy as np

def load_audio(audio_file_path):
    '''
    Opens an audio file using librosa.load or numpy.load if already in the
    format of a numpy array.

    Takes in the path to the audio file.
    Returns the sound array and the sample rate.
    '''
    file_base, file_extension = os.path.splitext(audio_file_path)

    if file_extension == ".wav" or file_extension == ".mp3":
        return librosa.load(audio_file_path)

    elif file_extension == ".npy":
        sound_arr = np.load(audio_file_path)
        sample_rate = SAMPLE_RATE

        return sound_arr, sample_rate

    return None, None