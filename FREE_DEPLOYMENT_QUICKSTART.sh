#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║        🤖 Mindneox AI - Free Deployment Quick Start 🚀        ║"
echo "║                                                                ║"
echo "║  Deploy your chatbot for FREE and start collecting data       ║"
echo "║  to train your own custom LLM!                                 ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Function to print step headers
print_step() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check prerequisites
print_step "Step 1: Checking Prerequisites"

echo "Checking required tools..."
MISSING_TOOLS=()

if ! command -v git &> /dev/null; then
    MISSING_TOOLS+=("git")
fi

if ! command -v python3 &> /dev/null; then
    MISSING_TOOLS+=("python3")
fi

if ! command -v node &> /dev/null; then
    MISSING_TOOLS+=("node")
fi

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "❌ Missing required tools: ${MISSING_TOOLS[*]}"
    echo "Please install them first."
    exit 1
fi

echo "✅ All prerequisites installed!"

# Setup accounts
print_step "Step 2: Account Setup"

echo "You'll need FREE accounts on these platforms:"
echo ""
echo "1. 🤗 Hugging Face (for backend hosting)"
echo "   → https://huggingface.co/join"
echo ""
echo "2. ▲ Vercel (for frontend hosting)"
echo "   → https://vercel.com/signup"
echo ""
echo "3. 🔥 Firebase (for data storage)"
echo "   → https://console.firebase.google.com"
echo ""
echo "4. 📊 Pinecone (optional - for vector search)"
echo "   → https://www.pinecone.io/start/"
echo ""

read -p "Have you created these accounts? (y/n): " ACCOUNTS_READY

if [ "$ACCOUNTS_READY" != "y" ]; then
    echo ""
    echo "Please create the accounts first, then run this script again."
    exit 0
fi

# Firebase setup
print_step "Step 3: Firebase Setup"

echo "Firebase setup instructions:"
echo ""
echo "1. Go to https://console.firebase.google.com"
echo "2. Create a new project (or use existing)"
echo "3. Enable Firestore Database"
echo "4. Go to Project Settings → Service Accounts"
echo "5. Click 'Generate New Private Key'"
echo "6. Save the JSON file as 'firebase-credentials.json'"
echo ""

read -p "Have you downloaded the Firebase credentials? (y/n): " FIREBASE_READY

if [ "$FIREBASE_READY" = "y" ]; then
    echo ""
    echo "📁 Place your firebase-credentials.json in this directory"
    read -p "Press Enter when done..."
    
    if [ -f "firebase-credentials.json" ]; then
        echo "✅ Firebase credentials found!"
        export FIREBASE_SERVICE_ACCOUNT_PATH="$(pwd)/firebase-credentials.json"
    else
        echo "⚠️  Credentials not found. You can add them later."
    fi
fi

# Deploy backend
print_step "Step 4: Deploy Backend to Hugging Face"

echo "Ready to deploy your backend?"
echo ""
echo "This will:"
echo "  • Create a Hugging Face Space"
echo "  • Upload your chatbot API"
echo "  • Make it accessible via HTTPS"
echo ""

read -p "Deploy backend now? (y/n): " DEPLOY_BACKEND

if [ "$DEPLOY_BACKEND" = "y" ]; then
    chmod +x deploy_to_huggingface.sh
    ./deploy_to_huggingface.sh
    
    echo ""
    read -p "Enter your Hugging Face Space URL (e.g., https://username-spacename.hf.space): " HF_SPACE_URL
    
    # Save for frontend deployment
    echo "VITE_API_URL=$HF_SPACE_URL" > mindneox-frontend/.env.production
    echo "✅ Backend URL saved for frontend deployment"
fi

# Deploy frontend
print_step "Step 5: Deploy Frontend to Vercel"

echo "Ready to deploy your frontend?"
echo ""
echo "This will:"
echo "  • Deploy your React app to Vercel"
echo "  • Connect it to your backend"
echo "  • Make it accessible worldwide"
echo ""

read -p "Deploy frontend now? (y/n): " DEPLOY_FRONTEND

if [ "$DEPLOY_FRONTEND" = "y" ]; then
    chmod +x deploy_frontend_vercel.sh
    ./deploy_frontend_vercel.sh
fi

# Data collection info
print_step "Step 6: Data Collection Setup"

echo "✅ Your chatbot is now deployed and collecting data!"
echo ""
echo "📊 Data Collection:"
echo "  • All conversations are saved to Firebase"
echo "  • User interactions are tracked"
echo "  • Ready for export and training"
echo ""
echo "🔍 Monitor your data:"
echo "  • Firebase Console: https://console.firebase.google.com"
echo "  • API Stats: $HF_SPACE_URL/api/stats"
echo ""

# Export data instructions
print_step "Step 7: Export Training Data (After Collecting)"

echo "After collecting conversations, export your data:"
echo ""
echo "  python export_training_data.py"
echo ""
echo "This will create:"
echo "  • training_data.jsonl - For fine-tuning"
echo "  • training_data.csv - For analysis"
echo "  • dataset_stats.json - Statistics"
echo ""

# Training instructions
print_step "Step 8: Train Your Custom Model"

echo "When you have 1000+ conversations:"
echo ""
echo "1. Export your data (see Step 7)"
echo "2. Open train_custom_llm.ipynb in Google Colab"
echo "3. Upload your training_data.jsonl"
echo "4. Run all cells to train your model"
echo "5. Deploy your custom model!"
echo ""
echo "📓 Colab Notebook: train_custom_llm.ipynb"
echo ""

# Summary
print_step "🎉 Deployment Complete!"

echo "Your Mindneox AI chatbot is now live!"
echo ""
echo "📍 Your URLs:"
if [ ! -z "$HF_SPACE_URL" ]; then
    echo "  Backend API: $HF_SPACE_URL"
fi
echo "  Frontend: (check Vercel dashboard)"
echo "  API Docs: $HF_SPACE_URL/docs"
echo ""
echo "📊 Next Steps:"
echo "  1. Share your chatbot link with users"
echo "  2. Monitor data collection in Firebase"
echo "  3. Export data after 1000+ conversations"
echo "  4. Train your custom model in Colab"
echo "  5. Deploy improved model and repeat!"
echo ""
echo "📚 Documentation:"
echo "  • Full Guide: COMPLETE_FREE_DEPLOYMENT_GUIDE.md"
echo "  • Training Notebook: train_custom_llm.ipynb"
echo "  • Export Script: export_training_data.py"
echo ""
echo "💰 Total Cost: $0/month (100% FREE!)"
echo ""
echo "🚀 Happy building!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
