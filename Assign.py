import pandas as pd


def AssignWeight(feature, df, total_tools):
    if feature == "tools" or feature == "crm":
        for index,row in df.iterrows():
            for tool in row['tools']:
                df.at[index,tool] =1/total_tools

    else:
        for index,row in df.iterrows():
            for contract in row[feature]:
                df.at[index,contract] = 1    

    return df