import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from pydantic import BaseModel
from typing import Union


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features:pd.DataFrame):
        try:
            # Get artifacts path
            model_path = 'artifacts/model.pkl'
            scaler_path = 'artifacts/scaler.pkl'
            labelencoder_path = 'artifacts/labelencoder.pkl'
            
            # Load the model, SMOTE, and scaler objects
            model = load_object(file_path=model_path)
            scaler = load_object(file_path=scaler_path)
            labelencoder = load_object(file_path=labelencoder_path)

            # Transform the features using scaler
            data_scaled = scaler.transform(features)
            print(data_scaled)
            # Make predictions using the model
            preds = model.predict(data_scaled).astype(int)
            print(preds)
            result = labelencoder.inverse_transform(preds)
            return result
        
        except Exception as e:
            # Raise a custom exception if an error occurs
            raise CustomException(e, sys) from e
      


class CustomData(BaseModel):
            Area:Union[float, int]
            Perimeter:float
            MajorAxisLength:float
            MinorAxisLength: float
            Aspectratio: float
            Eccentricity: float
            Convexarea: float
            Equivdiameter: float
            Extent: float
            Solidity: float
            Roundness: float
            Compactness: float
            ShapeFactor1: float
            ShapeFactor2: float
            ShapeFactor3: float
            ShapeFactor4: float

            def to_dataframe(self):
                try:
                    data = {
                        'Area': [self.Area],
                        'Perimeter': [self.Perimeter],
                        'MajorAxisLength': [self.MajorAxisLength],
                        'MinorAxisLength': [self.MinorAxisLength],
                        'AspectRatio': [self.Aspectratio],
                        'Eccentricity': [self.Eccentricity],
                        'ConvexArea': [self.Convexarea],
                        'EquivDiameter': [self.Equivdiameter],
                        'Extent': [self.Extent],
                        'Solidity': [self.Solidity],
                        'Roundness': [self.Roundness],
                        'Compactness': [self.Compactness],
                        'ShapeFactor1': [self.ShapeFactor1],
                        'ShapeFactor2': [self.ShapeFactor2],
                        'ShapeFactor3': [self.ShapeFactor3],
                        'ShapeFactor4': [self.ShapeFactor4]
                    }
                    return pd.DataFrame(data)
                
                except Exception as e:
                    raise CustomException(e, sys) from e