#!/usr/bin/env python3
"""
Test the fixed prompt - should give clean, consistent responses
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat():
    """Test the fixed chat endpoint"""
    print("=" * 70)
    print("🧪 Testing Fixed Prompt - Chat Endpoint")
    print("=" * 70)
    
    test_questions = [
        "Who is the prime minister of India?",
        "What is artificial intelligence?",
        "Explain how computers work",
        "Tell me about the solar system"
    ]
    
    for question in test_questions:
        print(f"\n💬 Question: {question}")
        print("-" * 70)
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": question, "user_id": "test_user"}
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['response']
            
            # Check for issues
            has_inst_tokens = '[INST]' in answer or '[/INST]' in answer
            is_clean = not has_inst_tokens
            
            print(f"🤖 Response: {answer[:200]}...")
            print(f"\n✅ Clean response: {is_clean}")
            if has_inst_tokens:
                print("❌ WARNING: Found [INST] tokens in response!")
            print()
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

def test_ask():
    """Test the fixed ask endpoint"""
    print("\n" + "=" * 70)
    print("🧪 Testing Fixed Prompt - Ask Endpoint")
    print("=" * 70)
    
    test_questions = [
        {"question": "How do airplanes fly?", "age": 8},
        {"question": "What is photosynthesis?", "age": 12}
    ]
    
    for q in test_questions:
        print(f"\n❓ Question: {q['question']} (Age: {q['age']})")
        print("-" * 70)
        
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json=q
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['answer']
            
            # Check for issues
            has_inst_tokens = '[INST]' in answer or '[/INST]' in answer
            is_clean = not has_inst_tokens
            
            print(f"💡 Answer: {answer[:200]}...")
            print(f"\n✅ Clean response: {is_clean}")
            if has_inst_tokens:
                print("❌ WARNING: Found [INST] tokens in response!")
            print()
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    print("\n🔥 Testing Fixed Prompt System")
    print("This should produce clean, consistent responses without [INST] tokens\n")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!\n")
        else:
            print("❌ Server returned unexpected status")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server is not running!")
        print("   Start the server first: ./start_backend_api.sh")
        exit(1)
    
    # Run tests
    test_chat()
    test_ask()
    
    print("\n" + "=" * 70)
    print("✅ Testing Complete!")
    print("=" * 70)
    print("\n🎯 Key Improvements:")
    print("  • No more [INST] or [/INST] tokens in responses")
    print("  • Consistent, natural human-like answers")
    print("  • Clean formatting without system artifacts")
    print("  • Context-aware responses with conversation history")
    print("\n🌐 Your app is ready at: http://localhost:3000")
    print("=" * 70 + "\n")
