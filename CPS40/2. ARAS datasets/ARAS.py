import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# use ggplot to make the graph looks better
plt.style.use('ggplot')

#-----------------------------------------------------------------------------
#1 

columnsName = ['Ph1','Ph2','Ir1','Fo1','Fo2','Di3','Di4','Ph3','Ph4','Ph5','Ph6','Co1','Co2','Co3','So1','So2','Di1','Di2','Te1','Fo3','R1','R2']

for x in range(1, 8):
    df = pd.read_csv('House A/DAY_'+ str(x) +'.txt', sep=" ", header=None)
    df.columns = columnsName
        
#   Histogram 
    mdf = df[['R1','R2']]
    s = "Day " + str(x)
    data = np.vstack([mdf.R1,mdf.R2]).T
    plt.hist(mdf.R1,alpha=0.5, color='green',bins = 30, label='R1')
    plt.hist(mdf.R2,alpha=0.5, color='red',bins = 30, label='R2')
    plt.xlabel("Day " + str(x))
    plt.ylabel("Frequency")
    plt.legend(loc='upper right')
    plt.show()
    
# Result
# activity 20 indicates shaving 
# Resident 1 never shaves (Likely to be a Woman)
# Resident 2 shaves everyday (Likely to be a Man)

#-----------------------------------------------------------------------------
#2

for x in range(1,8):
    df = pd.read_csv('House A/DAY_'+ str(x) +'.txt', sep=" ", header=None) 
    df.columns = columnsName
        
#   2D Scatter plot  
#   X-axis : activity of resident R1 or R2
#   Y-axis : Every second

    mdf = df[['R1']]
    plt.scatter(mdf['R1'], mdf.index)
    plt.xlabel('R1 - Day ' + str(x))
    plt.show()  
    
    mdf = df[['R2']]
    plt.scatter(mdf['R2'], mdf.index)
    plt.xlabel('R2 - Day ' + str(x))
    plt.show()  
    
# Result
#  Resident 1 sleep time is very consistent
#  Resident 1 goes out less and uses internet a lot 
#  Resident 1 could be not a outgoing person and have a good life balance at home
#  Resident 2 is always not home and doesn't clean his place
#  Resident 2 could be a outgoing and untidy person
#  More activities could be used to analyze a person's personalities

#-----------------------------------------------------------------------------
#3

# Result
# This can be answered by looking at column 20 and columne 21

#-----------------------------------------------------------------------------
#4
for x in range(1,8):
    df = pd.read_csv('House A/DAY_'+ str(x) +'.txt', sep=" ", header=None) 
    df.columns = columnsName
    resident = "R1"        
    mdf = df.loc[df[resident]==11]
    mdf = mdf[[resident]]
    plt.scatter(mdf[resident], mdf.index)
    plt.xlabel(resident+ ' - Day ' + str(x))
    plt.xlim(10,12)
    plt.show()  
    
# Result
# Without a light switch sensor, time is the only thing to look at.
# Resident 1
# Sleeping schedule is pretty normal.
# Resident 2
# Day 2 and Day 29 are not home.   
# Day 5 is a mistake definitely to say that person is sleeping for about 2 minutes

#-----------------------------------------------------------------------------
#5
for x in range(1,1):
    df = pd.read_csv('House A/DAY_'+ str(x) +'.txt', sep=" ", header=None) 
    df.columns = columnsName
    pattern = []
    unique = True
    for i in range(0, len(df)-1):
        if unique == True :
            pattern.append(df['R2'][i])
            unique = False
        if df['R2'][i] != df['R2'][i+1]:
            unique = True
    print pattern
    
# Result (R1)
# Day 1
# [12, 22, 12, 21, 15, 17, 11, 1, 12, 3, 4, 15, 17, 21, 13, 22, 13, 22, 13, 1, 19, 17, 15, 27, 2, 1, 7, 22, 7, 8, 17, 22, 12, 21, 12]
# Day 2
# [17, 10, 17, 10, 12, 13, 21, 1, 11, 12, 15, 3, 17, 3, 4, 13, 21, 15, 22, 14, 1, 13, 1, 2, 12, 5, 6, 9, 17, 15, 21, 14, 17, 27, 2, 27, 12, 17, 22, 15, 17]
# Day 3
# [10, 12, 25, 12, 17, 21, 15, 11, 1, 15, 1, 12, 3, 4, 9, 12, 17, 22, 17, 21, 12, 17, 10, 15, 14, 1, 5, 6, 9, 17, 22, 17, 18, 27, 2, 12, 27, 12, 13, 10, 15, 13, 22, 17, 22, 10, 12]
# Day 4           
# [12, 17, 22, 17, 21, 11, 15, 1, 17, 23, 3, 4, 9, 22, 15, 1, 21, 1, 12, 13, 22, 13, 5, 12, 5, 6, 9, 15, 13, 25, 13, 22, 13, 10, 12, 22, 13, 7, 8, 9, 12, 22, 12, 10, 15, 13, 17, 13, 22]
# Day 5
# [22, 12, 17, 21, 11, 25, 15, 4, 9, 1, 17, 22, 17, 21, 13, 22, 13, 12, 10, 12, 5, 6, 9, 17, 23, 16, 15, 14, 1, 13, 22, 13, 27, 2, 1, 27, 7, 8, 9, 15, 22, 17, 12, 1, 12, 22]

# Result (R2)
# Day 1
# [17, 15, 17, 11, 20, 21, 15, 27, 2, 14, 17, 12, 22, 10, 22, 12, 22, 12, 17, 15, 8, 9, 17, 21, 12]
# Day 2
# [2]
# Day 3
# [10, 17, 21, 15, 11, 20, 15, 3, 4, 21, 2, 15, 22, 17, 22, 17, 12, 22, 12]
# Day 4
# [17, 21, 11, 1, 11, 15, 20, 14, 3, 4, 21, 27, 2, 25, 15, 14, 27, 2]
# Day 5
# [2, 25, 27, 3, 4, 21, 20, 22, 2, 1, 27, 12, 22, 12, 15, 12, 17, 1, 17, 13, 22, 13, 21, 11]

#-----------------------------------------------------------------------------
#6

for x in range(1,2):
    df = pd.read_csv('House A/DAY_'+ str(x) +'.txt', sep=" ", header=None) 
    df.columns = columnsName
    resident = "R1"        
    mdf = df.loc[df[resident]==2]
    mdf = mdf[[resident]]
    plt.scatter(mdf[resident], mdf.index)
    plt.xlabel(resident+ ' - Day ' + str(x))
    plt.xlim(1,3)
    plt.show() 
    
# Result
# Resident 1  
# did not go out on Day 4, Day 6, Day 9
# Resident 2
# go out everday

#-----------------------------------------------------------------------------
#7

for x in range(1,8):
    df = pd.read_csv('House A/DAY_'+ str(x) +'.txt', sep=" ", header=None) 
    df.columns = columnsName
    plt.hist(df['R1'], bins = 30)
    plt.xlabel("R1")
    plt.xlim(0,28)
    plt.show()
    
for x in range(1,8):
    df = pd.read_csv('House A/DAY_'+ str(x) +'.txt', sep=" ", header=None) 
    df.columns = columnsName
    plt.hist(df['R2'], color="Green", bins = 30)
    plt.xlabel("R2")
    plt.xlim(0,28)
    plt.show()

# Result (for one week)
# R1 Outlier : 27
# R2 Outlier : 1

#-----------------------------------------------------------------------------
#8
# It is not possible to answer without having a video camera showing that the activity is performed by resident 1
 