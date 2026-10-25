"""Level 5: combine retrieval, generation, and empty-result handling."""

from typing import TypedDict

from langchain_core.runnables import Runnable

from . import level04_generation


class Answer(TypedDict):
    answer: str
    sources: list[str]


def answer_question(question: str, retriever: Runnable, model: Runnable) -> Answer:
    """Retrieve evidence and reuse level 4 to produce an answer with sources."""
    raise NotImplementedError("TODO RAG-L5: implement answer_question")
