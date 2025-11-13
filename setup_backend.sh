#!/bin/bash
# Setup script for Ask Anything backend

echo "=================================="
echo "🚀 Setting up Ask Anything Backend"
echo "=================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if model file is valid
MODEL_FILE="Mistral-7B-Instruct-v0.3.Q4_K_M.gguf"
MODEL_SIZE=$(stat -f%z "$MODEL_FILE" 2>/dev/null || echo "0")

if [ "$MODEL_SIZE" -lt 1000000 ]; then
    echo ""
    echo "⚠️  WARNING: Model file is too small or missing!"
    echo "   Current size: $MODEL_SIZE bytes"
    echo "   Expected size: ~4GB"
    echo ""
    echo "📥 You need to download the model. Options:"
    echo ""
    echo "1. Download from Hugging Face:"
    echo "   wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf"
    echo ""
    echo "2. Or use a different model you already have"
    echo ""
    read -p "Do you want to download the model now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📥 Downloading model (this will take a while - ~4GB)..."
        wget -O "$MODEL_FILE" "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf"
        
        if [ $? -eq 0 ]; then
            echo "✅ Model downloaded successfully!"
        else
            echo "❌ Download failed. Please download manually."
            exit 1
        fi
    else
        echo "⚠️  Skipping download. Backend won't work without a valid model."
        exit 1
    fi
fi

# Check Redis
echo ""
echo "🔍 Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running. Starting Redis..."
    echo "   Run: brew services start redis"
    echo "   Or: redis-server &"
fi

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo "=================================="
echo ""
echo "To run the backend:"
echo "  source .venv/bin/activate"
echo "  python ask_anything.py"
echo ""
