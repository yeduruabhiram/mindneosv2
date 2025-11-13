# Deploy Frontend to GitHub & Vercel 🚀

## Quick Deploy

### Step 1: Deploy to GitHub

```bash
./deploy_frontend_github.sh
```

**You'll need:**
1. GitHub repository URL (create one at https://github.com/new)
2. GitHub username
3. GitHub Personal Access Token (https://github.com/settings/tokens)

---

## Manual Deployment

### Option 1: Using Script (Recommended)

```bash
./deploy_frontend_github.sh
```

### Option 2: Manual Steps

#### 1. Create GitHub Repository
Go to: https://github.com/new
- Name: `mindneox-frontend`
- Public or Private
- Don't initialize with README

#### 2. Push to GitHub

```bash
cd mindneox-frontend

# Initialize git
git init
git branch -M main

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/mindneox-frontend.git

# Add files
git add .

# Commit
git commit -m "Initial commit - MindNeox Frontend"

# Push
git push -u origin main
```

---

## Deploy to Vercel

### Step 1: Connect GitHub

1. Go to https://vercel.com/new
2. Sign in with GitHub
3. Import your repository: `mindneox-frontend`

### Step 2: Configure Project

**Framework Preset:** Vite
**Root Directory:** `./` (or leave empty)
**Build Command:** `npm run build`
**Output Directory:** `dist`

### Step 3: Add Environment Variables

Click "Environment Variables" and add:

```env
VITE_API_URL=https://yeduru-mindneox-ai1.hf.space
VITE_CLERK_PUBLISHABLE_KEY=pk_test_ZWFzeS1tYXJtb3QtMzguY2xlcmsuYWNjb3VudHMuZGV2JA
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=mindneoxai.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mindneoxai
VITE_FIREBASE_STORAGE_BUCKET=mindneoxai.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

### Step 4: Deploy

Click **"Deploy"** button!

Vercel will:
1. Clone your repository
2. Install dependencies
3. Build your project
4. Deploy to production

---

## After Deployment

### Your URLs

**GitHub:** https://github.com/YOUR_USERNAME/mindneox-frontend
**Vercel:** https://mindneox-frontend.vercel.app (or custom domain)

### Test Your App

1. Visit your Vercel URL
2. Test Home page
3. Test Chatbot page
4. Try Coming Soon pages
5. Test email signup

---

## Update Deployment

### Push Updates to GitHub

```bash
cd mindneox-frontend
git add .
git commit -m "Update: description of changes"
git push
```

Vercel will automatically redeploy!

---

## Custom Domain (Optional)

### Add Custom Domain in Vercel

1. Go to Project Settings
2. Click "Domains"
3. Add your domain: `mindneox.ai`
4. Follow DNS instructions
5. Wait for verification

---

## Environment Variables Reference

### Required Variables:

```env
# Backend API
VITE_API_URL=https://yeduru-mindneox-ai1.hf.space

# Clerk Authentication
VITE_CLERK_PUBLISHABLE_KEY=your-clerk-key

# Firebase
VITE_FIREBASE_API_KEY=your-key
VITE_FIREBASE_AUTH_DOMAIN=your-domain
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

---

## Troubleshooting

### Build Failed?

**Check:**
1. All dependencies in package.json
2. Environment variables are set
3. Build command is correct: `npm run build`
4. Output directory is: `dist`

### API Not Working?

**Check:**
1. VITE_API_URL is correct
2. Backend is running on HF Spaces
3. CORS is enabled in backend
4. Network tab in browser console

### Firebase Not Working?

**Check:**
1. All Firebase env variables are set
2. Firebase project is created
3. Firestore is enabled
4. Security rules are set

---

## Files to Deploy

✅ All source files in `src/`
✅ `package.json`
✅ `vite.config.js`
✅ `index.html`
✅ `tailwind.config.js`
✅ `postcss.config.js`

❌ Don't commit:
- `node_modules/`
- `.env` (use Vercel env vars)
- `dist/`
- `.DS_Store`

---

## Quick Commands

### Deploy to GitHub
```bash
./deploy_frontend_github.sh
```

### Update Deployment
```bash
cd mindneox-frontend
git add .
git commit -m "Update"
git push
```

### Local Development
```bash
cd mindneox-frontend
npm run dev
```

### Build Locally
```bash
cd mindneox-frontend
npm run build
npm run preview
```

---

## Complete Deployment Checklist

### Backend ✅
- [x] Deployed to HF Spaces
- [x] Environment variables set
- [x] API responding

### Frontend
- [ ] Push to GitHub
- [ ] Deploy to Vercel
- [ ] Add environment variables
- [ ] Test all pages
- [ ] Custom domain (optional)

---

## Support

### GitHub Issues
Create issues at: https://github.com/YOUR_USERNAME/mindneox-frontend/issues

### Vercel Support
https://vercel.com/support

Ready to deploy! 🚀
