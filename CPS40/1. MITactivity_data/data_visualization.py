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

# Data visualization
fig = plt.gcf()
fig.set_size_inches(8.5, 4.5)
df = pd.read_csv('subject1/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
plt.bar(df.ActivityID, df['numOfoccurrences'], alpha = 0.5, color ='blue')
plt.title('Mar-Apr Activities')
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity ID')
plt.ylabel('NumOfoccurrences')
df = pd.read_csv('subject2/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
plt.bar(df.ActivityID, df['numOfoccurrences'], alpha= 0.5, color ='red')
plt.show()

# Data visualization
fig = plt.gcf()
fig.set_size_inches(8.5, 4.5)
df = pd.read_csv('subject1/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
plt.bar(df.ActivityID, df['avgDuration'], alpha = 0.5, color ='blue')
plt.title('Mar-Apr Activities')
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity ID')
plt.ylabel('avgDuration')
df = pd.read_csv('subject2/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
plt.bar(df.ActivityID, df['avgDuration'], alpha= 0.5, color ='red')
plt.show()


