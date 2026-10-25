"""Level 4: request structured model output and enforce a business limit."""

from langchain_core.language_models import BaseChatModel

from .ex02_tools import StudyPlan


def generate_plan(model: BaseChatModel, topic: str, max_minutes: int = 60) -> StudyPlan:
    """Request a StudyPlan and reject plans exceeding the caller's budget."""
    raise NotImplementedError("TODO LC-L4: implement generate_plan")
