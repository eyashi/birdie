# records audio then plots to spectrogram for proof of concept.

import os
import datetime

import numpy as np
import matplotlib.pyplot as plt

import librosa
from librosa import display

import sounddevice as sd

SAMPLE_RATE = 22050


def record(duration, fs=22050, write_out=None):
    raw_rec = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    # remove an extra axis that comes with the reording so that librosa likes it
    recording = np.squeeze(raw_rec)

    if write_out:
        if write_out == "numpy":
            np.save(
                os.path.join(
                    "output", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                ),
                recording,
            )

        elif write_out == "wav":
            librosa.output.write_wav(
                os.path.join(
                    "output", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S.wav")
                ),
                recording,
                fs,
            )

    return recording


def plot_spect(y):
    S = librosa.feature.melspectrogram(y=y, sr=SAMPLE_RATE)

    plt.figure(figsize=(10, 4))
    display.specshow(
        librosa.power_to_db(S, ref=np.max), y_axis="mel", fmax=8000, x_axis="time"
    )

    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel spectrogram")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # cool, it works.
    recording = record(10, fs=SAMPLE_RATE, write_out="wav")
    plot_spect(recording)
