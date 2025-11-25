# 🚀 Quick Start Guide - MindNeox Mobile App

## Step 1: Install Dependencies

```bash
cd mobile-app
npm install
```

## Step 2: Backend Already Configured! ✅

**Good news!** Your app is already configured to use your Hugging Face backend:

```javascript
const API_BASE = 'https://yeduru-abhi.hf.space';
```

No changes needed! The app will connect to your deployed backend automatically.

### Want to test with a different backend?

Open `App.js` and update line 17:

```javascript
// For local testing:
const API_BASE = 'http://192.168.1.5:8000'; // Your computer's IP

// For production:
const API_BASE = 'https://your-backend-url.com';
```

## Step 3: Start the App

```bash
npm start
```

This will show a QR code and options to run on:
- Press `i` for iOS Simulator (Mac only)
- Press `a` for Android Emulator
- Scan QR code with Expo Go app on your phone

## Step 4: Test on Your Phone

1. Install **Expo Go** from App Store (iOS) or Play Store (Android)
2. Scan the QR code shown in terminal
3. App will load on your device!

## Features Included

✅ Chat with MindNeox AI
✅ Beautiful dark UI with glass effects
✅ Message persistence (saved locally)
✅ Text-to-speech for AI responses
✅ Loading animations
✅ Clear chat option
✅ Works on iOS & Android

## Troubleshooting

### "Cannot connect to backend"
- Make sure your backend is running
- Check the API_BASE URL is correct
- For local testing, use your computer's IP, not "localhost"
- Make sure phone and computer are on same WiFi

### "Expo Go not loading"
- Clear Expo cache: `expo start -c`
- Restart the Metro bundler

### "Module not found"
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

## Next Steps

Want to add more features? Check out:
- Voice input (speech recognition)
- User authentication
- Push notifications
- Image attachments
- Offline mode

## Building for App Stores

### iOS (requires Mac + Apple Developer account):
```bash
expo build:ios
```

### Android:
```bash
expo build:android
```

## Need Help?

Check the full README.md for detailed documentation.
