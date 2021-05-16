# Implementation of Stowell Plumbley 2014 Unsupervised feature learning.

import os
import concurrent
import librosa
from librosa import display
import matplotlib.pyplot as plt

import numpy as np
from tqdm import tqdm

from sklearn.decomposition import PCA

import utils

test_path = os.path.join("recordings", "107607.wav")

# Open audio file, currently shape (220500,)
audio, sr = utils.load_audio(test_path)

# Convert to mel-spectrogram (time-frequency representation)
# Varying these window sizes may be helpful in domain training for different noise environments.
# Specify number of filter bins N=40 as in Stowell Plumbley
msg = librosa.feature.melspectrogram(
    y=audio, sr=sr, n_fft=1024, hop_length=512, n_mels=40
)

# Normalize the spectrogram
_min = msg.min()
_max = msg.max()
msg_norm = (msg - _min) / (_max - _min)

# PCA Whiten...
pca = PCA(n_components=msg_norm.shape[0], whiten=True)
msg_white = pca.fit_transform(msg_norm)
plt.imshow(msg_white)
plt.show()
print(msg_white.shape)

# Via Dieleman and Schrauwen:

# Divide into large pooling windows
# num_windows = 5 # cooresponding to 2 seconds of 10 second audio clip
# pooling_window_len = [int(msg.shape[0]/num_windows)]*num_windows
# pooling_window_len[-1] += msg.shape[0] % num_windows # add remainder to the last pooling window

# pooling_windows = []
# idx = 0

# for w in pooling_window_len:
# 	pooling_windows.append(msg[:, idx:idx+w])
# 	idx += w

# Divide into smaller consecutive frames and PCA whiten

# pca_windows = []

# for pw in pooling_windows:
# 	f_pca = PCA(n_components=1, whiten=True)
# 	pca_windows.append(f_pca.fit_transform(pw))

# img = np.concatenate(pca_windows, axis=1)

# print(img.shape)
# plt.imshow(pca_windows)
# plt.show()

# Then apply K-Means within pooling windows

# Pool by taking maximum across time TODO: Figure out what that means exactly.

# seg_size = 4
# seg = msg[:,0:seg_size]


def show_spectrogram(msg):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(
        librosa.power_to_db(msg, ref=np.max), y_axis="mel", fmax=8000, x_axis="time"
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel spectrogram")
    plt.tight_layout()
    plt.show()


def show_waveform(audio, sr):
    plt.figure()
    plt.subplot(3, 1, 1)
    display.waveplot(audio, sr=sr)
    plt.show()


# if __name__ == '__main__':
# f = pca_whiten(msg)
# pca_prewhite = PCA(n_components=64)
# pca_prewhite.fit(f)
# print(pca_prewhite.explained_variance_ratio_)
# pca = PCA(n_components=8, whiten=False)
# X_new = pca.fit_transform(msg)
# print(np.sum(pca.explained_variance_ratio_))
# print(X_new.shape)
# show_spectrogram(X_new)
# plt.imshow(X_new)
# plt.show()
