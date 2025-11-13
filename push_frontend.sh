#!/bin/bash

echo "🚀 Pushing Frontend to GitHub"
echo "=============================="
echo ""
echo "The frontend changes are committed and ready to push!"
echo ""
echo "You need to authenticate with GitHub."
echo ""
echo "Option 1: Use GitHub Personal Access Token"
echo "  1. Go to: https://github.com/settings/tokens"
echo "  2. Generate new token (classic)"
echo "  3. Select 'repo' scope"
echo "  4. Copy the token"
echo ""
echo "Option 2: Update git remote with token"
echo ""
read -p "Do you have a GitHub token? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    read -p "Enter your GitHub token: " GITHUB_TOKEN
    echo ""
    echo "Updating remote URL..."
    git remote set-url origin https://yeduruabhiram:$GITHUB_TOKEN@github.com/yeduruabhiram/mindneox.ai.git
    echo ""
    echo "Pushing to GitHub..."
    git push origin master
    echo ""
    echo "✅ Done! Check your repo: https://github.com/yeduruabhiram/mindneox.ai"
    echo ""
    echo "Vercel will auto-deploy from GitHub!"
    echo "Check: https://vercel.com/dashboard"
else
    echo ""
    echo "Please get a GitHub token first:"
    echo "https://github.com/settings/tokens"
    echo ""
    echo "Then run this script again or push manually:"
    echo "git push origin master"
fi

echo ""
echo "=============================="
