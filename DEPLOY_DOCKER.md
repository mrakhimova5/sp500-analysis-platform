# Docker Deployment Guide

Deploy your S&P 500 Analysis Platform using Docker on any cloud platform.

## Prerequisites

- Docker installed
- Docker Hub account (optional, for sharing images)
- Cloud platform account (AWS, GCP, Azure, DigitalOcean, etc.)

## Quick Start - Local Testing

### 1. Build Docker Image
```bash
cd "/Users/malikam/Desktop/python/Google copy"
docker build -t sp500-analysis .
```

### 2. Run Container
```bash
docker run -p 5001:5001 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  sp500-analysis
```

### 3. Test
Open browser: http://localhost:5001

## Using Docker Compose (Recommended)

### 1. Start Application
```bash
docker-compose up -d
```

### 2. View Logs
```bash
docker-compose logs -f
```

### 3. Stop Application
```bash
docker-compose down
```

### 4. Rebuild After Changes
```bash
docker-compose up -d --build
```

## Deploy to Cloud Platforms

---

## 1. AWS Elastic Container Service (ECS)

### Prerequisites
- AWS account
- AWS CLI installed

### Steps

#### 1.1 Install AWS CLI
```bash
brew install awscli  # macOS
aws configure
```

#### 1.2 Create ECR Repository
```bash
aws ecr create-repository --repository-name sp500-analysis
```

#### 1.3 Login to ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

#### 1.4 Tag and Push Image
```bash
docker tag sp500-analysis:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/sp500-analysis:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/sp500-analysis:latest
```

#### 1.5 Create ECS Task Definition
Create `ecs-task-definition.json`:
```json
{
  "family": "sp500-analysis",
  "containerDefinitions": [{
    "name": "sp500-analysis",
    "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/sp500-analysis:latest",
    "portMappings": [{
      "containerPort": 5001,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "FLASK_ENV", "value": "production"},
      {"name": "PORT", "value": "5001"}
    ],
    "memory": 512,
    "cpu": 256
  }]
}
```

#### 1.6 Register Task
```bash
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
```

#### 1.7 Create Service
```bash
aws ecs create-service \
  --cluster default \
  --service-name sp500-analysis \
  --task-definition sp500-analysis \
  --desired-count 1
```

**Cost:** ~$15-30/month

---

## 2. Google Cloud Run (Easiest Serverless)

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Steps

#### 2.1 Install gcloud CLI
```bash
brew install google-cloud-sdk  # macOS
gcloud init
```

#### 2.2 Enable Services
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### 2.3 Build and Deploy (One Command!)
```bash
gcloud run deploy sp500-analysis \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,PORT=5001 \
  --memory 1Gi \
  --timeout 300
```

#### 2.4 Get URL
```bash
gcloud run services describe sp500-analysis --region us-central1 --format 'value(status.url)'
```

**Cost:** Pay per use (~$0.10 per 1000 requests), free tier available

---

## 3. DigitalOcean App Platform

### Steps

#### 3.1 Install doctl (optional)
```bash
brew install doctl
doctl auth init
```

#### 3.2 Push to GitHub
```bash
git push origin main
```

#### 3.3 Via Dashboard
1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Choose "GitHub" and select your repo
4. Select Dockerfile deployment
5. Set environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
6. Choose plan: $5/month (Basic)
7. Click "Launch App"

#### 3.4 Via CLI
```bash
doctl apps create --spec app.yaml
```

Create `app.yaml`:
```yaml
name: sp500-analysis
services:
- name: web
  dockerfile_path: Dockerfile
  github:
    repo: YOUR_USERNAME/sp500-analysis-platform
    branch: main
  environment_slug: docker
  instance_size_slug: basic-xxs
  instance_count: 1
  http_port: 5001
  envs:
  - key: FLASK_ENV
    value: production
  - key: PORT
    value: "5001"
```

**Cost:** $5-12/month

---

## 4. Azure Container Instances

### Prerequisites
- Azure account
- Azure CLI installed

### Steps

#### 4.1 Install Azure CLI
```bash
brew install azure-cli
az login
```

#### 4.2 Create Resource Group
```bash
az group create --name sp500-rg --location eastus
```

#### 4.3 Create Container Registry
```bash
az acr create --resource-group sp500-rg --name sp500registry --sku Basic
```

#### 4.4 Build and Push
```bash
az acr build --registry sp500registry --image sp500-analysis:latest .
```

