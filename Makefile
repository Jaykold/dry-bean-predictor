PYTHON := python

# Define the scripts
DATA_TRAINING := src/components/model_trainer.py

# Default target
all: preprocess	

# Target to run model training
preprocess: ensure_artifacts_dir
	$(PYTHON) $(DATA_TRAINING)

ensure_artifacts_dir:
	if not exist artifacts mkdir artifacts

# Clean target (optional)
clean:
	if exist *.pyc del /Q *.pyc
	if exist __pycache__ rmdir /S /Q __pycache__

	# -del /Q *.pyc
	# -rmdir /S /Q __pycache__

.PHONY: all preprocess clean ensure_artifacts_dir



# Makefile for ML Project

# Variables
TRAIN_DATA_PATH = path/to/train_data.csv
VALIDATE_DATA_PATH = path/to/validate_data.csv
TRAIN_SCRIPT = src/components/model_trainer.py
DATA_INGEST_SCRIPT = src/components/data_ingestion.py
DATA_PREPROCESS_SCRIPT = src/components/data_preprocessing.py

# Targets

.PHONY: all data_ingest preprocess train clean

all: data_ingest preprocess train

data_ingest:
	@echo "Running Data Ingestion..."
	python $(DATA_INGEST_SCRIPT) --train_data $(TRAIN_DATA_PATH) --validate_data $(VALIDATE_DATA_PATH)

preprocess: data_ingest
	@echo "Running Data Preprocessing..."
	python $(DATA_PREPROCESS_SCRIPT) --train_data $(TRAIN_DATA_PATH) --validate_data $(VALIDATE_DATA_PATH)

train: preprocess
	@echo "Running Model Training..."
	python $(TRAIN_SCRIPT) --train_data $(TRAIN_DATA_PATH) --validate_data $(VALIDATE_DATA_PATH)

clean:
	@echo "Cleaning up..."
	rm -rf artifacts/ logs/

