# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 17:53:22 2018
@author: leonc
"""
import numpy as np
import pandas as pd
import json
import os, sys

np.get_printoptions()
np.set_printoptions(precision=3, suppress=True)
np.set_printoptions(threshold=sys.maxsize)

raange = pd.date_range(start='2017-02-08 00:00:00', end='2017-05-10 23:59:59', freq='min')
frame_Index = pd.date_range(start='2017-02-08', end='2017-05-10 ', freq='D')
range_plt = pd.date_range(start='2017-03-01 00:00:00', end='2017-03-28 23:59:59', freq='min')


# dataFile: data file in JSON format
# frequency: time duration used for resampling eg. "5min"
# returns numpy Array with axis-0 representing days and axis-1 including chunks in a day
def seqFunct(dataFile, frequency):
    fileObject = open(dataFile)
    jsonObject = json.load(fileObject)
    dataFrame = pd.DataFrame(jsonObject['items'], columns=['timestamp', 'value'])
    series = pd.to_numeric(dataFrame['value'])
    index = pd.to_datetime(dataFrame['timestamp'], infer_datetime_format=True)
    series.index = index
    series = series[raange]
    series = series.resample(frequency).sum()
    series_by_weekAndDate = series.groupby([series.index.week, series.index.date])
    chuncksPerDay = 0
    for (week, date), data in series_by_weekAndDate:
        chuncksPerDay = data.count()
        break
    days = int(series.size / chuncksPerDay)
    daysChunks_Array = np.array(series, dtype=np.float64).reshape((days, chuncksPerDay))
    # daysChunks_DataFrame = pd.DataFrame(data=daysChunks_Array,index=frame_Index)
    return daysChunks_Array


# dailyValues: 2D-array containing all the 5-min consumptions
# length : the subsequence length
# returns 3D-array of subSequences contained in all sequences
def subSeqFunct(daysChunks_Array, length):
    rows = np.size(daysChunks_Array, 0)
    cols = np.size(daysChunks_Array, 1)
    subSeqPerDay = (cols - (length - 1))
    subSeq_3D = np.zeros((rows, subSeqPerDay, length))
    day = 0
    while day < rows:
        subSeq = 0
        while subSeq < subSeqPerDay:
            subSeq_3D[day, subSeq, :] = daysChunks_Array[day, subSeq:(subSeq + length)]
            # subSeqSet=np.put(subSeqSet, [day, subSeq, :], dailyValues[day, subSeq:(subSeq + length)])
            subSeq += 1
        day += 1
    return subSeq_3D


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
