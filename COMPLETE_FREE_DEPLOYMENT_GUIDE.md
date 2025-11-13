# Complete Free Deployment & Data Collection Guide

## 🎯 Goal
Deploy your chatbot for FREE, collect user conversations, and prepare data for training your own LLM.

## 📊 Architecture

```
Users → Frontend (Vercel) → Backend API (Hugging Face Spaces) → Data Storage (Firebase)
                                                                → Vector DB (Pinecone)
```

## 🆓 Free Services Used

1. **Hugging Face Spaces** - Backend API (Free GPU)
2. **Vercel** - Frontend hosting (Free)
3. **Firebase Firestore** - Conversation storage (Free 1GB)
4. **Pinecone** - Vector embeddings (Free 100K vectors)
5. **Redis Cloud** - Session memory (Free 30MB)

---

## 📦 Step 1: Prepare Backend for Hugging Face Spaces

### 1.1 Create Hugging Face Account
- Go to https://huggingface.co/join
- Create free account
- Get your API token from https://huggingface.co/settings/tokens

### 1.2 Deploy to Hugging Face Spaces

```bash
# Run the deployment script
chmod +x deploy_to_huggingface.sh
./deploy_to_huggingface.sh
```

---

## 🌐 Step 2: Deploy Frontend to Vercel

### 2.1 Create Vercel Account
- Go to https://vercel.com/signup
- Sign up with GitHub

### 2.2 Deploy Frontend

```bash
cd mindneox-frontend
npm install -g vercel
vercel login
vercel --prod
```

### 2.3 Set Environment Variables in Vercel
```
VITE_API_URL=https://your-space.hf.space
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key
```

---

## 💾 Step 3: Data Collection Setup

### Your data is already being collected in:

1. **Firebase Firestore** - All conversations with metadata
   - Collection: `conversations`
   - Fields: user_message, assistant_response, timestamp, user_id, etc.

2. **Pinecone** - Vector embeddings for semantic search
   - Index: `mindnex-responses`
   - Useful for finding similar conversations

### 3.1 Export Data for Training

Use the provided script to export your collected data:

```bash
python export_training_data.py
```

This will create:
- `training_data.jsonl` - Conversation pairs for fine-tuning
- `training_data.csv` - CSV format for analysis
- `training_stats.json` - Dataset statistics

---

## 🤖 Step 4: Train Your Own LLM

### 4.1 Data Format for Training

Your exported data will be in this format:
```json
{"prompt": "User: Hello\n", "completion": "Assistant: Hi! How can I help you?\n"}
{"prompt": "User: What is AI?\n", "completion": "Assistant: AI stands for...\n"}
```

### 4.2 Training Options (All Free/Cheap)

#### Option A: Fine-tune on Google Colab (FREE)
```python
# Use the provided notebook: train_custom_llm.ipynb
# Upload your training_data.jsonl
# Fine-tune TinyLlama or Phi-2 model
```

#### Option B: Fine-tune on Hugging Face (FREE)
```bash
# Use AutoTrain on Hugging Face
# Upload dataset → Select base model → Train
```

#### Option C: Use Unsloth (FASTEST & FREE)
```python
# Unsloth makes training 2x faster and uses less memory
# Perfect for free Colab GPUs
```

---

## 📈 Step 5: Monitor Data Collection

### 5.1 Check Firebase Console
- Go to https://console.firebase.google.com
- View your `conversations` collection
- Export data anytime

### 5.2 API Endpoints for Data

```bash
# Get conversation stats
curl https://your-api.hf.space/api/stats

# Get recent conversations
curl https://your-api.hf.space/api/conversations?limit=100

# Get user history
curl https://your-api.hf.space/api/user/{user_id}/history
```

---

## 🔄 Step 6: Continuous Improvement Cycle

```
1. Deploy chatbot → 2. Collect conversations → 3. Export data → 
4. Train custom model → 5. Deploy improved model → Repeat
```

### 6.1 Weekly Data Export
```bash
# Set up cron job or GitHub Action
0 0 * * 0 python export_training_data.py
```

### 6.2 Monthly Model Training
- Collect 1000+ conversations
- Export and clean data
- Fine-tune model on Colab
- Deploy new model to HF Spaces

---

## 💰 Cost Breakdown (All FREE)

| Service | Free Tier | Your Usage |
|---------|-----------|------------|
| HF Spaces | 2 vCPU, 16GB RAM | ✅ Enough |
| Vercel | 100GB bandwidth | ✅ Enough |
| Firebase | 1GB storage, 50K reads/day | ✅ ~10K conversations |
| Pinecone | 100K vectors | ✅ ~50K conversations |
| Redis Cloud | 30MB | ✅ Enough for sessions |

**Total Cost: $0/month** 🎉

---

## 🚀 Quick Start Commands

```bash
# 1. Deploy backend to Hugging Face
./deploy_to_huggingface.sh

# 2. Deploy frontend to Vercel
cd mindneox-frontend && vercel --prod

# 3. Test the deployment
curl https://your-space.hf.space/health

# 4. Export training data (after collecting conversations)
python export_training_data.py

# 5. Train your model (use provided Colab notebook)
# Open: train_custom_llm.ipynb in Google Colab
```

---

## 📚 Next Steps

1. ✅ Deploy backend to HF Spaces
2. ✅ Deploy frontend to Vercel
3. ✅ Share your chatbot link
4. ⏳ Collect 1000+ conversations (1-2 weeks)
5. ⏳ Export data and analyze
6. ⏳ Fine-tune your custom model
7. ⏳ Deploy improved model

---

## 🆘 Troubleshooting

### Backend not responding
- Check HF Space logs
- Verify environment variables
- Restart the Space

### Data not saving
- Check Firebase credentials
- Verify Firestore rules
- Check API logs

### Frontend can't connect
- Update VITE_API_URL in Vercel
- Check CORS settings
- Verify API is running

---

## 📞 Support

- HF Spaces: https://huggingface.co/docs/hub/spaces
- Vercel: https://vercel.com/docs
- Firebase: https://firebase.google.com/docs

Ready to deploy? Run: `./deploy_to_huggingface.sh`
