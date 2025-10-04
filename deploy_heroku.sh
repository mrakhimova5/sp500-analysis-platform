#!/bin/bash

# Heroku Quick Deploy Script
# Run this script to automatically deploy to Heroku

echo "🚀 S&P 500 Analysis Platform - Heroku Deployment Script"
echo "=========================================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo -e "${RED}❌ Heroku CLI not found!${NC}"
    echo "Please install it first:"
    echo "  macOS: brew tap heroku/brew && brew install heroku"
    echo "  Or visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo -e "${GREEN}✅ Heroku CLI found${NC}"

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${YELLOW}📦 Initializing git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit - S&P 500 Analysis Platform"
    echo -e "${GREEN}✅ Git initialized${NC}"
else
    echo -e "${GREEN}✅ Git repository exists${NC}"
fi

# Login to Heroku
echo -e "${YELLOW}🔐 Logging into Heroku...${NC}"
heroku login

# Ask for app name
read -p "Enter your Heroku app name (e.g., sp500-analysis-app): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo -e "${RED}❌ App name cannot be empty${NC}"
    exit 1
fi

# Create Heroku app
echo -e "${YELLOW}🏗️  Creating Heroku app: $APP_NAME${NC}"
if heroku create $APP_NAME; then
    echo -e "${GREEN}✅ App created successfully${NC}"
else
    echo -e "${YELLOW}⚠️  App might already exist, continuing...${NC}"
fi

# Generate secret key
echo -e "${YELLOW}🔑 Generating secret key...${NC}"
SECRET_KEY=$(openssl rand -hex 32)

# Set environment variables
echo -e "${YELLOW}⚙️  Setting environment variables...${NC}"
heroku config:set FLASK_ENV=production --app $APP_NAME
heroku config:set SECRET_KEY=$SECRET_KEY --app $APP_NAME
heroku config:set MAX_CONTENT_LENGTH=52428800 --app $APP_NAME
heroku config:set DEBUG=False --app $APP_NAME
heroku config:set CORS_ORIGINS=* --app $APP_NAME
echo -e "${GREEN}✅ Environment variables set${NC}"

# Add Heroku remote if not exists
if ! git remote | grep -q heroku; then
    echo -e "${YELLOW}🔗 Adding Heroku remote...${NC}"
    heroku git:remote -a $APP_NAME
    echo -e "${GREEN}✅ Heroku remote added${NC}"
fi

# Deploy to Heroku
echo -e "${YELLOW}🚀 Deploying to Heroku...${NC}"
git push heroku main || git push heroku master

# Open the app
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Your app is deployed at:"
heroku info --app $APP_NAME | grep "Web URL"
echo ""
echo "Useful commands:"
echo "  View logs:     heroku logs --tail --app $APP_NAME"
echo "  Open app:      heroku open --app $APP_NAME"
echo "  Restart app:   heroku restart --app $APP_NAME"
echo "  Config vars:   heroku config --app $APP_NAME"
echo ""

# Ask if user wants to open the app
read -p "Would you like to open the app in your browser? (y/n): " OPEN_APP

if [[ $OPEN_APP == "y" || $OPEN_APP == "Y" ]]; then
    heroku open --app $APP_NAME
fi

echo -e "${GREEN}✅ All done! Your app is live!${NC}"
