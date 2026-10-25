"""Level 6: measure source recall over a labeled query set."""

from typing import TypedDict

from langchain_core.runnables import Runnable


class RetrievalCase(TypedDict):
    question: str
    relevant_sources: set[str]


class QueryRecall(TypedDict):
    question: str
    recall: float


class EvaluationReport(TypedDict):
    mean_recall: float
    per_query: list[QueryRecall]


def recall_at_k(
    retrieved_sources: list[str], relevant_sources: set[str], k: int
) -> float:
    """Measure the fraction of relevant sources found in the first k hits."""
    raise NotImplementedError("TODO RAG-L6A: implement recall_at_k")


def evaluate_retrieval(
    cases: list[RetrievalCase], retriever: Runnable, k: int
) -> EvaluationReport:
    """Report source recall for each query and its unweighted mean."""
    raise NotImplementedError("TODO RAG-L6B: implement evaluate_retrieval")
