#!/bin/bash

echo "🚀 Deploying Frontend to Vercel"
echo "================================"

cd mindneox-frontend

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo ""
echo "🔐 Login to Vercel..."
vercel login

echo ""
echo "⚙️  Before deploying, update your .env file with:"
echo "   VITE_API_URL=https://your-hf-space.hf.space"
echo ""
read -p "Press Enter when ready to deploy..."

echo ""
echo "🚀 Deploying to production..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Don't forget to set environment variables in Vercel dashboard:"
echo "   1. Go to your project settings"
echo "   2. Add VITE_API_URL"
echo "   3. Add VITE_CLERK_PUBLISHABLE_KEY (if using Clerk)"
echo "   4. Redeploy"
echo ""
echo "🌐 Your frontend is now live!"
