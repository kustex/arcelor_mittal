from develop.cluster import spectral_clustering
from develop.data_augmentation import augment_data
from develop.data_cleaner import dataclean
import pandas as pd


df=pd.read_csv('CoilDataAugmented_with_label.csv')
df=dataclean(df)
df=augment_data(df)
df.drop(['coil'],inplace=True,axis=1)
df.to_csv('CoilData_MetalGroups_Defective.csv')