import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


#-----------------------------------------------------------------------------
#1 

# Result
# Not possible to answer
# None of the data can show the gender of the subject

#-----------------------------------------------------------------------------
#2 
df = pd.read_csv('KasterenActData.txt', header=None)
df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')

df = df.loc[(df['ID']== '1') | (df['ID']== '5') | (df['ID']== '10')]

Duration = []
for index, row in df.iterrows():
   Duration.append(row['EndTime'] - row['StartTime'])

df['Duration'] = Duration

ndf = df.loc[df['ID'] == '1']
ndf['ID'] = pd.to_numeric(ndf['ID'], errors="coerce")
plt.scatter(ndf['ID'], ndf.index)
plt.xlabel('Living Style - Leave House')
plt.ylim(0,250)
plt.show()

print ndf['Duration'].mean()

ndf = df.loc[df['ID'] == '5']
ndf['ID'] = pd.to_numeric(ndf['ID'], errors="coerce")
plt.scatter(ndf['ID'], ndf.index)
plt.xlabel('Living Style - Take Shower')
plt.ylim(0,250)
plt.show()

print ndf['Duration'].mean()

ndf = df.loc[df['ID'] == '10']
ndf['ID'] = pd.to_numeric(ndf['ID'], errors="coerce")
plt.scatter(ndf['ID'], ndf.index)
plt.xlabel('Living Style - Go to bed')
plt.ylim(0,250)
plt.show()

print ndf['Duration'].mean()


# Result
# Analyzing the activity (Leave house, Take shower, Go to bed)
# The mean of the three : 06:36:32, 00:10:14, 09:11:26
# 1/4 of a day is used to go out -> not too outgoing
# 9/24 of a day is used to sleep -> healthy person 
# 0.10/24 of a day is used to shower -> normal

#-----------------------------------------------------------------------------
#3
df = pd.read_csv('KasterenActData.txt', header=None)

df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')
df = df.drop(df.index[245])

oneSubject = True
print df
for i in range(0, 1) :
    if df.iloc[i]['EndTime'] > df.iloc[i+1]['StartTime'] :
        oneSubject = False
        
print oneSubject

# Result
# The end time from one activity is less than the start time from the second activity
# only one subject is at home because there's no concurrent activity showing two subjects are at home.

#-----------------------------------------------------------------------------
#4
df = pd.read_csv('KasterenActData.txt', header=None)
df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df = df.loc[df['ID']== '10']
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')


Duration = []
for index, row in df.iterrows():
   Duration.append(row['EndTime'] - row['StartTime'])

df['Sleep_Duration'] = Duration
print df
print df['Sleep_Duration'].mean()

# Result
# On March 08, March 10 and March 21, sleep time is less than 3 hours. 
# Comparing to the mean value of sleep time, it's 6 hours less.
# These days could not be the days to sleep, maybe just a nap

#-----------------------------------------------------------------------------
#5
df = pd.read_csv('KasterenActData.txt', header=None)
df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])

newdf = pd.DataFrame(df.StartTime.str.split(' ',expand=True))
df = newdf[[0]].join(df)
df.columns = ['Date','StartTime','EndTime', 'ID']
unique = df.Date.unique()
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')
df= df.drop(df.index[245])


#for i in unique :
#    idList = []  
#    x = 1
#    day = []
#    print i
#    for index, row in df.iterrows():    
#        if(i == row['Date']) :
#            day.append(x)
#            x = x + 1
#            idList.append(row['ID'])
#    plt.scatter(day, idList)
#    plt.xlabel(str(i) + ' - Activity Pattern')
#    plt.show()        

# Result  
#activity id list:
#1: 'leave house'
#4: 'use toilet'
#5: 'take shower'
#10:'go to bed'
#13:'prepare Breakfast'
#15:'prepare Dinner'
#17:'get drink'

