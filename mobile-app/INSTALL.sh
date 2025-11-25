#!/bin/bash

# MindNeox Mobile App - Quick Install Script
# This script sets up everything you need

echo "🚀 MindNeox Mobile App - Quick Install"
echo "======================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found!"
    echo "Install from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js: $(node -v)"

# Check if we're on Mac and need to fix file limits
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "📝 Checking macOS file limits..."
    
    CURRENT_LIMIT=$(ulimit -n)
    if [ "$CURRENT_LIMIT" -lt 4096 ]; then
        echo "⚠️  File limit is low ($CURRENT_LIMIT)"
        echo "Increasing limit for this session..."
        ulimit -n 65536
        echo "✅ Limit increased to $(ulimit -n)"
        echo ""
        echo "💡 To make this permanent, see FIX_MAC_FILE_LIMIT.md"
    else
        echo "✅ File limit is good ($CURRENT_LIMIT)"
    fi
fi

echo ""
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "🎉 Your mobile app is ready!"
    echo ""
    echo "📱 Next steps:"
    echo "1. Run: npm start"
    echo "2. Install Expo Go on your phone"
    echo "3. Scan the QR code"
    echo ""
    echo "📖 Read START_HERE.md for detailed instructions"
    echo ""
    echo "🚀 Start now: npm start"
else
    echo ""
    echo "❌ Installation failed!"
    echo "Check the errors above and try again."
    exit 1
fi
