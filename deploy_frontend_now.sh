#!/bin/bash

echo "🎨 Deploying Mindneox AI Frontend to Vercel"
echo "==========================================="
echo ""

# Check if in correct directory
if [ ! -d "mindneox-frontend" ]; then
    echo "❌ Error: mindneox-frontend directory not found"
    echo "   Run this script from the project root"
    exit 1
fi

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
    echo ""
fi

# Update environment file
echo "⚙️  Updating environment configuration..."
cat > mindneox-frontend/.env.production << EOF
VITE_API_URL=https://yeduru-abhi.hf.space
EOF

echo "✅ Environment configured"
echo ""

# Go to frontend directory
cd mindneox-frontend

echo "🔐 Logging in to Vercel..."
echo "   (A browser window will open)"
echo ""
vercel login

echo ""
echo "🚀 Deploying to production..."
echo ""
vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅ Frontend Deployed Successfully!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Your frontend is now live!"
    echo ""
    echo "📝 Important: Set Environment Variables in Vercel"
    echo ""
    echo "   1. Go to: https://vercel.com/dashboard"
    echo "   2. Select your project"
    echo "   3. Go to Settings → Environment Variables"
    echo "   4. Add these variables:"
    echo ""
    echo "      VITE_API_URL = https://yeduru-abhi.hf.space"
    echo "      VITE_CLERK_PUBLISHABLE_KEY = <your-clerk-key>"
    echo ""
    echo "   5. Go to Deployments tab"
    echo "   6. Click '...' on latest deployment → Redeploy"
    echo ""
    echo "🧪 Test Your Chatbot:"
    echo "   Open your Vercel URL and try chatting!"
    echo ""
    echo "📊 Monitor:"
    echo "   Backend: https://huggingface.co/spaces/yeduru/abhi"
    echo "   Frontend: https://vercel.com/dashboard"
    echo ""
else
    echo ""
    echo "❌ Deployment failed"
    echo "   Check the error messages above"
    echo ""
    exit 1
fi
