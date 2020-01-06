# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 19:43:32 2018
@author: leonc
"""
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import silhouette_score
from utility import seqFunct, subSeqFunct
from sklearn.model_selection import RepeatedKFold
np.get_printoptions()
np.set_printoptions(precision=3, suppress=True)

loF = LocalOutlierFactor(n_neighbors=20, algorithm='auto', metric='euclidean')

# Compute average silhouette coefficient for a 3D array containing subsequences (several days)
def computeSilhouette(proper_3d):
    subSeqPerDay = np.size(proper_3d, 1)
    subSeq = 0
    silhouetteList = []
    while subSeq < subSeqPerDay:
        X = proper_3d[:, subSeq, :]
        labels = loF.fit_predict(X)
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
    subSeq_3D = subSeqFunct(train_DaysChunks, length)
    silhouettesList.append(computeSilhouette(subSeq_3D))
meanSilh = round((sum(silhouettesList) / len(silhouettesList)), 3)
print("Average Silhouette score for this household: ", meanSilh)


'''
# the function to compute nonConf scores of entire dataset (all sequences)
def scoresForPlotFunct(days_chunks,length) :
    entire_set=subSeqFunct(days_chunks,length)    
    days=np.size(entire_set,0)
    dailyNberOfSubSeq=np.size(entire_set,1)
    subSeqLength=np.size(entire_set,2)
    scores=np.zeros((days,dailyNberOfSubSeq))
    #scoresMax=np.zeros(days)
    day=0
    while day < days:
        currentDay=entire_set[day].flatten()
        currentDay=currentDay.reshape(nberOfSubSeq,subSeqLength)
        restOfDays=np.delete(entire_set,day,0)
        scores[day]=nonConfScoresFunct(restOfDays,currentDay)
        day +=1
    return scores
# Anomaly scores of all sequences
allScores=scoresForPlotFunct(days_chunks,length)
'''
