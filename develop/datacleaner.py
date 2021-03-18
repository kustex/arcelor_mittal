import re
import numpy as np

def dataclean(df):
    #removes records where there are empty whitespace cells
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    #removes '*******' from thicknessprofile
    df.replace(r'\*\*\*\*\*\*', np.nan, regex=True, inplace=True)
    df.dropna(inplace=True)
    return df
