"""Provided scripted chat fixture; it does not choose or execute tools."""

from typing import Any

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field


class ScriptedChatModel(BaseChatModel):
    """Return preset messages so native agent tool protocols can be tested."""

    responses: list[AIMessage]
    calls: int = 0
    recorded_messages: list[list[BaseMessage]] = Field(default_factory=list, exclude=True)
    bound_tool_names: list[str] = Field(default_factory=list, exclude=True)

    @property
    def _llm_type(self) -> str:
        return "scripted-offline-chat"

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):
        names = []
        for tool in tools:
            if isinstance(tool, dict):
                names.append(tool.get("name") or tool.get("function", {}).get("name", ""))
            else:
                names.append(tool.name)
        self.bound_tool_names = names
        return self

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.calls >= len(self.responses):
            raise RuntimeError("The offline response script is exhausted.")
        self.recorded_messages.append([message.model_copy(deep=True) for message in messages])
        response = self.responses[self.calls].model_copy(deep=True)
        self.calls += 1
        return ChatResult(generations=[ChatGeneration(message=response)])
