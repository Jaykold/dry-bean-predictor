import os
import sys

import pandas as pd
import numpy as np
import pickle
from typing import Any

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import RandomizedSearchCV

from src.exception import CustomException

def save_object(obj:Any, filename:str):
    try:
        dir_path = os.path.dirname(filename)
        os.makedirs(dir_path, exist_ok=True)
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path:str):
    try:
        with open(file_path, 'rb') as input:
            return pickle.load(input)
        
    except Exception as e:
        raise CustomException(e, sys)