"""Level 3: compose parallel analysis and explicit input routing."""

from langchain_core.runnables import Runnable


def build_parallel_analysis(summary_model: Runnable, keywords_model: Runnable) -> Runnable:
    """Return summary and keywords from two independently injected models."""
    raise NotImplementedError("TODO LC-L3A: implement build_parallel_analysis")


def build_router(routes: dict[str, Runnable], default: Runnable) -> Runnable:
    """Route each payload to its named branch or to the default runnable."""
    raise NotImplementedError("TODO LC-L3B: implement build_router")
