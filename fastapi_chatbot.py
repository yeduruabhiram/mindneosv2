#!/usr/bin/env python3
"""
FastAPI Chatbot with Firebase Firestore Storage + Redis Memory + Conversation Prediction
REST API for Mindneox.ai chatbot
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import hashlib
import json
import redis
import os
from typing import Any
import traceback

# Firebase imports
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

# AI Model imports
try:
    from llama_cpp import Llama
    from langchain_community.llms import LlamaCpp
    from sentence_transformers import SentenceTransformer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Pinecone imports
try:
    from pinecone import Pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI(
    title="Mindneox.ai Chatbot API",
    description="REST API for AI-powered chatbot with Firebase storage",
    version="1.0.0"
)

# CORS middleware - Allow all origins (configure for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    clerk_user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    firebase_id: Optional[str] = None
    pinecone_id: Optional[str] = None

class AskRequest(BaseModel):
    question: str
    topic: Optional[str] = None
    age: Optional[int] = 12

class AskResponse(BaseModel):
    answer: str
    question: str
    firebase_id: Optional[str] = None
    word_count: int
    timestamp: str

class ConversationResponse(BaseModel):
    id: str
    timestamp: str
    messages: List[dict]
    model_used: str


class ReportRequest(BaseModel):
    type: str  # 'bug' or 'feedback'
    description: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    clerk_user_id: Optional[str] = None
    user_email: Optional[str] = None
    metadata: Optional[dict] = None

class StatsResponse(BaseModel):
    total_conversations: int
    total_messages: int
    firebase_enabled: bool
    pinecone_enabled: bool
    ai_model_loaded: bool

# ============================================================================
# GLOBAL VARIABLES
# ============================================================================

llm = None
db = None
firebase_enabled = False
pinecone_index = None
pinecone_enabled = False
embedding_model = None
redis_client = None
redis_enabled = False

# ============================================================================
# FIREBASE INITIALIZATION
# ============================================================================

# Firebase service account should be provided via environment or a file.
# Supported methods:
# - FIREBASE_SERVICE_ACCOUNT_PATH -> path to the JSON service account file
# - FIREBASE_SERVICE_ACCOUNT_JSON -> full JSON string in an env var (escaped newlines handled)
# - FIREBASE_PRIVATE_KEY + FIREBASE_CLIENT_EMAIL + FIREBASE_PROJECT_ID -> individual fields
# The real credential is loaded during startup_event; keep this file free of secrets.

# ============================================================================
# STARTUP EVENT - Initialize Services
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize Firebase, AI Model, Redis Memory, and other services on startup"""
    global llm, db, firebase_enabled, pinecone_index, pinecone_enabled, embedding_model, redis_client, redis_enabled
    
    print("=" * 70)
    print("🚀 Starting Mindneox.ai API Server")
    print("=" * 70)
    
    # Initialize Redis for conversation memory
    try:
        print("\n🔴 Connecting to Redis for conversation memory...")
        redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_client.ping()
        redis_enabled = True
        print("✅ Redis connected! Conversation memory enabled.")
    except Exception as e:
        print(f"⚠️  Redis not available: {e}")
        print("   Conversation memory will be limited to session only")
        redis_enabled = False
    
    # Initialize Firebase (support multiple credential sources)
    if FIREBASE_AVAILABLE:
        try:
            print("\n🔥 Connecting to Firebase Firestore...")

            # Try multiple credential sources in order of preference
            import json
            from pathlib import Path

            cred_json = None
            sa_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
            sa_json_env = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")

            if sa_path and Path(sa_path).is_file():
                try:
                    cred_json = json.loads(Path(sa_path).read_text())
                except Exception as _e:
                    print(f"⚠️  Failed to read FIREBASE_SERVICE_ACCOUNT_PATH: {_e}")
                    cred_json = None
            elif sa_json_env:
                try:
                    cred_json = json.loads(sa_json_env)
                except Exception:
                    # Try to fix escaped newlines in the JSON
                    try:
                        tmp = sa_json_env.replace('\\n', '\n')
                        cred_json = json.loads(tmp)
                    except Exception as _e:
                        print(f"⚠️  FIREBASE_SERVICE_ACCOUNT_JSON could not be parsed as JSON: {_e}")
                        cred_json = None
            else:
                # Fallback to individual env vars
                pk = os.environ.get("FIREBASE_PRIVATE_KEY")
                client_email = os.environ.get("FIREBASE_CLIENT_EMAIL")
                project_id = os.environ.get("FIREBASE_PROJECT_ID")
                if pk and client_email and project_id:
                    if isinstance(pk, str):
                        pk = pk.replace('\\n', '\n')
                    cred_json = {
                        "type": "service_account",
                        "project_id": project_id,
                        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", ""),
                        "private_key": pk,
                        "client_email": client_email,
                        "client_id": os.environ.get("FIREBASE_CLIENT_ID", ""),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
                    }

            if not cred_json:
                print("⚠️  Firebase credentials not provided. Set FIREBASE_SERVICE_ACCOUNT_PATH or FIREBASE_SERVICE_ACCOUNT_JSON or FIREBASE_PRIVATE_KEY + FIREBASE_CLIENT_EMAIL + FIREBASE_PROJECT_ID.")
                firebase_enabled = False
            else:
                # Normalize private_key newlines
                pk = cred_json.get("private_key")
                if isinstance(pk, str):
                    cred_json["private_key"] = pk.replace('\\n', '\n')

                if not firebase_admin._apps:
                    cred = credentials.Certificate(cred_json)
                    firebase_admin.initialize_app(cred)

                db = firestore.client()
                firebase_enabled = True
                print(f"✅ Firebase connected! Project: {cred_json.get('project_id')}")

        except Exception as e:
            print(f"❌ Firebase failed: {e}")
            firebase_enabled = False
    else:
        print("⚠️  Firebase not available")
    
    # Initialize Pinecone
    if PINECONE_AVAILABLE:
        try:
            print("\n📊 Connecting to Pinecone...")
            PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
            if not PINECONE_API_KEY:
                raise ValueError("PINECONE_API_KEY environment variable not set")
            pc = Pinecone(api_key=PINECONE_API_KEY)
            pinecone_index = pc.Index("mindnex-responses")
            pinecone_enabled = True
            print("✅ Pinecone connected!")
        except Exception as e:
            print(f"❌ Pinecone failed: {e}")
            pinecone_enabled = False
    
    # Load Embedding Model
    if AI_AVAILABLE:
        try:
            print("\n🔤 Loading embedding model...")
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Embedding model loaded!")
        except Exception as e:
            print(f"❌ Embedding model failed: {e}")
    
    # Load AI Model
    if AI_AVAILABLE:
        try:
            print("\n🤖 Loading TinyLlama AI Model...")
            # Allow overriding model path via env var; validate file size before attempting load
            model_path = os.getenv("LOCAL_GGUF_MODEL_PATH", "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")
            try:
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Model file not found: {model_path}")
                # If file is very small, likely a placeholder/corrupt file — skip local load
                file_size = os.path.getsize(model_path)
                if file_size < 1_000_000:  # 1 MB threshold
                    raise RuntimeError(f"Model file appears too small ({file_size} bytes): {model_path}")

                llm = LlamaCpp(
                    model_path=model_path,
                    n_ctx=4096,
                    n_threads=4,
                    n_gpu_layers=50,
                    temperature=0.7,
                    top_p=0.95,
                    repeat_penalty=1.3,
                    max_tokens=300,
                    stop=["</s>", "<|user|>", "[INST]", "User:", "\n\n\n"],
                    verbose=False
                )
                print("✅ AI Model loaded successfully!")
            except Exception as _e:
                # Surface a clearer message when the local model cannot be used
                print(f"❌ AI Model failed: {_e}")
                print("   Tip: set LOCAL_GGUF_MODEL_PATH to a valid GGUF file or use Hugging Face fallback by setting HUGGINGFACE_HUB_TOKEN and HF_INFERENCE_MODEL.")
        except Exception as e:
            print(f"❌ AI Model failed: {e}")
            print("⚠️  API will run but AI endpoints will return errors")
    
    print("\n" + "=" * 70)
    print("✅ API Server Ready!")
    print("📍 Docs: http://localhost:8000/docs")
    print("=" * 70 + "\n")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def hf_text_generation(prompt: str, model: str, token: str, max_new_tokens: int = 300, temperature: float = 0.7) -> str:
    """Call Hugging Face Inference API (InferenceClient) and return text result.
    Returns a plain string if possible, otherwise raises Exception.
    This helper imports huggingface_hub lazily so the server can run without the package installed.
    """
    if not token:
        raise RuntimeError("Hugging Face token not provided for inference")

    try:
        from huggingface_hub import InferenceClient
    except Exception as e:
        raise RuntimeError(f"huggingface_hub not installed: {e}")

    client = InferenceClient(token=token)

    # text_generation returns different shapes across versions; normalize to text
    out = client.text_generation(prompt, model=model, max_new_tokens=max_new_tokens, temperature=temperature)
    # Normalize
    if isinstance(out, str):
        return out.strip()
    if isinstance(out, list) and out:
        first = out[0]
        if isinstance(first, str):
            return first.strip()
        if isinstance(first, dict):
            return first.get('generated_text') or first.get('text') or str(first)
    if hasattr(out, 'generated_text'):
        return getattr(out, 'generated_text').strip()

    # Last resort
    return str(out)


