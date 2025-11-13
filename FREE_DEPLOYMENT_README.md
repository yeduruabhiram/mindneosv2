# 🤖 Mindneox AI - Free Deployment & Custom LLM Training

## 🎯 Your Goal
Deploy a chatbot for **FREE**, collect user conversations, and train your own custom LLM model.

## ⚡ Quick Start (5 Minutes)

```bash
# Run the automated deployment script
./FREE_DEPLOYMENT_QUICKSTART.sh
```

That's it! The script will guide you through everything.

---

## 📋 What You Get

### 1. **Free Deployment** ($0/month)
- ✅ Backend API on Hugging Face Spaces (Free GPU)
- ✅ Frontend on Vercel (Free hosting)
- ✅ Firebase Firestore (1GB free storage)
- ✅ Pinecone vector DB (100K vectors free)
- ✅ Redis Cloud (30MB free)

### 2. **Automatic Data Collection**
- ✅ Every conversation saved to Firebase
- ✅ User metadata tracked
- ✅ Vector embeddings stored
- ✅ Export-ready format

### 3. **Custom Model Training**
- ✅ Google Colab notebook (Free GPU)
- ✅ Fine-tune on your data
- ✅ Deploy your custom model
- ✅ Continuous improvement cycle

---

## 🚀 Deployment Steps

### Option A: Automated (Recommended)
```bash
./FREE_DEPLOYMENT_QUICKSTART.sh
```

### Option B: Manual

#### 1. Deploy Backend
```bash
./deploy_to_huggingface.sh
```

#### 2. Deploy Frontend
```bash
./deploy_frontend_vercel.sh
```

#### 3. Configure Environment Variables

**Hugging Face Space Settings:**
```env
FIREBASE_SERVICE_ACCOUNT_JSON=<your-firebase-json>
PINECONE_API_KEY=<your-pinecone-key>
```

**Vercel Environment Variables:**
```env
VITE_API_URL=https://your-space.hf.space
VITE_CLERK_PUBLISHABLE_KEY=<your-clerk-key>
```

---

## 📊 Data Collection & Export

### Check Your Data
```bash
# View stats
curl https://your-space.hf.space/api/stats

# View conversations
curl https://your-space.hf.space/api/conversations?limit=10
```

### Export Training Data
```bash
python export_training_data.py
```

**Output:**
- `training_data.jsonl` - For model fine-tuning
- `training_data.csv` - For data analysis
- `full_conversations.json` - Complete conversation history
- `dataset_stats.json` - Dataset statistics

---

## 🤖 Train Your Custom Model

### Prerequisites
- 1000+ conversation pairs (recommended)
- Google account (for Colab)
- Hugging Face account

### Training Process

1. **Export your data**
   ```bash
   python export_training_data.py
   ```

2. **Open Colab Notebook**
   - Upload `train_custom_llm.ipynb` to Google Colab
   - Enable GPU: Runtime → Change runtime type → GPU

3. **Upload Training Data**
   - Upload your `training_data.jsonl` file

4. **Run Training**
   - Execute all cells in the notebook
   - Training takes 15-30 minutes

5. **Deploy Custom Model**
   - Model automatically uploads to Hugging Face
   - Update your backend to use the new model

### Training Options

| Base Model | Size | Speed | Quality | Colab |
|------------|------|-------|---------|-------|
| TinyLlama-1.1B | 1.1B | ⚡⚡⚡ | ⭐⭐ | Free ✅ |
| Phi-2 | 2.7B | ⚡⚡ | ⭐⭐⭐ | Free ✅ |
| Mistral-7B | 7B | ⚡ | ⭐⭐⭐⭐ | Pro 💰 |

---

## 🔄 Continuous Improvement Cycle

```
1. Deploy Chatbot
   ↓
2. Collect Conversations (1-2 weeks)
   ↓
3. Export Data (1000+ conversations)
   ↓
4. Train Custom Model (30 mins)
   ↓
5. Deploy Improved Model
   ↓
6. Repeat Monthly
```

### Monthly Improvement Plan

**Week 1-2:** Collect data
- Share chatbot link
- Promote on social media
- Add to your website

**Week 3:** Export and analyze
```bash
python export_training_data.py
```

**Week 4:** Train and deploy
- Train in Google Colab
- Deploy new model
- Monitor improvements

---

## 📈 Scaling Your Data Collection

### Get More Conversations

1. **Share Widely**
   - Social media posts
   - Reddit communities
   - Discord servers
   - Product Hunt launch

2. **Embed on Website**
   ```html
   <iframe src="https://your-vercel-app.vercel.app" 
           width="400" height="600"></iframe>
   ```

3. **Create Use Cases**
   - Customer support bot
   - Educational assistant
   - Coding helper
   - Creative writing aid

