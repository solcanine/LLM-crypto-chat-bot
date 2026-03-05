"""
Ingest documents per field (solana / evm): load from data/{field}/,
chunk, embed, and persist to FAISS index per field.
Uses pure-Python file loading and splitting to avoid torch/transformers (Windows DLL issues).
Run: python -m app.rag.ingest
"""
from pathlib import Path

from app.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_PROVIDER,
    EVM_DATA_DIR,
    FIELD_NAMES,
    HF_EMBEDDING_MODEL,
    HF_TOKEN,
    LOCAL_EMBEDDING_MODEL,
    SOLANA_DATA_DIR,
    USE_LOCAL_EMBEDDINGS,
    get_faiss_index_path,
)


# Map field name to data directory
FIELD_TO_DIR = {
    "solana": SOLANA_DATA_DIR,
    "evm": EVM_DATA_DIR,
}


def _read_text_file(path: Path) -> str:
    """Read a .md or .txt file with utf-8 or fallback encoding."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def _read_pdf(path: Path) -> str:
    """Extract text from a PDF file."""
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_documents(data_dir: Path) -> list[tuple[str, dict]]:
    """
    Load .md, .txt, and .pdf from data_dir. Returns list of (text, metadata) with source path.
    No LangChain loaders (avoids torch/transformers import).
    """
    from langchain_core.documents import Document

    docs = []
    for ext in ("*.md", "*.txt", "**/*.md", "**/*.txt"):
        for path in data_dir.glob(ext):
            if not path.is_file():
                continue
            try:
                text = _read_text_file(path)
                docs.append(Document(page_content=text, metadata={"source": str(path)}))
            except Exception as e:
                print(f"  [skip] {path}: {e}")
    for path in list(data_dir.glob("**/*.pdf")):
        if not path.is_file():
            continue
        try:
            text = _read_pdf(path)
            if text.strip():
                docs.append(Document(page_content=text, metadata={"source": str(path)}))
        except Exception as e:
            print(f"  [skip] {path}: {e}")
    return docs


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into chunks of chunk_size with overlap. No external deps."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    step = chunk_size - overlap
    if step <= 0:
        step = chunk_size
    out = []
    for start in range(0, len(text), step):
        chunk = text[start : start + chunk_size]
        if chunk.strip():
            out.append(chunk)
    return out


def split_documents(docs: list) -> list:
    """Split documents into chunks. Returns list of Document with chunked page_content."""
    from langchain_core.documents import Document

    chunks = []
    for doc in docs:
        parts = _split_text(doc.page_content, CHUNK_SIZE, CHUNK_OVERLAP)
        for p in parts:
            if p.strip():
                chunks.append(Document(page_content=p.strip(), metadata=dict(doc.metadata)))
    return chunks


def ingest_field(field: str) -> None:
    """Ingest one field: load docs from data/{field}/, chunk, embed, persist to FAISS."""
    if field not in FIELD_NAMES:
        raise ValueError(f"field must be one of {FIELD_NAMES}")
    data_dir = FIELD_TO_DIR[field]
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)

    docs = load_documents(data_dir)
    if not docs:
        print(f"[{field}] No documents in {data_dir}. Add .md, .txt, or .pdf files and re-run.")
        return

    chunks = split_documents(docs)
    print(f"[{field}] Loaded {len(docs)} docs, split into {len(chunks)} chunks.")

    if EMBEDDING_PROVIDER == "huggingface":
        from app.rag.embeddings_no_torch import HuggingFaceInferenceEmbeddings
        if not HF_TOKEN:
            print("HF_TOKEN not set. Get a free token at https://huggingface.co/settings/tokens and set HF_TOKEN in .env")
            return
        embeddings = HuggingFaceInferenceEmbeddings(model=HF_EMBEDDING_MODEL, api_key=HF_TOKEN)
    elif EMBEDDING_PROVIDER == "openai":
        from app.config import OPENAI_API_KEY, EMBEDDING_MODEL
        from app.rag.embeddings_no_torch import OpenAIEmbeddingsDirect
        if not OPENAI_API_KEY:
            print("OPENAI_API_KEY not set. Set it in .env or use EMBEDDING_PROVIDER=huggingface with HF_TOKEN.")
            return
        embeddings = OpenAIEmbeddingsDirect(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)
    else:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name=LOCAL_EMBEDDING_MODEL)

    from langchain_community.vectorstores import FAISS

    try:
        vector_store = FAISS.from_documents(chunks, embeddings)
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "quota" in err_msg or "ratelimit" in err_msg:
            print(
                "[ERROR] OpenAI API quota exceeded (429). Use free embeddings instead:\n"
                "  Set in .env: EMBEDDING_PROVIDER=huggingface and HF_TOKEN=hf_xxx\n"
                "  Get a free token at https://huggingface.co/settings/tokens\n"
                "  Then run: python -m app.rag.ingest"
            )
        raise
    index_path = get_faiss_index_path(field)
    index_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(index_path))
    print(f"[{field}] Persisted FAISS index to {index_path}.")


def main():
    """Ingest all fields."""
    for field in FIELD_NAMES:
        ingest_field(field)


if __name__ == "__main__":
    main()
