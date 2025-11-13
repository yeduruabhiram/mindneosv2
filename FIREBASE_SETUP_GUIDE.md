# Firebase Setup Guide for Email Collection

## Quick Setup (5 minutes)

### Step 1: Add Firebase Config to .env

Add these lines to your `mindneox-frontend/.env` file:

```env
# Firebase Configuration
VITE_FIREBASE_API_KEY=your-api-key-here
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

### Step 2: Get Your Firebase Config

1. Go to https://console.firebase.google.com/
2. Select your project: **mindneoxai**
3. Click the gear icon ⚙️ > Project Settings
4. Scroll down to "Your apps"
5. Click on the Web app (</> icon)
6. Copy the config values
7. Paste into your `.env` file

### Step 3: Install Firebase Package

```bash
cd mindneox-frontend
npm install firebase
```

### Step 4: Restart Dev Server

```bash
npm run dev
```

## That's it! 🎉

Your Coming Soon page will now save emails to Firestore automatically.

## Test It

1. Go to http://localhost:5173/ai-agent
2. Scroll to email form
3. Enter your email
4. Click "Notify Me"
5. Check Firebase Console to see the email saved!

## View Collected Emails

1. Go to Firebase Console
2. Click "Firestore Database"
3. Open `coming_soon_emails` collection
4. See all submitted emails!
