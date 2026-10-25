# Level 6：原生多工具 agent

**本级只解决：怎样让框架接管模型和工具之间的循环？**

前置：Level 5。完成 [level06_agents.py](../level06_agents.py) 的 `build_tool_agent(model, tools, middleware=None)`。

- 实际使用 `langchain.agents.create_agent`，返回 CompiledStateGraph；不手写循环模拟 agent。
- 使用传入的模型和工具，重复工具名在构建时抛 `ValueError`；空工具列表合法。
- system_prompt 严格为 `Use tools when needed. Never invent tool results.`。
- 若传入 middleware，则保留其顺序传给原生工厂；None 视为无中间件。
- 图接收 `{"messages": [HumanMessage(...)]}`，结果包含完整 messages。多次工具调用的请求、结果及最终 AIMessage 应由框架按协议连接。
- 调用者可通过 `config={"recursion_limit": ...}` 限制图执行；不吞掉框架的终止错误。

测试提供 [offline_models.py](../offline_models.py) 的 ScriptedChatModel。它返回预设 AIMessage，并支持 bind_tools，但不执行工具，也不具备选择工具的智能。测试会让原生 agent 实际执行加法、乘法等本地工具。

```bash
python -m pytest --run-exercises tests/langchain/test_level06_agents.py -q
```

完成标准：模型请求工具、工具返回结果、模型生成最终回复三段均能在消息中被观察。预设回复能证明协议连通，不能证明真实模型会正确规划调用。

[官方 agent 接口](https://docs.langchain.com/oss/python/langchain/agents)。下一步：[Level 7](07_memory.md)。
