


def get_results(df_user):


    import pandas as pd
    import numpy as np
    import os 
    import Assign
    from app import home

    ###################################  Getting Software data #######################################
    #get current working directory
    cwd = os.getcwd()
    #load the dataset
    df = pd.read_excel(cwd+"/B2B Data Provider-sample1.xlsx", index_col=0)
    #replace all Nan values with -
    df = df.replace(np.nan, "-")

    #removing unnecessary columns
    df_soft = df.drop(['Additional Pricing Info','Website','Unlimited Data Plan', 'Pricing Range', 'Pricing comments','Free Trial','Other'], axis=1)
    df_soft = df_soft.sort_values(by='location', ascending=False)
    #drop the pricing from data and this can be used to create a feature matrix
    df_pro = df_soft.drop(['Starting Price - Monthly', 'Starting Price - Annually','Price_min','Price_max'], axis=1)

    #get rid of last few numerical columns
    df_pro = df_pro.iloc[:, :8]

    ############################ Creating weight matrix #################################

    df_pro = Assign.get_software_data(df_pro)

    ############################### Getting User data from Q/A ##########################
    #Getting user data
    #df_user = pd.read_csv("user_data.csv", index_col=0)
    
    for i, col in enumerate(df_user.columns):
        if df_user[col].dtype == "int64" or df_user[col].dtype == "float64":
            pass
        else:
            if col == "Location":
                if df_user['Location'].item().replace("'", "").strip("[]") == "Global":
                    df_user['Location'] = [['usa/northamerica', 'international']]
                else:
                    df_user[col] = df_user[col].item().replace("'", "").strip("[]").lower()
                    df_user[col] = df_user[col].str.split(",")
            else:
                df_user[col] = df_user[col].item().replace("'", "").strip("[]").lower()
                df_user[col] = df_user[col].str.split(",")

    #####################  Weight matrix of User data   ##########################
    print(df_user)

    #create a matrix of user data
    df_user_matrix = Assign.get_user_data_matrix(df_user)

    #match columns and drop the ones that do not match
    for i,item in enumerate(df_pro):
        if item not in df_user_matrix.columns:
            df_pro.drop(item, axis=1, inplace=True)
        else:
            #for each company multiply the values of user matrix
            for index in range(len(df_pro)):
                df_pro[item][index] = df_pro[item][index] * df_user_matrix[item][0]
            
    #match columns and drop the ones that do not match
    for i,item in enumerate(df_user_matrix):
        if item not in df_pro.columns:
            df_user_matrix.drop(item, axis=1, inplace=True)


    print(df_pro.sum(axis=1))
    
    #adding the recommended weighted sum to the original dataframe
    df_soft['recommend']= df_pro.sum(axis=1)
    #add back the pricing range column 
    df_soft['Pricing Range'] = df['Pricing Range']
    

    # Finally filtering out the products based on pricing
    df_soft = Assign.get_price_match(df_soft, df_user)
    
    #filtering and sorting to provide the best results
    
    if type(df_user['price'].item()) == int:
        if len(df_user['Location'].item()[0]) != 0:
            result = df_soft.sort_values(by=['location','closest_price_diff'], ascending=[False,True])
            result = result.sort_values(by='recommend', ascending=False)
        else:
            result = df_soft.sort_values(by='closest_price_diff', ascending=True)
            result = result.sort_values(by='recommend', ascending=False)
            
    else:
        if len(df_user['contract'][0]) ==1 and "annual" in df_user['contract'][0] :
            df_soft['AP1'] = df_soft['AP1'].replace("-",np.nan).astype(float)
            result = df_soft.sort_values(by='AP1', ascending=True)
        else:
            df_soft['MP1'] = df_soft['MP1'].replace("-",np.nan).astype(float)
            result = df_soft.sort_values(by='MP1', ascending=True)
        
        result = result.sort_values(by='recommend', ascending=False)

    
    #replace unlimited values with 100000 and - with np.nan
    result = result.reset_index()
    result = result.replace("unlimited",100000)
    result = result.replace("-",np.nan)
    #create an empty column to store closest credits
    result['credit_rank'] = 0

    try:
        #call the functions and get the value
        top_5_pro, below_top_5_pro = Assign.get_credit_index(df_user, result)
        
        #sort the list values
        top_5_pro.sort()
        
        if len(top_5_pro) != 0:
            for i in range(len(top_5_pro)):
                result['credit_rank'][top_5_pro[i][0]] = top_5_pro[i][1]
        else:
            pass
        
        result = result.sort_values(by='credit_rank', ascending=False).reset_index(drop=True).set_index('Company')
    except:
        result = result.reset_index(drop=True).set_index('Company')
        print("please fill in the values")

    
    
    #capitalzing the values in user data "data" column
    df_user = Assign.format_user_data(df_user)
    
    return result[:5], df_user
