import zipfile
import re
import csv
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib. pyplot as plt

from scipy.interpolate import interp1d
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def get_df_length_and_values(path):
	'''
	- Reading, cleaning of CSV-file
	- Return = 2 pandas Series 1. Length, 2. Values
	'''
	df = pd.read_csv(f'../data/SignalExport/{path}.csv', header=None, index_col=0, squeeze=True)
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

def interpolate_values(x, y):
	'''
	Interpolation of the data so that we take the differences of b4 and b5.
	'''
	f = interp1d(x, y, fill_value="extrapolate")
	xnew = np.arange(0, 200, 0.1)
	ynew = f(xnew)
	return xnew, ynew

def get_dict_abs_differences():
	'''
	This function returns the max absolute difference between b4 and b5 in a dictionary, at the interval of 140m until 170m,
	for all the coils in the data folder.
	'''
	column_list = os.listdir('../data/SignalExport/')
	newlist = [name for name in column_list if name.endswith("B4.csv")]
	newdict = {}
	for name_b4 in newlist:
		for name_b5 in column_list:
			if name_b5[:-5] == name_b4[:-5] and name_b5 != name_b4:
				b4_x = get_df_length_and_values(name_b4[:-4])[0]
				b4_y = get_df_length_and_values(name_b4[:-4])[1]
				b5_x = get_df_length_and_values(name_b5[:-4])[0]
				b5_y = get_df_length_and_values(name_b5[:-4])[1]
				if len(b4_x) > 0 and len(b5_x) > 0:
					b4_x_values = [i for i in b4_x if i > 0]
					b4_y_values = [i for i in b4_y if i > 0]
					b5_x_values = [i for i in b5_x if i > 0]
					b5_y_values = [i for i in b5_y if i > 0]
					b4_l = interpolate_values(b4_x_values, b4_y_values)[1]
					b5_l = interpolate_values(b5_x_values, b5_y_values)[1]
					difference_b4_b5 = [abs(i-j) for i, j in zip(b4_l[140:170], b5_l[140:170])]
					max_abs_diff = max(difference_b4_b5)
					newdict[f'{name_b4[:-6]}'] = max_abs_diff
	return newdict

def get_five_perc_highest_abs_diff(dictionary):
	'''
	This function filters out the 5% of coils with the highest absolute difference.
	It returns a list of coils that have the highest chance of contraction in the dataset, by using the filtering method described above.
	'''
	def percentageOfList(l, p):
		return l[0:int(len(l) * p)]
	data = pd.DataFrame.from_dict(dictionary, orient='index', columns=['max_abs_diff'])
	data = percentageOfList(data.iloc[:,0].sort_values(ascending=False), 0.05)
	idx = data.index
	return idx.tolist()

with open('output.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(get_five_perc_highest_abs_diff(get_dict_abs_differences()))
	
