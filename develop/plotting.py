import matplotlib
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

def plot_min_max(df,alpha=0.5):
    colors = np.array(['#377eb8', '#ff7f00', '#4daf4a',
                         '#f781bf', '#a65628', '#984ea3',
                         '#999999', '#e41a1c', '#dede00'])
    plt.subplot(2, 1, 1)
    plt.scatter(df.B4max, df.B5min,color=colors[df.Cluster],alpha=alpha)
    plt.ylabel('B5min')
    plt.xlabel('B4max')

    plt.subplot(2, 1, 2)
    plt.scatter(df.B5max, df.B5min,color=colors[df.Cluster],alpha=alpha)
    plt.ylabel('B5min')
    plt.xlabel('B5max')

    plt.show()


