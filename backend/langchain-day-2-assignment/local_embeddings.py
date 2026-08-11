"""Small deterministic embeddings for local demos and tests.

These embeddings avoid external model downloads while still enabling vector
similarity examples for RAG and metadata-filtering assignments.
"""

import hashlib
import math
import re
from typing import List

from langchain_core.embeddings import Embeddings


class SimpleHashEmbeddings(Embeddings):
    """Deterministic bag-of-words hash embeddings."""

    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def _embed(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions
        tokens = re.findall(r"[A-Za-z0-9]+", text.lower())
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
            index = int(digest, 16) % self.dimensions
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)


def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
    """Compute cosine similarity for already normalized vectors."""
    return sum(a * b for a, b in zip(vector_a, vector_b))
