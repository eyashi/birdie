# for any repeatedly used utility functions

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

def check_data_drive(drive_name):
    # validates that the drive is present, returns the drive name if it is.
    if drive_name in [i.device for i in psutil.disk_partitions()]:
        return drive_name
    else:
        return False

def generate_subset_of_data(
    num_samples=10,
    output_path="samples",
    generate_new_subset=False,
    sample_dir
):
    '''
    Generates a text file with a file path to a sample on each line.
    Expects the sample directory provided to have individual datasets
    in folders within it, with the audio clips inside one more directory
    labeled with their file type. eg: D:/Birds/ff1010/wav/*.wav.
    
    The sample_dir parameter would then be D:/Birds/ for the above.
    '''

    if os.path.isfile(
        os.path.join(output_path, "{}-selected-samples.txt".format(num_samples))
    ):
        if not generate_new_subset:
            return

    sample_pool = []
    collected_samples = []

    # make the sample pool of all available audio files
    for fold in os.listdir(sample_dir):
        d1 = os.path.join(sample_dir, fold)
        try:
            if os.path.isdir(d1):
                for f in os.listdir(d1):
                    d2 = os.path.join(d1, f)
                    if os.path.isdir(d2):
                        sample_pool += [os.path.join(d2, i) for i in os.listdir(d2)]
        except:
            pass

    if num_samples == "all":
        with open(
            os.path.join(output_path, "{}-selected-samples.txt".format(num_samples)),
            "w",
        ) as f:
            for i in sample_pool:
                f.write(i + "\n")
    else:
        while len(collected_samples) < num_samples:
            idx = random.randint(0, len(sample_pool) - 1)
            collected_samples.append(sample_pool[idx])

        with open(
            os.path.join(output_path, "{}-selected-samples.txt".format(num_samples)),
            "w",
        ) as f:
            for i in collected_samples:
                f.write(i + "\n")

