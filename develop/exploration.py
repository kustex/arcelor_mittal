import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from dev import get_five_perc_highest_abs_diff, get_dict_abs_differences

contracted_coils = get_five_perc_highest_abs_diff(get_dict_abs_differences())
data = pd.read_csv('../data/CoilData.csv')
data = data[data['coil'].isin(contracted_coils)]
# print(data)
plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(data.corr(), vmin=-1, vmax=1, annot=True)
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);
plt.show()
