PYTHON := python

# Define the scripts
DATA_PREPROCESS := src/components/data_preprocess.py

# Default target
all: preprocess	

# Target to run data preprocessing
preprocess: ensure_artifacts_dir
	$(PYTHON) $(DATA_PREPROCESS)

ensure_artifacts_dir:
	if not exist artifacts mkdir artifacts

# Clean target (optional)
clean:
	del /Q *.pyc
	rmdir /S /Q __pycache__

.PHONY: all preprocess clean ensure_artifacts_dir
