# Dry Bean Classification Analysis 🚀

This project is focused on the classification of different types of dry beans using a machine learning approach. The dataset consists of 16 feature columns and 1 target column "Class" with 7 unique classes. The project is implemented with several packages and tools to facilitate data preprocessing, model training, and evaluation.

Table of Contents
* Dataset
* Installation
* Usage
* Components
* Model Training
* Logging and Monitoring
* Contributing

## Dataset
The dataset used in this project includes the following features:
* Area
* Perimeter
* MajorAxisLength
* MinorAxisLength
* AspectRatio
* Eccentricity
* ConvexArea
* EquivDiameter
* Extent
* Solidity
* Roundness
* Compactness
* ShapeFactor1
* ShapeFactor2
* ShapeFactor3
* ShapeFactor4
* Class {
    * Seker
    * Barbunya
    * Bombay
    * Cali
    * Horoz
    * Sira
    * Dermason
}

The target column is Class and it has 7 unique classes.

## Installation & Requirements
To run this project, you need to install the following packages:
* mlflow
* jupyter
* scikit-learn
* pandas
* seaborn
* ucimlrepo
* xgboost
* imbalanced-learn
* Flask
* tqdm
* pydantic
* pylint
* matplotlib

You can install the required packages using the provided `conda_dependencies.yml` file:
`conda env create -f conda_dependencies.yml`

Or using `requirements.txt`:

```pip install -r requirements.txt```

Alternatively, you can use the `setup.py` file to install the project and its dependencies:
`pip install .`

Usage
1. Clone the repository
`git clone https://github.com/Jaykold/dry-bean-predictor.git`

2. Navigate to the project directory
`cd dry-bean-predictor`

3. Run Jupyter Notebook
`jupyter notebook`

4. Open `dry_bean.ipynb` and execute the cells to preprocess the data and train the model

## Components

### Data Ingestion
The `data_ingestion.py` script is responsible for loading the dataset and performing initial data checks.

### Data Preprocessing
The `data_preprocess.py` script handles data cleaning, feature engineering, and splitting the data into training and testing sets.

### Model Training
The `model_trainer.py` script trains a classification model using the preprocessed data and evaluates its performance.

### Pipeline
The `pipeline` directory contains script for model prediction.
* `predict.py`

### Model training
To train the model, run the `model_trainer.py` script:
`python src/components/model_trainer.py`

This will train the model and save the results to the `artifacts` directory.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

