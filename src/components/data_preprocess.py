import os
import sys

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pydantic import BaseModel
from typing import Tuple

from src.components.data_ingestion import DataIngestion
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

class DataProcessConfig(BaseModel):
    labelencoder_path:str = os.path.join('artifacts', 'labelencoder.pkl')
    smote_file_path:str =os.path.join('artifacts', 'smote.pkl')
    scaler_file_path:str =os.path.join('artifacts', 'scaler.pkl')
    
class DataProcess:
    def __init__(self):
        self.data_preprocessor_config=DataProcessConfig()
        self.labelencoder = LabelEncoder()
        self.smote = SMOTE()
        self.scaler = StandardScaler()
    
    def initiate_data_preprocessing(self, train_path:str, val_path:str)->Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
            try:
                train_df:pd.DataFrame = pd.read_csv(train_path)
                val_df:pd.DataFrame = pd.read_csv(val_path)

                logging.info("Read train and validation data completed")

                # Obtain preprocessing object
                smote, scaler, label_encoder = self.smote, self.scaler, self.labelencoder
                
                # Define target column
                target = "Class"

                # Separate features and target
                features_train = train_df.drop(columns=target, axis=1)
                target_train = train_df[target]

                features_val = val_df.drop(columns=target, axis=1)
                target_val = val_df[target]

                # label encode target variable
                target_train_encoded = label_encoder.fit_transform(target_train)
                target_val_encoded = label_encoder.transform(target_val)

                logging.info("Applying preprocessing object on training dataframe and testing dataframe.")

                # Apply SMOTE to train features and target
                X_train_resampled, y_train_resampled = smote.fit_resample(
                     features_train, 
                     target_train_encoded)

                # Apply StandardScaler to train features and validation features
                X_train_scaled = scaler.fit_transform(X_train_resampled)
                X_val_scaled = scaler.transform(features_val)

                # combine scaled input features and target for train and validation data
                train_arr = np.c_[X_train_scaled, y_train_resampled]
                val_arr = np.c_[X_val_scaled, target_val_encoded]

                logging.info("Saved SMOTE and StandardScaler object.")

                save_object(obj=smote, file_path=self.data_preprocessor_config.smote_file_path )
                save_object(obj=scaler, file_path=self.data_preprocessor_config.scaler_file_path)
                save_object(obj=label_encoder, file_path=self.data_preprocessor_config.labelencoder_path)

                return (
                    train_arr,
                    val_arr,
                    features_val
                )

            except Exception as e:
                raise CustomException(e, sys) from e

if __name__=="__main__":
    obj=DataIngestion()
    train_data_path, validate_data_path, _ =obj.read_dataframe()

    data_preprocessing=DataProcess()
    train_arr, val_arr, features_val = data_preprocessing.initiate_data_preprocessing(train_data_path, validate_data_path)