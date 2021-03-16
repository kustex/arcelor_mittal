from develop.dev import get_df_length_and_values

path_b4 = '520677B4'
path_b5 = '520677B5'

length, width, df=get_df_length_and_values(path_b4)
print(length)
print(width)
print(df)