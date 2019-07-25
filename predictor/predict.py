import os
import numpy as np
from tqdm import tqdm
from keras.models import load_model

model_dir = "models"

model = load_model(os.path.join(model_dir, "final.h5"))

results = []

for f in tqdm(os.listdir("mel-self-record\\mel")):
	X_new = []
	fp = os.path.join("mel-self-record\\mel", f)
	arr = np.load(fp)
	X_new.append(np.resize(arr, (128, 216)))

	X = np.array(X_new)
	_min = X.min()
	_max = X.max()
	X = (X - _min) / (_max - _min)
	X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))
	y_pred = model.predict_classes(X)

	results.append([f, y_pred])

with open('prediction_results.csv', 'w') as f_out:
	f_out.write('file,prediction')
	for r in results:
		f_out.write('%s, %s\n' % (r[0], str(r[1])))