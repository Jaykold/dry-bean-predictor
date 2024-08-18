import os
import pandas as pd
from src.components.data_ingestion import DataIngestion

def setup_ingestion():
    ingestion = DataIngestion()
    return ingestion

def test_file_paths_exist():
    ingestion = setup_ingestion()
    train_path, validate_path, test_path = ingestion.read_dataframe()

    assert os.path.exists(train_path), f"Train file does not exist at {train_path}"
    assert os.path.exists(validate_path), f"Validate file does not exist at {validate_path}"
    assert os.path.exists(test_path), f"Test file does not exist at {test_path}"

def test_file_contents():
    ingestion = setup_ingestion()
    train_path, validate_path, test_path = ingestion.read_dataframe()

    train_df = pd.read_csv(train_path)
    validate_df = pd.read_csv(validate_path)
    test_df = pd.read_csv(test_path)

    assert not train_df.empty, "Train dataframe is empty"
    assert not validate_df.empty, "Validate dataframe is empty"
    assert not test_df.empty, "Test dataframe is empty"

def test_class_distribution():
    ingestion = setup_ingestion()
    train_path, validate_path, test_path = ingestion.read_dataframe()

    train_df = pd.read_csv(train_path)
    validate_df = pd.read_csv(validate_path)
    test_df = pd.read_csv(test_path)

    assert 'Class' in train_df.columns, "Class column not found in train dataframe"
    assert 'Class' in validate_df.columns, "Class column not found in validate dataframe"
    assert 'Class' in test_df.columns, "Class column not found in test dataframe"

    # Optional: Check the distribution of classes
    train_class_dist = train_df['Class'].value_counts(normalize=True)
    validate_class_dist = validate_df['Class'].value_counts(normalize=True)
    test_class_dist = test_df['Class'].value_counts(normalize=True)

    assert all(train_class_dist.index == validate_class_dist.index), "Class distribution mismatch between train and validate datasets"
    assert all(train_class_dist.index == test_class_dist.index), "Class distribution mismatch between train and test datasets"
