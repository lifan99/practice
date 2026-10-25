"""Level 1: inspect descriptors and distinguish tool result errors."""

from copy import deepcopy

import pytest
from mcp_types import CallToolResult, ImageContent, TextContent, Tool

from mcp_practice.level01_protocol import ToolCallFailed, summarize_tools, tool_text

pytestmark = pytest.mark.exercise


def test_tool_summaries_sort_without_mutation():
    tools = [Tool(name="z", input_schema={"type": "object"}), Tool(name="a", description="Add values", input_schema={"type": "object", "required": ["z", "a"]})]
    snapshot = deepcopy(tools)
    assert summarize_tools(tools) == [{"name": "a", "description": "Add values", "required": ["a", "z"]}, {"name": "z", "description": "", "required": []}]
    assert tools == snapshot


def test_duplicate_tool_names():
    descriptor = Tool(name="echo", input_schema={"type": "object"})
    with pytest.raises(ValueError):
        summarize_tools([descriptor, descriptor])


def test_empty_tools():
    assert summarize_tools([]) == []


def test_text_content_preserves_order_and_ignores_other_blocks():
    result = CallToolResult(content=[TextContent(type="text", text="first"), ImageContent(type="image", data="AA==", mime_type="image/png"), TextContent(type="text", text="second")], structured_content={"result": 3})
    snapshot = deepcopy(result)
    assert tool_text(result) == "first\nsecond"
    assert result == snapshot


def test_no_text_content():
    assert tool_text(CallToolResult(content=[])) == ""


@pytest.mark.parametrize("content,message", [([], "Tool failed."), ([TextContent(type="text", text="rejected")], "rejected")])
def test_tool_error_is_not_successful_text(content, message):
    with pytest.raises(ToolCallFailed) as caught:
        tool_text(CallToolResult(content=content, is_error=True))
    assert str(caught.value) == message
