from develop.dev import get_df_length_and_values
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math




from develop.plotting import plot_min_max
#
df=pd.read_csv('CoilDataAugmented.csv')


df['Cluster']=np.floor(np.random.rand(len(df),1)*9)
df.Cluster=df.Cluster.astype(int)
print(df.dtypes)
plot_min_max(df)
# plt.show()