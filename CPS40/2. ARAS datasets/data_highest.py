import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
# use ggplot to make the graph looks better
plt.style.use('ggplot')

house = 'A'
df= pd.read_csv('House ' + house +'/processed_ARAS_R1.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
df2= pd.read_csv('House ' + house +'/processed_ARAS_R2.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)

df = df.sort_values(['numOfoccurrences'], ascending=[False])
df2 = df2.sort_values(['numOfoccurrences'], ascending=[False])
df  = df.head(3)
df2 = df2.head(3)

fig = plt.gcf()
plt.title('ARAS House A\nThe Top 3 number of occurrences')
LABELS = ['Watching\nTV','Using\nInternet','Talking\non the\nPhone','Toileting','Other']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity')
plt.ylabel('NumOfoccurrences')
plt.xticks([1,5,10,15,20], LABELS)
plt.bar([1,5,10], df['numOfoccurrences'], alpha = 0.5, color ='blue')
plt.bar([1,15,20], df2['numOfoccurrences'], alpha = 0.5, color ='red')
plt.show()

df= pd.read_csv('House ' + house +'/processed_ARAS_R1.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
df2= pd.read_csv('House ' + house +'/processed_ARAS_R2.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)

df = df.sort_values(['avgDuration'], ascending=[False])
df2 = df2.sort_values(['avgDuration'], ascending=[False])
df  = df.head(3)
df2 = df2.head(3)

fig = plt.gcf()
plt.title('ARAS House A\nThe Top 3 average Duration')
LABELS = ['Going Out','Sleeping','Napping']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity')
plt.ylabel('avgDuration')
plt.xticks([1,5,10], LABELS)
plt.bar([1,5,10], df['avgDuration'], alpha = 0.5, color ='blue')
plt.bar([1,5,10], df2['avgDuration'], alpha = 0.5, color ='red')
plt.show()

#------------------------------------------------------------------------------
house = 'B'
df= pd.read_csv('House ' + house +'/processed_ARAS_R1.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
df2= pd.read_csv('House ' + house +'/processed_ARAS_R2.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)

df = df.sort_values(['numOfoccurrences'], ascending=[False])
df2 = df2.sort_values(['numOfoccurrences'], ascending=[False])
df  = df.head(3)
df2 = df2.head(3)

fig = plt.gcf()
plt.title('ARAS House B\nThe Top 3 number of occurrences')
LABELS = ['Other','Toileting','Watching TV','Changing Clothes']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity')
plt.ylabel('NumOfoccurrences')
plt.xticks([1,5,10,15], LABELS)
plt.bar([1,5,10], df['numOfoccurrences'], alpha = 0.5, color ='blue')
plt.bar([1,5,15], df2['numOfoccurrences'], alpha = 0.5, color ='red')
plt.show()

#------------------------------------------------------------------------------
df= pd.read_csv('House ' + house +'/processed_ARAS_R1.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
df2= pd.read_csv('House ' + house +'/processed_ARAS_R2.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)

df = df.sort_values(['avgDuration'], ascending=[False])
df2 = df2.sort_values(['avgDuration'], ascending=[False])
df  = df.head(3)
df2 = df2.head(3)

fig = plt.gcf()
plt.title('ARAS House B\nThe Top 3 average Duration')
LABELS = ['Going Out','Sleeping','Studying','Reading Book']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity')
plt.ylabel('avgDuration')
plt.xticks([1,5,10,15], LABELS)
plt.bar([1,5,10], df['avgDuration'], alpha = 0.5, color ='blue')
plt.bar([1,5,15], df2['avgDuration'], alpha = 0.5, color ='red')
plt.show()
