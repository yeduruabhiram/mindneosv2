#!/bin/bash

# Deploy Frontend to GitHub
echo "🚀 Deploying MindNeox Frontend to GitHub..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed${NC}"
    exit 1
fi

cd mindneox-frontend

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${BLUE}📦 Initializing git repository...${NC}"
    git init
    git branch -M main
fi

# Add GitHub remote (update with your repo URL)
echo -e "${BLUE}🔗 Setting up GitHub remote...${NC}"
echo ""
echo -e "${BLUE}Enter your GitHub repository URL:${NC}"
echo -e "${BLUE}Example: https://github.com/yourusername/mindneox-frontend.git${NC}"
read -p "GitHub URL: " GITHUB_URL

if [ -z "$GITHUB_URL" ]; then
    echo -e "${RED}❌ No URL provided${NC}"
    exit 1
fi

# Remove existing origin if exists
git remote remove origin 2>/dev/null

# Add new origin
git remote add origin $GITHUB_URL

# Create .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    echo -e "${BLUE}📝 Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Dependencies
node_modules
.pnp
.pnp.js

# Testing
coverage

# Production
dist
build

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Editor
.vscode/*
!.vscode/extensions.json
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Environment
.env
EOF
fi

# Add all files
echo -e "${BLUE}📦 Adding files...${NC}"
git add .

# Commit
echo -e "${BLUE}💾 Committing changes...${NC}"
git commit -m "Deploy MindNeox Frontend - Complete UI with glass design, coming soon pages, and Firebase integration"

# Push to GitHub
echo -e "${BLUE}📤 Pushing to GitHub...${NC}"
echo ""
echo -e "${BLUE}Enter your GitHub username:${NC}"
read -p "Username: " GITHUB_USER

echo -e "${BLUE}Enter your GitHub Personal Access Token:${NC}"
echo -e "${BLUE}(Generate at: https://github.com/settings/tokens)${NC}"
read -sp "Token: " GITHUB_TOKEN
echo ""

# Push with credentials
git push -f https://${GITHUB_USER}:${GITHUB_TOKEN}@${GITHUB_URL#https://} main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Frontend deployed to GitHub!${NC}"
    echo ""
    echo -e "${BLUE}📍 Repository: $GITHUB_URL${NC}"
    echo ""
    echo -e "${BLUE}🚀 Next: Deploy to Vercel${NC}"
    echo -e "${BLUE}   1. Go to https://vercel.com/new${NC}"
    echo -e "${BLUE}   2. Import your GitHub repository${NC}"
    echo -e "${BLUE}   3. Add environment variables${NC}"
    echo -e "${BLUE}   4. Deploy!${NC}"
    echo ""
else
    echo -e "${RED}❌ Push failed. Check your credentials.${NC}"
    exit 1
fi

cd ..
