import pandas as pd
import re

def csv_to_df(path):
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

