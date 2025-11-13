#!/usr/bin/env python3
"""
Export Training Data from Firebase
Exports conversations for LLM fine-tuning
"""

import json
import csv
import os
from datetime import datetime
from pathlib import Path

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("❌ Firebase not installed. Run: pip install firebase-admin")
    exit(1)

def initialize_firebase():
    """Initialize Firebase connection"""
    try:
        # Try multiple credential sources
        cred_json = None
        sa_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
        sa_json_env = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
        
        if sa_path and Path(sa_path).is_file():
            cred_json = json.loads(Path(sa_path).read_text())
        elif sa_json_env:
            cred_json = json.loads(sa_json_env.replace('\\n', '\n'))
        else:
            # Try local file
            if Path("mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json").exists():
                cred_json = json.loads(Path("mindneoxai-firebase-adminsdk-fbsvc-2609a1a210.json").read_text())
        
        if not cred_json:
            print("❌ Firebase credentials not found!")
            print("Set FIREBASE_SERVICE_ACCOUNT_PATH or FIREBASE_SERVICE_ACCOUNT_JSON")
            return None
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_json)
            firebase_admin.initialize_app(cred)
        
        return firestore.client()
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return None

def export_conversations(db, output_dir="training_data"):
    """Export all conversations from Firebase"""
    print("\n📊 Exporting conversations from Firebase...")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Fetch all conversations
    conversations_ref = db.collection('conversations')
    docs = conversations_ref.stream()
    
    all_conversations = []
    training_pairs = []
    
    for doc in docs:
        data = doc.to_dict()
        all_conversations.append({
            'id': doc.id,
            'timestamp': data.get('timestamp', ''),
            'messages': data.get('messages', []),
            'model_used': data.get('model_used', 'unknown'),
            'metadata': data.get('metadata', {})
        })
        
        # Extract training pairs (user message -> assistant response)
        messages = data.get('messages', [])
        for i in range(0, len(messages) - 1, 2):
            if i + 1 < len(messages):
                user_msg = messages[i]
                assistant_msg = messages[i + 1]
                
                if user_msg.get('role') == 'user' and assistant_msg.get('role') == 'assistant':
                    training_pairs.append({
                        'prompt': user_msg.get('content', ''),
                        'completion': assistant_msg.get('content', ''),
                        'timestamp': data.get('timestamp', ''),
                        'conversation_id': doc.id
                    })
    
    print(f"✅ Found {len(all_conversations)} conversations")
    print(f"✅ Extracted {len(training_pairs)} training pairs")
    
    return all_conversations, training_pairs

def save_jsonl(data, filename):
    """Save data in JSONL format (for fine-tuning)"""
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            # Format for fine-tuning
            training_item = {
                "prompt": f"User: {item['prompt']}\n",
                "completion": f"Assistant: {item['completion']}\n"
            }
            f.write(json.dumps(training_item, ensure_ascii=False) + '\n')
    print(f"✅ Saved JSONL: {filename}")

def save_csv(data, filename):
    """Save data in CSV format (for analysis)"""
    if not data:
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved CSV: {filename}")

def save_json(data, filename):
    """Save data in JSON format (full data)"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved JSON: {filename}")

def generate_stats(conversations, training_pairs):
    """Generate dataset statistics"""
    total_conversations = len(conversations)
    total_pairs = len(training_pairs)
    
    # Calculate average lengths
    if training_pairs:
        avg_prompt_length = sum(len(p['prompt'].split()) for p in training_pairs) / total_pairs
        avg_completion_length = sum(len(p['completion'].split()) for p in training_pairs) / total_pairs
    else:
        avg_prompt_length = 0
        avg_completion_length = 0
    
    # Get date range
    timestamps = [c['timestamp'] for c in conversations if c.get('timestamp')]
    date_range = {
        'earliest': min(timestamps) if timestamps else 'N/A',
        'latest': max(timestamps) if timestamps else 'N/A'
    }
    
    stats = {
        'export_date': datetime.now().isoformat(),
        'total_conversations': total_conversations,
        'total_training_pairs': total_pairs,
        'avg_prompt_words': round(avg_prompt_length, 2),
        'avg_completion_words': round(avg_completion_length, 2),
        'date_range': date_range,
        'ready_for_training': total_pairs >= 100
    }
    
    return stats

def main():
    print("=" * 70)
    print("🤖 Mindneox AI - Training Data Exporter")
    print("=" * 70)
    
    # Initialize Firebase
    db = initialize_firebase()
    if not db:
        return
    
    # Export conversations
    conversations, training_pairs = export_conversations(db)
    
    if not conversations:
        print("\n⚠️  No conversations found in Firebase!")
        print("Make sure your chatbot is collecting data.")
        return
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"training_data_{timestamp}"
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"\n💾 Saving data to: {output_dir}/")
    
    # Save in multiple formats
    save_jsonl(training_pairs, f"{output_dir}/training_data.jsonl")
    save_csv(training_pairs, f"{output_dir}/training_data.csv")
    save_json(conversations, f"{output_dir}/full_conversations.json")
    
    # Generate and save statistics
    stats = generate_stats(conversations, training_pairs)
    save_json(stats, f"{output_dir}/dataset_stats.json")
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 Dataset Summary")
    print("=" * 70)
    print(f"Total Conversations: {stats['total_conversations']}")
    print(f"Training Pairs: {stats['total_training_pairs']}")
    print(f"Avg Prompt Length: {stats['avg_prompt_words']} words")
    print(f"Avg Response Length: {stats['avg_completion_words']} words")
    print(f"Date Range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
    print()
    
    if stats['ready_for_training']:
        print("✅ Dataset is ready for fine-tuning!")
        print(f"📁 Training file: {output_dir}/training_data.jsonl")
        print()
        print("🚀 Next Steps:")
        print("1. Upload training_data.jsonl to Google Colab")
        print("2. Use the provided notebook: train_custom_llm.ipynb")
        print("3. Fine-tune TinyLlama or Phi-2 model")
        print("4. Deploy your custom model!")
    else:
        print("⚠️  Need more data for training (minimum 100 pairs)")
        print(f"Current: {stats['total_training_pairs']} pairs")
        print(f"Needed: {100 - stats['total_training_pairs']} more pairs")
        print()
        print("💡 Tips to collect more data:")
        print("- Share your chatbot with friends")
        print("- Post on social media")
        print("- Add to your website")
    
    print("\n" + "=" * 70)
    print("✅ Export complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
