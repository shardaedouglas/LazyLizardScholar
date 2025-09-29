#!/bin/bash

# Quick deployment script for updates
# Run this after making changes to your code

echo "🚀 Deploying CyberStudy updates to Cloud Run..."

# Build and push the new image
echo "📦 Building and pushing new image..."
gcloud builds submit --tag us-central1-docker.pkg.dev/tidy-forest-473621-j2/cyberstudy-repo/cyberstudy:latest

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy cyberstudy \
    --image us-central1-docker.pkg.dev/tidy-forest-473621-j2/cyberstudy-repo/cyberstudy:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1

echo "✅ Deployment complete!"
echo "🌐 Your app is live at: https://cyberstudy-204672424751.us-central1.run.app"
