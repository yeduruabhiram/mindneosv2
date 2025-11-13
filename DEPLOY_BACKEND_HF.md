# Deploy Backend to Hugging Face Spaces 🚀

## Quick Deploy (Automated)

### Option 1: Use Deployment Script

```bash
chmod +x deploy_backend_to_hf.sh
./deploy_backend_to_hf.sh
```

When prompted, enter your Hugging Face token from:
https://huggingface.co/settings/tokens

---

## Manual Deploy (Step by Step)

### Step 1: Clone Your Space

```bash
git clone https://huggingface.co/spaces/yeduru/mindneox.ai1
cd mindneox.ai1
```

### Step 2: Copy Backend Files

```bash
# Copy main files
cp ../fastapi_chatbot.py .
cp ../requirements.txt .
cp ../HF_Dockerfile ./Dockerfile

# Copy Firebase credentials
cp ../mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json .

# Copy models (if exists)
cp -r ../models . 2>/dev/null || echo "No models directory"
```

### Step 3: Create README.md

```bash
cat > README.md << 'EOF'
---
title: MindNeox AI Backend
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# MindNeox.AI Backend

AI-powered chatbot backend with FastAPI.

## Features
- 🤖 AI Chat with TinyLlama
- 🔥 Firebase integration
- 📊 Pinecone vector database
- ⚡ Redis caching

## API Endpoints
- `POST /api/chat` - Chat with AI
- `GET /api/user/{user_id}/history` - Chat history
EOF
```

### Step 4: Commit and Push

```bash
git add .
git commit -m "Deploy MindNeox AI Backend"
git push
```

When prompted for password, use your HF token.

---

## Set Environment Variables

After deployment, go to your Space settings and add:

### Required Variables:

```env
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=your-pinecone-env
```

### Optional Variables:

```env
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
```

---

## Verify Deployment

### 1. Check Build Status
Visit: https://huggingface.co/spaces/yeduru/mindneox.ai1

### 2. Test API
```bash
curl https://yeduru-mindneox-ai1.hf.space/
```

### 3. Test Chat Endpoint
```bash
curl -X POST https://yeduru-mindneox-ai1.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!",
    "user_id": "test_user"
  }'
```

---

## Update Frontend

After deployment, update your frontend `.env`:

```env
VITE_API_URL=https://yeduru-mindneox-ai1.hf.space
```

---

## Troubleshooting

### Build Failed?
1. Check logs in Space settings
2. Verify Dockerfile syntax
3. Check requirements.txt

### API Not Responding?
1. Check if Space is running
2. Verify port 7860 is used
3. Check environment variables

### Model Loading Issues?
1. Model file might be too large
2. Check model path in code
3. Consider using smaller model

---

## Files Needed

✅ `fastapi_chatbot.py` - Main application
✅ `requirements.txt` - Dependencies
✅ `Dockerfile` - Docker configuration
✅ `README.md` - Space metadata
✅ `mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json` - Firebase credentials

---

## Space URL

🌐 **Your Space:** https://huggingface.co/spaces/yeduru/mindneox.ai1

📊 **Settings:** https://huggingface.co/spaces/yeduru/mindneox.ai1/settings

---

## Next Steps

1. ✅ Deploy backend to HF Spaces
2. ✅ Set environment variables
3. ✅ Update frontend API URL
4. ✅ Test API endpoints
5. ✅ Deploy frontend to Vercel

Done! 🎉
