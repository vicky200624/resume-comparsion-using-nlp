FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libjpeg-dev \
    build-essential \
    openssl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "pymongo[srv]"

RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0.tar.gz

COPY . .

# ADD THIS LINE RIGHT HERE:
RUN mkdir -p uploads

RUN chmod +x start.sh

EXPOSE 8000 10000

CMD ["./start.sh"]