def store_in_firebase(user_message: str, assistant_response: str, metadata: dict = None) -> str:
    """Store conversation in Firebase Firestore"""
    if not firebase_enabled or not db:
        return None
    
    try:
        chat_id = str(uuid.uuid4())
        
        conversation_data = {
            'timestamp': datetime.now().isoformat(),
            'model_used': 'mindneox-v1',
            'messages': [
                {
                    'role': 'user',
                    'content': user_message,
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'role': 'assistant',
                    'content': assistant_response,
                    'timestamp': datetime.now().isoformat(),
                    'word_count': len(assistant_response.split()),
                    'char_count': len(assistant_response)
                }
            ],
            'embedding_id': metadata.get('embedding_id') if metadata else None,
            'embedding_status': 'stored' if metadata and metadata.get('embedding_id') else 'not_stored',
            'metadata': metadata if metadata else {},
            'source': 'fastapi'
        }
        
        db.collection('conversations').document(chat_id).set(conversation_data)
        return chat_id
        
    except Exception as e:
        print(f"Firebase storage error: {e}")
        return None

def store_in_pinecone(user_message: str, assistant_response: str) -> str:
    """Store conversation in Pinecone vector database"""
    if not pinecone_enabled or not pinecone_index or not embedding_model:
        return None
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = f"api_{timestamp}_{hashlib.md5(user_message.encode()).hexdigest()[:8]}"
        
        combined_text = f"User: {user_message}\nAssistant: {assistant_response}"
        embedding = embedding_model.encode(combined_text).tolist()
        
        pinecone_index.upsert(vectors=[{
            'id': unique_id,
            'values': embedding,
            'metadata': {
                'user_message': user_message,
                'bot_response': assistant_response,
                'timestamp': datetime.now().isoformat(),
                'source': 'fastapi',
                'type': 'chat'
            }
        }])
        
        return unique_id
        
    except Exception as e:
        print(f"Pinecone storage error: {e}")
        return None

