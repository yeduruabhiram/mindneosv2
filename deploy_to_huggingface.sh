#!/bin/bash

echo "🚀 Deploying Mindneox AI to Hugging Face Spaces"
echo "================================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Get Hugging Face username
read -p "Enter your Hugging Face username: " HF_USERNAME

# Get space name
read -p "Enter space name (e.g., mindneox-ai): " SPACE_NAME

# Create space URL
SPACE_URL="https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"

echo ""
echo "📝 Space will be created at: $SPACE_URL"
echo ""

# Ask for confirmation
read -p "Continue? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "Deployment cancelled."
    exit 0
fi

# Create deployment directory
DEPLOY_DIR="hf_deployment"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

echo ""
echo "📦 Preparing files for deployment..."

# Copy necessary files
cp fastapi_chatbot.py $DEPLOY_DIR/app.py
cp requirements.txt $DEPLOY_DIR/
cp tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf $DEPLOY_DIR/ 2>/dev/null || echo "⚠️  Model file not found locally (will download on HF)"

# Create README for HF Space
cat > $DEPLOY_DIR/README.md << 'EOF'
---
title: Mindneox AI Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Mindneox AI - Intelligent Chatbot

AI-powered chatbot with conversation memory and data collection for training custom models.

## Features
- 🤖 TinyLlama-based responses
- 💾 Firebase conversation storage
- 🧠 Redis memory for context
- 📊 Pinecone vector embeddings
- 🔐 Clerk authentication support

## API Endpoints
- `POST /api/chat` - Chat with AI
- `GET /api/conversations` - Get conversation history
- `GET /api/stats` - Get usage statistics
- `GET /health` - Health check

## Environment Variables Required
- `FIREBASE_SERVICE_ACCOUNT_JSON` - Firebase credentials
- `PINECONE_API_KEY` - Pinecone API key (optional)
- `HUGGINGFACE_HUB_TOKEN` - HF token for model access

Built with FastAPI, LangChain, and LlamaCpp.
EOF

# Create Dockerfile for HF Spaces
cat > $DEPLOY_DIR/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf . 2>/dev/null || true

# Download model if not present
RUN if [ ! -f "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf" ]; then \
    wget -q https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf; \
    fi

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Run the application
CMD ["python", "app.py"]
EOF

# Update app.py to use port 7860 (HF Spaces default)
sed -i.bak 's/port=8000/port=7860/g' $DEPLOY_DIR/app.py
rm $DEPLOY_DIR/app.py.bak 2>/dev/null || true

# Create .gitignore
cat > $DEPLOY_DIR/.gitignore << 'EOF'
__pycache__/
*.pyc
.env
.venv/
venv/
*.log
.DS_Store
EOF

echo "✅ Files prepared"
echo ""
echo "🔐 Setting up Git repository..."

cd $DEPLOY_DIR

# Initialize git
git init
git add .
git commit -m "Initial deployment of Mindneox AI"

echo ""
echo "📤 Pushing to Hugging Face Spaces..."
echo ""
echo "⚠️  You will need to:"
echo "1. Create the Space on Hugging Face first:"
echo "   Go to: https://huggingface.co/new-space"
echo "   - Name: $SPACE_NAME"
echo "   - SDK: Docker"
echo "   - Hardware: CPU Basic (free)"
echo ""
echo "2. Then run these commands:"
echo ""
echo "   cd $DEPLOY_DIR"
echo "   git remote add origin https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"
echo "   git push -u origin main"
echo ""
echo "3. Set these secrets in Space settings:"
echo "   - FIREBASE_SERVICE_ACCOUNT_JSON"
echo "   - PINECONE_API_KEY (optional)"
echo ""
echo "4. Your API will be available at:"
echo "   https://${HF_USERNAME}-${SPACE_NAME}.hf.space"
echo ""

read -p "Do you want to push now? (y/n): " PUSH_NOW

if [ "$PUSH_NOW" = "y" ]; then
    echo ""
    echo "Please create the Space first, then press Enter..."
    read
    
    git remote add origin "https://huggingface.co/spaces/${HF_USERNAME}/${SPACE_NAME}"
    git push -u origin main
    
    echo ""
    echo "✅ Deployment complete!"
    echo "🌐 Your Space: $SPACE_URL"
    echo ""
    echo "⚠️  Don't forget to set environment variables in Space settings!"
else
    echo ""
    echo "📝 Manual deployment instructions saved above."
    echo "Run the commands when ready."
fi

cd ..

echo ""
echo "🎉 Deployment preparation complete!"
