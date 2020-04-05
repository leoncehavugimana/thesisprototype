import json
import sys

import numpy as np
import pandas as pd

np.get_printoptions()
np.set_printoptions(precision=3, suppress=True)
np.set_printoptions(threshold=sys.maxsize)

raange = pd.date_range(start='2017-02-08 00:00:00', end='2017-05-10 23:59:59', freq='min')
frame_Index = pd.date_range(start='2017-02-08', end='2017-05-10 ', freq='D')
range_plt = pd.date_range(start='2017-03-01 00:00:00', end='2017-03-28 23:59:59', freq='min')

'''
 dataFile: data file in JSON format
 frequency: time duration used for resampling eg. "5min"
 returns 2D-Array with axis-0 representing days and axis-1 including chunks in a day
'''
def buildSequences(dataFile, frequency):
    with open(dataFile) as f:
        data = json.load(f)
        dataFrame = pd.DataFrame(data['items'], columns=['timestamp', 'value'])
        series = pd.Series(dataFrame['value'])
        series.index = pd.to_datetime(dataFrame['timestamp'], infer_datetime_format=True,utc=True)  #format='%Y-%m-%dT%H:%M:%S'
        series = pd.to_numeric(series)
        series = series[9960:]  # bcz raange seems to not functioning here
        series = series.resample(frequency,label='right').sum()
        n_array = series.to_numpy().reshape((92,288))
    return n_array

'''
 daysChunks_Array: 2D-array containing all days and each day with 5-min consumptions
 length : the subsequence length
 returns 3D-array holding subSequences contained in sequences
'''
def buildSubSequences(daysChunks_Array, length):
    rows = np.size(daysChunks_Array, 0)
    cols = np.size(daysChunks_Array, 1)
    subSeqPerDay = (cols - (length - 1))
    subSeq_3D = np.zeros((rows, subSeqPerDay, length))
    day = 0
    while day < rows:
        subSeq = 0
        while subSeq < subSeqPerDay:
            subSeq_3D[day, subSeq, :] = daysChunks_Array[day, subSeq:(subSeq + length)]
            subSeq += 1
        day += 1
    return subSeq_3D



# =======================================================================================================================
''' 
# returns one series used to plot the consumption curve
def plotFunct(dataFile, frequency):
    fileObject = open(dataFile)
    jsonObject = json.load(fileObject)
    dataFrame = pd.DataFrame(jsonObject['items'], columns=['timestamp', 'value'])
    series = pd.to_numeric(dataFrame['value'])
    index = pd.to_datetime(dataFrame['timestamp'], infer_datetime_format=True)
    series.index = index
    series = series[range_plt]
    series = series.resample(frequency).sum()
    return series
'''
'''
# returns statistics description of datasets
def describeFunct(dataFile):
    fileObject = open(dataFile)
    jsonObject = json.load(fileObject)
    dataFrame = pd.DataFrame(jsonObject['items'], columns=['timestamp', 'value'])
    series = pd.to_numeric(dataFrame['value'])
    index = pd.to_datetime(dataFrame['timestamp'], infer_datetime_format=True)
    series.index = index
    firstIndex = series.index[0]
    lastIndex = series.index[-1]
    series_description=series.describe()
    print( series_description)
# listing datasets files
listOfFiles = []
for fileName in os.listdir('D:\\thesis__prototype\\data'):
    absName = os.path.join('D:\\thesis__prototype\\data', fileName)
    listOfFiles.append(absName)
    for i in listOfFiles :
        describeFunct(i)
'''
'''
class item:
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit


class itemWrapper:
    def __init__(self, itemIndex, totalItems, items):
        self.itemIndex = itemIndex
        self.totalItems = totalItems
        self.items = items
'''
