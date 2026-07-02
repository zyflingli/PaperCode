# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 13:50:51 2017

@author: isaac
"""
import pandas as pd
import numpy as np

df_ActData = pd.read_csv('KasterenActData.txt', header=None)
df_ActData.drop(df_ActData.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df_ActData = pd.DataFrame(df_ActData[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df_ActData['StartTime'] = pd.to_datetime(df_ActData['StartTime'], errors='coerce')
df_ActData['EndTime'] = pd.to_datetime(df_ActData['EndTime'], errors='coerce')
df_ActData.drop(df_ActData.index[[245]], inplace=True)

Duration = []
DurationPerActivity = []
for index, row in df_ActData.iterrows():
   DurationPerActivity.append(round ((row['EndTime'] - row['StartTime']).total_seconds() / 3600.0 , 2))

df_ActData['Duration'] = DurationPerActivity
uniqueActivities = []
uniqueActivities = list(set(df_ActData['ID']))
uniqueActivities = sorted(uniqueActivities, key=int)

avgDuration = []
numOccurrences = []

for activity in uniqueActivities:
    count = 0
    for t in df_ActData['ID'] :
        if(activity==t) :
            count = count + 1
    numOccurrences.append(count)
    
for activity in uniqueActivities:
    df = df_ActData.loc[df_ActData['ID']==activity]
    df = df.reset_index(drop=True)
    Duration.append(round(sum(df['Duration']),2))
    
for index in range (0, len(uniqueActivities)):
    avgDuration.append(round(Duration[index] / numOccurrences[index],2))


df_processedActData = pd.DataFrame()
df_processedActData['ActivityID'] = uniqueActivities
df_processedActData['avgDuration'] = avgDuration
df_processedActData['numOfOccurrences'] = numOccurrences

df_processedActData[['ActivityID','avgDuration','numOfOccurrences']] =  df_processedActData[['ActivityID','avgDuration','numOfOccurrences']].apply(pd.to_numeric)

np.savetxt('processed_kasteren.txt', df_processedActData.values,fmt= '%d %.2f %d')  

        
        

        


