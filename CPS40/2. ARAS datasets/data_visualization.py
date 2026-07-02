import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
# use ggplot to make the graph looks better
plt.style.use('ggplot')

#-----------------------------------------------------------------------------
house = 'B'
df= pd.read_csv('House ' + house +'/processed_ARAS_R1.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
    
# Data visualization
fig = plt.gcf()
fig.set_size_inches(8.5, 4.5)
plt.bar(df.index, df['numOfoccurrences'], alpha = 0.5, color ='blue')
plt.title('30 Days of Activities in House ' + house)
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident 1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident 2')
plt.legend(handles=[patch,patch1]) 
plt.xticks(df.index)
plt.xlabel('Activity ID')
plt.ylabel('NumOfoccurrences')
df= pd.read_csv('House ' + house +'/processed_ARAS_R2.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
plt.bar(df.index, df['numOfoccurrences'], alpha= 0.5, color ='red')
plt.show()

df= pd.read_csv('House ' + house + '/processed_ARAS_R1.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
   
fig = plt.gcf()
fig.set_size_inches(8.5, 4.5)
plt.bar(df.index, df['avgDuration'], alpha = 0.5, color ='blue')
plt.title('30 Days of Activities in House ' + house)
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident 1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident 2')
plt.legend(handles=[patch,patch1]) 
plt.xticks(df.index)
plt.xlabel('Activity ID')
plt.ylabel('AvgDuration')
df= pd.read_csv('House ' + house + '/processed_ARAS_R2.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
plt.bar(df.index, df['avgDuration'], alpha= 0.5, color ='red')
plt.show()






