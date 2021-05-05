from flask import Flask, render_template
app = Flask(__name__)

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('fin_random_forest_model.pkl', 'rb'))

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    
    if request.method == 'POST':
        Year =request.form['Year']
        Present_Price=(request.form['Present_Price'])
        Kms_Driven=(request.form['Kms_Driven'])
        Owner=(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0

        columns = ['Year', 'Present_Price', 'Kms_Driven', 'Owner', 'Transmission_Manual',
       'Seller_Type_Individual', 'Fuel_Type_Diesel', 'Fuel_Type_Petrol']
        rows = [[Year, Present_Price, Kms_Driven, Owner, Transmission_Manual,
        Seller_Type_Individual, Fuel_Type_Diesel, Fuel_Type_Petrol]]

        input = pd.DataFrame(rows, columns =columns) 
        
        prediction=model.predict(input)
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return 'If not working'
        #return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)