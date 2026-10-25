# Level 6：Checkpoint 与线程隔离

**本级只解决：怎样跨多次图调用保留同一线程的状态？**

完成 [level06_checkpoints.py](../level06_checkpoints.py)。

- build_counter_graph(checkpointer) 使用传入的 checkpointer 编译 StateGraph；不创建替代 checkpointer 或全局计数器。
- 输入只含 delta 整数。accumulate 节点将其加到当前 total，首次 total 从 0 开始；0 和负 delta 合法。
- 相同 `configurable.thread_id` 累加，不同线程隔离；不改写输入。
- counter_snapshot(graph, thread_id) 用 get_state 读取 values，返回独立的 dict，不执行节点。空白 thread_id 抛 ValueError，非空 ID 原样保留；没有 checkpoint 的线程返回 `{}`。

例如 A 依次输入 delta=3、4，total 应为 3、7；B 首次 delta=2，total 仍为 2。

```bash
python -m pytest --run-exercises tests/langgraph/test_level06_checkpoints.py -q
```

测试使用 InMemorySaver，它只在进程内保留状态。完成标准：读取真实 checkpoint，并解释 thread-scoped 状态、跨线程 store、持久化数据库的区别。

下一步：[Level 7](07_interrupts.md)。
