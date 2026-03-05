"""
Embeddings without torch: OpenAI API or Hugging Face Inference API (free).
Use these to avoid langchain_openai.chat_models -> torch.
"""
from __future__ import annotations

import httpx


class HuggingFaceInferenceEmbeddings:
    """Embeddings via Hugging Face Inference API (free tier, no torch)."""

    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self._url = f"https://api-inference.huggingface.co/models/{model}"

    def _request(self, inputs: str | list[str]) -> list[list[float]]:
        with httpx.Client(timeout=60.0) as client:
            r = client.post(
                self._url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"inputs": inputs},
            )
            r.raise_for_status()
            data = r.json()
        if isinstance(data, list) and isinstance(data[0], (int, float)):
            return [data]
        return data

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        out = []
        for i in range(0, len(texts), 32):
            batch = texts[i : i + 32]
            out.extend(self._request(batch))
        return out

    def embed_query(self, text: str) -> list[float]:
        return self._request(text)[0]


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
