# just some example code to generate a spectrogram out of an mp3 file
# that's pretty neat.

# You do need ffmpeg installed on your computer and on the path for this to work (for the mp3)

import os

import numpy as np
import matplotlib.pyplot as plt

import librosa
from librosa import display

sample_path = os.path.join('samples', os.listdir('samples')[0])

y, sr = librosa.load(sample_path)
print(np.shape(y))
print(y)
S = librosa.feature.melspectrogram(y=y, sr=sr)

plt.figure(figsize=(10,4))
display.specshow(
    librosa.power_to_db(
        S, ref=np.max),
        y_axis='mel', fmax=8000,
        x_axis='time')

plt.colorbar(format='%+2.0f dB')
plt.title('Mel spectrogram')
plt.tight_layout()
plt.show()