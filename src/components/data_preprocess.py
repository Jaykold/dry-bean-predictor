import os
import sys

import numpy as np
import pandas as pd
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from pydantic import BaseModel

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

class DataProcessConfig(BaseModel):
    smote_file_path:str =os.path.join('artifacts', 'smote.pkl')
    scaler_file_path:str =os.path.join('artifacts', 'scaler.pkl')
    model_file_path:str =os.path.join('artifacts', 'model.pkl')

class DataProcess:
    def __init__(self):
        self.data_preprocessor_config=DataProcessConfig()

    def get_data_preprocessed_object(self):
        try:
            self.smote = SMOTE()
            self.scaler = StandardScaler()

            return self.smote, self.scaler

        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_preprocessing(self, train_path:str, val_path:str):
            try:
                train_df:pd.DataFrame = pd.read_csv(train_path)
                val_df:pd.DataFrame = pd.read_csv(val_path)

                logging.info("Read train and validation data completed")

                # Obtain preprocessing object
                smote, scaler = self.get_data_preprocessed_object()
                
                # Define target column
                target = "Class"

                # Separate features and target
                features_train = train_df.drop(columns=target, axis=1)
                target_train = train_df[target]

                features_val = val_df.drop(columns=target, axis=1)
                target_val = val_df[target]

                # label encode target variable
                label_encoder = LabelEncoder()
                target_train_encoded = label_encoder.fit_transform(target_train)
                target_val_encoded = label_encoder.transform(target_val)

                logging.info("Applying preprocessing object on training dataframe and testing dataframe.")

                # Apply SMOTE to train features and target
                X_train_resampled, y_train_resampled = smote.fit_resample(features_train, target_train_encoded)

                # Apply StandardScaler to train features and validation features
                X_train_scaled = scaler.fit_transform(X_train_resampled)
                X_val_scaled = scaler.transform(features_val)

                # combine scaled input features and target for train and validation data
                train_arr = np.c_[X_train_scaled, y_train_resampled]
                val_arr = np.c_[X_val_scaled, target_val_encoded]

                logging.info("Saved SMOTE and StandardScaler object.")

                save_object(obj=smote, file_path=self.data_preprocessor_config.smote_file_path )
                save_object(obj=scaler, file_path=self.data_preprocessor_config.scaler_file_path)

                return (
                    train_arr,
                    val_arr,
                    self.data_preprocessor_config.model_file_path
                )

            except Exception as e:
                raise CustomException(e, sys)