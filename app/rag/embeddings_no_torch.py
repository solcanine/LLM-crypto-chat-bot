"""
OpenAI embeddings via the openai package only.
Use this instead of langchain_openai.embeddings to avoid importing chat_models -> transformers -> torch.
"""
from __future__ import annotations


class OpenAIEmbeddingsDirect:
    """Minimal embeddings via OpenAI API (embed_documents, embed_query). No torch."""

    def __init__(self, model: str, api_key: str):
        self.model = model
        self._client = None
        self._api_key = api_key

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self._api_key)
        return self._client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        client = self._get_client()
        out = []
        for i in range(0, len(texts), 100):
            batch = texts[i : i + 100]
            r = client.embeddings.create(input=batch, model=self.model)
            for e in sorted(r.data, key=lambda x: x.index):
                out.append(e.embedding)
        return out

    def embed_query(self, text: str) -> list[float]:
        client = self._get_client()
        r = client.embeddings.create(input=[text], model=self.model)
        return r.data[0].embedding


def get_embeddings_for_field(use_local: bool, local_model: str, openai_model: str, openai_api_key: str):
    """Return an embeddings object for ingest/retrieval. Avoids torch when use_local=False."""
    if use_local:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=local_model)
    return OpenAIEmbeddingsDirect(model=openai_model, api_key=openai_api_key)
