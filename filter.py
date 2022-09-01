import pandas as pd
import numpy as np
import os

cwd = os.getcwd()

#get the dataframe from B2B
df_soft = pd.read_excel(cwd+"/B2B Data Provider-sample1.xlsx")

#get the user dataframe
df_user = pd.read_csv("user_data.csv")

data = df_user['data'].item().replace("'", "").strip("[]").replace(" ","").lower().split(",")
contract = df_user['contract'].item().replace("'", "").strip("[]").split(",")

result = df_soft[df_soft['Contract'].str.contains(r'\b(?:{})\b'.format('&|'.join(contract)))].reset_index(drop=True)

result = result[result['Solutions'].str.contains(r'\b(?:{})\b'.format('&|'.join(data)))].reset_index(drop=True)

recommend = "aefef"