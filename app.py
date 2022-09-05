

import pandas as pd
from email.policy import default
from flask import Flask, render_template, request, redirect, get_flashed_messages, flash
import os



#create an instance of app
app = Flask(__name__)



@app.route("/", methods = ['GET', 'POST'])
def home():
    #create empty dataframe to store user answers
    df = pd.DataFrame()
    
    if request.method == 'POST':

        data = request.form.getlist("data")
        contract = request.form.getlist("contract")
        price = request.form['Amount']
        contacts = request.form['contacts']
        duration = request.form.getlist("duration")
        Location = request.form.getlist("Location")
        features = request.form.getlist('feature')
        salesTeam = request.form.getlist('SalesTeam')
        crm = request.form.getlist('CRM')
        SEPI_tools = request.form.getlist('SEPI')
        
        
        #create a dataframe
        df['data'] = [str(data)]
        df['contract'] = [str(contract)]
        
        if price != '':
            df['price']  = int(price)
        else:
            df['price']  = price

        df['contacts']  = [str(contacts)]
        df['duration']  = [str(duration)]
        df['Location']  = [str(Location)]
        df['features'] = [str(features)]
        df['salesTeam'] = [str(salesTeam)]
        df['crm'] = [str(crm)]
        df['SEPI_tools'] = [str(SEPI_tools)]
        
        #export the dataframe to the csv file
        df.to_csv("user_data.csv")
        
        import rec
        result_final = rec.get_results(df)
        return render_template("result.html", company = result_final)
         
    else:
        
        return render_template("home.html")


@app.route("/result", methods=['GET', 'POST'])
def result():

    if request.method == 'POST':
        return render_template("home.html")
    
    return render_template("result.html")



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.secret_key='12345'
    app.run(host="0.0.0.0", port=port, debug=True)
