#!/bin/bash

# Force Deploy Backend to Hugging Face Spaces
echo "🚀 Deploying MindNeox Backend to Hugging Face Spaces..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Space details
SPACE_NAME="yeduru/mindneox.ai1"
SPACE_URL="https://huggingface.co/spaces/$SPACE_NAME"

echo -e "${BLUE}📍 Space: $SPACE_URL${NC}"

# Create deployment directory
DEPLOY_DIR="hf_deploy_temp"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

echo -e "${BLUE}📦 Preparing files...${NC}"

# Copy files
cp fastapi_chatbot.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/
cp HF_Dockerfile $DEPLOY_DIR/Dockerfile

# Copy Firebase credentials
if [ -f "mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json" ]; then
    cp mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json $DEPLOY_DIR/
fi

# Create README
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

AI-powered chatbot backend with FastAPI, Firebase, and Pinecone.

## Features
- 🤖 AI Chat with TinyLlama
- 🔥 Firebase Firestore
- 📊 Pinecone Vector DB
- ⚡ Redis Cache

## API Endpoints
- `POST /api/chat` - Chat with AI
- `GET /api/user/{user_id}/history` - Get history
EOF

cd $DEPLOY_DIR

# Initialize git
git init
git checkout -b main
git remote add origin https://huggingface.co/spaces/$SPACE_NAME

# Add and commit
git add .
git commit -m "Deploy MindNeox AI Backend"

echo ""
echo -e "${BLUE}🔐 Enter your Hugging Face token when prompted${NC}"
echo -e "${BLUE}   Get it from: https://huggingface.co/settings/tokens${NC}"
echo ""

# Force push
git push -f origin main

cd ..
rm -rf $DEPLOY_DIR

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${BLUE}🌐 Space: $SPACE_URL${NC}"
echo ""
