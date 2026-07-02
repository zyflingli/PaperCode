# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 13:50:51 2017

@author: isaac
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# use ggplot to make the graph looks better
plt.style.use('ggplot')

df = pd.read_csv('processed_kasteren.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])

# Data visualization
fig = plt.gcf()
plt.bar(df.ActivityID, df['numOfoccurrences'], alpha = 0.5, color ='blue')
plt.title('28 Days of Activities')
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident')
plt.legend(handles=[patch]) 
plt.xlabel('Activity ID')
plt.ylabel('NumOfoccurrences')
plt.show()

# Data visualization
fig = plt.gcf()
plt.bar(df.ActivityID, df['avgDuration'], alpha = 0.5, color ='blue')
plt.title('28 Days of Activities')
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident')
plt.legend(handles=[patch]) 
plt.xlabel('Activity ID')
plt.ylabel('avgDuration')
plt.show()


