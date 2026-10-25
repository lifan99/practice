"""Level 11: retrieve graph paths together with their document evidence."""

from collections.abc import Callable
from typing import TypedDict

from langchain_core.documents import Document

from .level10_knowledge_graph import KnowledgeGraph, Triple


class GraphAnswer(TypedDict):
    answer: str
    sources: list[str]
    paths: list[list[Triple]]


def find_paths(
    graph: KnowledgeGraph, start: str, target: str, max_hops: int = 3
) -> list[list[Triple]]:
    """Return bounded directed simple paths with provenance on every edge."""
    raise NotImplementedError("TODO RAG-L11A: implement find_paths")


def answer_graph_question(
    question: str,
    start: str,
    target: str,
    graph: KnowledgeGraph,
    documents: dict[str, Document],
    generator: Callable[[str, list[Triple], list[Document]], str],
    max_hops: int = 3,
) -> GraphAnswer:
    """Answer from retrieved graph facts and their supporting documents."""
    raise NotImplementedError("TODO RAG-L11B: implement answer_graph_question")
