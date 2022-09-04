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
    df_soft = df.drop(['Additional Pricing Info','Website','Unlimited Data Plan', 'Pricing Range', 'Pricing comments', 'SalesTeamType','Free Trial','Other'], axis=1)

    #drop the pricing from data and this can be used to create a feature matrix
    df_pro = df_soft.drop(['Starting Price - Monthly', 'Starting Price - Annually'], axis=1)

    #convert all the contract to list values
    df_pro['Contract'] = df_pro['Contract'].str.replace(" or ", ",").str.split(',')
    #convert all solutions values to list 
    df_pro['Solutions'] = df_pro['Solutions'].str.split(",")
    #convert all the CRM values to list
    df_pro['CRM Integrations'] = df_pro['CRM Integrations'].str.split(",")
    #convert all SEPI values to list
    df_pro['SEPI'] = df_pro['SEPI'].str.split(",")
    #convert all location values to list
    df_pro['location'] = df_pro['location'].str.split(",")


    ############################### Getting User data from Q/A ##########################
    #Getting user data
    #df_user = pd.read_csv("user_data.csv", index_col=0)
    df_user['data'] = df_user['data'].item().replace("'", "").strip("[]").lower()
    df_user['data'] = df_user['data'].str.split(",")
    df_user['contract'] = df_user['contract'].item().replace("'", "").strip("[]")
    df_user['contract'] = df_user['contract'].str.split(",")
    df_user['duration'] = df_user['duration'].item().replace("'", "").strip("[]")
    df_user['price'] = df_user['price'].item()

    if df_user['Location'].item().replace("'", "").strip("[]") == "All":
        df_user['Location'] = [['International', 'Domestic']]

    df_user['features'] = df_user['features'].item().replace("'", "").strip("[]")
    df_user['features'] = df_user['features'].str.split(",")

    if df_user['tools'].item().replace("'", "").strip("[]").replace(" ","") == "All":
        df_user['tools']= [['Outreach', 'Salesloft','Reply','Woodpecker','Lemlist','Close','HubSpot','Salesforce','Pipedrive','Nutshell','Zoho','Freshworks']]
    else:
        df_user['tools'] = df_user['tools'].item().replace("'", "").strip("[]")
        df_user['tools'] = df_user['tools'].str.split(",")

    if df_user['crm'].item().replace("'", "").strip("[]").replace(" ","") == "All":
        df_user['crm' ]= [['Microsoft Dynamics','HubSpot','Salesforce','Pipedrive','SugarCRM','Zoho','Insightly','Copper','Nimble','Infusionsoft','Capsule','Nutshell','Base','Vtiger','Keap','Freshsales']]
    else:
        df_user['crm'] = df_user['crm'].item().replace("'", "").strip("[]")
        df_user['crm'] = df_user['crm'].str.split(",")

    #we will remove the price for now 
    df_user_matrix = df_user.drop(['price','user'], axis=1)


    #calculate the total number of tools for crm and sales engagement. We will assign a weighted value to each tool.
    total_tools = len(df_user_matrix['tools'].item()) + len(df_user_matrix['crm'].item())


    ############################ Creating weight matrix #################################

    df_pro = Assign.AssignWeight("Contract", df_pro, total_tools)

    df_pro = Assign.AssignWeight("Solutions", df_pro, total_tools)

    df_pro = Assign.AssignWeight("CRM Integrations", df_pro, total_tools)

    df_pro = Assign.AssignWeight("SEPI", df_pro, total_tools)

    df_pro = Assign.AssignWeight("location", df_pro, total_tools)


    #replace the Yes and no values to 1 and 0 respectively for ContactEnrichment and IntentData columns
    df_pro = df_pro.replace('Yes', 1.0)
    df_pro = df_pro.replace('No', 0)

    #now drop all the initial columns that is not a matrix
    df_pro =df_pro.drop(['Contract','Solutions','CRM Integrations','SEPI','location', '-'], axis=1)

    #lastly replace all the nan values with 0
    df_pro= df_pro.replace(np.nan, 0)


    #### Weight matrix of User data

    df_user_matrix = Assign.AssignWeight("data", df_user_matrix, total_tools)

    df_user_matrix = Assign.AssignWeight("contract", df_user_matrix, total_tools)

    df_user_matrix = Assign.AssignWeight("Location", df_user_matrix, total_tools)

    df_user_matrix = Assign.AssignWeight("tools", df_user_matrix, total_tools)

    df_user_matrix = Assign.AssignWeight("features", df_user_matrix, total_tools)

    df_user_matrix = Assign.AssignWeight("crm", df_user_matrix, total_tools)

    #rename column Work phone
    df_user_matrix = df_user_matrix.rename(columns={' work phone':'workphone'})


    ## Assigning the extra value of 1 to all the weighted values 
    for i,item in enumerate(df_user_matrix):
        item = item.lstrip(" ")
        
        if item in df_pro.columns:
            print(item, df_pro[item].dtype)
            df_pro[item] = df_pro[item]+1


    print(df_pro.sum(axis=1))

    #adding the recommended weighted sum to the original dataframe
    df_soft['recommend']= df_pro.sum(axis=1)
    #add back the pricing range column 
    df_soft['Pricing Range'] = df['Pricing Range']

    # Finally filtering out the products based on pricing
    if df_user['duration'].item() == "Monthly":
        result = df_soft[df_soft['Starting Price - Monthly'] <= df_user['price'].item()].sort_values(by='recommend', ascending=False)
    elif df_user['duration'].item() == "Annual":
        result = df_soft[df_soft['Starting Price - Annually'] <= df_user['price'].item()].sort_values(by='recommend', ascending=False)
    else:
        result = df_soft.sort_values(by='recommend', ascending=False)


    #filtering top three
    result_final = result[:3]
    return result_final
