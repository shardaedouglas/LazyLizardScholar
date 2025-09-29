#!/bin/bash

# Start script for Cloud Run deployment
# This script handles both development and production modes

set -e

# Set default port if not provided
export PORT=${PORT:-8080}

echo "Starting CyberStudy application on port $PORT"

# Check if we're in development mode
if [ "$FLASK_ENV" = "development" ]; then
    echo "Running in development mode with Flask dev server"
    python app.py
else
    echo "Running in production mode with Gunicorn"
    exec gunicorn \
        --bind 0.0.0.0:$PORT \
        --workers 1 \
        --threads 8 \
        --timeout 0 \
        --keep-alive 2 \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --preload \
        app:app
fi