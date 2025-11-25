# MindNeox AI Mobile App

A React Native mobile application for MindNeox AI chatbot built with Expo.

## Features

- 💬 Real-time chat with MindNeox AI
- 🎨 Beautiful dark glass-morphism UI
- 💾 Local message persistence
- 🔊 Text-to-speech for AI responses
- 📱 iOS and Android support
- ⚡ Fast and responsive

## Prerequisites

- Node.js 16+ installed
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac) or Android Studio (for emulator)
- Expo Go app on your phone (for testing on device)

## Installation

1. Navigate to the mobile-app directory:
```bash
cd mobile-app
```

2. Install dependencies:
```bash
npm install
```

3. Update API endpoint in `App.js`:
```javascript
const API_BASE = 'https://yeduru-abhi.hf.space'; // Your Hugging Face backend
```

**Your backend is already configured!** The app is set to use your deployed Hugging Face Space.

## Running the App

### Start the development server:
```bash
npm start
```

### Run on iOS Simulator (Mac only):
```bash
npm run ios
```

### Run on Android Emulator:
```bash
npm run android
```

### Run on your phone:
1. Install "Expo Go" app from App Store or Play Store
2. Scan the QR code shown in terminal
3. App will load on your device

## Building for Production

### iOS (requires Mac):
```bash
expo build:ios
```

### Android:
```bash
expo build:android
```

## Project Structure

```
mobile-app/
├── App.js              # Main app component
├── app.json            # Expo configuration
├── package.json        # Dependencies
└── assets/             # Images and icons
```

## Configuration

### Backend Connection

Update the `API_BASE` constant in `App.js`:

```javascript
// For local development
const API_BASE = 'http://localhost:8000';

// For production
const API_BASE = 'https://your-backend-url.com';
```

### Note for iOS Simulator
If testing on iOS simulator with localhost backend, use your computer's IP address:
```javascript
const API_BASE = 'http://192.168.1.X:8000'; // Replace X with your IP
```

## Features Included

✅ **Splash screen** with animated logo
✅ **Direct to chat** - no home page, instant access
✅ Chat interface with message bubbles
✅ Loading states and animations
✅ Message persistence (AsyncStorage)
✅ Text-to-speech for AI responses
✅ Clear chat functionality
✅ Responsive design
✅ Dark theme with glass-morphism
✅ Keyboard handling

## Next Steps

To add more features:
- Voice input (speech-to-text)
- Push notifications
- User authentication
- Chat history management
- Image attachments
- Offline mode

## Troubleshooting

### Cannot connect to backend
- Make sure backend is running
- Check API_BASE URL is correct
- For local testing, use your computer's IP address, not localhost

### App crashes on startup
- Clear cache: `expo start -c`
- Reinstall dependencies: `rm -rf node_modules && npm install`

### Build errors
- Make sure you have latest Expo CLI: `npm install -g expo-cli@latest`
- Check Node.js version: `node -v` (should be 16+)

## Support

For issues or questions, please check the main MindNeox documentation or create an issue on GitHub.
