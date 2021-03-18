from develop.cluster import spectral_clustering
from develop.data_augmentation import augment_data
from develop.data_cleaner import dataclean
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
df.drop(['coil'],inplace=True,axis=1)
