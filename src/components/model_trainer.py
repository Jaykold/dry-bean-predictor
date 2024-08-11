from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV, KFold
from typing import Union
from pydantic import BaseModel

from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_preprocess import DataProcess

import mlflow
import os
import sys

class ModelTrainerConfig(BaseModel):
    trained_model_file_path:str=os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, val_array, model_path):
        try:
            logging.info("Split training and test input data")
            X_train, y_train = (train_array[:,:-1],
                                train_array[:,-1])
            X_val, y_val = (val_array[:,:-1],
                            val_array[:,-1])

        except Exception as e:
            raise CustomException(e, sys)








    def random_search_hyperparameter_tuning_classification(X:Union[np.array, pd.DataFrame], y:pd.Series)->pd.DataFrame:
        # input schema for MLflow
        schema = X.head(1)

        param = {
            'Logistic_Regression': {
                'model': LogisticRegression(),
                'params': {
                    'penalty': ['l1', 'l2', 'elasticnet'],
                    'C': [0.01, 0.1, 1],
                    'solver': ['newton-cg', 'lbfgs', 'liblinear']
                }
            },
            'Random_Forest': {
                'model': RandomForestClassifier(),
                'params': {
                    'n_estimators': [10, 50, 100, 200],
                    'max_features': ['sqrt', 'log2'],
                    'max_depth': [None, 10, 20, 30, 40, 50],
                    'criterion': ['gini', 'entropy']
                }
            },
            'XGBoost': {
                'model': XGBClassifier(),
                'params': {
                    'n_estimators': [50, 100, 150],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7, 9],
                    'subsample': [0.6, 0.8, 1.0],
                    'colsample_bytree': [0.6, 0.8, 1.0]
                }
            }
        }

        results = []

        kf = KFold(n_splits=5, shuffle=True, random_state=20)
        for key, values in param.items():

            with mlflow.start_run(run_name = key):

                mlflow.set_tag("developer", "Christian")

                random_search = RandomizedSearchCV(values['model'], values['params'], cv=kf, return_train_score=False, refit=True)
                random_search.fit(X, y)

                # Log parameters
                for param_name, param_value in random_search.best_params_.items():
                    mlflow.log_param(param_name, param_value)
                
                # Log metrics
                mlflow.log_metric("best_score", random_search.best_score_)
                
                # Log the model
                if key == 'XGBoost':
                    mlflow.xgboost.log_model(random_search.best_estimator_, "xgboost_model", input_example=schema)
                else:
                    mlflow.sklearn.log_model(random_search.best_estimator_, "model", input_example=schema)

                results.append({
                    'model_name': key,
                    'best_score': random_search.best_score_,
                    'best_param': random_search.best_params_
                })
        return pd.DataFrame(results, columns=['model_name', 'best_score', 'best_param'])

