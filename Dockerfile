# Use the official Python image from the Docker Hub
FROM python:3.12-slim

RUN pip install -U pip

WORKDIR /app

COPY requirements.txt .

COPY setup.py .
# installs the project in executable mode
RUN pip install -e .

# Copy the rest of the application code
COPY . .

# Expose the port the application will run on
EXPOSE 9696

# Define the entry point for the container
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "app:app"]
