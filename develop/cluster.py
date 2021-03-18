from sklearn.cluster import SpectralClustering
import numpy as np

def spectral_clustering(df):
    '''
    Spectral clustering performs very badly, so don't use this
    '''
    b4=np.array(df['B4max'].astype(float).values)
    b5=np.array(df[['B5min','B4max']].astype(float).values)

    clustering = SpectralClustering(n_clusters=3,
                                    assign_labels="discretize",
                                    random_state=0).fit(b5[:1000,])
    print(clustering.labels_)
    return df