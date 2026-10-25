# Level 7：并发、超时、取消与进度

**本级只解决：多个或较慢的工具调用，怎样保持有界和可观察？**

完成 [level07_execution.py](../exercises/level07_execution.py)。

## A：客户端执行约束

call_tools_bounded 接收已经连接的 client 和 ToolCall 列表。

- max_concurrency 为正整数；timeout_seconds 为有限正数，否则在调用客户端前抛 ValueError，空列表也先校验。
- 每项调用 client.call_tool(name, arguments) 一次，最多 max_concurrency 项同时执行；不得自动重试。
- timeout_seconds 是每项实际开始调用后的期限，不把等待并发名额的时间算入。超时返回该位置的 TimeoutError，取消底层等待。
- 返回顺序与输入一致；普通 Exception 保留为对应异常对象，其他项继续完成。
- is_error=True 的 CallToolResult 仍是结果对象，不与连接异常混为一谈。
- 外层取消须传播，并等待已启动的子任务退出；不修改输入或关闭调用者拥有的 client。

这里的“一次”指应用层 call_tool 调用。SDK 可能为版本或工具 schema 协商补充协议请求，本题不承诺分布式调用的 exactly-once 语义。

## B：server 进度

build_progress_server 返回 MCPServer，注册异步工具 count_steps(steps: int, ctx: Context) -> int，Context 从 `mcp.server.mcpserver` 导入，由 SDK 注入，不出现在工具输入 schema。

- steps 在 1–5 之间，否则抛 SDK ToolError，不发送进度。
- 每步报告 progress=i、total=steps、message=`step {i}`，i 从 1 递增到 steps；各步允许协作式调度，不作阻塞等待。
- 返回 steps；未传 progress_callback 时也应成功。

```bash
python -m pytest --run-exercises tests/mcp/test_level07_execution.py -q
```

进度测试采用进程内 Client，确保回调已交付后断言结果；真实传输的回调可能与最终响应交错，不能照搬时序假设。[官方进度说明](https://py.sdk.modelcontextprotocol.io/handlers/progress/)

下一步：[Level 8](08_files.md)。
