import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
# use ggplot to make the graph looks better
plt.style.use('ggplot')

#df= pd.read_csv('House A/processed_ARAS.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)
df= pd.read_csv('House B/processed_ARAS.txt', names = ["avgDuration","numOfoccurrences","numOfsensors"],sep="\t", header=None)

#-----------------------------------------------------------------------------
#Data modeling 
X = np.column_stack((df['avgDuration'], df['numOfoccurrences']))
kmeans = KMeans(n_clusters = 3)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_
colors = ["g.","r.","b."]

for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

patch = mpatches.Patch(color='green', label='Cluster 0')
patch1 = mpatches.Patch(color='red', label='Cluster 1')
patch2 = mpatches.Patch(color='blue', label='Cluster 2')
plt.legend(handles=[patch,patch1,patch2]) 
plt.scatter(centroids[:,0], centroids[:,1], marker='x', c='red', alpha=0.5, linewidths=3, s=150, zorder=10)

plt.show()


X = np.column_stack((df['avgDuration'], df['numOfsensors']))
kmeans = KMeans(n_clusters = 3, random_state=0, max_iter=300)
kmeans.fit(X)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
colors = ["g.","r.","b."]

for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

patch = mpatches.Patch(color='green', label='Cluster 0')
patch1 = mpatches.Patch(color='red', label='Cluster 1')
patch2 = mpatches.Patch(color='blue', label='Cluster 2')
plt.legend(handles=[patch,patch1,patch2]) 
plt.scatter(centroids[:,0], centroids[:,1], marker='x', c='red', alpha=0.5, linewidths=3, s=150, zorder=10)
plt.show()

X = np.column_stack((df['numOfoccurrences'], df['numOfsensors']))
kmeans = KMeans(n_clusters = 3, random_state=0, max_iter=300)
kmeans.fit(X)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
colors = ["g.","r.","b."]

patch = mpatches.Patch(color='green', label='Cluster 0')
patch1 = mpatches.Patch(color='red', label='Cluster 1')
patch2 = mpatches.Patch(color='blue', label='Cluster 2')
plt.legend(handles=[patch,patch1,patch2]) 
for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)
    
plt.scatter(centroids[:,0], centroids[:,1], marker='x', c='red', alpha=0.5, linewidths=3, s=150, zorder=10)
plt.show()

fig = plt.figure()
ax = plt.axes(projection='3d')
X = np.column_stack((df['avgDuration'], df['numOfoccurrences'], df['numOfsensors']))
kmeans = KMeans(n_clusters = 3)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

plt.scatter(df['avgDuration'],df['numOfoccurrences'],df['numOfsensors'])

plt.scatter(centroids[:,0], centroids[:,1], marker='x', c='red', alpha=0.5, linewidths=3, s=150, zorder=10)

plt.show()
