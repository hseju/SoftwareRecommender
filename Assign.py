import pandas as pd
import numpy as np

def AssignWeight(feature, df, total_tools):
    if feature == "SEPI_tools" :
        for index,row in df.iterrows():
            for tool in row['SEPI_tools']:
                df.at[index,tool] =1/total_tools
    elif feature == "crm":
        for index,row in df.iterrows():
            for crm in row['crm']:
                df.at[index,crm] =1/total_tools
    else:
        for index,row in df.iterrows():
            for contract in row[feature]:
                df.at[index,contract] = 1    

    return df


def get_software_data(dataframe):

    #convert all the contract to list values
    dataframe['Contract'] = dataframe['Contract'].str.replace(" or ", ",").str.split(',')
    #convert all solutions values to list 
    dataframe['Solutions'] = dataframe['Solutions'].str.split(",")
    #convert all the CRM values to list
    dataframe['CRM Integrations'] = dataframe['CRM Integrations'].str.split(",")
    #convert all SEPI values to list
    dataframe['SEPI'] = dataframe['SEPI'].str.split(",")
    #convert all location values to list
    dataframe['location'] = dataframe['location'].str.split(",")
    #convert all location values to list
    dataframe['SalesTeamType'] = dataframe['SalesTeamType'].str.lower().str.split(",")

    for i, col in enumerate(dataframe.columns):

        for index,row in dataframe.iterrows():
            for column in row[col]:
                if (dataframe.at[index,col] == "Yes") or (dataframe.at[index,col] == "No"):
                    pass
                else:
                    dataframe.at[index,column] =1

    #replace the Yes and no values to 1 and 0 respectively for ContactEnrichment and IntentData columns
    dataframe = dataframe.replace('Yes', 1.0)
    dataframe = dataframe.replace('No', 0)


    #now drop all the initial columns that is not a matrix
    dataframe =dataframe.drop(['Contract','Solutions','CRM Integrations','SEPI','location', '-', 'SalesTeamType'], axis=1)

    #lastly replace all the nan values with 0
    dataframe= dataframe.replace(np.nan, 0)

    #lower casing all the column names
    dataframe.columns = dataframe.columns.str.lower()
    dataframe.columns = dataframe.columns.str.replace(" ","")
    return dataframe


def get_user_data_matrix(dataframe):
    
    
    for i, col in enumerate(dataframe.columns):
        if col not in ['price','contacts']:
            if dataframe[col][0][0] == '"i dont have any crm"' or dataframe[col][0][0] == '"i dont have a sales engagement platform"':
                pass
            else:
                if col in ['crm', 'SEPI_tools']:
                    total_tools = len(dataframe['SEPI_tools'].item()) + len(dataframe['crm'].item())
                    for index,row in dataframe.iterrows():
                        for item in row[col]:
                            dataframe.at[index,item] = 1+(1/total_tools)
                elif col in ['Location']:
                    total_tools = len(dataframe['SEPI_tools'].item()) + len(dataframe['crm'].item())
                    for index,row in dataframe.iterrows():
                        for item in row[col]:
                            dataframe.at[index,item] = 1.5+(1/len(dataframe[col]))
                else:
                    for index,row in dataframe.iterrows():
                        for item in row[col]:
                            dataframe.at[index,item] =1+(1/ len(dataframe[col]))
            
    
    
    #now drop all the initial columns that is not a matrix
    dataframe = dataframe.iloc[:,10:]

    #lastly replace all the nan values with 0
    dataframe= dataframe.replace(np.nan, 0)

    #lower casing all the column names
    dataframe.columns = dataframe.columns.str.lower()
    
    #lower casing all the column names
    dataframe.columns = dataframe.columns.str.strip(" ")
   
    
    if "crm" in dataframe.columns:
        dataframe.drop(['crm'], axis=1, inplace=True)
    
    if 'SEPI_tools' in dataframe.columns:
        dataframe.drop(['SEPI_tools'], axis=1, inplace=True)
        
    return dataframe

