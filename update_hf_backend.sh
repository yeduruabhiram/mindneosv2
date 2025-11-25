#!/bin/bash

echo "🚀 Updating Hugging Face Space Backend..."
echo "=========================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed"
    exit 1
fi

# HF Space URL
HF_SPACE="https://huggingface.co/spaces/yeduru/abhi"
TEMP_DIR="hf_space_temp"

echo ""
echo "📦 Cloning your HF Space..."
rm -rf $TEMP_DIR
git clone $HF_SPACE $TEMP_DIR

if [ ! -d "$TEMP_DIR" ]; then
    echo "❌ Failed to clone HF Space"
    exit 1
fi

cd $TEMP_DIR

echo ""
echo "📝 Updating backend files..."

# Copy the updated app.py
cp ../hf_space_deploy/app.py ./app.py

# Copy Firebase credentials
cp ../hf_space_deploy/firebase-credentials.json ./firebase-credentials.json

# Check if files exist
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found"
    exit 1
fi

if [ ! -f "firebase-credentials.json" ]; then
    echo "⚠️  firebase-credentials.json not found"
fi

echo ""
echo "✅ Files updated successfully"
echo ""
echo "📤 Committing and pushing changes..."

git add app.py firebase-credentials.json
git commit -m "Fix: Add Firebase credentials file for data storage"
git push

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Backend updated successfully!"
    echo "=========================================="
    echo ""
    echo "🌐 Your Space: https://huggingface.co/spaces/yeduru/abhi"
    echo ""
    echo "⏳ Wait 1-2 minutes for the Space to rebuild"
    echo "🧪 Then test: https://yeduru-abhi.hf.space/api/chat"
    echo ""
else
    echo ""
    echo "❌ Failed to push changes"
    echo "You may need to enter your HF token as password"
    exit 1
fi

cd ..
rm -rf $TEMP_DIR

echo "✨ Done!"
