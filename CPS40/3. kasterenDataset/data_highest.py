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
df = df.sort_values(['numOfoccurrences'], ascending=[False])
df  = df.head(3)

fig = plt.gcf()
plt.title('Kasteren\nThe Top 3 number of occurrences')
LABELS = ['Use toilet','Leave house','Go to bed']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
plt.legend(handles=[patch]) 
plt.xlabel('Activity')
plt.ylabel('NumOfoccurrences')
plt.xticks([1,5,10], LABELS)
plt.bar([1,5,10], df['numOfoccurrences'], alpha = 0.5, color ='blue')
plt.show()

df = pd.read_csv('processed_kasteren.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
df = df.sort_values(['avgDuration'], ascending=[False])
df  = df.head(3)

fig = plt.gcf()
plt.title('Kasteren\nThe Top 3 average Duration')
LABELS = ['Leave house','Go to bed','Prepare dinner']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
plt.legend(handles=[patch]) 
plt.xlabel('Activity')
plt.ylabel('avgDuration')
plt.xticks([1,5,10], LABELS)
plt.bar([1,5,10], df['avgDuration'], alpha = 0.5, color ='blue')
plt.show()