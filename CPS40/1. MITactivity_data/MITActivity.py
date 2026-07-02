import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

#-----------------------------------------------------------------------------
#1 

df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []

for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce')
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce')

Duration = []
for index, row in ndf.iterrows():
   Duration.append(row['EndTime'] - row['StartTime'])

ndf['Duration'] = Duration
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time

ndf = ndf.loc[ndf['Activity']=='Bathing']

print ndf['Duration'].mean()

 # Result
 # Not 100% sure because there's no activities are female related.
 # Average Bathing time is about 23:49 minutes
 # The subject might be a Female
 # But by looking at the sensor data, a jewelry box is used before going out to work
 # It proves that the subject should be a female
 
#-----------------------------------------------------------------------------
#2

df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []
for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce')
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce')

Duration = []
for index, row in ndf.iterrows():
   Duration.append(row['EndTime'] - row['StartTime'])

ndf['Duration'] = Duration
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time

temp = ndf.loc[(ndf['Activity']=='Bathing')]

print temp['Duration'].mean()
print len(temp['Duration'])

temp = ndf.loc[(ndf['Activity']=='Cleaning')]

print temp['Duration'].mean()
print len(temp['Duration'])

temp = ndf.loc[(ndf['Activity']=='Doing laundry')]

print temp['Duration'].mean()
print len(temp['Duration'])

# to check if a person is a workaholic or healthy (work + relax)
temp = ndf.loc[(ndf['Activity']=='Going out to work')]

print "Going out to work:"
print temp['Duration'].mean()
print len(temp['Duration'])

temp = ndf.loc[(ndf['Activity']=='Watching TV')]

print "Wacthing TV:"
print temp['Duration'].mean()
print len(temp['Duration'])

temp = ndf.loc[(ndf['Activity']=='Going out for entertainment')]

print "Going out for entertainment:"
print temp['Duration'].mean()
print len(temp['Duration'])

temp = ndf.loc[(ndf['Activity']=='Going out for shopping')]

print "Going out for shopping:"
print temp['Duration'].mean()
print len(temp['Duration'])
# Result
# List of activities
#    Bathing
#    Toileting
#    Going out to work
#    Preparing lunch
#    Preparing dinner
#    Preparing breakfast
#    Dressing
#    Grooming
#    Preparing a snack
#    Preparing a beverage
#    Washing dishes
#    Doing laundry
#    Cleaning
#    Putting away dishes
#    Washing hands
#    Putting away groceries
#    Other
#    Watching TV
#    Going out for shopping
#    Going out for entertainment
#    Lawnwork
#    Putting away laundry
# The average time of bathing is 23:49 minutes. (18 times from 3/27/03 to 4/11/03)
# The average time of cleaning is 18:39 minutes (9 times from 3/27/03 to 4/11/03)
# The average time of doing laundry is 11:23 minutes (9 times from 3/27/03 to 4/11/03)
# The subject is a person which is quite clean and tidy.

# The average time in this case is not useful because it is not the actual time of the activity
# The subject goes out to work 12 times in 16 days
# The subject goes out for entertainment once in 16 days
# The subject goes out for shopping twice in 16 days
# The subject watches TV 3 times in 16 days
# The subject is a person which is a normal worker without lot of entertainments.

#-----------------------------------------------------------------------------
#3
df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []
for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time
ndf = ndf.sort(['Date','StartTime'])
ndf.index = range(0,len(ndf))

oneSubject = True
for i in range(0, len(ndf)-1) :
    
    if (ndf.loc[i]['Date'] == ndf.loc[i+1]['Date']) & (ndf.loc[i]['EndTime'] > ndf.loc[i+1]['StartTime']) :
        print ndf.index[i]
        oneSubject = False

print ndf
print oneSubject

# Result
# Most of the end time from one activity is less than the start time from the second activity
# only one subject is at home.
# There are few cases where the subjects dress before turn off the shower faucet, Groom and do other things.

#-----------------------------------------------------------------------------
#4
df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []
for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time
ndf = ndf.sort(['Date','StartTime'])
ndf.index = range(0,len(ndf))

lt = ndf['Activity'].unique()

print "List all activities :"
for i in lt:
    print i

# Result
# Unfortunately, there is no sleeping activities in this dataset

#-----------------------------------------------------------------------------
#5
df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []
for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time
ndf = ndf.sort(['Date','StartTime'])
ndf.index = range(0,len(ndf))

unique = ndf['Date'].unique()
for x in unique:
    print 'Activities on ' + str(x) + ':'
    for i in range(0,len(ndf)):
        if (ndf.loc[i]['Date'] == x):
            print ndf.loc[i]['Activity'] 
    print ' '
    print '----------------------------------------------------------'


# Result
# Pattern is generated in text. There is a reason why it is not shown on a graph.
# Converting text into Integers is easy but looking up what number refers to what activity takes time
# Result is on the console.

#-----------------------------------------------------------------------------
#6
df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []
for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce')
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce')
ndf = ndf.sort(['Date','StartTime'])
ndf.index = range(0,len(ndf))

ndf = ndf.loc[(ndf['Activity']=='Going out to work') | (ndf['Activity']=='Going out for shopping') | (ndf['Activity']=='Going out for entertainment')]

Duration = []
for index, row in ndf.iterrows():
   Duration.append(row['EndTime'] - row['StartTime'])

ndf['Duration'] = Duration
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time

print ndf

# Result
# Subject goes out to work 12 times in 16 days
# leaving time (7:51,12:32,13:42,10:18,7:02,12:15,8:30,12:14,9:34,14:05,9:50,7:32)
# Thur(27) -> Fri(28) -> Sat (29) -> Sun (30) -> Mon (31) -> Tue (1)
# Subject goes out for shopping twice in 16 days
# Leaving time (18:48,9:56)
# Subject goes out for entertainment once in 16 days
# Leaving time (18:54)

#-----------------------------------------------------------------------------
#7
plt.style.use('ggplot')
df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []
for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time
ndf = ndf.sort(['Date','StartTime'])
ndf.index = range(0,len(ndf))

ndf['ActivityCode'] = pd.Categorical.from_array(ndf['Activity']).labels 
print ndf
plt.hist(ndf['ActivityCode'])
plt.show()

print ndf.loc[ndf['ActivityCode']== 15]


# Result
# From the activity data, 15-17 are rarely done by the subject
# Putting away dishes, Putting away groceries, Putting away laundry deviate from what is standard

#-----------------------------------------------------------------------------
#8
df = pd.read_csv('subject1/activities_data.csv',header=None)
activities = []
sensors = []
for i in range(0, len(df),5):
    activity = [df[0][i],df[1][i],df[2][i],df[3][i]]
    activities.append(activity) 
   
ndf = pd.DataFrame(activities, columns=['Activity','Date','StartTime', 'EndTime'])
ndf['StartTime'] = pd.to_datetime(ndf['StartTime'],errors='coerce').dt.time
ndf['EndTime'] = pd.to_datetime(ndf['EndTime'], errors='coerce').dt.time
ndf = ndf.sort(['Date','StartTime'])
ndf.index = range(0,len(ndf))


print ndf
# Result
# The time after every last activity of the day could possbily indicate the sleep time
 
 
 
 