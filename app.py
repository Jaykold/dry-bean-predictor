from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from src.pipeline.predict import CustomData, PredictPipeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_data():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data=CustomData(
            Area=request.form.get('area'),
            Perimeter=request.form.get('perimeter'),
            MajorAxisLength=request.form.get('majoraxislength'),
            MinorAxisLength=request.form.get('minoraxislength'),
            AspectRatio=request.form.get('aspectratio'),
            Eccentricity=request.form.get('eccentricity'),
            ConvexArea=request.form.get('convexarea'),
            EquivDiameter=request.form.get('equivdiameter'),	
            Extent=request.form.get('extent'),
            Solidity=request.form.get('solidity'),
            Roundness=request.form.get('roundness'),
            Compactness=request.form.get('compactness'),
            ShapeFactor1=request.form.get('shapefactor1'),
            ShapeFactor2=request.form.get('shapefactor2'),
            ShapeFactor3=request.form.get('shapefactor3'),
            ShapeFactor4=request.form.get('shapefactor4')
        )
        pred_df=data.to_dataframe()
        print(pred_df)
        
        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)