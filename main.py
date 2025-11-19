from llama_cpp import Llama
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import RedisCache
import redis
import hashlib
from datetime import datetime
import uuid
from transformers import pipeline

import os



# crash the whole process at module-import time when running under Uvicorn).
# If pinecone raises anything during import (for example because an old
# `pinecone-client` package is present), we'll catch it, log it, and continue
# with Pinecone disabled. This lets the web server bind and respond to health
# checks while we investigate the dependency issue.
pinecone = None
PINECONE_AVAILABLE = False
try:
    # Importing pinecone can raise a runtime Exception if an incompatible
    # `pinecone-client` package is installed in the environment; catch any
    # Exception (not only ImportError) so startup is resilient.
    import pinecone as _pinecone
    from langchain_community.embeddings import HuggingFaceEmbeddings

    pinecone = _pinecone
    PINECONE_AVAILABLE = True
except Exception as e:
    # Non-fatal at startup: log and continue with Pinecone disabled.
    # application will still run and can use Redis or in-memory cache.
    print(f"⚠️  Pinecone import failed at startup (continuing without Pinecone): {e}")
    pinecone = None
    PINECONE_AVAILABLE = False

# Firebase integration
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    import uuid
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

print("=" * 60)
print("Educational Explainer (Mistral-7B + Pinecone + Firebase)")
print("=" * 60)

# Initialize Pinecone (if available)
pinecone_index = None
embeddings = None

if PINECONE_AVAILABLE:
    try:
        print("\n🔗 Connecting to Pinecone...")
        # Use environment variable for API key in production. Do NOT hardcode secrets.
        PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
        INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "mindnex-responses")

        if not PINECONE_API_KEY:
            raise RuntimeError("PINECONE_API_KEY not set in environment")

        # Initialize the official pinecone client
        pinecone.init(api_key=PINECONE_API_KEY)
        pinecone_index = pinecone.Index(INDEX_NAME)

        # Initialize embeddings
        print("🔤 Loading embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

        # Check index stats
        stats = pinecone_index.describe_index_stats()
        print(f"✅ Pinecone connected! ({stats['total_vector_count']} vectors stored)\n")
    except Exception as e:
        print(f"⚠️  Pinecone connection failed: {e}")
        print("💾 Responses will only be cached in Redis.\n")
        pinecone_index = None
        embeddings = None
else:
    print("\n⚠️  Pinecone not installed. Responses will only be cached in Redis.")
    print("💡 Install with: pip install pinecone sentence-transformers\n")

# Initialize Firebase Firestore (if available)
firebase_db = None
firebase_enabled = False

if FIREBASE_AVAILABLE:
    try:
        print("\n🔗 Connecting to Firebase Firestore...")

        # Support multiple ways to provide the service account:
        # 1) FIREBASE_SERVICE_ACCOUNT_PATH -> path to JSON file
        # 2) FIREBASE_SERVICE_ACCOUNT_JSON -> full JSON string in env
        # 3) individual env vars (FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL, FIREBASE_PROJECT_ID, ...)
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
                # If the env contains escaped newlines, try fixing private_key field
                try:
                    tmp = sa_json_env.replace('\\n', '\n')
                    cred_json = json.loads(tmp)
                except Exception as _e:
                    print(f"⚠️  FIREBASE_SERVICE_ACCOUNT_JSON could not be parsed as JSON: {_e}")
                    cred_json = None
        else:
            # Fallback to individual env vars (common on some deploy platforms)
            pk = os.environ.get("FIREBASE_PRIVATE_KEY")
            client_email = os.environ.get("FIREBASE_CLIENT_EMAIL")
            project_id = os.environ.get("FIREBASE_PROJECT_ID")
            if pk and client_email and project_id:
                # ensure newlines in the private key are correct
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
            # Normalize escaped newlines in private_key if present
            pk = cred_json.get("private_key")
            if isinstance(pk, str):
                cred_json["private_key"] = pk.replace('\\n', '\n')

            # Initialize Firebase app once
            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_json)
                firebase_admin.initialize_app(cred)

            firebase_db = firestore.client()
            firebase_enabled = True
            print(f"✅ Firebase connected! Project: {cred_json.get('project_id')}")
            print("✅ Stateless storage enabled (no login required)\n")

    except Exception as e:
        print(f"⚠️  Firebase connection failed: {e}")
        print("💾 Responses will be saved to Pinecone/redis only.\n")
        firebase_db = None
        firebase_enabled = False
