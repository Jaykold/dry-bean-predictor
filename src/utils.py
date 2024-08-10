import os
import sys

import pandas as pd
import numpy as np
import pickle
from typing import Any

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import RandomizedSearchCV

from src.exception import CustomException

def save_object(obj:Any, file_path:str):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path:str):
    try:
        with open(file_path, 'rb') as input:
            return pickle.load(input)
        
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train,X_val,y_val,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = RandomizedSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_val_pred = model.predict(X_val)

            test_model_score = accuracy_score(y_val, y_val_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)