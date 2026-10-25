"""Core 7: measure retrieval coverage and ranking quality."""

from .types import RetrievalCase, Retriever


def recall_at_k(ranked_ids: list[str], relevant_ids: set[str], k: int) -> float:
    """Measure unique relevant IDs in the first k result positions."""
    raise NotImplementedError("TODO CORE-7A: implement recall_at_k")


def reciprocal_rank_at_k(ranked_ids: list[str], relevant_ids: set[str], k: int) -> float:
    """Return the reciprocal position of the first relevant hit."""
    raise NotImplementedError("TODO CORE-7B: implement reciprocal_rank_at_k")


def ndcg_at_k(ranked_ids: list[str], relevance: dict[str, int], k: int) -> float:
    """Measure graded ranking using exponential gains and log2 discounts."""
    raise NotImplementedError("TODO CORE-7C: implement ndcg_at_k")


def evaluate(cases: list[RetrievalCase], retrieve: Retriever, k: int) -> dict[str, float]:
    """Return macro recall, MRR, and NDCG for a fixed labeled query set."""
    raise NotImplementedError("TODO CORE-7D: implement evaluate")
