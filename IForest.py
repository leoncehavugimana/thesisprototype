# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:50:14 2019
@author: Leonce
"""
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import  sys
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
from utility import seqFunct, subSeqFunct
from sklearn.model_selection import RepeatedKFold
np.set_printoptions(precision=3, suppress=True)
np.set_printoptions(threshold=sys.maxsize)

iForest = IsolationForest(n_estimators=100, max_samples="auto", contamination="legacy",
                          bootstrap=False, behaviour='old', random_state=None)

# Compute average silhouette coefficient for a 3D array containing subsequences(Several days)
def silhouetteFunct (proper_3d) :
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


# Find silhouette coefficient for each fold, then computer average
daysChunks_Array = seqFunct('data/A', '5min')
length = 3
rkf = RepeatedKFold(n_splits=2, n_repeats=10)
silhouettesList = []
for train_index, test_index in rkf.split(daysChunks_Array):
    train_DaysChunks = np.take(daysChunks_Array, train_index, axis=0)
    proper_3d = subSeqFunct(train_DaysChunks, length)
    silhouettesList.append(silhouetteFunct(proper_3d))
averSilh = round((sum(silhouettesList) / len(silhouettesList)), 3)
print("Average silhouette coeff. for this house:", averSilh)
