def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import silhouette_score
from utility import buildSequences, buildSubSequences
from sklearn.model_selection import RepeatedKFold

np.get_printoptions()
np.set_printoptions(precision=3, suppress=True)

localOutlierFactor = LocalOutlierFactor(n_neighbors=20,algorithm='auto',metric='euclidean',novelty=False)

'''
Compute average silhouette coefficient for a 3D array of subsequences
'''
def computeSilhouette(proper_3d):
    subSeqPerDay = np.size(proper_3d, 1)
    subSeq = 0
    silhouetteList = []
    while subSeq < subSeqPerDay:
        x = proper_3d[:, subSeq, :]
        labels = localOutlierFactor.fit_predict(x)
        silhouette = silhouette_score(x, labels, metric='euclidean')
        silhouetteList.append(silhouette)
        subSeq += 1
        break
    return round((sum(silhouetteList) / len(silhouetteList)), 3)

''' 
Find silhouette coefficient for each fold, then computer average
'''
daysChunks_Array = buildSequences('data/A', '5min')
length = 12
rkf = RepeatedKFold(n_splits=2, n_repeats=10)
silhouettesList = []
for train_index, test_index in rkf.split(daysChunks_Array):
    train_DaysChunks = np.take(daysChunks_Array, train_index, axis=0)
    proper_3d = buildSubSequences(train_DaysChunks, length)
    silhouettesList.append(computeSilhouette(proper_3d))
averSilh = round((sum(silhouettesList) / len(silhouettesList)), 3)
print("Average silhouette coeff. for this house _ LOF:", averSilh)
