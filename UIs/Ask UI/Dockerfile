# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to /app
COPY requirements.txt ./

# Copy the application code to /app/src
COPY src/ ./src/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set HOME to a writable directory (and create the directory)
ENV HOME=/app
RUN mkdir -p /app/.streamlit
RUN chmod 777 /app/.streamlit # Add this line to give write permissions

# Create Streamlit config file to disable XSRF and set max upload size
RUN echo "[server]\nenableXsrfProtection = false\nmaxUploadSize = 100" > /app/.streamlit/config.toml

# Expose the port that Streamlit uses (default is 8501)
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://0.0.0.0:8501/_stcore/health

# Command to run the Streamlit application
ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
