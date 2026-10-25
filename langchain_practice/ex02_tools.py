"""Exercise 2: expose a tool and validate structured model output."""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class StudyPlan(BaseModel):
    topic: str = Field(min_length=1)
    steps: list[str] = Field(min_length=1, max_length=3)
    minutes: int = Field(ge=1, le=120)


def make_word_count_tool() -> BaseTool:
    """Return a tool named word_count with a text input and an integer output."""
    raise NotImplementedError("TODO LC-2A: implement make_word_count_tool")


def parse_study_plan(text: str) -> StudyPlan:
    """Parse model JSON through a LangChain PydanticOutputParser."""
    raise NotImplementedError("TODO LC-2B: implement parse_study_plan")
