"""Level 7: isolate conversation history using agent checkpoints."""

from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph


def build_memory_agent(
    model: BaseChatModel, checkpointer: BaseCheckpointSaver
) -> CompiledStateGraph:
    """Create a conversational agent using the supplied checkpointer."""
    raise NotImplementedError("TODO LC-L7A: implement build_memory_agent")


def chat(agent: CompiledStateGraph, thread_id: str, text: str) -> str:
    """Submit only the new message to a specific conversation thread."""
    raise NotImplementedError("TODO LC-L7B: implement chat")
