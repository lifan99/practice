# Level 1：协议对象与工具结果

**本级只解决：工具描述和一次工具调用结果分别告诉客户端什么？**

前置：字典、列表、异常。使用官方 SDK 的 mcp_types 对象，不手写 JSON-RPC 编解码。完成 [level01_protocol.py](../exercises/level01_protocol.py)。

- `summarize_tools(tools)`：返回按工具 name 升序排列的摘要，每项包含 name、description、required。description 为 None 时用空串；required 取 input_schema 的 required 列表并按字符串排序，缺省用空列表。重复工具名抛 ValueError；不修改原对象。
- `tool_text(result)`：按顺序用换行连接所有 TextContent.text，忽略其他内容块；没有文本返回空串，不解析其中的 JSON。如果 is_error=True，抛提供的 ToolCallFailed，消息为拼接后的文本，无文本时为 `Tool failed.`。

调用成功与工具业务失败可能都收到 CallToolResult；is_error 标识后者。连接错误、超时和协议错误是另一类失败，不能只检查“有没有返回文本”。structured_content 也应保留在原始结果中，不能当作所有文本块的替代品。

```bash
python -m pytest --run-exercises tests/mcp/test_level01_protocol.py -q
```

完成标准：测试通过，能区分 schema、content、structured_content 与 is_error。还需说明 tools、resources、prompts 三类能力分别用于执行、读取和模板化交互；这不表示工具描述本身就是调用授权。

下一步：[Level 2](02_tools.md)。
