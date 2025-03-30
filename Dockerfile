FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for pygame
RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Health check endpoint
RUN echo 'from flask import Flask; app = Flask(__name__); @app.route("/health") ; def health(): return "OK"' > health.py

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:8080", "--timeout", "120", "app:app"]
