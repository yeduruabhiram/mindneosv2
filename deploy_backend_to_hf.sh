#!/bin/bash

# Deploy Backend to Hugging Face Spaces
# Space URL: https://huggingface.co/spaces/yeduru/mindneox.ai1

echo "🚀 Deploying MindNeox Backend to Hugging Face Spaces..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install git first.${NC}"
    exit 1
fi

# Check if HF CLI is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo -e "${BLUE}📦 Installing Hugging Face CLI...${NC}"
    curl -LsSf https://hf.co/cli/install.sh | bash
fi

# Space details
SPACE_NAME="yeduru/mindneox.ai1"
SPACE_URL="https://huggingface.co/spaces/$SPACE_NAME"

echo -e "${BLUE}📍 Space: $SPACE_URL${NC}"
echo ""

# Create temporary deployment directory
DEPLOY_DIR="hf_deploy_temp"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

echo -e "${BLUE}📦 Preparing files for deployment...${NC}"

# Copy necessary files
cp fastapi_chatbot.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/
cp HF_Dockerfile $DEPLOY_DIR/Dockerfile
cp -r models $DEPLOY_DIR/ 2>/dev/null || echo "No models directory found"

# Copy Firebase credentials if exists
if [ -f "mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json" ]; then
    cp mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json $DEPLOY_DIR/
    echo -e "${GREEN}✅ Firebase credentials copied${NC}"
fi

# Create README.md for the Space
cat > $DEPLOY_DIR/README.md << 'EOF'
---
title: MindNeox AI Backend
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# MindNeox.AI Backend

AI-powered chatbot backend with FastAPI, Firebase, and Pinecone integration.

## Features

- 🤖 AI Chat with TinyLlama
- 🔥 Firebase Firestore integration
- 📊 Pinecone vector database
- ⚡ Redis caching
- 🚀 FastAPI framework

## API Endpoints

- `GET /` - Health check
- `POST /api/chat` - Chat with AI
- `GET /api/user/{user_id}/history` - Get chat history
- `GET /api/user/{user_id}/predict` - Get personalized greeting

## Environment Variables

Set these in your Space settings:

- `PINECONE_API_KEY` - Your Pinecone API key
- `PINECONE_ENVIRONMENT` - Pinecone environment
- `REDIS_HOST` - Redis host (optional)
- `REDIS_PORT` - Redis port (optional)
- `REDIS_PASSWORD` - Redis password (optional)

## Tech Stack

- FastAPI
- TinyLlama (1.1B parameters)
- Firebase Firestore
- Pinecone Vector DB
- Redis Cache
EOF

echo -e "${GREEN}✅ Files prepared${NC}"
echo ""

# Initialize git in deploy directory
cd $DEPLOY_DIR
git init
git remote add origin https://huggingface.co/spaces/$SPACE_NAME

echo -e "${BLUE}🔐 Please enter your Hugging Face token when prompted${NC}"
echo -e "${BLUE}   Generate one at: https://huggingface.co/settings/tokens${NC}"
echo ""

# Add all files
git add .
git commit -m "Deploy MindNeox AI Backend"

# Push to HF Spaces
echo -e "${BLUE}📤 Pushing to Hugging Face Spaces...${NC}"
git push -f origin main

cd ..
rm -rf $DEPLOY_DIR

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}🌐 Your Space: $SPACE_URL${NC}"
echo -e "${BLUE}📊 Check build status at: $SPACE_URL/settings${NC}"
echo ""
echo -e "${BLUE}⚙️  Don't forget to set environment variables in Space settings!${NC}"
echo ""
