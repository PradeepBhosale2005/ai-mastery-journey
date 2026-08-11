"""Small deterministic embeddings for the Mini-RAG assignment.

This avoids external embedding API calls and keeps the assignment runnable when
corporate security blocks SaaS APIs. The class follows LangChain's Embeddings
interface and is suitable for a tiny demo text file.
"""

import hashlib
import math
import re
from typing import List

from langchain_core.embeddings import Embeddings


class HashEmbeddings(Embeddings):
    """Deterministic bag-of-words hash embeddings for local demos."""

    def __init__(self, dimensions: int = 128) -> None:
        self.dimensions = dimensions

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of document strings."""
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed one query string."""
        return self._embed(text)

    def _embed(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions
        words = re.findall(r"[a-zA-Z0-9]+", text.lower())

        for word in words:
            digest = hashlib.sha256(word.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], byteorder="big") % self.dimensions
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector

        return [value / norm for value in vector]
