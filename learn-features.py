# Implementation of Stowell Plumbley 2014 Unsupervised feature learning.

import os
import concurrent
import librosa
from librosa import display
import matplotlib.pyplot as plt

import numpy as np
from tqdm import tqdm

import utils

test_path = os.path.join('recordings', '19037.wav')

# Open audio file, currently shape (220500,)
audio, sr = utils.load_audio(test_path)

# Convert to mel-spectrogram (time-frequency representation)
# Varying these window sizes may be helpful in domain training for different noise environments.
msg = librosa.feature.melspectrogram(
	y=audio, sr=sr, n_fft=1024, hop_length=512, window='hann'
)

# Segment these into windows, then PCA whiten.
# At first let's just whiten the whole thing?
def pca_whiten(section, eps=1e-15):
	'''
	Whitening for windowed sections of the spectrogram.
	eps value chosen arbitrarily to keep numbers from getting
	too high. See snippets/pca-whitening.py for details

	I've had to increase the fudge value all the way to 1
	There were negative values in the covariance matrix. Look up best ways to handle this.
	Some random dudes here told me to add a positive number to offset:
	https://www.researchgate.net/post/How_to_deal_with_negative_eigenvalue_during_whitening_matrix_computation_in_CSP

	What happens if I set all negative numbers to zero?
	Not really much in light of me adding an enormous value of 1 back to the matrix. Makes it easy to
	visualize but it might not be important for me really, if the program can tell the difference.
	Small values do seem to totally mess up real isolation though... not great.
	'''
	X = section

	# covariance matrix
	# In this case, time by frequency is being compared.
	# produces shape (431, 431)
	# goal of covariance matrix was to make a symmetric matrix
	# for the decomposition into eigenvalues TODO:LEARN MORE!
	Xcov = np.dot(X.T, X)

	# eigenvalue decomposition of the matrix
	# d is an array of values, V is a np.array shape (431, 431)
	d, V = np.linalg.eigh(Xcov)

	# calculate diagonals? this is the whitening step
	# divide by square root. re-read this section
	# image is now a beautiful line that fades...
	# can't show the spectrogram of this array
	D = np.diag(1.0 / np.sqrt(d.clip(0) + eps))

	# whitening matrix
	# quite literally has plotted a completely blank thing.
	# is this broken.
	W = np.dot(np.dot(V, D), V.T)

	# multiply by the whitening matrix
	X_white = np.dot(X, W)

	print(X_white)
	# plt.imshow(X_white, interpolation='nearest')
	# plt.show()
	show_spectrogram(X_white)

def show_spectrogram(msg):
	plt.figure(figsize=(10,4))
	librosa.display.specshow(librosa.power_to_db(
		msg,
		ref=np.max
	),
	y_axis='mel', fmax=8000,
	x_axis='time'
	)
	plt.colorbar(format='%+2.0f dB')
	plt.title('Mel spectrogram')
	plt.tight_layout()
	plt.show()

def show_waveform(audio, sr):
	plt.figure()
	plt.subplot(3, 1, 1)
	display.waveplot(audio, sr=sr)
	plt.show()

if __name__ == '__main__':
	pca_whiten(msg)