#!/bin/bash
# Run Ask Anything Backend with checks

echo "=================================="
echo "🚀 Starting Ask Anything Backend"
echo "=================================="

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv .venv"
    exit 1
fi

# Check model file
MODEL_FILE="Mistral-7B-Instruct-v0.3.Q4_K_M.gguf"
if [ -f "$MODEL_FILE" ]; then
    MODEL_SIZE=$(stat -f%z "$MODEL_FILE" 2>/dev/null || echo "0")
    MODEL_SIZE_MB=$((MODEL_SIZE / 1024 / 1024))
    
    echo "📦 Model file: $MODEL_FILE"
    echo "   Size: ${MODEL_SIZE_MB}MB"
    
    if [ "$MODEL_SIZE" -lt 1000000 ]; then
        echo ""
        echo "❌ ERROR: Model file is too small!"
        echo "   Current: ${MODEL_SIZE} bytes"
        echo "   Expected: ~4GB (4,000,000,000 bytes)"
        echo ""
        echo "📥 Download the model with:"
        echo "   wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf"
        echo ""
        echo "Or use curl:"
        echo "   curl -L -o $MODEL_FILE https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf"
        echo ""
        exit 1
    fi
else
    echo "❌ Model file not found: $MODEL_FILE"
    exit 1
fi

# Check Redis
echo ""
echo "🔍 Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running"
    echo "   Starting Redis in background..."
    redis-server --daemonize yes 2>/dev/null || echo "   Please start Redis manually: redis-server"
fi

# Check Python packages
echo ""
echo "🔍 Checking Python packages..."
python -c "import llama_cpp; print('✅ llama-cpp-python installed')" 2>/dev/null || echo "❌ llama-cpp-python not installed"
python -c "import langchain; print('✅ langchain installed')" 2>/dev/null || echo "❌ langchain not installed"
python -c "import redis; print('✅ redis installed')" 2>/dev/null || echo "❌ redis not installed"

echo ""
echo "=================================="
echo "🚀 Starting backend..."
echo "=================================="
echo ""

# Run the backend
python ask_anything.py "$@"
