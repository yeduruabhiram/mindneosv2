#!/bin/bash

# MindNeox Mobile App Setup Script
# This script helps you set up the mobile app quickly

echo "🚀 MindNeox Mobile App Setup"
echo "=============================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed!"
    exit 1
fi

echo "✅ npm version: $(npm -v)"
echo ""

# Install Expo CLI globally if not installed
if ! command -v expo &> /dev/null; then
    echo "📦 Installing Expo CLI globally..."
    npm install -g expo-cli
else
    echo "✅ Expo CLI is already installed"
fi

echo ""
echo "📦 Installing project dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "📱 Next steps:"
    echo "1. Update API_BASE in App.js with your backend URL"
    echo "2. Run 'npm start' to start the development server"
    echo "3. Scan QR code with Expo Go app on your phone"
    echo ""
    echo "📖 For detailed instructions, see:"
    echo "   - QUICKSTART.md (quick reference)"
    echo "   - README.md (full documentation)"
    echo ""
    echo "🎉 Happy coding!"
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please check the error messages above and try again."
    exit 1
fi
