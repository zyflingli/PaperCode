import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
# use ggplot to make the graph looks better
plt.style.use('ggplot')

# declare variables
Duration = []
avgDuration = []
numOccurrences = []
numSensors = []

# read input file and clean up the data
df = pd.read_csv('subject1/activities_data.csv',header=None);
print df
