"""Exercise 1: compose a prompt, a chat model, and a string parser."""

from langchain_core.runnables import Runnable


def build_chain(model: Runnable) -> Runnable:
    """Accept topic/audience inputs and produce a parsed model response."""
    raise NotImplementedError("TODO LC-1: implement build_chain")
