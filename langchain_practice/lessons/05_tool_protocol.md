# Level 5：工具调用协议与结果关联

**本级只解决：模型发出的 tool calls 怎样对应到工具结果？**

前置：Level 2、AIMessage 与 ToolMessage。完成 [level05_tool_protocol.py](../exercises/level05_tool_protocol.py) 的 `execute_tool_calls(message, tools)`；只处理一批已给定的调用，不实现 agent 决策循环。

- tools 是 BaseTool 列表，工具名不能重复，否则抛 `ValueError`。
- 在执行任何工具前，检查本批所有调用的 ID 非空且不重复，否则抛 `ValueError`；工具名都必须存在，否则抛 `KeyError(工具名)`。
- 按 tool_calls 中的顺序，用各调用的 args 字典调用对应工具 `.invoke()` 一次。
- 返回同序的 ToolMessage，name 为工具名，tool_call_id 为原调用 ID，不重新生成 ID。
- 工具返回字符串时原样使用；返回其他 JSON 可序列化值时，以 `json.dumps(..., ensure_ascii=False, sort_keys=True)` 得到 content。
- 没有调用时返回 `[]`，但仍须检查重复工具名。不修改输入消息、参数和工具列表；工具执行或序列化异常直接传播。
- 本题使用纯本地工具。预检查仅针对名字和 ID，不承诺工具执行的事务回滚或对所有参数预先完成 schema 验证。

例如 name=`add`、args=`{"a":2,"b":3}`、id=`call-1` 的调用，应得到 name=`add`、tool_call_id=`call-1`、content=`5` 的 ToolMessage。

```bash
python -m pytest --run-exercises tests/langchain/test_level05_tool_protocol.py -q
```

完成标准：测试通过，能解释工具请求消息与执行结果消息为何需要同一个 ID。下一步使用框架原生 agent 执行循环，不要求把本级手写 dispatch 接入原生 agent。

下一步：[Level 6](06_agents.md)。
