"""Level 10: expose lazy model text streams and close their resources."""

from collections.abc import AsyncIterator, Iterator

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


def stream_text(model: BaseChatModel, messages: list[BaseMessage]) -> Iterator[str]:
    """Yield nonempty text chunks without buffering the complete reply."""
    raise NotImplementedError("TODO LC-L10A: implement stream_text")


def astream_text(model: BaseChatModel, messages: list[BaseMessage]) -> AsyncIterator[str]:
    """Return an asynchronous text iterator with explicit stream cleanup."""
    raise NotImplementedError("TODO LC-L10B: implement astream_text")
