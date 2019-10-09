import numpy as np

# To make this easy on myself sklearn has a flipping param for this in the PCA module:
from sklearn.decomposition import PCA

pca = PCA(whiten=True)
whitened = pca.fit_transform(X)
# Seems too easy to be true...

# via : https://stackoverflow.com/questions/6574782/how-to-whiten-matrix-in-pca

def whiten(X,fudge=1E-18):

   # the matrix X should be observations-by-components
   # TODO: Understand what is meant by this input structure...

   # get the covariance matrix
   Xcov = np.dot(X.T,X)

   # eigenvalue decomposition of the covariance matrix
   d, V = np.linalg.eigh(Xcov)

   # a fudge factor can be used so that eigenvectors associated with
   # small eigenvalues do not get overamplified.
   D = np.diag(1. / np.sqrt(d+fudge))

   # whitening matrix
   W = np.dot(np.dot(V, D), V.T)

   # multiply by the whitening matrix
   X_white = np.dot(X, W)

   return X_white, W

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