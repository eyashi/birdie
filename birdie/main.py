from features.grill_schluter import Features
from utils import audio

f = Features()

f.process_from_path("test.mp3")

audio.plot_spectrogram(f.msg)