# ============================================================================
# REDIS MEMORY FUNCTIONS - Conversation Memory & Prediction
# ============================================================================

def store_user_conversation_in_redis(user_id: str, message: str, response: str, session_id: str):
    """Store conversation in Redis for memory and pattern analysis"""
    if not redis_enabled or not redis_client:
        return False
    
    try:
        # Store conversation history (last 20 messages per user)
        history_key = f"user:{user_id}:history"
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_message': message,
            'assistant_response': response,
            'session_id': session_id
        }
        redis_client.lpush(history_key, json.dumps(conversation))
        redis_client.ltrim(history_key, 0, 19)  # Keep last 20 messages
        redis_client.expire(history_key, 86400 * 30)  # 30 days TTL
        
        # Store user context (topics, interests)
        context_key = f"user:{user_id}:context"
        words = message.lower().split()
        for word in words:
            if len(word) > 4:  # Only meaningful words
                redis_client.zincrby(context_key, 1, word)
        redis_client.expire(context_key, 86400 * 30)
        
        # Store session context
        session_key = f"session:{session_id}:messages"
        redis_client.lpush(session_key, json.dumps(conversation))
        redis_client.expire(session_key, 3600)  # 1 hour session
        
        return True
    except Exception as e:
        print(f"Redis storage error: {e}")
        return False

