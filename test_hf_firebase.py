#!/usr/bin/env python3
"""
Test Firebase connection on Hugging Face Space
"""
import requests
import json

print("🧪 Testing Hugging Face Space Backend")
print("=" * 60)

# Test root endpoint
print("\n1️⃣ Testing root endpoint...")
response = requests.get("https://yeduru-abhi.hf.space/")
data = response.json()

print(f"   Status: {data['status']}")
print(f"   Firebase: {data['services']['firebase']}")
print(f"   Data Collection: {data['features']['data_collection']}")

if data['services']['firebase'] == 'disconnected':
    print("\n❌ Firebase is NOT connected!")
    print("\n📋 To fix this:")
    print("   1. Go to: https://huggingface.co/spaces/yeduru/abhi/settings")
    print("   2. Scroll to 'Repository secrets'")
    print("   3. Check if 'FIREBASE_CREDENTIALS' secret exists")
    print("   4. If not, add it using: ./setup_hf_firebase_secret.sh")
else:
    print("\n✅ Firebase is connected!")

# Test chat endpoint
print("\n2️⃣ Testing chat endpoint...")
try:
    response = requests.post(
        "https://yeduru-abhi.hf.space/api/chat",
        json={
            "message": "test firebase storage",
            "user_id": "test_user_123"
        },
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Chat response received")
        print(f"   Firebase ID: {data.get('firebase_id', 'None')}")
        
        if data.get('firebase_id'):
            print("\n✅ Data is being stored in Firebase!")
        else:
            print("\n⚠️  Chat works but data is NOT being stored in Firebase")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test stats endpoint
print("\n3️⃣ Testing stats endpoint...")
try:
    response = requests.get("https://yeduru-abhi.hf.space/api/stats")
    data = response.json()
    print(f"   Total training conversations: {data.get('total_training_conversations', 0)}")
    print(f"   Collection: {data.get('collection', 'N/A')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
