"""Level 4: generate an answer from explicitly supplied evidence."""

from langchain_core.documents import Document
from langchain_core.runnables import Runnable


def format_context(documents: list[Document]) -> str:
    """Format each source and its evidence as a traceable context block."""
    raise NotImplementedError("TODO RAG-L4A: implement format_context")


def generate_answer(question: str, documents: list[Document], model: Runnable) -> str:
    """Ask the injected model to answer using only the supplied documents."""
    raise NotImplementedError("TODO RAG-L4B: implement generate_answer")
