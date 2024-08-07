import sys
import pandas as pd
from src.exception import CustomException


class PredictPipeline:
    def __init__(self):
        pass

class CustomData:
    def __init__(self,
                Area:float,
                Perimeter:float,
                MajorAxisLength:float,
                MinorAxisLength: float,
                AspectRatio: float,
                Eccentricity: float,
                ConvexArea: float,
                EquivDiameter: float,	
                Extent: float,
                Solidity: float,
                Roundness: float,
                Compactness: float,
                ShapeFactor1: float,
                ShapeFactor2: float,
                ShapeFactor3: float,
                ShapeFactor4: float):
        
        self.area = Area
        self.perimeter = Perimeter
        self.majoraxislength = MajorAxisLength
        self.minoraxislength = MinorAxisLength
        self.aspectratio = AspectRatio
        self.eccentricity = Eccentricity
        self.convexarea = ConvexArea
        self.equivdiameter = EquivDiameter
        self.extent = Extent
        self.solidity = Solidity
        self.roundness = Roundness
        self.compactness = Compactness
        self.shapefactor1 = ShapeFactor1
        self.shapefactor2 = ShapeFactor2
        self.shapefactor3 = ShapeFactor3
        self.shapefactor4 = ShapeFactor4

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