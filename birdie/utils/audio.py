import os

import librosa
import librosa.display
import numpy as np

import matplotlib.pyplot as plt


def load_audio(audio_file_path):
    """
    Opens an audio file using librosa.load or numpy.load if already in the
    format of a numpy array.

    Takes in the path to the audio file.
    Returns the sound array and the sample rate.
    """
    file_base, file_extension = os.path.splitext(audio_file_path)

    if file_extension == ".wav" or file_extension == ".mp3":
        return librosa.load(audio_file_path)

    elif file_extension == ".npy":
        sound_arr = np.load(audio_file_path)
        sample_rate = 44100

        return sound_arr, sample_rate

    return None, None


def plot_spectrogram(msg):
    # Pass in a spectrogram, get to view the spectrogram

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(
        librosa.power_to_db(msg, ref=np.max),
        y_axis="mel",
        fmax=8000,
        x_axis="time",
    )

    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel spectrogram")
    plt.tight_layout()
    plt.show()
