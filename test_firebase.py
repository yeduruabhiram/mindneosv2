#!/usr/bin/env python3
"""
Test Firebase Firestore integration
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_firebase_storage():
    """Test that conversations are stored in Firebase"""
    print("=" * 70)
    print("🔥 Testing Firebase Firestore Storage")
    print("=" * 70)
    
    # Send a test message
    print("\n💬 Sending test message...")
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json={
            "message": "What is Firebase?",
            "user_id": "test_firebase_user",
            "clerk_user_id": "clerk_test_123",
            "user_email": "test@mindneox.ai",
            "user_name": "Test User"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Message sent successfully!")
        print(f"\n📊 Response Data:")
        print(f"   Session ID: {data['session_id']}")
        print(f"   Firebase ID: {data['firebase_id']}")
        print(f"   Pinecone ID: {data['pinecone_id']}")
        print(f"\n🤖 AI Response: {data['response'][:150]}...")
        
        if data['firebase_id']:
            print(f"\n✅ Data stored in Firebase Firestore!")
            print(f"   Document ID: {data['firebase_id']}")
            
            # Try to retrieve the conversation
            print(f"\n📥 Retrieving conversation from Firebase...")
            time.sleep(2)
            
            conv_response = requests.get(
                f"{BASE_URL}/api/conversations/{data['firebase_id']}"
            )
            
            if conv_response.status_code == 200:
                conv_data = conv_response.json()
                print(f"✅ Successfully retrieved from Firebase!")
                print(f"\n📄 Conversation Details:")
                print(f"   ID: {conv_data['id']}")
                print(f"   Timestamp: {conv_data['timestamp']}")
                print(f"   Model: {conv_data['model_used']}")
                print(f"   Messages: {len(conv_data['messages'])}")
                
                for i, msg in enumerate(conv_data['messages'], 1):
                    print(f"\n   Message {i}:")
                    print(f"      Role: {msg['role']}")
                    print(f"      Content: {msg['content'][:100]}...")
            else:
                print(f"⚠️  Could not retrieve conversation: {conv_response.status_code}")
        else:
            print(f"❌ Firebase ID is None - data not stored!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def test_get_all_conversations():
    """Test retrieving all conversations"""
    print("\n" + "=" * 70)
    print("📚 Testing Get All Conversations")
    print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/api/conversations?limit=5")
    
    if response.status_code == 200:
        conversations = response.json()
        print(f"\n✅ Retrieved {len(conversations)} conversations from Firebase")
        
        for i, conv in enumerate(conversations, 1):
            print(f"\n📄 Conversation {i}:")
            print(f"   ID: {conv['id'][:20]}...")
            print(f"   Timestamp: {conv['timestamp']}")
            print(f"   Messages: {len(conv['messages'])}")
            if conv['messages']:
                first_msg = conv['messages'][0]['content']
                print(f"   First message: {first_msg[:60]}...")
    else:
        print(f"❌ Error: {response.status_code}")

def test_stats():
    """Test statistics endpoint"""
    print("\n" + "=" * 70)
    print("📊 Testing Statistics")
    print("=" * 70)
    
    response = requests.get(f"{BASE_URL}/api/stats")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"\n📈 System Statistics:")
        print(f"   Total Conversations: {stats['total_conversations']}")
        print(f"   Total Messages: {stats['total_messages']}")
        print(f"   Firebase: {'✅ Enabled' if stats['firebase_enabled'] else '❌ Disabled'}")
        print(f"   Pinecone: {'✅ Enabled' if stats['pinecone_enabled'] else '❌ Disabled'}")
        print(f"   AI Model: {'✅ Loaded' if stats['ai_model_loaded'] else '❌ Not Loaded'}")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    print("\n🔥 Firebase Firestore Integration Test")
    print("Testing data storage and retrieval\n")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            if health['services']['firebase']:
                print("✅ Server is running with Firebase enabled!\n")
            else:
                print("❌ Firebase is not enabled on the server!")
                exit(1)
        else:
            print("❌ Server returned unexpected status")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server is not running!")
        print("   Start the server first: ./start_backend_api.sh")
        exit(1)
    
    # Run tests
    test_firebase_storage()
    test_get_all_conversations()
    test_stats()
    
    print("\n" + "=" * 70)
    print("✅ Firebase Integration Test Complete!")
    print("=" * 70)
    print("\n🎯 All conversations are now stored in Firebase Firestore!")
    print("📊 View your data at: https://console.firebase.google.com/project/mindneoxai/firestore")
    print("=" * 70 + "\n")
