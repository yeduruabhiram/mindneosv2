# 📱 MindNeox Mobile App - Complete Setup Guide

Your web chatbot has been converted into a **React Native mobile app** using Expo!

## 🎯 What's Been Created

A complete mobile app in the `mobile-app/` folder with:

- ✅ **Full chat interface** - Message bubbles, loading states, animations
- ✅ **Message persistence** - Chats saved locally on device
- ✅ **Text-to-speech** - AI responses can be spoken aloud
- ✅ **Beautiful UI** - Dark theme with glass-morphism effects
- ✅ **iOS & Android support** - Works on both platforms
- ✅ **Keyboard handling** - Smart input management
- ✅ **Backend integration** - Connects to your existing API

## 📁 Project Structure

```
mobile-app/
├── App.js              # Main app component (chat interface)
├── app.json            # Expo configuration
├── package.json        # Dependencies
├── babel.config.js     # Babel configuration
├── README.md           # Full documentation
├── QUICKSTART.md       # Quick start guide
└── assets/             # App icons and images
```

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies

```bash
cd mobile-app
npm install
```

### 2. Backend Already Configured! ✅

**Great news!** Your app is already connected to your Hugging Face backend:

```javascript
const API_BASE = 'https://yeduru-abhi.hf.space';
```

**No configuration needed!** Skip to step 3.

#### Optional: Use a Different Backend

If you want to test with a local backend, open `mobile-app/App.js` and change line 17:

```javascript
// For local testing (use your computer's IP address)
const API_BASE = 'http://192.168.1.X:8000'; // Replace X with your IP
```

**Finding your IP address:**
- Mac: System Preferences → Network → Your IP is shown
- Windows: Open CMD → type `ipconfig` → look for IPv4 Address
- Linux: Open Terminal → type `hostname -I`

### 3. Start the App

```bash
npm start
```

Then:
- Press `i` for iOS Simulator (Mac only)
- Press `a` for Android Emulator
- Scan QR code with **Expo Go** app on your phone

## 📱 Testing on Your Phone

1. **Install Expo Go**
   - iOS: [App Store](https://apps.apple.com/app/expo-go/id982107779)
   - Android: [Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

2. **Make sure your phone and computer are on the same WiFi**

3. **Scan the QR code** shown in terminal

4. **App loads instantly!** No need to build or deploy

## 🎨 Features Included

### Core Features
- 💬 Real-time chat with MindNeox AI
- 💾 Local message persistence (AsyncStorage)
- 🔊 Text-to-speech for AI responses
- ⌨️ Smart keyboard handling
- 🎨 Beautiful dark UI with glass effects
- ⚡ Loading states and animations
- 🗑️ Clear chat functionality

### UI/UX
- Smooth scrolling to latest message
- Message timestamps
- User vs AI message styling
- Responsive design
- Native feel on both platforms

## 🔧 Backend Configuration

### Local Development

Your backend must be accessible from your phone/emulator:

**iOS Simulator:**
```javascript
const API_BASE = 'http://192.168.1.5:8000'; // Your computer's IP
```

**Android Emulator:**
```javascript
const API_BASE = 'http://10.0.2.2:8000'; // Special Android localhost
```

**Physical Device:**
```javascript
const API_BASE = 'http://192.168.1.5:8000'; // Your computer's IP (same WiFi)
```

### Production

Update to your deployed backend:
```javascript
const API_BASE = 'https://your-backend.herokuapp.com';
// or
const API_BASE = 'https://your-backend.railway.app';
```

## 📦 Building for Production

### iOS (requires Mac + Apple Developer Account)

```bash
cd mobile-app
expo build:ios
```

Follow prompts to:
1. Sign in with Apple Developer account
2. Choose build type (archive for App Store)
3. Wait for build to complete
4. Download IPA file
5. Upload to App Store Connect

### Android

```bash
cd mobile-app
expo build:android
```

Follow prompts to:
1. Choose build type (APK for testing, AAB for Play Store)
2. Wait for build to complete
3. Download APK/AAB file
4. Upload to Google Play Console

### Using EAS Build (Recommended)

Expo's new build service:

```bash
npm install -g eas-cli
eas build --platform ios
eas build --platform android
```

## 🎯 Next Steps & Enhancements

### Easy Additions
- [ ] Voice input (speech-to-text)
- [ ] Copy message to clipboard
- [ ] Share messages
- [ ] Dark/light theme toggle
- [ ] Custom user avatars

### Advanced Features
- [ ] User authentication (Firebase, Clerk)
- [ ] Push notifications
- [ ] Image attachments
- [ ] File uploads
- [ ] Offline mode with sync
- [ ] Chat history management
- [ ] Multiple conversations
- [ ] Search messages

### Backend Enhancements
- [ ] WebSocket for real-time updates
- [ ] Typing indicators
- [ ] Read receipts
- [ ] Message reactions

## 🐛 Troubleshooting

### Cannot connect to backend

**Problem:** App shows "Failed to send message"

**Solutions:**
1. Check backend is running: `curl http://localhost:8000/api/chat`
2. Verify API_BASE URL in App.js
3. For local testing, use IP address not "localhost"
4. Check phone and computer on same WiFi
5. Disable firewall temporarily to test

### Expo Go not loading

**Problem:** QR code scanned but app doesn't load

**Solutions:**
```bash
# Clear cache and restart
expo start -c

# Check Expo CLI is latest
npm install -g expo-cli@latest

# Restart Metro bundler
expo start --clear
```

### Module not found errors

**Problem:** "Unable to resolve module..."

**Solutions:**
```bash
# Delete and reinstall
rm -rf node_modules
npm install

# Clear watchman cache (Mac)
watchman watch-del-all

# Reset Metro bundler
expo start -c
```

### Build errors

**Problem:** Build fails with errors

**Solutions:**
1. Check Node.js version: `node -v` (should be 16+)
2. Update Expo CLI: `npm install -g expo-cli@latest`
3. Check app.json configuration
4. Ensure all dependencies are compatible

## 📚 Resources

### Documentation
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/)
- [Expo Go App](https://expo.dev/client)

### Tutorials
- [Expo Tutorial](https://docs.expo.dev/tutorial/introduction/)
- [React Native Tutorial](https://reactnative.dev/docs/tutorial)

### Community
- [Expo Forums](https://forums.expo.dev/)
- [React Native Community](https://reactnative.dev/community/overview)

## 🎉 You're All Set!

Your MindNeox chatbot is now a mobile app! 

**To get started right now:**

```bash
cd mobile-app
npm install
npm start
```

Then scan the QR code with Expo Go on your phone.

## 💡 Tips

1. **Start with Expo Go** - Test on your phone instantly without building
2. **Use your IP address** - For local backend testing
3. **Check the logs** - Terminal shows helpful error messages
4. **Hot reload works** - Save files and see changes instantly
5. **Test on real device** - Better than simulator for UX testing

## 🆘 Need Help?

1. Check `mobile-app/README.md` for detailed docs
2. Check `mobile-app/QUICKSTART.md` for quick reference
3. Review Expo documentation
4. Check backend is running and accessible

---

**Happy coding! 🚀**

Your web chatbot is now in your pocket!
