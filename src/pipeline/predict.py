import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from pydantic import BaseModel


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features:pd.DataFrame):
        try:
            # Get artifacts path
            model_path = 'artifacts/model.pkl'
            scaler_path = 'artifacts/scaler.pkl'
            
            # Load the model, SMOTE, and scaler objects
            model = load_object(model_path)
            scaler = load_object(scaler_path)

            # Transform the features using scaler
            data_scaled = scaler.transform(features)

            # Make predictions using the model
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            # Raise a custom exception if an error occurs
            raise CustomException(e, sys)
      


class CustomData(BaseModel):
            area:float
            perimeter:float
            majoraxislength:float
            minoraxislength: float
            aspectratio: float
            eccentricity: float
            convexarea: float
            equivdiameter: float
            extent: float
            solidity: float
            roundness: float
            compactness: float
            shapefactor1: float
            shapefactor2: float
            shapefactor3: float
            shapefactor4: float

            def to_dataframe(self):
                try:
                    data = {
                        'Area': [self.area],
                        'Perimeter': [self.perimeter],
                        'MajorAxisLength': [self.majoraxislength],
                        'MinorAxisLength': [self.minoraxislength],
                        'AspectRatio': [self.aspectratio],
                        'Eccentricity': [self.eccentricity],
                        'ConvexArea': [self.convexarea],
                        'EquivDiameter': [self.equivdiameter],
                        'Extent': [self.extent],
                        'Solidity': [self.solidity],
                        'Roundness': [self.roundness],
                        'Compactness': [self.compactness],
                        'ShapeFactor1': [self.shapefactor1],
                        'ShapeFactor2': [self.shapefactor2],
                        'ShapeFactor3': [self.shapefactor3],
                        'ShapeFactor4': [self.shapefactor4]
                    }
                    return pd.DataFrame(data)
                except Exception as e:
                    raise CustomException(e, sys)