def get_user_conversation_history(user_id: str, limit: int = 10) -> List[dict]:
    """Get user's conversation history from Redis"""
    if not redis_enabled or not redis_client:
        return []
    
    try:
        history_key = f"user:{user_id}:history"
        messages = redis_client.lrange(history_key, 0, limit - 1)
        return [json.loads(msg) for msg in messages]
    except Exception as e:
        print(f"Redis retrieval error: {e}")
        return []

def get_user_context_keywords(user_id: str, limit: int = 10) -> List[tuple]:
    """Get user's most discussed topics/keywords"""
    if not redis_enabled or not redis_client:
        return []
    
    try:
        context_key = f"user:{user_id}:context"
        keywords = redis_client.zrevrange(context_key, 0, limit - 1, withscores=True)
        return [(k.decode() if isinstance(k, bytes) else k, int(s)) for k, s in keywords]
    except Exception as e:
        print(f"Redis context error: {e}")
        return []

def predict_next_conversation(user_id: str) -> str:
    """Predict likely next conversation topic based on user history"""
    if not redis_enabled or not redis_client:
        return "How can I assist you today?"
    
    try:
        # Get user's top interests
        keywords = get_user_context_keywords(user_id, 5)
        if not keywords:
            return "Hello! How can I help you today?"
        
        # Generate contextual greeting
        top_topics = [k[0] for k in keywords[:3]]
        if top_topics:
            topics_str = ", ".join(top_topics)
            return f"Welcome back! Would you like to continue discussing {topics_str}?"
        
        return "Hello! What would you like to talk about?"
    except Exception as e:
        print(f"Prediction error: {e}")
        return "How can I assist you?"

def get_session_context(session_id: str) -> List[dict]:
    """Get current session conversation context"""
    if not redis_enabled or not redis_client:
        return []
    
    try:
        session_key = f"session:{session_id}:messages"
        messages = redis_client.lrange(session_key, 0, -1)
        return [json.loads(msg) for msg in messages]
    except Exception as e:
        return []

def clean_ai_response(response: str) -> str:
    """
    Clean AI response by removing special tokens and repetitive patterns
    """
    import re
    
    # Remove special tokens
    special_tokens = [
        '[INST]', '[/INST]', '<s>', '</s>', '<|system|>', '<|user|>', '<|assistant|>',
        '<0x0A>', '<<SYS>>', '<</SYS>>'
    ]
    
    for token in special_tokens:
        response = response.replace(token, '')
    
    # Remove repetitive patterns (e.g., "[/INST] that is the ai [/INST]")
    # Match any pattern that repeats more than 2 times
    response = re.sub(r'(.{10,}?)\1{2,}', r'\1', response)
    
    # Remove lines that are just repetitions of tokens
    lines = response.split('\n')
    cleaned_lines = []
    prev_line = None
    
    for line in lines:
        line = line.strip()
        # Skip empty lines and repetitive lines
        if line and line != prev_line:
            # Skip lines that are mostly special tokens or repetitions
            if not re.match(r'^(\[/?INST\]|\s)+$', line):
                cleaned_lines.append(line)
                prev_line = line
    
    response = '\n'.join(cleaned_lines)
    
    # Final cleanup
    response = response.strip()
    
    # If response is too short or empty, provide a fallback
    if len(response) < 10:
        response = "I apologize, but I couldn't generate a proper response. Could you please rephrase your question?"
    
    return response

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Mindneox.ai Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "firebase": "connected" if firebase_enabled else "disconnected",
        "pinecone": "connected" if pinecone_enabled else "disconnected",
        "ai_model": "loaded" if llm else "not loaded",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/chat",
            "ask": "/api/ask",
            "conversations": "/api/conversations",
            "stats": "/api/stats",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "firebase": firebase_enabled,
            "pinecone": pinecone_enabled,
            "redis": redis_enabled,
            "ai_model": llm is not None,
            "embedding_model": embedding_model is not None
        }
    }

