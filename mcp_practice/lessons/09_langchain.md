# Level 9：适配为 LangChain 异步工具

**本级只解决：怎样把已连接 MCP client 的工具交给应用层？**

前置：LangChain 的 StructuredTool、异步工具与 ToolMessage。完成 [level09_langchain.py](../level09_langchain.py) 的 make_langchain_tools(client, tools)。

- 按输入顺序返回 StructuredTool；名字保留原值，重复名字抛 ValueError。测试工具名适合 LangChain，不要求实现通用名字转义。
- description 保留原值，缺省时使用 `MCP tool {name}.`；args_schema 使用对应 input_schema，保留 required 和属性类型。
- 每个工具 coroutine 将自己的名字和参数传给 client.call_tool 一次；不同工具不能错误地共用最后一个名字。
- 使用 content_and_artifact 返回模式。成功时 content 来自 Level 1 的 tool_text，artifact 是原始 CallToolResult。
- is_error=True 时抛 LangChain ToolException，不把它伪装成成功文本；连接异常直接传播。
- 只实现异步调用，不用 asyncio.run 包装同步函数。client 生命周期属于调用者，不在适配器里连接或关闭。

```bash
python -m pytest --run-exercises tests/mcp/test_level09_langchain.py -q
```

测试使用 ToolCall 形式的 `.ainvoke()`，检查生成 ToolMessage 的关联 ID 与 artifact，并用替代文本函数隔离 Level 1。此轻量适配练习不声称覆盖 langchain-mcp-adapters 的全部能力或版本兼容矩阵。

下一步：[Level 10](10_multiserver.md)。
