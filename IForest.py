def warn(*args, **kwargs):
    pass
import warnings

warnings.warn = warn
import sys
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
from utility import buildSequences, buildSubSequences
from sklearn.model_selection import RepeatedKFold

np.set_printoptions(precision=3, suppress=True)
np.set_printoptions(threshold=sys.maxsize)

iForest = IsolationForest()

# Compute average silhouette coefficient for a 3D_array containing subsequences(Several days)
def computeSilhouette(proper_3d):
    subSeqPerDay = np.size(proper_3d, 1)
    subSeq = 0
    silhouetteList = []
    while subSeq < subSeqPerDay:
        X = proper_3d[:, subSeq, :]
        labels = iForest.fit_predict(X)
        silhouette = silhouette_score(X, labels, metric='euclidean')
        silhouetteList.append(silhouette)
        subSeq += 1
    return round((sum(silhouetteList) / len(silhouetteList)), 3)

# Find silhouette coefficient for each fold, then co  mputer average
daysChunks_Array = buildSequences('data/A', '5min')
length = 12
rkf = RepeatedKFold(n_splits=2, n_repeats=2)
silhouettesList = []
for train_index, test_index in rkf.split(daysChunks_Array):
    train_DaysChunks = np.take(daysChunks_Array, train_index, axis=0)
    proper_3d = buildSubSequences(train_DaysChunks, length)
    silhouettesList.append(computeSilhouette(proper_3d))
averSilh = round((sum(silhouettesList) / len(silhouettesList)), 3)
print("Average silhouette coeff. for this house _ iFOREST:", averSilh)
