"""Level 5: execute one model-requested batch of tools with matched IDs."""

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool


def execute_tool_calls(message: AIMessage, tools: list[BaseTool]) -> list[ToolMessage]:
    """Dispatch declared calls and return one correlated result per call."""
    raise NotImplementedError("TODO LC-L5: implement execute_tool_calls")
