# 🚀 CyberStudy Deployment Guide - Google Cloud Run

This guide will help you deploy your CyberStudy Flask application to Google Cloud Platform (GCP) Cloud Run.

## 📋 Prerequisites

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud CLI**: Install from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
3. **Docker**: Install from [docker.com](https://docker.com) (optional, Cloud Build can handle this)

## 🔧 Setup Steps

### 1. Authenticate with Google Cloud

```bash
# Login to your Google account
gcloud auth login

# Set your project ID (replace with your actual project ID)
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Update Configuration

Before deploying, update the `deploy.sh` script:

```bash
# Edit deploy.sh and replace "your-project-id" with your actual GCP project ID
nano deploy.sh
```

## 🚀 Deployment Options

### Option 1: Quick Deployment (Recommended)

```bash
# Make the script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

### Option 2: Manual Deployment

```bash
# Build and push the Docker image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cyberstudy

# Deploy to Cloud Run
gcloud run deploy cyberstudy \
    --image gcr.io/YOUR_PROJECT_ID/cyberstudy \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --set-env-vars "FLASK_ENV=production"
```

### Option 3: Using Cloud Build (Advanced)

```bash
# Trigger a build using cloudbuild.yaml
gcloud builds submit --config cloudbuild.yaml
```

## 🔐 Environment Variables

Set any additional environment variables:

```bash
gcloud run services update cyberstudy \
    --region us-central1 \
    --set-env-vars "SECRET_KEY=your-secret-key,FLASK_ENV=production"
```

## 📊 Monitoring and Logs

### View Logs
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=cyberstudy" --limit 50
```

### Monitor Performance
- Go to [Cloud Console > Cloud Run](https://console.cloud.google.com/run)
- Select your service to view metrics, logs, and performance data

## 🌐 Custom Domain (Optional)

1. **Map Custom Domain**:
   ```bash
   gcloud run domain-mappings create \
       --service cyberstudy \
       --domain your-domain.com \
       --region us-central1
   ```

2. **Update DNS**: Add the CNAME record provided by Google Cloud

## 🔄 Updating Your Application

To update your deployed application:

```bash
# Simply run the deployment script again
./deploy.sh
```

Or manually:

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cyberstudy
gcloud run deploy cyberstudy --image gcr.io/YOUR_PROJECT_ID/cyberstudy --region us-central1
```

## 💰 Cost Optimization

### Reduce Costs:
- Set `--min-instances 0` (default) to scale to zero when not in use
- Use `--cpu 1` and `--memory 1Gi` for most applications
- Monitor usage in Cloud Console

### Pricing:
- Cloud Run charges only for actual usage
- Free tier includes 2 million requests per month
- See [Cloud Run Pricing](https://cloud.google.com/run/pricing) for details

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**:
   ```bash
   # Check build logs
   gcloud builds list
   gcloud builds log BUILD_ID
   ```

2. **Service Won't Start**:
   ```bash
   # Check service logs
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=cyberstudy"
   ```

3. **Permission Issues**:
   ```bash
   # Ensure you have the right roles
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
       --member="user:YOUR_EMAIL" \
       --role="roles/run.admin"
   ```

### Health Checks:
Your application includes a health check endpoint at `/` that Cloud Run will use to verify the service is running.

## 📝 Post-Deployment Checklist

- [ ] Service is accessible via the provided URL
- [ ] All pages load correctly
- [ ] Sign-in functionality works
- [ ] Admin dashboard is accessible
- [ ] Static files (images, CSS) load properly
- [ ] Environment variables are set correctly
- [ ] Monitoring is configured
- [ ] Custom domain is mapped (if applicable)

## 🆘 Support

If you encounter issues:

1. Check the [Cloud Run Documentation](https://cloud.google.com/run/docs)
2. Review [Cloud Run Troubleshooting Guide](https://cloud.google.com/run/docs/troubleshooting)
3. Check the [Flask on Cloud Run Guide](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)

## 🎉 Success!

Once deployed, your CyberStudy application will be:
- ✅ Scalable and serverless
- ✅ Highly available
- ✅ Cost-effective
- ✅ Easy to update
- ✅ Secure by default

Your application URL will be provided after successful deployment!
