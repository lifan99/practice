"""Level 8: distinguish retry, fallback, and recoverable tool errors."""

from langchain.agents.middleware import AgentMiddleware
from langchain_core.runnables import Runnable


def build_resilient_chain(
    primary: Runnable, fallback: Runnable, max_attempts: int = 2
) -> Runnable:
    """Retry primary timeouts before invoking the timeout-only fallback."""
    raise NotImplementedError("TODO LC-L8A: implement build_resilient_chain")


def make_tool_error_middleware() -> AgentMiddleware:
    """Translate tool ValueError into an explicitly failed ToolMessage."""
    raise NotImplementedError("TODO LC-L8B: implement make_tool_error_middleware")
