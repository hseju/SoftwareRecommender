import pandas as pd
import numpy as np
import os

cwd = os.getcwd()

#get the dataframe from B2B
df_soft = pd.read_excel(cwd+"/B2B Data Provider.csv")
#removing unnecessary columns
df_soft = df_soft.drop(['Additional Pricing Info','Website','Unlimited Data Plan'], axis=1) 
#replace all Nan values with -
df_soft = df_soft.replace(np.nan, "-")

#get the user dataframe
df_user = pd.read_csv("user_data.csv")

## Preprocess the data
# get the data of ways to connect from user
data = df_user['data'].item().replace("'", "").strip("[]").replace(" ","").lower().split(",")
# get the types of contract from user
contract = df_user['contract'].item().replace("'", "").strip("[]").split(",")

# get the duration of contract from user
duration = df_user['duration'].item().replace("'", "").strip("[]")
# get the budget monthly or annual from user
price = df_user['price'].item()
# get the right tools of sales engagement from user
tools = df_user['tools'].item().replace("'", "").strip("[]").replace(" ","").split(",")
#get features
features = df_user['features'].item().replace("'", "").strip("[]").replace(" ","").split(",")
# get crm tools
crm = df_user['crm'].item().replace("'", "").strip("[]").replace(" ","").split(",")



def recommend(data,contract,duration,price, tools, features, crm ):
    result = df_soft[df_soft['Contract'].str.contains(r'\b(?:{})\b'.format('|'.join(contract)))].reset_index(drop=True)

    if len(result) >3 and (len(result)-1!=1):
        result = result[result['Solutions'].str.contains(r'\b(?:{})\b'.format('|'.join(data)))].reset_index(drop=True)
    else:
        result = result.copy()

    if len(result) >3 and (len(result)-1!=1):
        if duration in df_soft.columns[1]:
            result = result[result['Starting Price - Monthly'] <= price].reset_index(drop=True)
        elif duration in df_soft.columns[2]:
            result = result[result['Starting Price - Annually'] <= price].reset_index(drop=True)
        else: 
            pass
    else:
        result = result.copy()

        

    if len(result) >3 and (len(result)-1!=1):
        #location
        try:
            if df_user['location'].str == "International":
                result = result[result['location']=="International"]
            elif df_user['location'].str == "Domestic":
                result = result[result['location']=="Domestic"]
            else:
                result = result.copy()
        except ValueError:
            print(f"No {df_user['location'].str} not found.")
            
    else:
        result = result.copy()


    if len(result) >3 and (len(result)-1!=1): 
        if not "All" in tools:
            result = result[result['SEPI'].str.contains(r'\b(?:{})\b'.format('|'.join(tools)))].reset_index(drop=True)
        else:
            pass
    else:
        result = result.copy()
        
        
        
    if len(result) >3 and (len(result)-1!=1):
        try:
            result= result[result['features']==features[0]]
        except:
            pass
    else:
        result = result.copy()
        
        

    if len(result)> 3 and (len(result)-1!=1):
        try:
            result= result[result['features']==features[1]]
        except:
            pass
    else:
        result = result.copy()

    if len(result)>3 and (len(result)-1!=1):  
        if not "All" in crm:
            result = result[result['CRM Integrations'].str.contains(r'\b(?:{})\b'.format('|'.join(crm)))].reset_index(drop=True)
        else:
            pass
        
    else:
        result = result.copy()
        
    #return the dataframe
    return result



#get the final dataframe with recommendations
recommend_soft = recommend(data,contract,duration,price, tools, features, crm )

#get the list of all company names
list_of_companies = recommend_soft['Company']
Company1 = list_of_companies[0]
Company2 = list_of_companies[1]
Company3 = list_of_companies[2]

