import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
# use ggplot to make the graph looks better
plt.style.use('ggplot')

df = pd.read_csv('processed_kasteren.txt', header= None, sep="\s+", names=['ActivityID','avgDuration','numOfoccurrences'])

print df
#K-mean clustering 
X = np.column_stack((df['avgDuration'], df['numOfoccurrences']))

kmeans = KMeans(n_clusters=3, init='k-means++', 
            max_iter=100, n_init=1, verbose=0, random_state=3425)

kmeans.fit(X)

centroids = kmeans.cluster_centers_
print centroids
labels = kmeans.labels_

colors = ["g.","r.","b."]

for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

patch = mpatches.Patch(color='green', label='Activities')
patch1 = mpatches.Patch(color='red', label='Activities')
patch2 = mpatches.Patch(color='blue', label='Activities')
plt.legend(handles=[patch,patch1,patch2]) 
plt.title('28 Days of Activities')
plt.xlabel('avgDuration')
plt.ylabel('numOfoccurrences')
plt.scatter(centroids[:,0], centroids[:,1], marker='x', c='red', alpha=0.5, linewidths=3, s=150, zorder=10)
plt.show()
df = []