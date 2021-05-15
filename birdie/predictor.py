"""
The class that runs the new clips by the model to determine if there is a bird sound or not.
"""
import os
import numpy as np

import learn.get_features as gf
from keras.models import load_model

model_dir = os.path.join("learn", "models")


class Predictor:
    def __init__(self):
        self.model = load_model(os.path.join(model_dir, "final.h5"))
        self.results = []

    def predict(self, new_clip, save_features):
        """
        Takes in the new clip, extracts features, and makes a prediction.
        """
        features = gf.extract_features(new_clip, save_features)
        y_pred = self.model.predict_classes(X)

        return new_clip, y_pred[0]

    def predict_dir(self, clip_dir, save_features):
        results = []
        for f in os.listdir(clip_dir):
            clip_name, pred = self.predict(f, save_features)
            results.append([clip_name, pred])

        return results
