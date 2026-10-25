"""Exercise 2: generate grounded answers and evaluate retrieval."""

from typing import TypedDict

from langchain_core.runnables import Runnable


class Answer(TypedDict):
    answer: str
    sources: list[str]


def answer_question(question: str, retriever: Runnable, model: Runnable) -> Answer:
    """Return an answer and the unique sources supplied as context."""
    raise NotImplementedError("TODO RAG-2A: implement answer_question")


def recall_at_k(
    retrieved_sources: list[str], relevant_sources: set[str], k: int
) -> float:
    """Measure the fraction of relevant sources found in the first k hits."""
    raise NotImplementedError("TODO RAG-2B: implement recall_at_k")
