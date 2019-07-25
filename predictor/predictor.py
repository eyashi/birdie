'''
The class that runs the new clips by the model to determine if there is a bird sound or not.
'''
import os
import numpy as np

import lrn.get_features as gf
from keras.models import load_model

model_dir = os.path.join("lrn", "models")

class Predictor():
	def __init__(self):
		self.model = load_model(os.path.join(model_dir, "final.h5"))
		self.results = []

	def predict(self, new_clip):
		'''
		Takes in the new clip, extracts features, and makes a prediction.
		'''
		sound_arr, sample_rate = gf.load_audio(new_clip)