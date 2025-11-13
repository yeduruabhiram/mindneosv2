# 🚀 Mindneox.ai - Quick Start Guide

## ✅ Everything is Running!

Your full-stack AI chatbot is now live with clean, consistent responses.

## 🌐 Access Your App

**Frontend**: http://localhost:3000
**Backend API**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

## 📊 Current Status

### Backend API (Port 8000) ✅
- TinyLlama AI model loaded (638MB)
- Redis conversation memory active
- Pinecone vector database connected
- Clean prompt system (no [INST] token leakage)
- Auto-reload enabled for development

### Frontend (Port 3000) ✅
- React + Vite dev server
- Clerk authentication configured
- Connected to backend API
- Real-time chat interface

### Additional Services ✅
- `ask_anything.py` - Standalone Q&A assistant (Port 3000 interactive)
- Redis - Conversation memory & caching
- Pinecone - Vector search & embeddings

## 🎯 What Was Fixed

### Problem
- AI responses contained broken `[INST]` and `[/INST]` tokens
- Inconsistent answer formats
- Model confusion from context overflow

### Solution
1. **Clean System Prompt**: Explicit instructions to avoid system tokens
2. **Response Post-Processing**: Automatic token removal
3. **Context Management**: Proper conversation history handling
4. **Model Optimization**: Using TinyLlama with correct parameters

### Result
✅ All responses are now clean and natural
✅ No system token leakage
✅ Consistent formatting
✅ Context-aware conversations

## 🧪 Test It

```bash
# Test the fixed prompts
python test_fixed_prompt.py

# Or test via curl
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Who is the prime minister of India?"}'
```

## 🛠️ Managing Services

### Stop All Services
```bash
# Stop backend API
pkill -f "uvicorn fastapi_chatbot"

# Stop frontend
pkill -f "vite"

# Stop ask_anything
pkill -f "ask_anything.py"
```

### Restart Services
```bash
# Backend API
./start_backend_api.sh

# Frontend
cd mindneox-frontend && npm run dev

# Ask Anything (optional)
source .venv/bin/activate && python ask_anything.py
```

## 📁 Project Structure

```
llm-testing/
├── fastapi_chatbot.py          # Main backend API (FIXED ✅)
├── ask_anything.py             # Standalone Q&A assistant
├── main.py                     # Educational explainer
├── start_backend_api.sh        # Backend startup script
├── test_fixed_prompt.py        # Test script for clean responses
├── tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf  # AI model (638MB)
├── mindneox-frontend/          # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── requirements.txt            # Python dependencies
```

## 🔑 Key Features

### Chat API (`/api/chat`)
- General conversation with AI
- Conversation memory via Redis
- Context-aware responses
- Clerk user authentication
- Stores in Firebase & Pinecone

### Educational Q&A (`/api/ask`)
- Age-appropriate explanations
- Topic-based learning
- Clean, simple language
- Educational context

### User Memory
- `/api/user/{user_id}/history` - Get conversation history
- `/api/user/{user_id}/predict` - Predictive greeting
- `/api/user/{user_id}/context` - User interests & topics

## 🎨 Frontend Features

- Modern React UI with Tailwind CSS
- Clerk authentication
- Real-time chat interface
- Conversation history
- User profile management
- Report/feedback system

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/api/chat` | POST | Chat with AI |
| `/api/ask` | POST | Educational Q&A |
| `/api/conversations` | GET | List conversations |
| `/api/stats` | GET | System statistics |
| `/api/user/{id}/history` | GET | User chat history |
| `/api/report` | POST | Submit bug/feedback |

## 🔧 Configuration

### Environment Variables

Backend (`.env` or export):
```bash
LOCAL_GGUF_MODEL_PATH=tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
PINECONE_API_KEY=your_key_here
FIREBASE_SERVICE_ACCOUNT_PATH=path/to/service-account.json
```

Frontend (`mindneox-frontend/.env`):
```bash
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key
VITE_API_URL=http://localhost:8000
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative docs)
- **Prompt Fix Details**: See `PROMPT_FIX_SUMMARY.md`
- **Backend Fix Guide**: See `BACKEND_FIX_GUIDE.md`

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Check model file
ls -lh tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# Check Redis
redis-cli ping
```

### Frontend won't start
```bash
# Check if port 3000 is in use
lsof -i :3000

# Reinstall dependencies
cd mindneox-frontend && npm install
```

### AI responses still have issues
```bash
# Test the prompt fix
python test_fixed_prompt.py

# Check backend logs
tail -f nohup.out
```

## 🎉 You're All Set!

Your AI chatbot is production-ready with:
- ✅ Clean, consistent responses
- ✅ Conversation memory
- ✅ Vector search capabilities
- ✅ User authentication
- ✅ Modern React frontend

**Start chatting at: http://localhost:3000** 🚀
