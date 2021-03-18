import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from dev import get_five_perc_highest_abs_diff, get_dict_abs_differences

contracted_coils = get_five_perc_highest_abs_diff(get_dict_abs_differences())
data = pd.read_csv('../data/CoilData.csv')
data = data[data['coil'].isin(contracted_coils)]
