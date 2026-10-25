# LangChain 分级练习

从组件组合逐步进入原生 agent 和异步运行，分成 **基础两级 + 进阶八级**。每级都有任务说明、代码骨架与独立验收；保留 TODO，不附完整答案。整个路径使用已锁定依赖，无需 API Key。

## 学习路径

| 级别 | 核心能力 | 任务 | 代码 |
| --- | --- | --- | --- |
| 1 · 提示词链 | 输入字典、消息、模型、字符串输出 | [说明](lessons/01_chain.md) | [level01_chain.py](exercises/level01_chain.py) |
| 2 · 工具与解析 | 工具 schema、Pydantic 输出解析 | [说明](lessons/02_tools_parser.md) | [level02_tools.py](exercises/level02_tools.py) |
| 3 · Runnable 组合 | 并行分析、批处理、显式路由 | [说明](lessons/03_composition.md) | [level03_composition.py](exercises/level03_composition.py) |
| 4 · 结构化输出 | 模型 schema 绑定、业务约束 | [说明](lessons/04_structured.md) | [level04_structured.py](exercises/level04_structured.py) |
| 5 · 工具调用协议 | tool call ID、参数分发、ToolMessage | [说明](lessons/05_tool_protocol.md) | [level05_tool_protocol.py](exercises/level05_tool_protocol.py) |
| 6 · 多工具 agent | 原生 create_agent、工具循环、中间件注入 | [说明](lessons/06_agents.md) | [level06_agents.py](exercises/level06_agents.py) |
| 7 · 会话记忆 | checkpointer、thread_id、消息隔离 | [说明](lessons/07_memory.md) | [level07_memory.py](exercises/level07_memory.py) |
| 8 · 可靠性 | 超时重试、fallback、工具错误中间件 | [说明](lessons/08_reliability.md) | [level08_reliability.py](exercises/level08_reliability.py) |
| 9 · 异步并发 | 最大并发、结果顺序、单项失败与取消 | [说明](lessons/09_async.md) | [level09_async.py](exercises/level09_async.py) |
| 10 · 流式输出 | 同步/异步增量文本、异常、提前关闭 | [说明](lessons/10_streaming.md) | [level10_streaming.py](exercises/level10_streaming.py) |

建议按顺序学习。也可以按依赖选择分支：Level 3 依赖 Level 1，Level 4 依赖 Level 2，Level 5–7 依次衔接；Level 8 需要 Runnable 与 agent 基础；Level 9–10 还需要 async/await 和迭代器。

每级完成标准是：公开测试通过，能解释本级数据流与失败分支，并按说明完成观察任务。测试只覆盖公开契约的一部分；不要用硬编码结果代替实现。

## 如何运行

先按[总说明](../README.md)安装依赖，在仓库根目录执行：

```bash
python -m pytest --run-exercises tests/langchain/test_level01_chain.py -q
python -m pytest --run-exercises tests/langchain/test_level02_tools.py -q
python -m pytest --run-exercises tests/langchain -q
```

默认 `python -m pytest -q` 只运行环境检查，练习全部跳过。加上 `--run-exercises` 后，尚未实现的函数会报 NotImplementedError。环境检查通过不代表进阶练习已经完成。

## 测试与模型的边界

- 基础链使用 FakeListChatModel。固定文本回复不验证真实提示词效果。
- [offline_models.py](support/offline_models.py) 提供 ScriptedChatModel，返回预设 AIMessage，记录消息和绑定工具名，不选择或执行工具。Level 6 会让原生 agent 实际执行本地工具；测试验证协议，不评价规划智能。
- Level 4 用结构化绑定替代模型，验证调用和业务边界；真实 provider 的结构化输出兼容性需另测。
- Level 7 检查实际传给模型的历史消息，不用“模型回答记得什么”代替会话隔离验证。InMemorySaver 不跨进程持久化。
- Level 8 验证指定错误类别的处理；工具错误中间件只要求同步 hook。
- Level 9 使用独立本地协程，Level 10 使用受控增量流，不依赖脚本模型具备并发能力、网络延迟或真实 token 分块规律。

可通过 Runnable config 的 tags、metadata 和本地 callbacks 观察调用。基础训练不要求开通 LangSmith 或发送 trace 到外部服务。

## 和其他练习如何衔接

基础 Level 1–2 可以支持 RAG 的框架集成；Level 5–8 可以支持多工具检索应用。需要自己设计状态、分支和恢复流程时，再学习 [LangGraph](../langgraph_practice/README.md) 与 [RAG 纠正检索](../rag_practice/workflows/lessons/01_corrective.md)。

## 后续项目

以下方向尚未提供实现与独立验收：agent 的 structured_response 与 provider/tool strategy 对比、异步工具中间件、agent 事件流、消息裁剪与持久化、跨会话长期记忆、人工介入与远程工具、真实模型回归评估。每次选一个可观察目标再增加组件，不把基础模拟结果当成真实模型质量结论。
