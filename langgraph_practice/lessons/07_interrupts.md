# Level 7：人工中断与显式恢复

**本级只解决：怎样在模拟动作之前停下来等待外部决定？**

完成 [level07_interrupts.py](../exercises/level07_interrupts.py) 的 build_approval_graph(checkpointer, publish)。publish 是注入的纯本地模拟函数，不发送外部消息。

- 使用指定 checkpointer 编译图；输入 `{"draft": str}`。
- prepare 去掉 draft 两端空白，空白时 ValueError；设置 status=pending、receipt=空串。
- review 调用 interrupt，载荷严格为 `{"kind":"approval","draft":规范化文本}`。
- 首次 invoke 暂停，不调用 publish；用同一 thread_id 和 `Command(resume=True/False)` 恢复。
- 恢复值必须是 bool，其他值抛 ValueError；True 时 publish 节点恰好调用一次 publish(draft)，status=published、receipt=返回值；False 时 status=rejected、receipt=空串，不调用 publish。
- approved 保存布尔决定。依赖异常直接传播，不修改原输入。

```bash
python -m pytest --run-exercises tests/langgraph/test_level07_interrupts.py -q
```

本级使用锁定版本的默认 invoke 字典格式，从 `__interrupt__` 观察暂停；Level 10 再使用 v3 投影。不要吞掉框架中断。中断节点恢复时会重新从节点开头执行，因此不可在 interrupt 前安排不可重复的外部副作用。

完成标准：验证批准、拒绝和非法恢复值三条路径。这里“一次 publish”只针对正常的一次恢复路径，不是分布式 exactly-once 承诺。

下一步：[Level 8](08_recovery.md)。
