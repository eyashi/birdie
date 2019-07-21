import os
import librosa
from librosa import display
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

import utils

DATA_DRIVE = "E:\\"  # usb that the data is on
SAMPLE_RATE = 22050


def load_audio(audio_file_path):
    file_base, file_extension = os.path.splitext(audio_file_path)

    if file_extension == ".wav" or file_extension == ".mp3":
        return librosa.load(audio_file_path)

    elif file_extension == ".npy":
        sound_arr = np.load(audio_file_path)
        sample_rate = SAMPLE_RATE

        return sound_arr, sample_rate

    return None, None


def show_numpy_graph(data):
    plt.imshow(msg, interpolation="nearest")
    plt.show()


def export_spectrogram_image(msg, sample_file_path):
    plt.figure(figsize=(10, 4))
    display.specshow(
        librosa.power_to_db(msg, ref=np.max), y_axis="mel", fmax=8000, x_axis="time"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()
    plt.savefig(
        os.path.join("output", os.path.splitext(os.path.basename(sample_file_path))[0])
    )
    plt.close()


def extract_features(audio_file_path):
    # load in the sample
    audio_raw, sample_rate = load_audio(audio_file_path)

    # compute the mel spectrogram
    msg = librosa.feature.melspectrogram(
        y=audio_raw, sr=SAMPLE_RATE, n_fft=2048, hop_length=1024, window="hann"
    )

    return msg


def output_mel(trial_size, overwrite=False):
    if overwrite:
        os.rmdir("mel")
        os.mkdir("mel")

    with open(
        os.path.join("samples", "{}-selected-samples.txt".format(trial_size)), "r"
    ) as f:
        sample_paths = list(filter(None, f.read().split("\n")))

    for sample in tqdm(sample_paths):
        mel_path = os.path.join("mel", os.path.splitext(os.path.basename(sample))[0])
        if os.path.exists(mel_path) and not overwrite:
            return
        else:
            msg = extract_features(sample)
            np.save(mel_path, msg)


def run(trial_size=100, generate_new_subset=False, overwrite_mel=False):
    """
		Main task runner for this script.
		Select a trial size to randomly assemble a list of files to perform analysis on.
		Set trialSize to 'all' to run on entire dataset.
		Set generateNewSubset to 'True' if you've ran the same trial size before and want new samples.
	"""
    if trial_size is "all":
        pass
    else:
        utils.generate_subset_of_data(
            DATA_DRIVE, num_samples=trial_size, generate_new_subset=generate_new_subset
        )
        output_mel(trial_size, overwrite=overwrite_mel)


if __name__ == "__main__":
    run(1000, generate_new_subset=False, overwrite_mel=True)