else:
    print("\n⚠️  Firebase not installed. Install with: pip install firebase-admin\n")

print("\nInitializing cache...")
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    # Use Redis cache for persistent storage
    set_llm_cache(RedisCache(redis_client))
    print("✅ Redis cache connected! Data will persist across runs.\n")
except Exception as e:
    print(f"⚠️  Redis connection failed: {e}")
    print("💾 Using in-memory cache (data will be lost when program ends).\n")
    set_llm_cache(InMemoryCache())
    redis_client = None

print("\nLoading Mistral-7B model (GGUF quantized)...")
print("This uses Apple Silicon GPU acceleration!\n")
llm = None
_model_file_candidates = [
    "./models/Mistral-7B-Instruct-v0.3.Q4_K_M.gguf",
    "./Mistral-7B-Instruct-v0.3.Q4_K_M.gguf",
]
_model_path = None
for _p in _model_file_candidates:
    try:
        if os.path.isfile(_p):
            _model_path = _p
            break
    except Exception:
        continue

if not _model_path:
    print("⚠️  GGUF model file not found in ./models or repo root. Skipping model load.")
else:
    try:
        llm = LlamaCpp(
            model_path=_model_path,
            n_ctx=4096,
            n_threads=4,
            n_gpu_layers=50,
            temperature=0.7,
            top_p=0.95,
            repeat_penalty=1.2,
            max_tokens=300,
            verbose=False
        )
        print(f"Model loaded successfully from {_model_path}!\n")
    except Exception as _e:
        print(f"❌ AI Model failed to load from {_model_path}: {_e}")
        llm = None

# Create prompt template with LangChain
prompt_template = PromptTemplate(
    input_variables=["topic", "age"],
    template="[INST] Explain {topic} in detail for a {age} year old to understand. [/INST]"
)

# Create chain using LCEL (LangChain Expression Language) only if LLM loaded
if llm is not None:
    try:
        chain = prompt_template | llm
    except Exception as _e:
        print(f"⚠️  Failed to compose LangChain chain: {_e}")
        chain = None
else:
    chain = None


def store_in_pinecone(topic: str, response: str, age: str):
    """Store response in Pinecone vector database"""
    
    if not pinecone_index or not embeddings:
        return None
    
    try:
        print("\n💾 Storing in Pinecone...")
        
        # Generate embedding
        embedding = embeddings.embed_query(response)
        
        # Create unique ID
        vector_id = f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(topic) % 10000}"
        
        # Prepare metadata
        metadata = {
            'topic': topic,
            'age': int(age) if age.isdigit() else 12,
            'response': response,
            'word_count': len(response.split()),
            'character_count': len(response),
            'timestamp': datetime.now().isoformat(),
            'response_preview': response[:200]
        }
        
        # Store in Pinecone
        pinecone_index.upsert(
            vectors=[{
                'id': vector_id,
                'values': embedding,
                'metadata': metadata
            }]
        )
        
        print(f"   ✅ Stored in Pinecone with ID: {vector_id}")
        
        # Also cache in Redis
        if redis_client:
            cache_key = f"pinecone:{vector_id}"
            redis_client.set(cache_key, str(metadata))
            print(f"   ✅ Cached in Redis: {cache_key}")
        
        return vector_id
    
    except Exception as e:
        print(f"   ⚠️  Pinecone storage failed: {e}")
        return None


def store_in_firebase(topic: str, response: str, age: str, embedding_id: str | None = None):
    """Store response in Firebase Firestore (no login required)"""
    
    if not firebase_enabled or not firebase_db:
        return None
    
    try:
        print("\n🔥 Storing in Firebase...")
        
        # Auto-generate unique chat ID
        chat_id = str(uuid.uuid4())
        
        # Create conversation document
        conversation_data = {
            'timestamp': datetime.now().isoformat(),
            'model_used': 'mindneox-v1',  # Mistral 7B
            'messages': [
                {
                    'role': 'user',
                    'content': f"Explain {topic} for a {age} year old",
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().isoformat(),
                    'word_count': len(response.split()),
                    'char_count': len(response)
                }
            ],
            'embedding_id': embedding_id if embedding_id else None,
            'embedding_status': 'stored' if embedding_id else 'not_stored',
            'metadata': {
                'source': 'educational_explainer',
                'topic': topic,
                'age': int(age) if age.isdigit() else 12
            }
        }
        
        # Store in Firestore: conversations/{chatID}
        firebase_db.collection('conversations').document(chat_id).set(conversation_data)
        
        print(f"   ✅ Stored in Firebase with ID: {chat_id[:8]}...")
        
        return chat_id
        
    except Exception as e:
        print(f"   ⚠️  Firebase storage failed: {e}")
        return None


