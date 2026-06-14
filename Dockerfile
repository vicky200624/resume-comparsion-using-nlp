# Use the Python runtime from your runtime.txt
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (from your packages.txt and build essentials for compiling)
RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libjpeg-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "pymongo[srv]"

# Download the specific SpaCy medium model required by your NLP script
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0.tar.gz

# Copy the rest of the application code
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Expose FastAPI and Streamlit ports
EXPOSE 8000 10000

# Run the startup script
CMD ["./start.sh"]