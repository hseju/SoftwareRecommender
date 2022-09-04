
import pandas as pd
from email.policy import default
from flask import Flask, render_template, request, redirect
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
        duration = request.form.getlist("duration")
        price = request.form['Amount']
        Location = request.form.getlist("Location")
        users = request.form['users']
        tools = request.form.getlist('tools')
        features = request.form.getlist('feature')
        crm = request.form.getlist('integrate')

        df['data'] = [str(data)]
        df['contract'] = [str(contract)]
        df['duration']  = [str(duration)]
        if price != '':
            df['price']  = int(price)
        else:
            df['price']  = price
        df['Location']  = [str(Location)]
        df['user'] = int(users) 
        df['tools'] = [str(tools)]
        df['features'] = [str(features)]
        df['crm'] = [str(crm)]

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

    app.run(host="0.0.0.0", port=port, debug=True)
