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
            Area=request.form.get('Area'),
            Perimeter=request.form.get('Perimeter'),
            MajorAxisLength=request.form.get('MajorAxisLength'),
            MinorAxisLength=request.form.get('MinorAxisLength'),
            Aspectratio=request.form.get('Aspectratio'),
            Eccentricity=request.form.get('Eccentricity'),
            Convexarea=request.form.get('Convexarea'),
            Equivdiameter=request.form.get('Equivdiameter'),	
            Extent=request.form.get('Extent'),
            Solidity=request.form.get('Solidity'),
            Roundness=request.form.get('Roundness'),
            Compactness=request.form.get('Compactness'),
            ShapeFactor1=request.form.get('ShapeFactor1'),
            ShapeFactor2=request.form.get('ShapeFactor2'),
            ShapeFactor3=request.form.get('ShapeFactor3'),
            ShapeFactor4=request.form.get('ShapeFactor4')
        )
        pred_df=data.to_dataframe()
        print(pred_df)
        
        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)