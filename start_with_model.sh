#!/bin/bash

# Start backend with TinyLlama model
export LOCAL_GGUF_MODEL_PATH="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

echo "🚀 Starting backend with TinyLlama model..."
echo "📍 Model: $LOCAL_GGUF_MODEL_PATH"
echo ""

python fastapi_chatbot.py
