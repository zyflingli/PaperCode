import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
# use ggplot to make the graph looks better
plt.style.use('ggplot')

df = pd.read_csv('subject1/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
df2 = pd.read_csv('subject2/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
df = df.sort_values(['numOfoccurrences'], ascending=[False])
df2 = df2.sort_values(['numOfoccurrences'], ascending=[False])
df  = df.head(3)
df2 = df2.head(3)

fig = plt.gcf()
plt.title('MIT\nThe Top 3 number of occurrences')
LABELS = ['Toileting','Grooming','Dressing','Preparing\nlunch','Washing\nDishes']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity')
plt.ylabel('NumOfoccurrences')
plt.xticks([1,5,10,15,20], LABELS)
plt.bar([1,5,10], df['numOfoccurrences'], alpha = 0.5, color ='blue')
plt.bar([1,15,20], df2['numOfoccurrences'], alpha = 0.5, color ='red')
plt.show()

#-------------------------------------------------------------------------------------

df = pd.read_csv('subject1/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
df2 = pd.read_csv('subject2/processed_MITActivity.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])
df = df.sort_values(['avgDuration'], ascending=[False])
df2 = df2.sort_values(['avgDuration'], ascending=[False])
df  = df.head(3)
df2 = df2.head(3)

fig = plt.gcf()
plt.title('MIT\nThe Top 3 average Duration')
LABELS = ['Going out\nfor shopping','Washing\nhands','Other','Putting away\nlaundry','Putting away\ngroceries']
patch = mpatches.Patch(color='blue', alpha= 0.5, label='Resident1')
patch1 = mpatches.Patch(color='red', alpha= 0.5, label='Resident2')
plt.legend(handles=[patch,patch1]) 
plt.xlabel('Activity')
plt.ylabel('avgDuration')
plt.xticks([1,5,10,15,20], LABELS)
plt.bar([1,5,10], df['avgDuration'], alpha = 0.5, color ='blue')
plt.bar([10,15,20], df2['avgDuration'], alpha = 0.5, color ='red')
plt.show()