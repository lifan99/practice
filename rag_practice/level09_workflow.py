"""Level 9: orchestrate bounded retrieval correction with LangGraph."""

from collections.abc import Callable
from typing import TypedDict

from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langgraph.graph.state import CompiledStateGraph


class AdaptiveRAGState(TypedDict, total=False):
    question: str
    query: str
    documents: list[Document]
    accepted: bool
    attempts: int
    rewrites: int
    answer: str
    sources: list[str]
    status: str
    trace: list[str]


def build_adaptive_rag(
    retriever: Runnable,
    grader: Callable[[str, list[Document]], bool],
    rewriter: Callable[[str], str],
    generator: Callable[[str, list[Document]], str],
    max_rewrites: int = 2,
) -> CompiledStateGraph:
    """Build a graph that grades evidence, rewrites queries, and terminates."""
    raise NotImplementedError("TODO RAG-L9: implement build_adaptive_rag")
