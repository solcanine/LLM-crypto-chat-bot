"""
RAG chain per field: load FAISS index by field, retrieve, then LLM with context.
Uses direct OpenAI API (no ChatOpenAI) to avoid langchain_openai.chat_models -> transformers -> torch.
Exposes get_answer(field, message) -> str.
"""
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import (
    EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    FIELD_NAMES,
    HF_EMBEDDING_MODEL,
    HF_TOKEN,
    LOCAL_EMBEDDING_MODEL,
    LLM_MODEL,
    OPENAI_API_KEY,
    RETRIEVE_TOP_K,
    get_faiss_index_path,
)

SYSTEM_TEMPLATE = """You are a helpful expert for the {field} blockchain ecosystem.
Answer the user's question using the following context when possible.
If the context does not contain relevant information, say so and give a brief general answer.
Do not make up details that are not in the context.

Context:
{context}"""


def _get_retriever(field: str):
    """Load FAISS index for the given field and return a retriever."""
    index_path = Path(get_faiss_index_path(field))
    index_file = index_path / "index.faiss"
    if not index_file.exists():
        raise FileNotFoundError(
            f"Vector index not found for '{field}'. Run from project root: python -m app.rag.ingest"
        )
    if EMBEDDING_PROVIDER == "huggingface":
        from app.rag.embeddings_no_torch import HuggingFaceInferenceEmbeddings
        embeddings = HuggingFaceInferenceEmbeddings(model=HF_EMBEDDING_MODEL, api_key=HF_TOKEN)
    elif EMBEDDING_PROVIDER == "openai":
        from app.rag.embeddings_no_torch import OpenAIEmbeddingsDirect
        embeddings = OpenAIEmbeddingsDirect(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)
    else:
        embeddings = HuggingFaceEmbeddings(model_name=LOCAL_EMBEDDING_MODEL)
    try:
        vector_store = FAISS.load_local(
            str(index_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )
    except Exception as e:
        raise FileNotFoundError(
            f"Vector index not found or invalid for '{field}'. Run: python -m app.rag.ingest. ({e})"
        ) from e
    return vector_store.as_retriever(search_kwargs={"k": RETRIEVE_TOP_K})


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def _call_openai_chat(system: str, user: str) -> str:
    """Call OpenAI Chat Completions API directly (no LangChain chat model -> no torch)."""
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0,
    )
    return (resp.choices[0].message.content or "").strip()


def get_answer(field: str, message: str) -> str:
    """
    Run RAG for the given field and user message; return the assistant reply.
    field must be one of FIELD_NAMES (e.g. 'solana', 'evm').
    """
    if field not in FIELD_NAMES:
        raise ValueError(f"field must be one of {FIELD_NAMES}")

    retriever = _get_retriever(field)
    docs = retriever.invoke(message)
    context = _format_docs(docs)
    system = SYSTEM_TEMPLATE.format(context=context, field=field)
    return _call_openai_chat(system, message)
