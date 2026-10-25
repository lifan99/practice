# Level 7：会话记忆与线程隔离

**本级只解决：怎样保留同一会话的历史，同时隔离其他会话？**

前置：Level 6。完成 [level07_memory.py](../level07_memory.py) 的两个函数。

## A：带 checkpointer 的 agent

`build_memory_agent(model, checkpointer)` 使用 create_agent 返回无工具的对话 agent，传入指定的模型与 checkpointer，system_prompt 为 `You are a helpful tutor.`。不得在函数内改建自己的全局历史缓存或替换 checkpointer。

## B：只提交新一轮消息

`chat(agent, thread_id, text)` 返回最终模型回复文本。

- thread_id 不能为空白；非空 ID 按原样使用，不自动合并或重命名。text 去掉两端空白，空白 text 抛 `ValueError`；两者都应在 agent 调用前校验。
- 输入只包含本轮一个 HumanMessage，不手工重发历史。
- 通过 `config={"configurable":{"thread_id": thread_id}}` 调用 agent 一次，结果读取最终 AIMessage 的字符串 content。
- 依赖异常直接传播。不同 thread_id 之间不能出现对方消息，同一 thread_id 的成功轮次应出现在后续模型输入中。

测试注入 `InMemorySaver`，重启进程后不会自动保留。持久化存储、历史裁剪和跨会话长期记忆属于后续扩展。

```bash
python -m pytest --run-exercises tests/langchain/test_level07_memory.py -q
```

完成标准：分别验证 A、B 两个会话，并检查 A 的第二轮模型输入。预设模型不会真的“记住姓名”，验收应检查历史消息，而不是相信预设答案。

[官方短期记忆说明](https://docs.langchain.com/oss/python/langchain/short-term-memory)。下一步：[Level 8](08_reliability.md)。
