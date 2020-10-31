# -*- coding: utf-8 -*-
"""StockPricePredictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uA898LNB42ySft0Jz_6vFtZQ6nUMVYZ1
"""

# import neccessary packages
# quandl documentation: https://docs.quandl.com/docs/python-tables
!pip install quandl
import pandas as pd
import numpy as np
import quandl
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

# get with 'WIKI/' returns specific stock
df = quandl.get("WIKI/UPS")  # UPS: United Parcel Service

print(df.tail())

# Adjusted price: a stock's closing price to reflect that stock's value after accounting for any corporate actions
df = df[['Adj. Close']]
print(df.tail())

# Forecasts the prediction "n" days out
forecast_out = 30
# Creates a prediction column of price shifted "x" days ahead 
df['Prediction'] = df[['Adj. Close']].shift(-forecast_out)
# Prints dataset
print(df.tail())

#### MACHINE LEARNING ####

# Create an independent dataset (X) 
# Convert the dataframe into a numpy array
X = np.array(df.drop(['Prediction'], 1))
# Removes the last 30 rows
X = X[:-forecast_out]
print(X)

# Create an dependent dataset (Y)
# Convert the dataframe into a numpy array **INCLUDING THE NaNs**
Y = np.array(df['Prediction'])
# Removes the last 30 rows
Y = Y[:-forecast_out]
print(Y)

# Split the dataset into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

# Create and train the Support Vector Machine (Regressor)
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
# Finds intercepts to create a baseline trend
svr_rbf.fit(x_train, y_train)

# Gets the accuracy of the model
svr_c = svr_rbf.score(x_test, y_test)
print('svr confidence: ', svr_c)

# Create the Linear Regression Model
lr = LinearRegression()
# Finds intercepts to create a baseline trend
lr.fit(x_train, y_train)

# Gets the accuary of the model
lr_c = lr.score(x_test, y_test)
print('linear regression confidence: ', lr_c)

# Sets x_forecast equal to the last 30 rows from "ADJ. Close"
x_forecast = np.array(df.drop(['Prediction'], 1))[-forecast_out:]
print(x_forecast)

# Predicts 30 days out using linear regression
lr_prediction = lr.predict(x_forecast)
print(lr_prediction)

# Predicts 30 days out using the Support Vector Machine
svm_prediction = svr_rbf.predict(x_forecast)
print(svm_prediction)