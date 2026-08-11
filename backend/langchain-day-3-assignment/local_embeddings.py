"""Deterministic local embeddings and an in-memory vector store."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9$,.]+")


class LocalHashEmbeddings(Embeddings):
    """Small deterministic token-count embeddings for local demos and tests."""

    def __init__(self, dimensions: int = 256) -> None:
        self.dimensions = dimensions

    def _token_index(self, token: str) -> int:
        total = 0
        for position, character in enumerate(token):
            total += (position + 1) * ord(character)
        return total % self.dimensions

    def _embed(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions
        tokens = TOKEN_PATTERN.findall(text.lower())
        for token in tokens:
            vector[self._token_index(token)] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed a query string."""
        return self._embed(text)


def cosine_similarity(left: List[float], right: List[float]) -> float:
    """Return cosine similarity for normalized vectors."""
    return sum(a * b for a, b in zip(left, right))


@dataclass
class _StoredDocument:
    document: Document
    embedding: List[float]


class SimpleMemoryVectorStore:
    """Tiny in-memory vector store with a LangChain-like similarity_search method."""

    def __init__(self, embeddings: Embeddings) -> None:
        self.embeddings = embeddings
        self._documents: List[_StoredDocument] = []

    @classmethod
    def from_documents(cls, documents: List[Document], embeddings: Embeddings) -> "SimpleMemoryVectorStore":
        """Create a vector store from documents."""
        store = cls(embeddings)
        vectors = embeddings.embed_documents([document.page_content for document in documents])
        store._documents = [
            _StoredDocument(document=document, embedding=embedding)
            for document, embedding in zip(documents, vectors)
        ]
        return store

    def similarity_search(self, query: str, k: int = 4, filter: Optional[dict] = None) -> List[Document]:
        """Return the k most similar documents, optionally filtered by metadata."""
        query_embedding = self.embeddings.embed_query(query)
        scored = []
        for stored in self._documents:
            if filter and any(stored.document.metadata.get(key) != value for key, value in filter.items()):
                continue
            score = cosine_similarity(query_embedding, stored.embedding)
            scored.append((score, stored.document))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [document for _, document in scored[:k]]
