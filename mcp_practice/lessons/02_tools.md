# Level 2：构建 typed tools server

**本级只解决：怎样把带类型的 Python 函数注册为 MCP 工具？**

完成 [level02_tools.py](../level02_tools.py) 的 build_calculator_server，返回官方 `mcp.server.MCPServer`，注册两个有非空英文说明的工具：

- add(a: int, b: int) -> int：返回 a+b。
- divide(a: float, b: float) -> float：返回 a/b；b 为 0 时抛 SDK 的 ToolError，消息包含 `nonzero`。

SDK 应产生对应的 input schema、结果内容与结构化结果。普通数值输出在本 SDK 中表现为 structured_content 的 result 字段。参数校验由 SDK 处理，不要求拒绝它允许的类型转换。工具函数可使用 async def。每次构建独立 server，不启动端口或子进程。

ToolError 从 mcp.server.mcpserver.exceptions 导入，表示预期的工具业务错误；普通意外异常在 SDK v2 中可能被隐藏细节，不能依赖其原始文本出现在客户端。

```bash
python -m pytest --run-exercises tests/mcp/test_level02_tools.py -q
```

测试通过 Client(server) 做真实的进程内 MCP 调用，检查工具发现、有效参数、无效参数和业务错误；不使用手写的假 server。

完成后可运行 `python -m mcp_practice.run_server --transport stdio`，由另一个 MCP 客户端连接。stdio 的 stdout 是协议通道，不输出调试 print；诊断日志走 stderr。

下一步：[Level 3](03_context.md)。
