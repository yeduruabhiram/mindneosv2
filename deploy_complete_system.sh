#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     🚀 Complete Mindneox AI Deployment - Backend + Frontend   ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Backend Status
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Step 1: Backend Deployment Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

BACKEND_URL="https://yeduru-abhi.hf.space"

echo "🌐 Backend URL: $BACKEND_URL"
echo "⏳ Checking backend status..."
echo ""

# Check backend health
response=$(curl -s "$BACKEND_URL/health" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ Backend is responding!"
    echo ""
    echo "📊 Health Status:"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    echo ""
else
    echo "⚠️  Backend is still building or starting up..."
    echo "   This is normal for first deployment (takes 2-3 minutes)"
    echo "   Check status: https://huggingface.co/spaces/yeduru/abhi"
    echo ""
fi

# Step 2: Add Secrets Reminder
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Step 2: Configure Backend Secrets (IMPORTANT!)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "⚠️  You need to add these secrets to your HF Space:"
echo ""
echo "1. Go to: https://huggingface.co/spaces/yeduru/abhi/settings"
echo "2. Scroll to 'Repository secrets'"
echo "3. Add these secrets:"
echo ""
echo "   Name: FIREBASE_SERVICE_ACCOUNT_JSON"
echo "   Value: <your-firebase-json>"
echo ""
echo "   Name: PINECONE_API_KEY"
echo "   Value: pcsk_5A9JjS_JVvYF7aE1kieuSnTXitm1pEMdVhg2wkpijQ3hiV9aC7rZ2CurG5qRfXE9FxHLAh"
echo ""
echo "📖 Full instructions: SETUP_HF_SECRETS.md"
echo ""

read -p "Have you added the secrets? (y/n): " SECRETS_ADDED

if [ "$SECRETS_ADDED" != "y" ]; then
    echo ""
    echo "⚠️  Please add secrets first, then run this script again."
    echo "   Or continue to deploy frontend and add secrets later."
    echo ""
fi

# Step 3: Frontend Deployment
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Step 3: Frontend Deployment to Vercel"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "🎨 Frontend Directory: mindneox-frontend"
echo "🌐 Backend API: $BACKEND_URL"
echo ""

read -p "Deploy frontend to Vercel now? (y/n): " DEPLOY_FRONTEND

if [ "$DEPLOY_FRONTEND" = "y" ]; then
    echo ""
    echo "🚀 Deploying frontend..."
    echo ""
    
    cd mindneox-frontend
    
    # Login to Vercel
    echo "🔐 Login to Vercel..."
    vercel login
    
    echo ""
    echo "📦 Deploying to production..."
    vercel --prod
    
    VERCEL_EXIT=$?
    cd ..
    
    if [ $VERCEL_EXIT -eq 0 ]; then
        echo ""
        echo "✅ Frontend deployed successfully!"
        echo ""
        echo "⚠️  Don't forget to set environment variables in Vercel:"
        echo "   1. Go to your Vercel project settings"
        echo "   2. Add these variables:"
        echo "      VITE_API_URL=$BACKEND_URL"
        echo "      VITE_CLERK_PUBLISHABLE_KEY=<your-clerk-key>"
        echo "   3. Redeploy"
        echo ""
    else
        echo ""
        echo "❌ Frontend deployment failed"
        echo "   Check the error messages above"
        echo ""
    fi
else
    echo ""
    echo "⏭️  Skipping frontend deployment"
    echo "   You can deploy later with: ./deploy_frontend_vercel.sh"
    echo ""
fi

# Step 4: Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉 Deployment Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "✅ What's Deployed:"
echo ""
echo "   🔧 Backend API:"
echo "      URL: $BACKEND_URL"
echo "      Docs: $BACKEND_URL/docs"
echo "      Status: Check logs at https://huggingface.co/spaces/yeduru/abhi"
echo ""

if [ "$DEPLOY_FRONTEND" = "y" ]; then
    echo "   🎨 Frontend:"
    echo "      Check Vercel dashboard for URL"
    echo "      Settings: https://vercel.com/dashboard"
    echo ""
fi

echo "📋 Next Steps:"
echo ""
echo "   1. ✅ Add secrets to HF Space (if not done)"
echo "   2. ✅ Set environment variables in Vercel (if deployed)"
echo "   3. ✅ Test your chatbot"
echo "   4. ✅ Share the link and collect data"
echo "   5. ✅ Export data after 1000+ conversations"
echo "   6. ✅ Train your custom model"
echo ""

echo "🧪 Test Commands:"
echo ""
echo "   # Test backend"
echo "   curl $BACKEND_URL/health"
echo ""
echo "   # Test chat"
echo "   curl -X POST $BACKEND_URL/api/chat \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"message\": \"Hello!\", \"session_id\": \"test\"}'"
echo ""

echo "📚 Documentation:"
echo "   - Setup Secrets: SETUP_HF_SECRETS.md"
echo "   - Complete Guide: FREE_DEPLOYMENT_README.md"
echo "   - Quick Start: START_HERE.md"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Deployment process complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
