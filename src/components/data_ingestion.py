from ucimlrepo import fetch_ucirepo 
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

def read_dataframe()->pd.DataFrame:
    # fetch dataset 
    dry_bean = fetch_ucirepo(id=602) 
    
    # data (as pandas dataframes) 
    X = dry_bean.data.features 
    y = dry_bean.data.targets

    return pd.concat([X, y], axis=1)