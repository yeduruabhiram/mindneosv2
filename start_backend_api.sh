#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
export LOCAL_GGUF_MODEL_PATH="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
export FIREBASE_SERVICE_ACCOUNT_PATH="firebase-service-account.json"
exec uvicorn fastapi_chatbot:app --host 0.0.0.0 --port 8000 --reload
