
import email
import smtplib
from unicodedata import name
import pandas as pd
import numpy as np
from email.policy import default
from flask import Flask, render_template, request, redirect, get_flashed_messages, flash 
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create an instance of app
app = Flask(__name__)



#config the URI to the database
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CustomerData.sqlite3'


#createa a database object and model
db= SQLAlchemy(app)
class CustomerData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.String(200))
    contract = db.Column(db.String(200))
    price = db.Column(db.Integer)
    contacts = db.Column(db.String(200))
    duration = db.Column(db.String(200))
    Location = db.Column(db.String(200))
    features = db.Column(db.String(200))
    salesTeam = db.Column(db.String(200))
    crm = db.Column(db.String(200))
    SEPI_tools = db.Column(db.String(200))



#home page
@app.route("/", methods = ['GET', 'POST'])
def home():

    #create empty dataframe to store user answers
    df = pd.DataFrame()
    
    if request.method == 'POST':

        data = request.form.getlist("data")
        contract = request.form.getlist("contract")
        try:
            price = request.form['Amount']
        except:
            price = ''
        contacts = request.form['contacts']
        duration = request.form.getlist("duration")
        Location = request.form.getlist("Location")
        features = request.form.getlist('feature')
        salesTeam = request.form.getlist('SalesTeam')
        crm = request.form.getlist('CRM')
        SEPI_tools = request.form.getlist('SEPI')
        name = request.form.get("CustomerName")
        email = request.form.get("email")
        
        
        #Customer_data = CustomerData(name, email,date, data, contract, price,contacts, duration,Location, features,salesTeam,crm,SEPI_tools)
        customer_data = CustomerData(name = name, email=email, price=price) 
        db.session.add(customer_data)
        db.session.commit()
        

        #create a dataframe
        df['data'] = [str(data)]
        df['contract'] = [str(contract)]

        if price != '':
            df['price']  = int(price)
        else:
            df['price']  = np.nan

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
        result_final, df_user = rec.get_results(df)
        return render_template("result.html", company = result_final, user_data= df_user)
         
    else:
    
        return render_template("home.html")

    
    return render_template("home.html")



@app.route("/contact", methods=['GET', 'POST'])
def result():

    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.login("recommender.sales@outlook.com", passwrd.PASS)
    # server.sendmail("recommender.sales@outlook.com", email, message)
    # server.quit()


    # return render_template("contact.html",user_name=user_name, email=email,subject=subject,message=message )
    

    return render_template("contact.html")

    
#run the application
if __name__ == "__main__":
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.secret_key='12345'
    app.run(host="0.0.0.0", port=port, debug=True)
