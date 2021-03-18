from sklearn.cluster import SpectralClustering
import numpy as np


# X = np.array([[1, 1], [2, 1], [1, 0],
#                [4, 7], [3, 5], [3, 6]])

def spectral_clustering(df):
    b4=np.array(df['B4max'].astype(float).values)
    b5=np.array(df[['B5min','B4max']].astype(float).values)

    clustering = SpectralClustering(n_clusters=3,
                                    assign_labels="discretize",
                                    random_state=0).fit(b5[:1000,])
    print(clustering.labels_)
    # df['Cluster']=clustering.labels_
    return df