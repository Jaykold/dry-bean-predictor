# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Upgrade pip without caching to save space
RUN pip install --no-cache-dir -U pip

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt setup.py ./
RUN pip install -e ./

# Copy the rest of the application code
COPY . .

# Expose the port the application will run on
EXPOSE 9696

# Define the entry point for the container
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "app:app"]