#### 4.5 Deploy Container
```bash
az container create \
  --resource-group sp500-rg \
  --name sp500-analysis \
  --image sp500registry.azurecr.io/sp500-analysis:latest \
  --dns-name-label sp500-analysis \
  --ports 5001 \
  --environment-variables FLASK_ENV=production PORT=5001
```

#### 4.6 Get URL
```bash
az container show --resource-group sp500-rg --name sp500-analysis --query ipAddress.fqdn
```

**Cost:** ~$15-30/month

---

## 5. Railway (Easiest Overall)

### Steps

#### 5.1 Via Dashboard (Recommended)
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway auto-detects Dockerfile
7. Set environment variables in dashboard
8. Deploy automatically

#### 5.2 Via CLI
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**Cost:** $5-10/month, free $5 credit

---

## Environment Variables for All Platforms

Set these for production:

```bash
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
PORT=5001
DEBUG=False
MAX_CONTENT_LENGTH=52428800
CORS_ORIGINS=*
```

Generate secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Docker Commands Cheat Sheet

### Build
```bash
docker build -t sp500-analysis .
```

### Run
```bash
docker run -p 5001:5001 sp500-analysis
```

### Run with Environment Variables
```bash
docker run -p 5001:5001 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=abc123 \
  sp500-analysis
```

### Run in Background
```bash
docker run -d -p 5001:5001 --name sp500 sp500-analysis
```

### View Logs
```bash
docker logs -f sp500
```

### Stop Container
```bash
docker stop sp500
```

### Remove Container
```bash
docker rm sp500
```

### List Running Containers
```bash
docker ps
```

### Shell into Container
```bash
docker exec -it sp500 /bin/bash
```

### Clean Up
```bash
docker system prune -a
```

---

## Testing Docker Build Locally

### 1. Build
```bash
docker build -t sp500-analysis .
```

### 2. Run
```bash
docker run -p 5001:5001 sp500-analysis
```

### 3. Test Health Check
```bash
curl http://localhost:5001/health
```

### 4. Test Upload (from another terminal)
```bash
curl -X GET http://localhost:5001/
```

---

## Production Best Practices

### 1. Multi-Stage Build (Optional - for smaller images)
Update Dockerfile:
```dockerfile
# Builder stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD gunicorn backend_app:app --bind 0.0.0.0:$PORT
```

### 2. Use .dockerignore
Already included in your project!

### 3. Health Checks
Already configured in Dockerfile!

### 4. Logging
View logs:
```bash
docker logs -f container-name
```

### 5. Persistent Storage
Mount volumes for uploads/outputs:
```bash
docker run -v ./outputs:/app/outputs -v ./uploads:/app/uploads sp500-analysis
```

---

## Kubernetes Deployment (Advanced)

If you need to scale to 100+ users:

### 1. Create Deployment
`k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sp500-analysis
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sp500-analysis
  template:
    metadata:
      labels:
        app: sp500-analysis
    spec:
      containers:
      - name: sp500-analysis
        image: your-registry/sp500-analysis:latest
        ports:
        - containerPort: 5001
        env:
        - name: FLASK_ENV
          value: "production"
```

### 2. Apply
```bash
kubectl apply -f k8s-deployment.yaml
```

---

## Monitoring

### Docker Stats
```bash
docker stats sp500
```

### Health Check
```bash
curl http://your-domain/health
```

### Container Logs
```bash
docker logs --tail 100 -f sp500
```

---

## Troubleshooting

### Build Fails
**Check:** Dockerfile syntax
```bash
docker build --no-cache -t sp500-analysis .
```

### Container Exits Immediately
**Check:** Logs
```bash
docker logs sp500
```

### Port Already in Use
**Solution:**
```bash
docker stop $(docker ps -q --filter "publish=5001")
```

### Out of Memory
**Solution:** Increase memory limit
```bash
docker run -m 1g -p 5001:5001 sp500-analysis
```

---

## Cost Comparison

| Platform | Cost/Month | Pros | Cons |
|----------|-----------|------|------|
| Google Cloud Run | $0-5 | Pay per use, auto-scale | Cold starts |
| Railway | $5-10 | Easiest setup | Limited free tier |
| DigitalOcean | $5-12 | Simple pricing | Manual scaling |
| Heroku | $7-25 | Easy deployment | More expensive |
| AWS ECS | $15-30 | Full AWS ecosystem | Complex setup |
| Azure | $15-30 | Enterprise features | Learning curve |

---

**Deployment Ready:** ✅  
**Docker Images:** Built 🐳  
**Cloud Ready:** Yes ☁️
