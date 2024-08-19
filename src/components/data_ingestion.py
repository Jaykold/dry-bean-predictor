import os
import sys
from typing import Tuple
import warnings
import pandas as pd

from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from ucimlrepo import fetch_ucirepo # Get data from UCI ML repo

from src.exception import CustomException
from src.logger import logging

warnings.filterwarnings("ignore")

class DataIngestionConfig(BaseModel):
    raw_data_path: str = os.path.join('artifacts', "data.csv")
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    validate_data_path: str = os.path.join('artifacts', "validate.csv")


class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config=DataIngestionConfig()
       
        if os.path.exists(self.ingestion_config.raw_data_path):
            # Check if the file is readable
            if os.access(self.ingestion_config.raw_data_path, os.W_OK):
                print("File is writeable")
            else:
                print("File is not writeable, check permissions")
        else:
            print("File does not exist")

    def read_dataframe(self)->Tuple[str, str, str]:
        logging.info("Reading data from UCI Machine Learning Repository")
        try:
            # fetch dataset 
            dry_bean = fetch_ucirepo(id=602) 
            logging.info("Read data from UCI Machine Learning Repository")

            # data (as pandas dataframes) 
            X = dry_bean.data.features 
            y = dry_bean.data.targets            
            df = pd.concat([X, y], axis=1)
            
            #print(self.ingestion_config.raw_data_path)

            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info("Train test split initiated")
            train_df, temp = train_test_split(df, 
                                              test_size=0.3, 
                                              random_state=42, 
                                              stratify=df['Class'])
            
            val_df, test_df = train_test_split(temp, 
                                               test_size=0.4, 
                                               random_state=42, 
                                               stratify=temp['Class'])

            logging.info("Save train, test, and validate dataset")
            train_df.to_csv(self.ingestion_config.train_data_path, index=False)
            test_df.to_csv(self.ingestion_config.test_data_path, index=False)
            val_df.to_csv(self.ingestion_config.validate_data_path, index=False)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.validate_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys) from e