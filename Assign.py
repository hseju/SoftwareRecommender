import pandas as pd
import numpy as np


def get_software_data(dataframe):

    #convert all the contract to list values
    dataframe['Contract'] = dataframe['Contract'].str.replace(" or ", ",").str.lower().str.split(',')
    #convert all solutions values to list 
    dataframe['Solutions'] = dataframe['Solutions'].str.lower().str.split(",")
    #convert all the CRM values to list
    dataframe['CRM Integrations'] = dataframe['CRM Integrations'].str.lower().str.split(",")
    #convert all SEPI values to list
    dataframe['SEPI'] = dataframe['SEPI'].str.lower().str.split(",")
    #convert all location values to list
    dataframe['location'] = dataframe['location'].str.lower().str.split(",")
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
            if col in ['crm', 'SEPI_tools']:
                total_tools = len(dataframe['SEPI_tools'].item()) + len(dataframe['crm'].item())
                for index,row in dataframe.iterrows():
                    for item in row[col]:
                        dataframe.at[index,item] = 1+(1/total_tools)
            elif col in ['Location']:
                for index,row in dataframe.iterrows():
                    for item in row[col]:
                        dataframe.at[index,item] = 3+(1/len(dataframe[col]))

            elif col in ['contract']:
                if len(dataframe['contract'][0]) ==2:
                    for index,row in dataframe.iterrows():
                        for item in row['duration']:
                            dataframe.at[index,item] = 5.5+(1/len(dataframe['duration']))
                else:
                    for index,row in dataframe.iterrows():
                        for item in row[col]:
                            dataframe.at[index,item] = 5.5+(1/len(dataframe[col]))

            else:
                for index,row in dataframe.iterrows():
                    for item in row[col]:
                        dataframe.at[index,item] =2
            
    
    
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



def get_price_match(df_1, df_2):
    
    df_1['Starting Price - Monthly'] = df_1['Starting Price - Monthly'].str.replace(" ","").str.split(",")
    df_1['Starting Price - Annually'] = df_1['Starting Price - Annually'].str.replace(" ","").str.split(",")
    #create a column that has difference of price between the input budget and available plans 
    #set initial values to zero
    df_1['closest_price_diff'] = 0

    #loop through each price in the list for a given product and get the difference
    #Assign the lowest price difference to the newly created column 
    if "monthly" in df_2['contract'].item() and len(df_2['contract'].item())==1:
        
        for i in range(len(df_1)):
            diff = 0
            df_1['closest_price_diff'][i] = 50000
            
            for j in range(len(df_1['Starting Price - Monthly'][i])):
                diff =  abs(df_2['price'][0] - int(df_1['Starting Price - Monthly'][i][j]))
                if diff < df_1['closest_price_diff'][i]: 
                    df_1['closest_price_diff'][i] = diff
    elif "annual" in df_2['contract'].item() and len(df_2['contract'].item())==1 :
        
        for i in range(len(df_1)):
            diff = 0
            df_1['closest_price_diff'][i] = 50000
            for j in range(len(df_1['Starting Price - Annually'][i])):
                try:
                    diff =  abs(df_2['price'][0] - int(df_1['Starting Price - Annually'][i][j]))
                    if diff < df_1['closest_price_diff'][i]: 
                        df_1['closest_price_diff'][i] = diff
                except:
                    pass
    elif len(df_2['contract'][0])==2:
        if "monthly" in df_2['duration'].item() and len(df_2['duration'].item())==1:

            for i in range(len(df_1)):
                diff = 0
                df_1['closest_price_diff'][i] = 50000

                for j in range(len(df_1['Starting Price - Monthly'][i])):
                    diff =  abs(df_2['price'][0] - int(df_1['Starting Price - Monthly'][i][j]))
                    if diff < df_1['closest_price_diff'][i]: 
                        df_1['closest_price_diff'][i] = diff

        elif "annual" in df_2['duration'].item() and len(df_2['duration'].item())==1 :

            for i in range(len(df_1)):
                diff = 0
                df_1['closest_price_diff'][i] = 50000

                for j in range(len(df_1['Starting Price - Annually'][i])):
                    try:
                        diff =  abs(df_2['price'][0] - int(df_1['Starting Price - Annually'][i][j]))

                        if diff < df_1['closest_price_diff'][i]: 
                            df_1['closest_price_diff'][i] = diff
                    except:
                        pass
        
    else:
        pass
        
    return df_1



def credit_fider(df_user_data,df_result, start_column, end_column):
    top_5 = []
    below_top_5 = []
    for i, col in enumerate(df_result.iloc[:,start_column:end_column].columns):
        if i%2 !=0:
         
            for index, item in enumerate(df_result[col]):
                if isinstance(df_user_data['contacts'][0], np.floating):
                    pass

                elif isinstance(df_user_data['contacts'][0], list) and len(df_user_data['contacts'].item())==2:
                        if (item >= int(df_user_data['contacts'].item()[0].split("-")[0]) and item <= int(df_user_data['contacts'].item()[0].split("-")[1])) :
                            if index <=4:
                                top_5.append((index, item))
                                print(index, i,item , col)
                            else:
                                below_top_5.append((index, item))

                elif len(df_user_data['contacts'].item())==1:

                        if item > 5000:
                            if index <=4:
                                top_5.append((index, item))
                                print(index, i,item , col)
                            else:
                                below_top_5.append((index, item))
    
    return top_5, below_top_5


    
def get_credit_index(df_user_data, df_result):
    if "monthly" in df_user_data['contract'].item() and len(df_user_data['contract'].item())==1:
        #result = result.iloc[:,23:33]
        top_5_pro, below_top_5_pro = credit_fider(df_user_data,df_result, 24, 34)
        return top_5_pro, below_top_5_pro

    elif "annual" in df_user_data['contract'].item() and len(df_user_data['contract'].item())==1 :
        #result = result.iloc[:,13:23]
        top_5_pro, below_top_5_pro = credit_fider(df_user_data,df_result, 14, 24)
        return top_5_pro, below_top_5_pro

    elif len(df_user_data['contract'][0])==2 and len(df_user_data['duration'][0]) > 1:
        if "monthly" in df_user_data['duration'].item() and len(df_user_data['duration'].item())==1:
            #result = result.iloc[:,23:33]
            top_5, below_top_5 = credit_fider(df_user_data,df_result, 24, 34)
            return top_5, below_top_5

        elif "annual" in df_user_data['duration'].item() and len(df_user_data['duration'].item())==1 :
            #result = result.iloc[:,13:23]
            top_5, below_top_5 = credit_fider(df_user_data,df_result, 14, 24)
            return top_5, below_top_5
        
    else:
        top_5, below_top_5 = credit_fider(df_user_data,df_result, 14, 34)
        return top_5, below_top_5
        
                            
def format_user_data(dataframe):
    for k, row in dataframe.iterrows():
        #data format
        dataframe['data'][0] = [data.replace(" ","").capitalize() for data in row['data']]

    return dataframe