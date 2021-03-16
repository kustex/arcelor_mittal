import zipfile
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

path_b4 = '520677B4'
path_b5 = '520677B5'



def get_df_length_and_values(path):
    '''
    Reading, cleaning of CSV-file
    return = 2 pandas Series 1. Length, 2. Values

    '''
    df = pd.read_csv(f'../data/SignalExport/{path}.csv', header = None, index_col = 0, squeeze = True)
    df = str(pd.Series(data=df.index).tolist())
    df = re.split(';', df)[3:]

    length_p = []
    for i in df:
        if i != 'Values':
            length_p.append(i)
        else:
            break

    length_p = length_p[:-1]
    length_p = [float(i) for i in length_p]
    values = df[len(length_p)+3:][:-1]
    values = [float(i) for i in values]
    values = [i for i in values if i != 0]
    length_p = [i for i in length_p if i != 0]

    df = list(zip(length_p, values))
    df = pd.DataFrame(data=df, columns=['length_p','values'])
    length_p = df['length_p']
    values = df['values']
    return length_p, values, df

df_b4 = get_df_length_and_values(path_b4)[2]
df_b5 = get_df_length_and_values(path_b5)[2]

def interpolate_values(x, y):
	x = x
	y = y 
	f = interp1d(x, y)
	xnew = np.linspace(0,200, 0.001)
	ynew = f(xnew)
	return xnew, ynew



def get_mean_until_140(df_b4, df_b5):  
    lst_b4 = []
    lst_b5 = []
    for i, j in zip(df_b4['length_p'], df_b4['values']):
        if i < 140:
            lst_b4.append(j)
        else:
            break
    for i, j in zip(df_b5['length_p'], df_b5['values']):
        if i < 140:
            lst_b5.append(j)
        else:
            break
    b4_mean = np.mean(lst_b4)
    b5_mean = np.mean(lst_b5)
    return b4_mean, b5_mean

def get_values_between_140_and_170(df_b4, df_b5):
    lst_b4 = []
    lst_b5 = []
    for i, j in zip(df_b4['length_p'], df_b4['values']):
        if i >= 140 and i <= 170:
            lst_b4.append(j)
    for i, j in zip(df_b5['length_p'], df_b5['values']):
        if i >= 140 and i <= 170:
            lst_b5.append(j)
    return len(lst_b4), len(lst_b5)





# fig, ax = plt.subplots(figsize=(20,10))
# l1, = ax.plot(df_b4['length_p'][10:], df_b4['values'][10:])
# l2, = ax.plot(df_b5['length_p'][10:], df_b5['values'][10:])
# ax.legend([l1, l2], ['B4','B5'])
# plt.title('B4 and B5 measurements')
# plt.xlabel('Length metal plate')
# plt.ylabel('Width metal plate')
# plt.show()
