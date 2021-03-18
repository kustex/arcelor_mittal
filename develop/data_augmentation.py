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

def maingroup(x):
    return re.search(r'^\w\w\w', x).group()

def subgroup(x):
    return re.search(r'\w\s$', x).group()

def turn_groups_into_dummies(df):
    main_df=pd.get_dummies(df['maingroup'],prefix='maingroup',sparse=True)
    sub_df = pd.get_dummies(df['subgroup'],prefix='subgroup',sparse=True)
    df=df.join([main_df,sub_df])
    return df

def convert_analyse_into_categorical(df):
    df['maingroup'] = df['analyse'].apply(maingroup)
    df['subgroup'] = df['analyse'].apply(subgroup)
    df = turn_groups_into_dummies(df)
    df.drop(['analyse','maingroup', 'subgroup'], inplace=True, axis=1)
    return df

def augment_data(df):
    '''
    Converts analyse into maingroup and subgroup columns and than dummies them
    After dummy-encoding gets rid of the obsolete columns 'analyse' , 'maingroup' ,'subgroup'
    '''
    df = convert_analyse_into_categorical(df)
    return df
