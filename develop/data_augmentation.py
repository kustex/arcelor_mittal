import os
import pandas as pd
import re
from develop.dev import get_df_length_and_values

def read_all_csv():
    augm_df = pd.DataFrame()
    for filename in os.listdir('../data/SignalExport'):
        if filename.endswith(".csv"):
            filename = filename.replace('.csv', '')
            length, width, df = get_df_length_and_values(filename)
            max = width.max()
            min = width.min()
            coil = re.search(r'\d+', filename).group()
            b4_b5 = re.search(r'\D\d', filename).group()
            if b4_b5 == 'B4':
                augm_df.at[coil, 'B4max'] = max
                augm_df.at[coil, 'B4min'] = min
            else:
                augm_df.at[coil, 'B5max'] = max
                augm_df.at[coil, 'B5min'] = min
    return augm_df

df=pd.read_csv('minmax.csv',index_col=0)
coildata=pd.read_csv('../data/CoilData.csv',index_col='coil')
coildata.join(df).to_csv('../data/CoilDataAugmented.csv')
