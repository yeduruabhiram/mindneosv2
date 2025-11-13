#!/bin/bash

echo "🔄 Updating Hugging Face Space: yeduru/abhi"
echo "============================================"

# Copy latest backend
echo "📦 Copying latest backend..."
cp fastapi_chatbot.py hf_space_deploy/app.py
cp requirements.txt hf_space_deploy/

# Check for changes
if git -C hf_space_deploy diff --quiet; then
    echo "✅ No changes detected. Space is up to date!"
    exit 0
fi

echo ""
echo "📝 Changes detected:"
git -C hf_space_deploy status --short

echo ""
read -p "Commit message (or press Enter for default): " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update backend - $(date '+%Y-%m-%d %H:%M')"
fi

echo ""
echo "🚀 Committing and pushing..."
git -C hf_space_deploy add -A
git -C hf_space_deploy commit -m "$COMMIT_MSG"
git -C hf_space_deploy push origin main

echo ""
echo "✅ Update complete!"
echo "🌐 Your Space: https://yeduru-abhi.hf.space"
echo "📊 Check logs: https://huggingface.co/spaces/yeduru/abhi"
echo ""
echo "⏳ Space will rebuild automatically (takes ~2-3 minutes)"
