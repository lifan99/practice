"""Core 6: compose retrieval and generation with ordinary callables."""

from .types import Answer, ChatModel, Chunk, Retriever


def format_context(chunks: list[Chunk]) -> str:
    """Render chunk IDs, sources, and evidence in a stable format."""
    raise NotImplementedError("TODO CORE-6A: implement format_context")


def answer_question(question: str, retrieve: Retriever, generate: ChatModel) -> Answer:
    """Retrieve once, abstain on no hits, and call the injected model once."""
    raise NotImplementedError("TODO CORE-6B: implement answer_question")
