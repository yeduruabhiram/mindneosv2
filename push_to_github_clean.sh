#!/bin/bash

echo "🧹 Creating clean repository for GitHub"
echo "========================================"
echo ""

# Create a new temporary directory
TEMP_DIR="mindneox_clean"
rm -rf $TEMP_DIR
mkdir $TEMP_DIR

echo "📦 Copying essential files..."

# Copy important directories
cp -r mindneox-frontend $TEMP_DIR/
cp -r hf_space_deploy $TEMP_DIR/

# Copy important files
cp fastapi_chatbot.py $TEMP_DIR/
cp requirements.txt $TEMP_DIR/
cp .gitignore $TEMP_DIR/
cp README.md $TEMP_DIR/

# Copy deployment scripts
cp deploy_*.sh $TEMP_DIR/ 2>/dev/null
cp FREE_DEPLOYMENT_*.sh $TEMP_DIR/ 2>/dev/null
cp export_training_data.py $TEMP_DIR/
cp train_custom_llm.ipynb $TEMP_DIR/

# Copy documentation
cp START_HERE.md $TEMP_DIR/
cp FREE_DEPLOYMENT_README.md $TEMP_DIR/
cp SETUP_HF_SECRETS.md $TEMP_DIR/
cp HF_SPACE_DEPLOYED.md $TEMP_DIR/

echo "✅ Files copied"
echo ""

cd $TEMP_DIR

# Initialize fresh git repo
git init
git add -A
git commit -m "Initial commit - Mindneox AI v2 with data collection and training"

# Add remote
git remote add origin https://github.com/yeduruabhiram/mindneosv2.git
git branch -M main

echo ""
echo "🚀 Ready to push to GitHub"
echo ""
echo "Run these commands:"
echo "  cd $TEMP_DIR"
echo "  git push -u origin main --force"
echo ""
echo "⚠️  This will overwrite the existing repository"
