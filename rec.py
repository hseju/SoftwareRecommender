


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

    #drop the pricing from data and this can be used to create a feature matrix
    df_pro = df_soft.drop(['Starting Price - Monthly', 'Starting Price - Annually'], axis=1)

    

    ############################ Creating weight matrix #################################

    df_pro = Assign.get_software_data(df_pro)

    ############################### Getting User data from Q/A ##########################
    #Getting user data
    #df_user = pd.read_csv("user_data.csv", index_col=0)
    

    for i, col in enumerate(df_user.columns):
        if df_user[col].dtype == "int64":
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
    if str(df_user['price'].item()) not in ["nan"]:
        if "monthly" in df_user['duration'].item():
            result = df_soft[df_soft['Starting Price - Monthly'] <= df_user['price'].item()].sort_values(by='Starting Price - Monthly', ascending=True)
        elif "annual" in df_user['duration'].item():
            result = df_soft[df_soft['Starting Price - Annually'] <= df_user['price'].item()].sort_values(by='Starting Price - Annually', ascending=True)
        else:
            result = df_soft.sort_values(by='Starting Price - Monthly', ascending=True)
    else:
        result = df_soft.sort_values(by='recommend', ascending=False)


    #filtering top three
    result_final = result[:5]
    return result_final
