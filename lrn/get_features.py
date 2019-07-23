import os
import shutil
import concurrent
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


def load_desc_dict(desc_file):
    # parses a csv file with id of sample and the label
    with open(desc_file, "r") as d_labels:
        lines = d_labels.read().split("\n")
        items = [i.split(",") for i in lines]
        desc_dict = {i[0]: i[1] for i in items if len(i) == 2}

    return desc_dict


def build_all_label_dict(label_dir):
    all_label_dict = {}
    for root, dirs, files in os.walk(label_dir):
        for f in files:
            name, ext = os.path.splitext(f)
            if ext == ".csv":
                d = load_desc_dict(os.path.join(root, f))
                all_label_dict.update(d)

    return all_label_dict


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

    mel_path = os.path.join(
        "mel", os.path.splitext(os.path.basename(audio_file_path))[0]
    )
    np.save(mel_path, msg)


def output_mel(trial_size, overwrite=False):
    if overwrite:
        shutil.rmtree("mel")
        os.mkdir("mel")
    else:
        return

    with open(
        os.path.join("samples", "{}-selected-samples.txt".format(trial_size)), "r"
    ) as f:
        sample_paths = list(filter(None, f.read().split("\n")))

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_msg = {
            executor.submit(extract_features, sample): sample for sample in sample_paths
        }
        print("Extracting features!")
        for future in tqdm(
            concurrent.futures.as_completed(future_to_msg), total=len(sample_paths)
        ):
            msg = future_to_msg[future]
            try:
                data = future.result()
            except Exception as exc:
                print("%r generated an exception: %s" % (msg, exc))
            else:
                pass

    # for sample in tqdm(sample_paths):
    #     mel_path = os.path.join("mel", os.path.splitext(os.path.basename(sample))[0])
    #     if os.path.exists(mel_path) and not overwrite:
    #         return
    #     else:
    #         msg = extract_features(sample)
    #         np.save(mel_path, msg)


def label_mel(mel_dir, label_dir):
    X, y = [], []

    labels = build_all_label_dict(label_dir)
    print("Labeling mel data")
    for f in tqdm(os.listdir(mel_dir)):
        fp = os.path.join(mel_dir, f)
        arr = np.load(fp)
        X.append(np.resize(arr, (128, 216)))
        key = os.path.splitext(f)[0]
        y.append(labels[key])

    X, y = np.array(X), np.array(y)
    # normalize the values of X
    _min = X.min()
    _max = X.max()
    X = (X - _min) / (_max - _min)

    return X, y


def run(trial_size=100, generate_new_subset=False, overwrite_mel=False):
    """
		Main task runner for this script.
		Select a trial size to randomly assemble a list of files to perform analysis on.
		Set trialSize to 'all' to run on entire dataset.
		Set generateNewSubset to 'True' if you've ran the same trial size before and want new samples.
	"""
    utils.generate_subset_of_data(
        DATA_DRIVE, num_samples=trial_size, generate_new_subset=generate_new_subset
    )
    output_mel(trial_size, overwrite=overwrite_mel)
    X, y = label_mel("mel", "eval")

    return X, y


if __name__ == "__main__":
    X, y = run("all", generate_new_subset=False, overwrite_mel=True)