def generate_text(topic: str, age: str) -> str:
    """Generate text using Mistral-7B GGUF model with LangChain caching"""
    
    try:
        print("Generating response...")
        # If chain isn't available, return a friendly message
        if chain is None:
            return "AI model not available. Please ensure the GGUF model is present or run with RUN_LLAMA_NATIVE=1 to use native Llama." 

        # Use LangChain to generate response (caching is handled automatically by LangChain)
        response = chain.invoke({"topic": topic, "age": age})
        
        # Store in Pinecone if available
        embedding_id = None
        if pinecone_index and embeddings:
            embedding_id = store_in_pinecone(topic, response, age)
        
        # Store in Firebase if available
        if firebase_enabled and firebase_db:
            store_in_firebase(topic, response, age, embedding_id)
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"


if __name__ == "__main__":
    topic = input("Enter topic: ")
    age = input("Enter age: ")
    text = generate_text(topic, age)
    print("\n--- MODEL OUTPUT ---\n")
    print(text)
    
    print("\n" + "="*60)
    print("✅ Response saved to:")
    if redis_client:
        print("   • Redis cache (for fast retrieval)")
    if pinecone_index:
        print("   • Pinecone vector database (for semantic search)")
    if firebase_enabled:
        print("   • Firebase Firestore (stateless storage, no login)")
    
    if pinecone_index or firebase_enabled:
        print("\n💡 Search for similar responses:")
        print("   python pinecone_integration.py")
    print("="*60)

    # Optional: run a direct Llama native call if requested
    # Set environment variable RUN_LLAMA_NATIVE=1 to enable
    if os.environ.get('RUN_LLAMA_NATIVE', '0') == '1':
        print("\n🔬 Running direct Llama native call...")
        try:
            from llama_cpp import Llama as LlamaNative
            import os as _os

            # prefer models/ path but fall back to repo root filename
            _candidate_paths = ["./models/Mistral-7B-Instruct-v0.3.Q4_K_M.gguf", "./Mistral-7B-Instruct-v0.3.Q4_K_M.gguf"]
            _model_path = next((p for p in _candidate_paths if _os.path.isfile(p)), _candidate_paths[0])

            if not _os.path.isfile(_model_path):
                print(f"⚠️  Model file not found at {_model_path}. Skipping native Llama call.")
            else:
                print("🚀 Loading Mistral model...")
                llm_native = LlamaNative(
                    model_path=_model_path,
                    n_ctx=4096,
                    n_threads=4,
                    n_gpu_layers=40,  # tuned for Apple Silicon GPU
                    verbose=True
                )

                prompt = "What is Mindneox.ai?"
                out = llm_native(prompt, max_tokens=150)

                # Output shape may vary between versions; try to extract text safely
                resp_text = None
                if isinstance(out, dict):
                    # common shape: {'choices': [{'text': '...'}]}
                    choices = out.get('choices') or out.get('data')
                    if choices and isinstance(choices, list) and len(choices) > 0:
                        first = choices[0]
                        if isinstance(first, dict):
                            resp_text = first.get('text') or first.get('generated_text') or str(first)
                        else:
                            resp_text = str(first)
                elif isinstance(out, str):
                    resp_text = out

                print('\n🧠 Response:', resp_text)

        except Exception as _e:
            print(f"⚠️  Direct Llama native call failed: {_e}")

    # Optional: quick Llama native test (use env var RUN_LLAMA_TEST=1 to run)
    if os.environ.get('RUN_LLAMA_TEST', '0') == '1':
        print('\n🔬 Running quick Llama native test...')
        try:
            from llama_cpp import Llama as LlamaNative
            llm_native = LlamaNative(
                model_path="./models/mistral-7b-instruct-v0.3.Q4_K_M.gguf",
                n_ctx=4096,
                n_threads=4,
            )
            resp = llm_native("Hello! How are you?")
            print('\n--- LLAMA NATIVE RESPONSE ---')
            print(resp)
        except Exception as e:
            print(f"⚠️  Llama native test failed: {e}")
