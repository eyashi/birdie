from tqdm import tqdm

from sklearn.decomposition import PCA

import librosa

from utils.audio import load_audio


class Features:
    def __init__(self, settings=None):
        if not settings:
            settings = {"n_fft": 1024, "hop_length": 512, "n_mels": 80}

        self.n_fft = settings["n_fft"]
        self.hop_length = settings["hop_length"]
        self.n_mels = settings["n_mels"]

        self.msg = None

    def process_from_path(self, path):
        self.process(*load_audio(path))

    def process(self, audio, sample_rate):
        self.msg = librosa.feature.melspectrogram(
            y=audio,
            sr=sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels,
        )

        # Normalize the spectrogram
        _min = self.msg.min()
        _max = self.msg.max()
        msg_norm = (self.msg - _min) / (_max - _min)
