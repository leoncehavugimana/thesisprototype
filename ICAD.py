def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from utility import buildSequences, buildSubSequences
from sklearn.model_selection import ShuffleSplit

np.get_printoptions()
np.set_printoptions(precision=3, suppress=True)

''' 
Compute NonConformity Score of each subSeq in @test. 
*proper is 3-D array, *test is 2-D array(subsequences within a (part of) day)
The function returns 1D-array containing nonconf. scores. The length of that array is equal to the nber of subsequences in @test. 
'''
localOutlierFactor = LocalOutlierFactor(n_neighbors=20, algorithm='auto', metric='euclidean', novelty=False)
def computeNonConfScore(proper, test):
    proper_days = np.size(proper, 0)
    test_nberOfSubSeq = np.size(test, 0)
    test_subSeqLength = np.size(test, 1)
    row = 0
    scores = np.zeros(test_nberOfSubSeq)
    while row < test_nberOfSubSeq:
        proper_CurrentSubseq = proper[:, row, :]
        properTest_current = np.append(proper_CurrentSubseq, test[row])
        properTest_current = properTest_current.reshape(proper_days + 1, test_subSeqLength)
        labels = localOutlierFactor.fit_predict(properTest_current)
        score = localOutlierFactor.negative_outlier_factor_
        scores[row] = -score[-1]
        row += 1
    return scores

''' 
calib_scores is 1D-array, test_score is single value
'''
def computePvalue(calib_scores, test_score):
    calib_test_combined = []
    for nonConf in np.nditer(calib_scores):
        calib_test_combined.append(nonConf)
    calib_test_combined.append(test_score)
    greaterOrEq = [i for i in calib_test_combined if i >= test_score]
    pValue = len(greaterOrEq) / len(calib_test_combined)
    return pValue

''' 
Add highest score of each test sample to calib. scores; then compute pValue day_wise 
'''
days_chunks = buildSequences('data/A', '5min')
length = 12  # Subsequence length
dictOfPvaluesLessThanThresh = {}  # key is iteration number, value is list of pvalues which are less than the threshold per iteration nber
ss = ShuffleSplit(n_splits=10, test_size=0.5, random_state=0)  # random_state is explicitly set to zero to control randomness state for reproducibility
calibScoresList = []
iternber = 0
for train_index, test_index in ss.split(days_chunks):
    properdays_chunks = np.take(days_chunks, train_index, axis=0)  # For proper training set
    proper_set = buildSubSequences(properdays_chunks, length)  # returns 3D-array

    calibdays_chunks = np.take(days_chunks, test_index[:30], axis=0)  # For calibration set
    calib_set = buildSubSequences(calibdays_chunks, length)  # returns 3D-array

    testdays_chunks = np.take(days_chunks, test_index[30:], axis=0)  # For test set => each sample will be predicted individually
    test_set = buildSubSequences(testdays_chunks, length)  # 3D-array

    # ------------------------------------------------------------------------------
    # compute nonconf. scores of calibration set
    calib_days = np.size(calib_set, 0)
    calib_nberOfSubSeq = np.size(calib_set, 1)
    # calibScores=np.zeros((calib_days,calib_nberOfSubSeq))
    calib_MaxScoresArray = np.zeros(calib_days)  # To hold highest NonConf. score per sequence in calib. set => 1-D array
    day = 0
    while day < calib_days:  # Iterate through calib. sequences computing their outlierness scores w.r.t proper set
        calib_currentDay = calib_set[day, :, :].flatten()
        calib_currentDay = calib_currentDay.reshape(calib_nberOfSubSeq, length)
        calib_MaxScoresArray[day] = np.amax(computeNonConfScore(proper_set, calib_currentDay)) # size of calib_MaxScoresArray should be equal to calib_set
        day += 1

    # --------------------------------------------------------------------------------
    # compute nonconf. scores of test set
    test_days = np.size(test_set, 0)
    test_nberOfSubSeq = np.size(test_set, 1)
    # testScores=np.zeros((test_days,test_nberOfSubSeq))
    test_MaxScoresArray = np.zeros(test_days)  # To hold highest NonConf. score per sequence in test set => 1-D array
    day = 0
    while day < test_days:  # Iterate through test sequences computing their outlierness scores w.r.t proper set
        test_currentDay = test_set[day, :, :].flatten()
        test_currentDay = test_currentDay.reshape(test_nberOfSubSeq, length)
        test_MaxScoresArray[day] = np.amax(computeNonConfScore(proper_set, test_currentDay))
        day += 1

    #------------------------------------------------------------------------------------
    # compute pValue for test sequences one by one => Size of listOfPvalues should be equal to size of test set
    listOfPvalues = []
    for test_DayScore in np.nditer(test_MaxScoresArray):
        listOfPvalues.append(computePvalue(calib_MaxScoresArray, test_DayScore))

    # ------------------------------------------------------------------------------------
    # For analysis purpose
    iternber += 1  # iteration counter, corresponding to fold nber which is being tested now
    pvaluesLessThanThresh = [i for i in listOfPvalues if i <= 0.033]  # From the 16 p-value values corresponding to 16 test samples, put in the list those which are less than the threshold(0.033)
    dictOfPvaluesLessThanThresh[iternber] = pvaluesLessThanThresh  # Dict. of p-value values less than threshold per iteration => <key,value> <=> <iternber,list_of_Pvalues_lessThan_threshold>

    # ------------------------------------------------------------------------------------
    #For each of the 10 iterations(test_folds), Print the number of sequences(days) whose p-value is below the threshold
for key in dictOfPvaluesLessThanThresh:
    print(key, dictOfPvaluesLessThanThresh[key], '\n')
