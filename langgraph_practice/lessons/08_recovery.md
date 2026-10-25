# Level 8：节点 RetryPolicy 与失败恢复

**本级只解决：暂时失败与整次运行失败，应该怎样分别处理？**

完成 [level08_recovery.py](../exercises/level08_recovery.py) 的 build_recoverable_graph(checkpointer, prepare, deliver, max_attempts=2)。

- max_attempts 为正整数，否则构图时 ValueError；包含一次节点调度中的首次尝试。
- 图使用指定 checkpointer；输入 payload 字符串，去掉两端空白，空白时 ValueError，不调用回调。
- prepare 节点恰好调用 prepare(payload)，把返回文本保存为 prepared。
- deliver 节点调用 deliver(prepared)，成功时保存 receipt。该节点使用原生 RetryPolicy，只重试 TimeoutError，最多 max_attempts 次。
- 离线训练将 initial_interval=0、jitter=False，避免重试等待；其他错误不自动重试或伪装成成功。
- deliver 失败并传播后，可用同一配置 `graph.invoke(None, config)` 重新调度未完成节点；已 checkpoint 的 prepare 不应再执行。
- 不使用全局业务状态替代 checkpoint，不修改输入。

```bash
python -m pytest --run-exercises tests/langgraph/test_level08_recovery.py -q
```

完成标准：分别展示单次节点内超时恢复，以及异常后从 checkpoint 恢复。外部重新调度会开启新的尝试预算，并不是全局重试次数限制；真实副作用仍需幂等性设计。

下一步：[Level 9](09_subgraphs.md)。
