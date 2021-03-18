from develop.cluster import spectral_clustering
from develop.data_augmentation import augment_data
from develop.datacleaner import dataclean
from develop.dev import get_df_length_and_values
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import re
from develop.plotting import plot_min_max

df=pd.read_csv('CoilDataAugmented.csv')
df=dataclean(df)
df=augment_data(df)
df.drop(['analyse','coil'],inplace=True,axis=1)
# df.to_csv('output.csv')
# df['Cluster']=np.floor(np.random.rand(len(df),1)*9)

df=spectral_clustering(df)
# df.Cluster=df.Cluster.astype(int)
# print(df.dtypes)
# plot_min_max(df)
# plt.show()