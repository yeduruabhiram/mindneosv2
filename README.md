# MindNeox.AI - AI-Powered Chatbot Platform

Complete AI chatbot platform with FastAPI backend, React frontend, Firebase integration, and modern glassmorphism design.

## 🚀 Quick Start

### Backend (Already Deployed)
**Live at:** https://huggingface.co/spaces/yeduru/mindneox.ai1

### Frontend (Local Development)
```bash
cd mindneox-frontend
npm install
npm run dev
```

## 📁 Project Structure

```
mindneox/
├── fastapi_chatbot.py          # Backend API
├── requirements.txt            # Python dependencies
├── mindneox-frontend/          # React frontend
│   ├── src/
│   │   ├── pages/             # Page components
│   │   ├── components/        # Reusable components
│   │   └── hooks/             # Custom hooks
│   └── package.json
└── models/                     # AI models
```

## ✨ Features

### Backend
- 🤖 AI Chat with TinyLlama
- 🔥 Firebase Firestore integration
- 📊 Pinecone vector database
- ⚡ Redis caching
- 🚀 FastAPI framework

### Frontend
- 🎨 Modern glassmorphism design
- 📱 Mobile-optimized UI
- 🔒 Coming Soon pages for locked features
- 📧 Email collection with Firebase
- 🎭 Smooth animations with Framer Motion
- 🌓 Dark theme

## 🛠️ Setup

### Backend Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export PINECONE_API_KEY=your-key
export PINECONE_ENVIRONMENT=your-env
```

3. **Run backend:**
```bash
python fastapi_chatbot.py
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd mindneox-frontend
npm install
```

2. **Configure environment:**
Create `.env` file:
```env
VITE_API_URL=https://yeduru-mindneox-ai1.hf.space
VITE_CLERK_PUBLISHABLE_KEY=your-clerk-key
VITE_FIREBASE_API_KEY=your-firebase-key
VITE_FIREBASE_AUTH_DOMAIN=mindneoxai.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mindneoxai
VITE_FIREBASE_STORAGE_BUCKET=mindneoxai.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

3. **Run development server:**
```bash
npm run dev
```

## 🚢 Deployment

### Backend (Hugging Face Spaces)
```bash
./deploy_hf_force.sh
```

### Frontend (Vercel)
1. Push to GitHub
2. Import to Vercel
3. Add environment variables
4. Deploy

## 📚 Documentation

- **Backend Deployment:** `DEPLOY_BACKEND_HF.md`
- **Frontend Deployment:** `FINAL_PUSH_INSTRUCTIONS.md`
- **Firebase Setup:** `FIREBASE_SETUP_GUIDE.md`
- **Glass Design:** `GLASS_DESIGN_APPLIED.md`
- **Mobile Optimization:** `MOBILE_UX_OPTIMIZED.md`
- **Coming Soon Pages:** `PAGES_LOCKED_COMING_SOON.md`

## 🎯 Available Pages

### Open Pages
- ✅ **Home** (`/`) - Landing page
- ✅ **Chatbot** (`/chatbot`) - AI chat interface

### Coming Soon Pages
- 🔒 **AI Agent** (`/ai-agent`)
- 🔒 **Marketplace** (`/marketplace`)
- 🔒 **Dashboard** (`/dashboard`)
- 🔒 **Profile** (`/profile`)
- 🔒 **Report** (`/report`)

## 🔧 Tech Stack

### Backend
- FastAPI
- TinyLlama (1.1B)
- Firebase Firestore
- Pinecone Vector DB
- Redis Cache

### Frontend
- React + Vite
- Tailwind CSS
- Framer Motion
- Firebase SDK
- Clerk Auth

## 📝 API Endpoints

- `GET /` - Health check
- `POST /api/chat` - Chat with AI
- `GET /api/user/{user_id}/history` - Get chat history
- `GET /api/user/{user_id}/predict` - Get personalized greeting

## 🌐 Live URLs

- **Backend:** https://huggingface.co/spaces/yeduru/mindneox.ai1
- **Frontend:** (Deploy to get URL)

## 📧 Contact

For issues or questions, create an issue in the repository.

## 📄 License

MIT License
