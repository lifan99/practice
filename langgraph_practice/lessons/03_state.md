# Level 3：Reducer 与带 ID 的消息状态

**本级只解决：节点的部分状态更新应如何合并？**

完成 [level03_state.py](../exercises/level03_state.py)。

## A：消息更新

merge_messages(existing, updates) 实际使用原生 add_messages，先保护调用者对象不被修改。

- 新 ID 追加到末尾；已存在 ID 在原位置被替换。
- RemoveMessage 删除匹配 ID；删除不存在的 ID 按原生规则抛 ValueError。
- 无 ID 的消息可以由库赋 ID，但输入列表和输入消息本身必须保持原样。
- 输入是 BaseMessage 对象列表，不要求支持序列化字典或 REMOVE_ALL_MESSAGES 特殊值。

## B：消息图

build_message_graph(responder) 返回单个 respond 节点的 StateGraph。状态 messages 使用本级的 merge_messages 作为 reducer。

- 输入 `{"messages": [...消息...]}`，空消息列表抛 ValueError，不调用 responder。
- responder 收到已有消息列表，调用一次并返回 AIMessage；通过 reducer 应用该回复，而不是直接覆盖整个历史。
- 保留同 ID 替换语义，不修改调用者消息；图无 checkpointer，不同 invoke 之间不自动保留历史。
- responder 异常直接传播。

```bash
python -m pytest --run-exercises tests/langgraph/test_level03_state.py -q
```

完成标准：用追加、替换、删除三个例子解释 reducer。能说明为何普通列表覆盖、operator.add 与 add_messages 的含义不同。

下一步：[Level 4](04_parallel.md)。
