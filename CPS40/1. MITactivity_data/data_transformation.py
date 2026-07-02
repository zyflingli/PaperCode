import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

#-----------------------------------------------------------------------------
activitiesdf = pd.read_csv('subject1/Activities.csv',header=None)

df = pd.read_csv('subject1/activities_data.csv',header=None,  sep='\t')

activities = []
Duration = []
templist = []
tempActivity = []
tempStartTime = []
tempEndTime = []
for i in range(0, len(df),5):
    templist = df[0][i].split(',')
    tempActivity.append(templist[0])
    tempStartTime.append(templist[2])
    tempEndTime.append(templist[3])
    
ndf = pd.DataFrame(columns=['Activity','StartTime', 'EndTime'])  
ndf['Activity'] = tempActivity
ndf['StartTime'] = tempStartTime
ndf['EndTime'] = tempEndTime

activitiesdf.drop(activitiesdf.index[[0]], inplace=True)
activitiesdf = activitiesdf.reset_index(drop=True)
ndf['Activity'].replace(list(activitiesdf[2]),list(activitiesdf[3]), inplace= True)

templist_startTime = []
templist_endTime = []
for index, row in ndf.iterrows():
    templist_startTime = row['StartTime'].split(':')
    templist_endTime =row['EndTime'].split(':')
    duration = (int(templist_endTime[0]) * 3600 + int(templist_endTime[1]) * 60 + int(templist_endTime[2])) - (int(templist_startTime[0]) * 3600 + int(templist_startTime[1]) * 60 + int(templist_startTime[2]))
    print duration
    duration = round (duration/3600.0,2)
    Duration.append(duration)

ndf['Duration'] = Duration
ndf['Duration'] = pd.to_numeric(ndf['Duration'], errors='coerce')
ndf.columns = ['ActivityID','StartTime', 'EndTime', 'Duration']

uniqueActivities = []
uniqueActivities = list(set(ndf['ActivityID']))
uniqueActivities = sorted(uniqueActivities, key=int)

avgDuration = []
numOccurrences = []

for activity in uniqueActivities:
    count = 0
    for t in ndf['ActivityID'] :
        if(activity==t) :
            count = count + 1
    numOccurrences.append(count)

for activity in uniqueActivities:
    ndf = ndf.loc[ndf['ActivityID']==activity]
    ndf = ndf.reset_index(drop=True)
    Duration.append(round(sum(ndf['Duration']),2))
    
for index in range (0, len(uniqueActivities)):
    avgDuration.append(round(Duration[index] / numOccurrences[index],2))

df_processedActData = pd.DataFrame()
df_processedActData['ActivityID'] = uniqueActivities
df_processedActData['avgDuration'] = avgDuration
df_processedActData['numOfOccurrences'] = numOccurrences

df_processedActData[['ActivityID','avgDuration','numOfOccurrences']] =  df_processedActData[['ActivityID','avgDuration','numOfOccurrences']].apply(pd.to_numeric)

print df_processedActData
np.savetxt('subject1/processed_MITActivity.txt', df_processedActData.values,fmt= '%d %.2f %d') 
 
 
 
 