# Activity pattern :  
#25-Feb-2008
#['10', '4', '13', '5', '1', '4', '17', '4', '15', '17', '4', '10', '4']
#26-Feb-2008
#['4', '4', '4', '4', '13', '5', '1', '4', '17', '4', '10']
#27-Feb-2008
#['4', '13', '4', '5', '1', '15', '17', '4']
#28-Feb-2008
#['4', '10', '4', '4', '13', '4', '5', '1', '4', '1', '4', '4', '10']
#29-Feb-2008
#['4', '13', '4', '5', '1', '1', '4', '15', '1']
#02-Mar-2008
#['4', '15', '4', '10']
#03-Mar-2008
#['4', '13', '5', '1']
#04-Mar-2008
#['4', '1', '4', '1', '4', '17']
#05-Mar-2008
#['4', '4', '10', '4', '4', '13', '5', '1', '15', '4', '4', '4', '10']
#06-Mar-2008
#['4', '4', '13', '4', '5', '1', '17', '4', '15', '17', '17', '4', '4', '10']
#07-Mar-2008
#['4', '4', '17', '13', '5', '1']
#08-Mar-2008
#['17', '4', '10', '4', '17', '4', '4', '10', '13', '4', '5', '1']
#10-Mar-2008
#['10', '4', '4', '13', '5', '1', '4', '15', '17', '4', '17', '4', '10']
#11-Mar-2008
#['4', '4', '4', '5', '1', '15', '17', '4', '1', '17', '17', '4', '10']
#12-Mar-2008
#['4', '4', '13', '17', '4', '1', '5', '1']
#13-Mar-2008
#['4', '10', '4', '4', '13', '5', '1', '4', '4', '1']
#14-Mar-2008
#['4', '10', '4', '4', '13', '4', '5', '1', '4', '1', '4', '4', '10']
#15-Mar-2008
#['4', '4', '4', '13', '4', '4', '4', '5', '15', '17', '4', '1']
#16-Mar-2008
#['4', '10', '4', '4', '13', '5', '1', '4', '10', '4']
#17-Mar-2008
#['4', '4', '13', '5', '4', '1', '4', '15', '4', '17', '17', '4']
#18-Mar-2008
#['4', '10', '4', '4', '13', '5', '1', '4', '4', '1']
#19-Mar-2008
#['4', '10', '4', '13', '4', '5', '1', '5', '1', '4', '4', '10']
#20-Mar-2008
#['4', '4', '4', '13', '5', '1', '4', '4', '4', '10']
#21-Mar-2008
#['4', '4', '4', '5', '1', '4', '10', '4', '1']

#-----------------------------------------------------------------------------
#6
df = pd.read_csv('KasterenActData.txt', header=None)
df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df = df.loc[df['ID']== '1']
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')

Duration = []
for index, row in df.iterrows():
   Duration.append(row['EndTime'] - row['StartTime'])

df['NotHome_Duration'] = Duration

print df
print df['NotHome_Duration'].mean()

# Result
# On March 2, March 10 and March 23, the subject left home for a day and more
# The mean of the duration is 0 days 06:36:32  

#-----------------------------------------------------------------------------
#7

#Activities
plt.style.use('ggplot')
df = pd.read_csv('KasterenActData.txt', header=None)
df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')
df = df.drop(df.index[245])

df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
plt.hist(df['ID'], bins =30)
plt.show()

#Sensors
df = pd.read_csv('KasterenSenseData.txt', header=None)
df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',3).tolist(), columns=['StartTime', 'EndTime', 'ID', ' Val'])
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')
df = df.drop(df.index[1319])

df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
plt.hist(df['ID'], bins = 30)
plt.show()

# Result 
# From the activity data, preparing dinner is rarely done by the subject
# From the sensor data, subject rarely washes dishes 

#-----------------------------------------------------------------------------
#8
plt.style.use('ggplot')
df = pd.read_csv('KasterenActData.txt', header=None)
df.drop(df.index[[0,1,2,3,4,5,6,7,8,9,10,11,12]], inplace=True)
df = pd.DataFrame(df[0].str.split('\t',2).tolist(), columns=['StartTime', 'EndTime', 'ID'])
df['StartTime'] = pd.to_datetime(df['StartTime'], errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], errors='coerce')
df = df.drop(df.index[245])

df = df.loc[df['ID']== '13']
print df


# Result
# Checking the time preparing breakfast
# The time making the breakfast is always between 8 to 10 
# There's no data showing that the subject makes lunch 