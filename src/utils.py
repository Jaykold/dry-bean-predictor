import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
import pickle
from typing import Any, Union, Tuple
import mlflow
import pandas as pd
import numpy as np

from sklearn.model_selection import RandomizedSearchCV, KFold
from sklearn.metrics import accuracy_score, classification_report

from src.exception import CustomException
from src.logger import logging

def save_object(obj:Any, file_path:str):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        logging.info(f"File succesfully saved in {file_path}")

    except Exception as e:
        raise CustomException(e, sys) from e
    
def load_object(file_path:str):
    try:
        with open(file_path, 'rb') as f_in:
            obj=pickle.load(f_in)
            logging.info(f"File sucessfully loaded from {file_path}")
            return obj
        
    except Exception as e:
        raise CustomException(e, sys) from e
    

def initialize_mlflow():
    try:
        logging.info("Initializing database...")
        MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
        MLFLOW_EXPERIMENT_NAME = "dry-bean-detection"

        # Check if the database exists
        db_exists = os.path.exists("mlflow.db")
        if db_exists:
            # Try connecting to the database to check its validity
            try:
                engine = create_engine(MLFLOW_TRACKING_URI)
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                logging.info(f"Existing database tables: {tables}")
            except OperationalError:
                print("removing db...")
                logging.error("Database schema is outdated or corrupted.", exc_info=True)
                logging.info("Deleting the old database and creating a new one.")
                os.remove("mlflow.db")
                print("db removed")
 
        # Initialize MLflow
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

        logging.info("Mlflow database initialized")

    except Exception as e:
        raise CustomException(e, sys) from e

def random_search_hyperparameter_tuning_classification(X: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.Series], param:dict) -> pd.DataFrame:
    kf = KFold(n_splits=5, shuffle=True, random_state=20)
    
    try:
        logging.info("Starting hyperparameters tuning...")
        results = []

        for key, values in param.items():
            random_search = RandomizedSearchCV(values['model'], values['params'], cv=kf, return_train_score=False, refit=True)
            random_search.fit(X, y)

            run = mlflow.start_run(run_name=key)
            mlflow.set_tag("developer", "Christian")
            for param_name, param_value in random_search.best_params_.items():
                mlflow.log_param(param_name, param_value)
            mlflow.log_metric("best_score", random_search.best_score_)

            results.append({
                'model_name': key,
                'best_score': random_search.best_score_,
                'best_param': random_search.best_params_,
                'run_id': run.info.run_id,
                'model': random_search.best_estimator_
            })
            
            mlflow.end_run()

        results_df = pd.DataFrame(results, columns=['model_name', 'best_score', 'best_param', 'run_id', 'model'])
        logging.info("Best hyperparameters successfully loaded to a DataFrame")

        return results_df
    
    except Exception as e:
        raise CustomException(e, sys) from e

    
def log_best_model(results: pd.DataFrame, features:pd.DataFrame):
    
    try:
        # input schema for MLflow
        schema =  features.iloc[0].to_dict()
        best_model_info = results.loc[results['best_score'].idxmax()]
        best_run_id = best_model_info['run_id']
        best_model_name = best_model_info['model_name']
        model = results.loc[results['best_score'].idxmax()]['model']

        best_model_uri = f"runs:/{best_run_id}/model"

        with mlflow.start_run(run_id=best_run_id):
            if best_model_name == 'XGBoost':
                mlflow.xgboost.log_model(model, "xgboost_model", input_example=schema)
                best_model_uri = f"runs:/{best_run_id}/xgboost_model"
                logging.info("XGBoost model succesfully loaded")
            else:
                mlflow.sklearn.log_model(model, "model", input_example=schema)
                best_model_uri = f"runs:/{best_run_id}/model"
                logging.info("Sklearn model succesfully loaded")
        
        print(type(model))
        print(best_model_uri)

        return best_model_uri
    
    except Exception as e:
        raise CustomException(e, sys) from e
    
def load_model(model_uri:str):
    '''
    Load a model from MLflow.

    This function takes in the URI of the best model and loads the model from MLflow.
    It handles both scikit-learn and XGBoost models.

    Parameters:
    model_uri (str): The URI of the model to load.

    Returns:
    model: The loaded model, either a scikit-learn model or an XGBoost model.

    Raises:
    CustomException: If there is an error loading the model.
    '''

    try:
       logging.info("Getting model from Mlfow.")

       # Load model as a PyFuncModel.
       loaded_model = mlflow.pyfunc.load_model(model_uri)

       if loaded_model.loader_module == 'mlflow.sklearn':
           logging.info("Model gotten is an Sklearn model")
           skl_model = mlflow.sklearn.load_model(model_uri)
           return skl_model
       
       logging.info("Model gotten is an XGBoost model")
       xgb_model = mlflow.xgboost.load_model(model_uri)
       return xgb_model
        
    except Exception as e:
        raise CustomException(e, sys) from e


def evaluate_model(model, X_val, y_val, model_path)-> Tuple[float, str]:
    """
    This function evaluates a given classification model on validation data, 
    calculates the accuracy score, generates a classification report, 
    and saves the model to the specified path.

    Parameters:
    model: The classification model to be evaluated.
    X_val: Validation features (numpy array or pandas DataFrame).
    y_val: Validation labels (numpy array or pandas Series).
    model_path (str): The file path where the model should be saved.
    output_dict (bool): If True, return the classification report as a dictionary. Default is False.

    Returns:
    Tuple[float, Union[str, dict]]: A tuple containing the accuracy score (float) 
    and the classification report
    (str or dict, depending on the value of output_dict).

    Raises:
    CustomException: If an error occurs during model evaluation or saving.
    """

    try:
        save_object(obj=model, file_path=model_path)
        y_pred = model.predict(X_val)
        acc_score = accuracy_score(y_val, y_pred)
        report = classification_report(y_val, y_pred)
        
        return acc_score, report
    
    except Exception as e:
        raise CustomException(e, sys) from e