"""Provided offline fixtures; these are infrastructure, not exercise answers."""

import re

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.fake_chat_models import FakeListChatModel


class KeywordEmbeddings(Embeddings):
    """Deterministic word counts for plumbing tests, not semantic embeddings."""

    vocabulary = (
        "langchain", "prompt", "tool", "langgraph", "graph", "checkpoint",
        "rag", "retrieval", "vector", "source",
    )

    def _encode(self, text: str) -> list[float]:
        words = re.findall(r"[a-z]+", text.casefold())
        counts = [float(words.count(word)) for word in self.vocabulary]
        return counts + [0.0 if any(counts) else 1.0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._encode(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._encode(text)


def fake_chat_model(*responses: str) -> FakeListChatModel:
    """Create a preset-response model without a network call."""
    if not responses:
        raise ValueError("At least one response is required.")
    return FakeListChatModel(responses=list(responses))
