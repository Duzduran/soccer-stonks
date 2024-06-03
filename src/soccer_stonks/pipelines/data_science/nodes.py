import logging
from typing import Dict, Tuple


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def split_data(df: pd.DataFrame, test_size: float):
    X = df.drop("Value", axis=1)
    y = df["Value"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

def train_random_forest(X_train, y_train):
    rf = RandomForestRegressor(random_state=0)
    rf.fit(X_train, y_train)
    return rf

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    return mae
