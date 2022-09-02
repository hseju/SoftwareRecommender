
from select import select
from unicodedata import name
import pandas as pd
import numpy as np

import inquirer

from email.policy import default
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime



app = Flask(__name__)



@app.route("/", methods = ['GET', 'POST'])
def home():
    #create empty dataframe to store user answers
    df = pd.DataFrame()
    
    if request.method == 'POST':
        data = request.form.getlist("data")
        contract = request.form.getlist("contract")
        duration = request.form.getlist("duration")
        price = request.form['Amount']
        Location = request.form.getlist("Location")
        users = request.form['users']
        tools = request.form.getlist('tools')
        features = request.form.getlist('feature')
        crm = request.form.getlist('integrate')

        df['data'] = [data]
        df['contract'] = [contract]
        df['duration']  = [duration]
        df['price']  = price
        df['Location']  = [Location]
        df['user'] = users 
        df['tools'] = [tools]
        df['features'] = [features]
        df['crm'] = [crm]

        df.to_csv("user_data.csv")

        import rec
        return render_template("result.html", company = rec.result)
         
    else:
        
        return render_template("home.html")


@app.route("/result", methods=['GET', 'POST'])
def result():

    if request.method == 'POST':
        return redirect("home")
    
    return render_template("result.html")



if __name__ == "__main__":
    app.run()
