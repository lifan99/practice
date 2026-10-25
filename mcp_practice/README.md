# MCP 基础与进阶练习

使用官方 **MCP Python SDK 2.3.0**，Python 3.12，分为基础五级和进阶五级。每级提供任务说明、TODO 骨架与独立验收；不附完整答案，不需要模型 API Key。

## 版本与学习边界

本套以 2026-10-25 核对的 SDK v2 / 2026-07-28 协议文档为依据。使用 MCPServer、Client 和 mcp_types 的 snake_case Python 字段；不混用旧版 FastMCP / ClientSession.initialize 示例。兼容旧协议时的协商交给 SDK，不自行实现 JSON-RPC 或初始化流程。

MCP 定义应用与服务之间的能力和通信协议，本身不替你选择模型、规划工具调用、实现 OAuth 或完成业务访问控制。

## 基础路径

| 级别 | 核心能力 | 任务 | 代码 |
| --- | --- | --- | --- |
| 1 · 协议对象 | 工具描述、文本块、结构化结果与错误标识 | [说明](lessons/01_protocol.md) | [level01_protocol.py](exercises/level01_protocol.py) |
| 2 · Tools server | 工具注册、类型 schema、成功与业务失败 | [说明](lessons/02_tools.md) | [level02_tools.py](exercises/level02_tools.py) |
| 3 · 上下文能力 | 静态资源、URI 模板、prompts | [说明](lessons/03_context.md) | [level03_context.py](exercises/level03_context.py) |
| 4 · stdio client | 本地子进程、能力发现、调用和释放 | [说明](lessons/04_stdio.md) | [level04_stdio.py](exercises/level04_stdio.py) |
| 5 · Streamable HTTP | ASGI endpoint、SDK lifespan、真实协议往返 | [说明](lessons/05_http.md) | [level05_http.py](exercises/level05_http.py) |

## 进阶路径

| 级别 | 核心能力 | 任务 | 代码 |
| --- | --- | --- | --- |
| 6 · 分页发现 | 不透明 cursor、去重、循环检测与页数上限 | [说明](lessons/06_pagination.md) | [level06_pagination.py](exercises/level06_pagination.py) |
| 7 · 执行控制 | 并发上限、每项超时、取消、服务端进度 | [说明](lessons/07_execution.md) | [level07_execution.py](exercises/level07_execution.py) |
| 8 · 文件资源边界 | 路径解析、符号链接、受限 Markdown 读取 | [说明](lessons/08_files.md) | [level08_files.py](exercises/level08_files.py) |
| 9 · LangChain 适配 | 异步 StructuredTool、schema 与原始结果 artifact | [说明](lessons/09_langchain.md) | [level09_langchain.py](exercises/level09_langchain.py) |
| 10 · 多服务组合 | 连接作用域、部分失败回收、工具命名空间 | [说明](lessons/10_multiserver.md) | [level10_multiserver.py](exercises/level10_multiserver.py) |

前置：Python 类型标注、字典、异常、async/await 与异步上下文管理器。建议基础级依次完成；第 6–8 级可在理解 Client 后独立练习。第 9 级建议先学 LangChain 的工具与 ToolMessage，不要求先实现完整 agent。第 10 级再组合连接、发现和适配。

## 安装与验收

在仓库根目录按[总说明](../README.md)安装锁定依赖：

```bash
python -m pip install -r requirements-lock.txt
python -m pytest tests/environment/test_mcp.py -q
python -m pytest --run-exercises tests/mcp/test_level01_protocol.py -q
python -m pytest --run-exercises tests/mcp/test_level04_stdio.py -q
python -m pytest --run-exercises tests/mcp -q
```

默认测试验证提供的 SDK 环境和传输设施，所有学生练习仍被跳过。`--run-exercises` 才启用验收；初始 NotImplementedError 表示对应任务尚未实现。每级测试通过后，还应解释本级输入输出和失败路径。

测试分三类：SDK 对象与本地策略的单元测试；Client(server) 的真实内存协议调用；stdio 子进程和进程内 ASGI Streamable HTTP 调用。分页、并发、异常与生命周期使用受控依赖验证边界，不把替代客户端称为已验证的外部服务。若执行环境限制子进程通信，stdio 验收应在允许该通信的普通终端运行；内存和 ASGI 测试不需要此权限。

## 实际运行自己完成的 server

完成 Level 2 后可通过 stdio 运行；完成 Level 5 后可提供本机 HTTP endpoint：

```bash
python -m mcp_practice.run_server --transport stdio
python -m mcp_practice.run_server --transport http --port 8000
```

stdio 命令供其他 MCP 客户端启动，不应在它的 stdout 打印调试内容。HTTP 命令只监听 127.0.0.1；练习不会自动部署或注册到任何桌面宿主。

[reference_server.py](support/reference_server.py) 是提供好的 echo/health 传输测试设施，独立于练习答案；[transports.py](support/transports.py) 使用 httpx2.ASGITransport，不开放 socket。第 4 级则会由 SDK 启动并关闭本项目的 reference_server 子进程。

## 后续项目

尚未提供实现与完整验收的方向：OAuth 与身份/授权服务器、elicitation 与多轮输入、订阅与缓存一致性、持久化审计、远程部署、真实模型驱动的跨服务 agent。旧协议中的 sampling、roots 和部分连接行为已有弃用或变化，扩展前先核对指定协议版本，不作为必修的新功能练习。

## 官方参考

- [Python SDK v2 变更](https://py.sdk.modelcontextprotocol.io/whats-new/)
- [Python server](https://py.sdk.modelcontextprotocol.io/servers/)
- [Client 与传输](https://py.sdk.modelcontextprotocol.io/client/transports/)
- [协议传输规范](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
- [错误处理](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/)