@app.get("/api/user/{user_id}/history")
async def get_user_history(user_id: str, limit: int = 20):
    """
    Get user's conversation history from Redis memory
    Returns last N conversations with timestamp and context
    """
    try:
        if not redis_enabled:
            return {
                "status": "error",
                "message": "Redis memory not enabled",
                "history": []
            }
        
        history = get_user_conversation_history(user_id, limit)
        
        return {
            "status": "success",
            "user_id": user_id,
            "count": len(history),
            "history": history,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

@app.get("/api/user/{user_id}/predict")
async def predict_conversation(user_id: str):
    """
    Get predictive conversation greeting based on user's interests
    Analyzes user's past conversations to suggest topics
    """
    try:
        if not redis_enabled:
            return {
                "status": "error",
                "message": "Redis memory not enabled",
                "greeting": "Hello! What would you like to talk about?"
            }
        
        # Get predictive greeting
        greeting = predict_next_conversation(user_id)
        
        # Get top keywords/topics
        keywords = get_user_context_keywords(user_id, 5)
        
        return {
            "status": "success",
            "user_id": user_id,
            "greeting": greeting,
            "top_keywords": [{"keyword": k, "frequency": f} for k, f in keywords],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting conversation: {str(e)}")

@app.get("/api/user/{user_id}/context")
async def get_user_context(user_id: str):
    """
    Get user's conversation context including keywords and patterns
    Provides insights into user's interests and discussion topics
    """
    try:
        if not redis_enabled:
            return {
                "status": "error",
                "message": "Redis memory not enabled",
                "keywords": []
            }
        
        # Get top keywords with frequency scores
        keywords = get_user_context_keywords(user_id, 10)
        
        # Get recent conversation count
        history = get_user_conversation_history(user_id, 100)
        
        return {
            "status": "success",
            "user_id": user_id,
            "total_conversations": len(history),
            "top_keywords": [{"keyword": k, "frequency": f} for k, f in keywords],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching context: {str(e)}")

@app.delete("/api/user/{user_id}/history")
async def delete_user_history(user_id: str):
    """
    Delete all conversation history for a user from Redis
    Clears both conversation history and context keywords
    """
    try:
        if not redis_enabled:
            return {
                "status": "error",
                "message": "Redis memory not enabled"
            }
        
        # Delete user history and context from Redis
        redis_client.delete(f'user:{user_id}:history')
        redis_client.delete(f'user:{user_id}:context')
        
        return {
            "status": "success",
            "message": "All conversation history deleted successfully",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting history: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Chat endpoint - Send a message and get AI response
    Stores conversation in Firebase, Pinecone, and Redis (memory)
    Integrates with Clerk authentication for user tracking
    Uses Redis for conversation memory and context prediction
    """
    # If the AI model isn't loaded, return a graceful stub so frontend and other
    # services can continue to function while the model is fixed.
    if not llm:
        # Create session/user identifiers similar to normal flow
        session_id = request.session_id or str(uuid.uuid4())
        user_id = request.clerk_user_id or request.user_id or f"anonymous_{session_id}"

        # Friendly fallback response
        response_text = "AI model not available. Please try again later. This is a stub response."
        # Try Hugging Face Inference API fallback if HF token is available
        try:
            hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
            if hf_token:
                # Use Hugging Face InferenceClient for a more robust fallback
                try:
                    print(f"🔁 HF fallback enabled at request-time. Token present: {bool(hf_token)}. HF model env: {os.getenv('HF_INFERENCE_MODEL')}")
                    from huggingface_hub import InferenceClient
                    hf_model = os.getenv("HF_INFERENCE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
                    client = InferenceClient(token=hf_token)
                    # text_generation expects a prompt string as first arg
                    out = client.text_generation(request.message, model=hf_model, max_new_tokens=300, temperature=0.7)
                    # Normalize different return shapes
                    if isinstance(out, str):
                        response_text = out.strip()
                    elif isinstance(out, list) and out:
                        first = out[0]
                        if isinstance(first, str):
                            response_text = first.strip()
                        elif isinstance(first, dict) and "generated_text" in first:
                            response_text = first.get("generated_text", response_text).strip()
                    elif hasattr(out, "generated_text"):
                        response_text = getattr(out, "generated_text", response_text).strip()
                except Exception as _hf_e:
                    # Log HF fallback failure so we can diagnose token / client errors
                    print(f"⚠️ HF fallback attempt failed: {repr(_hf_e)}")
                    tb = traceback.format_exc()
                    print(tb)
                    # continue to stub response
                    pass
        except Exception:
            # Keep stub if HF fallback fails
            pass

        # Store in Redis memory if enabled
        if redis_enabled:
            try:
                store_user_conversation_in_redis(user_id, request.message, response_text, session_id)
            except Exception:
                pass

        # Background storage (Pinecone / Firebase) if available
        embedding_id = None
        if pinecone_enabled:
            try:
                embedding_id = store_in_pinecone(request.message, response_text)
            except Exception:
                embedding_id = None

        firebase_id = None
        if firebase_enabled:
            try:
                metadata = {
                    'session_id': session_id,
                    'user_id': user_id,
                    'clerk_user_id': request.clerk_user_id,
                    'user_email': request.user_email,
                    'user_name': request.user_name,
                    'embedding_id': embedding_id,
                    'has_context': False
                }
                firebase_id = store_in_firebase(request.message, response_text, metadata)
            except Exception:
                firebase_id = None

        return ChatResponse(
            response=response_text,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            firebase_id=firebase_id,
            pinecone_id=embedding_id
        )
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Use Clerk user ID if available, otherwise use provided user_id
        user_id = request.clerk_user_id or request.user_id or f"anonymous_{session_id}"
        
        # Get conversation context from Redis (last 5 messages)
        conversation_history = get_user_conversation_history(user_id, 5)
        
        # Build context-aware prompt with proper formatting
        context = ""
        if conversation_history:
            context = "\nPrevious conversation:\n"
            for hist in reversed(conversation_history[-3:]):  # Last 3 for context
                context += f"User: {hist['user_message']}\nAssistant: {hist['assistant_response']}\n"
            context += "\n"

        # Clean prompt template - TinyLlama format
        prompt = f"<|system|>\nYou are Mindneox AI, a helpful and intelligent assistant. Answer directly, clearly, and naturally. Do not repeat the user's question. Do not echo special tokens.</s>\n<|user|>\n{context}{request.message}</s>\n<|assistant|>\n"

        # Optionally prefer a Hugging Face deployed model if configured.
        # Set USE_HF_DEPLOYED=1 or configure HF_INFERENCE_MODEL to enable.
        hf_model_env = os.getenv("HF_INFERENCE_MODEL")
        use_hf = (os.getenv("USE_HF_DEPLOYED", "0") == "1") or bool(hf_model_env)
        response = None
        if use_hf:
            hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
            hf_model = hf_model_env or os.getenv("HF_INFERENCE_MODEL", "yeduru/mindneox-ai-test")
            print(f"🔁 Startup: USE_HF_DEPLOYED={os.getenv('USE_HF_DEPLOYED')} use_hf={use_hf} hf_token_present={bool(hf_token)} hf_model={hf_model}")
            if hf_token:
                try:
                    response = hf_text_generation(prompt, model=hf_model, token=hf_token, max_new_tokens=400, temperature=0.7)
                    response = response.strip()
                except Exception as e:
                    # HF inference failed; log and fall back to local llm
                    print(f"⚠️ HF inference failed at startup-time, falling back to local llm: {e}")

        # If no HF response, use local llm
        if not response:
            response = llm.invoke(prompt)
            response = response.strip()
        
        # Clean response - remove special tokens and repetitions
        response = clean_ai_response(response)
        
        # Store in Redis memory (user history + session context)
        if redis_enabled:
            store_user_conversation_in_redis(user_id, request.message, response, session_id)
        
        # Store in Pinecone (background task)
        embedding_id = None
        if pinecone_enabled:
            embedding_id = store_in_pinecone(request.message, response)
        
        # Store in Firebase (background task) with Clerk user data
        firebase_id = None
        if firebase_enabled:
            metadata = {
                'session_id': session_id,
                'user_id': user_id,
                'clerk_user_id': request.clerk_user_id,
                'user_email': request.user_email,
                'user_name': request.user_name,
                'embedding_id': embedding_id,
                'has_context': len(conversation_history) > 0
            }
            firebase_id = store_in_firebase(request.message, response, metadata)
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            firebase_id=firebase_id,
            pinecone_id=embedding_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.post('/api/report')
async def submit_report(request: ReportRequest):
    """
    Submit a user report (bug or feedback). Stores report documents in Firestore collection 'reports'.
    """
    if not firebase_enabled or not db:
        raise HTTPException(status_code=503, detail='Firebase not available')

    try:
        report_id = str(uuid.uuid4())
        report_doc = {
            'type': request.type,
            'description': request.description,
            'user_id': request.user_id,
            'session_id': request.session_id,
            'clerk_user_id': request.clerk_user_id,
            'user_email': request.user_email,
            'metadata': request.metadata or {},
            'source': 'frontend',
            'timestamp': datetime.now().isoformat()
        }

        db.collection('reports').document(report_id).set(report_doc)

        return {
            'status': 'success',
            'id': report_id,
            'message': 'Report submitted'
        }
    except Exception as e:
        print(f"Error storing report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to store report: {str(e)}")

@app.post("/api/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Ask endpoint - Get AI answer to any question
    Educational explainer mode
    """
    # If AI model not loaded, provide a graceful stub answer rather than 503
    if not llm:
        answer_stub = "AI model not available. Please try again later."
        # Try Hugging Face Inference API for an answer if token available
        try:
            hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
            if hf_token:
                try:
                    from huggingface_hub import InferenceClient
                    hf_model = os.getenv("HF_INFERENCE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
                    client = InferenceClient(token=hf_token)
                    if request.topic:
                        prompt = f"[INST] Explain {request.topic} in detail for a {request.age} year old to understand: {request.question} [/INST]"
                    else:
                        prompt = f"[INST] Answer this question clearly for a {request.age} year old: {request.question} [/INST]"
                    out = client.text_generation(prompt, model=hf_model, max_new_tokens=300, temperature=0.7)
                    if isinstance(out, str):
                        answer_stub = out.strip()
                    elif isinstance(out, list) and out:
                        first = out[0]
                        if isinstance(first, str):
                            answer_stub = first.strip()
                        elif isinstance(first, dict) and "generated_text" in first:
                            answer_stub = first.get("generated_text", answer_stub).strip()
                    elif hasattr(out, "generated_text"):
                        answer_stub = getattr(out, "generated_text", answer_stub).strip()
                except Exception:
                    # fall back to stub if any HF client errors occur
                    pass
        except Exception:
            pass

        # Optional: store stub answer in Pinecone / Firebase when available
        embedding_id = None
        if pinecone_enabled:
            try:
                embedding_id = store_in_pinecone(request.question, answer_stub)
            except Exception:
                embedding_id = None

        firebase_id = None
        if firebase_enabled:
            try:
                metadata = {
                    'topic': request.topic,
                    'age': request.age,
                    'embedding_id': embedding_id,
                    'type': 'educational_stub'
                }
                firebase_id = store_in_firebase(request.question, answer_stub, metadata)
            except Exception:
                firebase_id = None

        return AskResponse(
            answer=answer_stub,
            question=request.question,
            firebase_id=firebase_id,
            word_count=len(answer_stub.split()),
            timestamp=datetime.now().isoformat()
        )
    
    try:
        # Create educational prompt
        if request.topic:
            prompt = f"[INST] Explain {request.topic} in detail for a {request.age} year old to understand: {request.question} [/INST]"
        else:
            prompt = f"[INST] Answer this question clearly for a {request.age} year old: {request.question} [/INST]"
        
        # Generate answer
        answer = llm.invoke(prompt)
        answer = answer.strip()
        
        # Clean answer - remove special tokens
        answer = clean_ai_response(answer)
        
        # Store in databases
        embedding_id = None
        if pinecone_enabled:
            embedding_id = store_in_pinecone(request.question, answer)
        
        firebase_id = None
        if firebase_enabled:
            metadata = {
                'topic': request.topic,
                'age': request.age,
                'embedding_id': embedding_id,
                'type': 'educational'
            }
            firebase_id = store_in_firebase(request.question, answer, metadata)
        
        return AskResponse(
            answer=answer,
            question=request.question,
            firebase_id=firebase_id,
            word_count=len(answer.split()),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ask error: {str(e)}")

@app.get("/api/conversations", response_model=List[ConversationResponse])
async def get_conversations(limit: int = 10):
    """
    Get recent conversations from Firebase
    """
    if not firebase_enabled or not db:
        raise HTTPException(status_code=503, detail="Firebase not available")
    
    try:
        conversations_ref = db.collection('conversations')
        docs = conversations_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        conversations = []
        for doc in docs:
            data = doc.to_dict()
            conversations.append(ConversationResponse(
                id=doc.id,
                timestamp=data.get('timestamp', ''),
                messages=data.get('messages', []),
                model_used=data.get('model_used', 'unknown')
            ))
        
        return conversations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")

@app.get("/api/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str):
    """
    Get a specific conversation by ID
    """
    if not firebase_enabled or not db:
        raise HTTPException(status_code=503, detail="Firebase not available")
    
    try:
        doc = db.collection('conversations').document(conversation_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        data = doc.to_dict()
        return ConversationResponse(
            id=doc.id,
            timestamp=data.get('timestamp', ''),
            messages=data.get('messages', []),
            model_used=data.get('model_used', 'unknown')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversation: {str(e)}")

@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get API statistics
    """
    total_conversations = 0
    total_messages = 0
    
    if firebase_enabled and db:
        try:
            docs = list(db.collection('conversations').stream())
            total_conversations = len(docs)
            total_messages = sum(len(doc.to_dict().get('messages', [])) for doc in docs)
        except Exception as e:
            print(f"Error getting stats: {e}")
    
    return StatsResponse(
        total_conversations=total_conversations,
        total_messages=total_messages,
        firebase_enabled=firebase_enabled,
        pinecone_enabled=pinecone_enabled,
        ai_model_loaded=llm is not None
    )

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation by ID
    """
    if not firebase_enabled or not db:
        raise HTTPException(status_code=503, detail="Firebase not available")
    
    try:
        db.collection('conversations').document(conversation_id).delete()
        return {"message": "Conversation deleted successfully", "id": conversation_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

@app.get("/api/chat/history/{clerk_user_id}")
async def get_user_chat_history(clerk_user_id: str, limit: int = 50):
    """
    Get chat history for a specific Clerk user
    Returns all conversations for the authenticated user
    """
    if not firebase_enabled or not db:
        raise HTTPException(status_code=503, detail="Firebase not available")
    
    try:
        # Query conversations by clerk_user_id
        conversations_ref = db.collection('conversations')
        query = conversations_ref.where('metadata.clerk_user_id', '==', clerk_user_id).order_by('timestamp', direction='DESCENDING').limit(limit)
        docs = query.stream()
        
        messages = []
        for doc in docs:
            data = doc.to_dict()
            if data and 'messages' in data:
                # Extract messages from conversation
                for msg in data['messages']:
                    messages.append({
                        'role': msg.get('role'),
                        'content': msg.get('content'),
                        'timestamp': msg.get('timestamp'),
                    })
        
        return {
            "user_id": clerk_user_id,
            "message_count": len(messages),
            "messages": messages
        }
        
    except Exception as e:
        print(f"Error loading chat history: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading chat history: {str(e)}")

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n🚀 Starting FastAPI server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔧 ReDoc: http://localhost:8000/redoc")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
