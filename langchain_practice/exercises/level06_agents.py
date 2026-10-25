"""Level 6: configure the native LangChain tool-calling agent loop."""

from langchain.agents.middleware import AgentMiddleware
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph


def build_tool_agent(
    model: BaseChatModel,
    tools: list[BaseTool],
    middleware: list[AgentMiddleware] | None = None,
) -> CompiledStateGraph:
    """Build a create_agent workflow with injected tools and middleware."""
    raise NotImplementedError("TODO LC-L6: implement build_tool_agent")
