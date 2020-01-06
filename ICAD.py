# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 17:58:11 2018
@author: leonc
"""
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from utility import seqFunct,subSeqFunct
from sklearn.model_selection import ShuffleSplit
np.get_printoptions()
np.set_printoptions(precision=3, suppress=True)

localOutlierFactor = LocalOutlierFactor(n_neighbors=20, algorithm='auto', metric='euclidean',novelty=False)

''' 
Compute NonConformity Score of each subSeq in @test. 
*proper is 3-D array, *test is 2-D array(subsequences of a day)
The function returns 1D-array containing nonconf scores. The length of that array is equal to the nber of subsequences in @test. 
'''
def computeNCScores(proper,test):
    proper_shape = proper.shape
    proper_days = proper_shape[0]
    test_nberOfSubSeq=np.size(test,0)
    test_subSeqLength=np.size(test,1)
    row=0
    scores=np.zeros(test_nberOfSubSeq)
    while row < test_nberOfSubSeq:
        proper_CurrentSubseq=proper[:,row,:]
        properTest_current=np.append(proper_CurrentSubseq,test[row])
        properTest_current=properTest_current.reshape(proper_days+1,test_subSeqLength)
        localOutlierFactor.fit_predict(properTest_current)
        score=localOutlierFactor.negative_outlier_factor_
        scores[row]=-score[-1]
        row +=1
    return scores

def computePvalue(calib_scores,test_score): #The 1st parameter is 1D-array, The 2nd is single value
    newList=[]
    for nonConf in np.nditer(calib_scores):
        newList.append(nonConf)
    newList.append(test_score)
    greaterOrEq=[i for i in newList if i >= test_score]
    pValue=len(greaterOrEq)/len(newList)
    return pValue



''' 
Add highest score of each test sample to calib. scores; then compute pValue day_wise 
'''
days_chunks = seqFunct('D:\\thesis__prototype\data\B','5min')
length = 12 #Subsequence length
dictOfPvaluesLessThanThresh = {} # key is iteration number, value is list of pvalues which are less than the threshold for that particular iteration nber
ss = ShuffleSplit(n_splits=10,test_size=0.5,random_state=0) # random_state is explicitly set to zero to control randomness state for reproducibility
calibScoresList = []
iternber = 0
calibConfPlot = 0
testConfPlot = 0
for train_index,test_index in ss.split(days_chunks) :
    properdays_chunks=np.take(days_chunks,train_index,axis=0)       #For proper training set
    proper_set=subSeqFunct(properdays_chunks,length)                #3D-array
    
    calibdays_chunks=np.take(days_chunks,test_index[:30],axis=0)    #For calibration set 
    calib_set=subSeqFunct(calibdays_chunks,length)                  #3D-array               
    
    testdays_chunks=np.take(days_chunks,test_index[30:],axis=0)     #For test set => each sample will be predicted individually
    test_set=subSeqFunct(testdays_chunks,length)                    #3D-array
    
    #compute nonconf. scores of calibration set
    calib_days = np.size(calib_set,0)
    calib_nberOfSubSeq = np.size(calib_set,1)
    calib_subSeqLength = np.size(calib_set,2)
    #calibScores=np.zeros((calib_days,calib_nberOfSubSeq))
    calib_MaxScoresSet = np.zeros(calib_days)     #To hold highest score per sequence in calib. set => 1-D array
    day=0
    while day < calib_days:                     #Iterate through calib. sequences computing their outlierness scores w.r.t proper set 
        calib_currentDay=calib_set[day,:,:].flatten()
        calib_currentDay=calib_currentDay.reshape(calib_nberOfSubSeq,calib_subSeqLength)
        calib_MaxScoresSet[day]=np.amax(computeNCScores(proper_set,calib_currentDay))
        day +=1
        
    #compute nonconf. scores of test set
    test_days=np.size(test_set,0)
    test_nberOfSubSeq=np.size(test_set,1)
    test_subSeqLength=np.size(test_set,2)
    #testScores=np.zeros((test_days,test_nberOfSubSeq))
    test_MaxScoresSet=np.zeros(test_days)       #To hold highest score per sequence in test set => 1-D array
    day=0
    while day < test_days :                     #Iterate through test sequences computing their outlierness scores w.r.t proper set
        test_currentDay=test_set[day,:,:].flatten()
        test_currentDay=test_currentDay.reshape(test_nberOfSubSeq,test_subSeqLength)
        test_MaxScoresSet[day]=np.amax(computeNCScores(proper_set,test_currentDay))
        day +=1
    
    #compute pValue for test sequences one by one
    listOfPvalues = []
    for test_DayScore in np.nditer(test_MaxScoresSet) :
        listOfPvalues.append(computePvalue(calib_MaxScoresSet,test_DayScore))

    iternber +=1            # iteration counter, corresponding to fold nber which is being tested now
    PvaluesLessThanThresh = [ i for i in listOfPvalues if i <= 0.033 ] # In the 16 p-value values corresponding to 16 test samples, put in the list those which are less than the threshold(0.033)
    dictOfPvaluesLessThanThresh[iternber] = PvaluesLessThanThresh     #Dict. of p-value values less than threshold per iteration => <key,value> <=> <iternber,lists>
    #calibConfPlot=calibScores
    #testConfPlot=testScores

''' Print the number of sequences whose p-value is below the threshold for each of the 10 iterations'''
for key in dictOfPvaluesLessThanThresh :
   print(key,dictOfPvaluesLessThanThresh[key], '\n')