4. **Incentivize Usage**
   - Gamification
   - Leaderboards
   - Rewards for feedback

---

## 💾 Data Storage Limits

| Service | Free Tier | Conversations |
|---------|-----------|---------------|
| Firebase | 1GB | ~10,000 |
| Pinecone | 100K vectors | ~50,000 |
| Redis | 30MB | Sessions only |

**When you hit limits:**
- Export and archive old data
- Upgrade to paid tier ($25-50/month)
- Use multiple Firebase projects

---

## 🛠️ Advanced Features

### Custom Model Deployment

After training, deploy your model:

**Option 1: Hugging Face Inference**
```python
# Update fastapi_chatbot.py
HF_INFERENCE_MODEL = "your-username/mindneox-custom"
USE_HF_DEPLOYED = "1"
```

**Option 2: Local GGUF**
```bash
# Convert to GGUF format
python convert_to_gguf.py your-model/

# Quantize
./llama.cpp/quantize your-model.gguf your-model-q4.gguf q4_k_m

# Use in backend
LOCAL_GGUF_MODEL_PATH = "your-model-q4.gguf"
```

### A/B Testing

Test multiple models:
```python
# Route 50% to old model, 50% to new model
if random.random() < 0.5:
    response = old_model.generate(prompt)
else:
    response = new_model.generate(prompt)
```

### Analytics Dashboard

Track improvements:
- Response quality scores
- User satisfaction ratings
- Conversation length
- Topic distribution

---

## 🐛 Troubleshooting

### Backend Issues

**Model not loading:**
```bash
# Check HF Space logs
# Verify model file exists
# Check memory limits
```

**Firebase connection failed:**
```bash
# Verify credentials in Space settings
# Check Firestore rules
# Test with curl
```

### Frontend Issues

**Can't connect to API:**
```bash
# Check VITE_API_URL in Vercel
# Verify CORS settings
# Test API directly
```

**Build failed:**
```bash
# Check Node version (use 18+)
# Clear cache: rm -rf node_modules package-lock.json
# Reinstall: npm install
```

### Training Issues

**Out of memory:**
```python
# Reduce batch size
per_device_train_batch_size = 2

# Increase gradient accumulation
gradient_accumulation_steps = 8

# Use smaller model
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

**Poor quality:**
- Collect more data (3000+ conversations)
- Train for more epochs (5-10)
- Clean your dataset
- Use better base model

---

## 📚 Resources

### Documentation
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
- [Vercel Deployment](https://vercel.com/docs)
- [Firebase Firestore](https://firebase.google.com/docs/firestore)
- [PEFT Training](https://huggingface.co/docs/peft)

### Community
- [Hugging Face Discord](https://discord.gg/hugging-face)
- [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA)
- [r/MachineLearning](https://reddit.com/r/MachineLearning)

### Tools
- [Unsloth](https://github.com/unslothai/unsloth) - 2x faster training
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) - Advanced training
- [LM Studio](https://lmstudio.ai/) - Local model testing

---

## 💡 Tips for Success

### Data Quality
- ✅ Diverse conversations
- ✅ Natural language
- ✅ Clear responses
- ❌ Avoid spam/gibberish
- ❌ Remove personal info

### Training Best Practices
- Start with 1000+ conversations
- Use validation set (10%)
- Monitor loss curves
- Test before deploying
- Keep old model as backup

### Cost Optimization
- Use free tiers first
- Archive old data
- Optimize model size
- Cache responses
- Use CDN for frontend

---

## 🎯 Success Metrics

Track these to measure improvement:

1. **Data Collection**
   - Conversations per day
   - Unique users
   - Average conversation length

2. **Model Quality**
   - Response relevance
   - User satisfaction
   - Task completion rate

3. **Technical**
   - Response time
   - Error rate
   - Uptime

---

## 🚀 Next Steps

1. ✅ **Deploy Now**
   ```bash
   ./FREE_DEPLOYMENT_QUICKSTART.sh
   ```

2. ✅ **Share Your Chatbot**
   - Get your first 100 users
   - Collect feedback
   - Iterate quickly

3. ✅ **Train Your Model**
   - Export data weekly
   - Train monthly
   - Deploy improvements

4. ✅ **Scale Up**
   - Upgrade services as needed
   - Add more features
   - Build community

---

## 📞 Support

Need help? Check:
- 📖 [Full Guide](COMPLETE_FREE_DEPLOYMENT_GUIDE.md)
- 💻 [Training Notebook](train_custom_llm.ipynb)
- 🔧 [Export Script](export_training_data.py)

---

## 📄 License

MIT License - Free to use and modify

---

## 🌟 Star This Project

If this helps you, give it a star on GitHub!

**Ready to build your own AI? Let's go! 🚀**

```bash
./FREE_DEPLOYMENT_QUICKSTART.sh
```
