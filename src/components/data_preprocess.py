import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from typing import Union, Tuple
import numpy as np

def encode(df:pd.DataFrame, label:pd.Series, labelencoder:LabelEncoder)->pd.Series:
    df[label] = labelencoder.transform(df[label])
    return df[label]

def split_data(df:pd.DataFrame, label:pd.Series)->Tuple:

    X = df.drop(columns=label)
    y = df[label]

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify = y)

    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.4, random_state=42, stratify = y_temp)

    return X_train, X_val, X_test, y_train, y_val, y_test

def sampling(X_train:pd.DataFrame, y_train:pd.Series):
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    return X_train_res, y_train_res

def standardize(X_train_res:pd.DataFrame, X_val:pd.DataFrame, scaler:StandardScaler):
    X_train_res = scaler.fit_transform(X_train_res)
    X_val = scaler.transform(X_val)

    return X_train_res, X_val