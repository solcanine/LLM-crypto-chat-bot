import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Fields (chain-specific knowledge)
FIELD_NAMES = ["solana", "evm"]

# Paths (project root = parent of app/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"

# Ensure dirs exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# Per-field data subdirs
SOLANA_DATA_DIR = DATA_DIR / "solana"
EVM_DATA_DIR = DATA_DIR / "evm"
SOLANA_DATA_DIR.mkdir(parents=True, exist_ok=True)
EVM_DATA_DIR.mkdir(parents=True, exist_ok=True)

# FAISS index path per field (vector_store/solana, vector_store/evm)
def get_faiss_index_path(field: str) -> Path:
    return VECTOR_STORE_DIR / field

# API and models
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
# Embeddings: "openai" | "huggingface" (free API) | "local" (sentence-transformers, needs torch)
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
if EMBEDDING_PROVIDER not in ("openai", "huggingface", "local"):
    EMBEDDING_PROVIDER = "huggingface"
# Hugging Face free inference API (no OpenAI quota, no torch)
HF_TOKEN = os.getenv("HF_TOKEN", "") or os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
# OpenAI embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
# Local (sentence-transformers) - needs torch
USE_LOCAL_EMBEDDINGS = EMBEDDING_PROVIDER == "local"
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# RAG
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVE_TOP_K = 4
