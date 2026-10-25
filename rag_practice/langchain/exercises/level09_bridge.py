"""Adapter exercises: convert boundary types without changing core logic."""

from langchain_core.documents import Document as LangChainDocument
from langchain_core.runnables import Runnable

from rag_practice.core.types import ChatModel, Chunk, Retriever


def to_langchain(chunk: Chunk) -> LangChainDocument:
    """Preserve content, identity, source, and offsets in a LangChain document."""
    raise NotImplementedError("TODO ADAPTER-1A: implement to_langchain")


def from_langchain(document: LangChainDocument) -> Chunk:
    """Restore a core chunk from the adapter's metadata contract."""
    raise NotImplementedError("TODO ADAPTER-1B: implement from_langchain")


def as_core_retriever(retriever: Runnable) -> Retriever:
    """Adapt LangChain documents to core hits with neutral score zero."""
    raise NotImplementedError("TODO ADAPTER-2: implement as_core_retriever")


def as_core_chat_model(model: Runnable) -> ChatModel:
    """Convert plain role/content messages and return text content."""
    raise NotImplementedError("TODO ADAPTER-3: implement as_core_chat_model")
