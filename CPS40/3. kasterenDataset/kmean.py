import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
# use ggplot to make the graph looks better
plt.style.use('ggplot')

# declare variables
Duration = []
avgDuration = []
numOccurrences = []
numSensors = []
activitiesID = [1,4,5,10,13,15,17]
sensorsID = [1,5,6,7,8,9,12,13,14,17,18,20,23,24]
totalDuration = 0

# read input file and clean up the data
df_ActData = pd.read_csv('kasterenActData.txt',header=None);
df_ActData.drop(df_ActData.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df_ActData = pd.DataFrame(df_ActData[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df_ActData.drop(df_ActData.index[[245]], inplace=True)

df_SenData = pd.read_csv('kasterenSenseData.txt',header=None);
df_SenData.drop(df_SenData.index[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]], inplace=True)
df_SenData = pd.DataFrame(df_SenData[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df_SenData['ID']= df_SenData['ID'].replace({'\t1': ''}, regex=True)
df_SenData.drop(df_SenData.index[[1319]], inplace=True)
df_SenData['ID'] = pd.to_numeric(df_SenData['ID'], errors="coerce")
print df_SenData.dtypes

# Calculate avgDuration
df_ActData['StartTime'] = pd.to_datetime(df_ActData['StartTime'], errors='coerce')
df_ActData['EndTime'] = pd.to_datetime(df_ActData['EndTime'], errors='coerce')
for index, row in df_ActData.iterrows():
   Duration.append(row['EndTime'] - row['StartTime'])
df_ActData['Duration'] = Duration
df_ActData['ID'] = pd.to_numeric(df_ActData['ID'], errors="coerce")

for activitiesid in activitiesID:
    temp= df_ActData.loc[df_ActData['ID'] == activitiesid]
    for i in temp['Duration'] :
        seconds = i.components.hours * 3600 + i.components.minutes * 60 + i.components.seconds
        totalDuration = totalDuration + round((seconds / 3600.0), 2)
        
    mean = round(totalDuration / len(temp['Duration']),2)
    totalDuration = 0
    avgDuration.append(mean)
    
# Calculate numberOfOccurrences
for activitiesid in activitiesID:
    temp = df_ActData.loc[df_ActData['ID'] == activitiesid]
    numOccurrences.append(len(temp['ID']))

# Calculate numberOfSensors
for sensorid in sensorsID:
    temp = df_SenData.loc[df_SenData['ID'] == sensorid]
    numSensors.append(len(temp['ID']))
    
# create new dataframe that stores desirable data
ndf = pd.DataFrame()  
ndf['ActivitiesID'] = activitiesID
ndf['avgDuration'] = avgDuration
ndf['numOfoccurrences'] = numOccurrences

print ndf