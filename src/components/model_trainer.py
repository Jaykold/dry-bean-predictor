import os
import sys
import numpy as np
from pydantic import BaseModel

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_preprocess import DataProcess
from src.utils import (
    initialize_mlflow,
    random_search_hyperparameter_tuning_classification,
    log_best_model,
    load_model,
    evaluate_model)


class ModelTrainerConfig(BaseModel):
    trained_model_file_path:str=os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self, train_array:np.ndarray,
                               val_array:np.ndarray,
                               features)->str:

        try:
            logging.info("Split training and test input data")
            X_train, y_train = (train_array[:,:-1],
                                train_array[:,-1])
            X_val, y_val = (val_array[:,:-1],
                            val_array[:,-1])
            
            params = {
                'Logistic_Regression': {
                    'model': LogisticRegression(),
                    'params': {
                    'penalty': ['l1', 'l2'],
                    'C': [0.01, 0.1],
                    'solver': ['newton-cg', 'lbfgs']
                    }
                },
                'Random_Forest': {
                    'model': RandomForestClassifier(),
                    'params': {
                    'n_estimators': [10, 50],
                    'max_features': ['sqrt', 'log2'],
                    'max_depth': [None, 10, 20],
                    'criterion': ['gini', 'entropy']
                    }
                },
                'XGBoost': {
                    'model': XGBClassifier(),
                    'params': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5],
                    'subsample': [0.6, 0.8],
                    'colsample_bytree': [0.6, 0.8]
                    }
                }
            }

            initialize_mlflow()
            models_result:dict = random_search_hyperparameter_tuning_classification(
                X_train,
                y_train,
                params)
            best_model_uri = log_best_model(models_result, features)
            model = load_model(best_model_uri)
            acc_score, report = evaluate_model(model,
                                               X_val,
                                               y_val,
                                               model_path=self.model_trainer_config.trained_model_file_path)

            return f"Accuracy score: {acc_score}, \nClassification report:\n{report}"

        except Exception as e:
            raise CustomException(e, sys) from e
        

if __name__=="__main__":
    # data ingestion phase
    obj=DataIngestion()
    train_data_path, validate_data_path, _ =obj.read_dataframe()

    # data preprocessing phase
    data_preprocessing=DataProcess()
    train_arr, val_arr, features_val = data_preprocessing.initiate_data_preprocessing(
        train_data_path,
        validate_data_path)

    # model training
    model_training=ModelTrainer()
    print(model_training.initiate_model_trainer(train_arr, val_arr, features_val))