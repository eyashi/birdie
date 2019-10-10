import numpy as np

# To make this easy on myself sklearn has a flipping param for this in the PCA module:
from sklearn.decomposition import PCA

pca = PCA(whiten=True)
whitened = pca.fit_transform(X)
# Seems too easy to be true...

# via : https://stackoverflow.com/questions/6574782/how-to-whiten-matrix-in-pca

# Segment these into windows, then PCA whiten.
# At first let's just whiten the whole thing?
def pca_whiten(section, eps=1):
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

	# make the mean of the dataset 0.
	X = section - section.mean(axis=0)

	# covariance matrix
	# In this case, time by frequency is being compared.
	# produces shape (431, 431)
	# goal of covariance matrix was to make a symmetric matrix
	# for the decomposition into eigenvalues TODO:LEARN MORE!
	# Dot product = covariance when mean = 0.
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
	W = np.dot(np.dot(V, D), V.T)

	# multiply by the whitening matrix
	X_white = np.dot(X, W)

	# plt.imshow(X_white)
	# plt.show()

	return X_white

# or using svd
def svd_whiten(X):

    U, s, Vt = np.linalg.svd(X, full_matrices=False)

    # U and Vt are the singular matrices, and s contains the singular values.
    # Since the rows of both U and Vt are orthonormal vectors, then U * Vt
    # will be white
    X_white = np.dot(U, Vt)

    return X_white
# comment said this method is slower but maybe more numerically stable?
# Possibly to do with the fudge value and the potential to divide by a very small number above.