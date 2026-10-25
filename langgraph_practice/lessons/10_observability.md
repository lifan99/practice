# Level 10：状态更新、快照与事件投影

**本级只解决：怎样观察图执行，并区分完成、暂停和失败？**

完成 [level10_observability.py](../exercises/level10_observability.py)。两函数都是执行入口，不能为了观察同一次真实动作而连续执行两次；本级回调均为纯本地测试。

## A：v2 更新封装

collect_updates(graph, inputs, config=None) 调用 graph.stream，指定 stream_mode=updates、version=v2，并传递 config。

- 返回按实际发出顺序排列的 NodeUpdate，每项为 `{"node":节点名,"values":部分更新dict}`。
- 只收集 updates part 中普通节点的 dict 更新；忽略名字以 `__` 开头的框架条目和非 dict 节点值。
- 返回深拷贝，不把变化中的对象作为历史记录。普通执行异常传播，离开时释放支持 close 的底层迭代器。
- 并行节点的观察顺序不等于业务排序；更新列表为空也不证明成功。

## B：v3 状态投影

observe_run 使用 `with graph.stream_events(..., version="v3") as stream`，完整消费 stream.values，返回 RunReport：

- snapshots：依序记录并深拷贝每个全量状态。
- output：消费完成后 stream.output 的独立副本。
- interrupted：stream.interrupted。
- interrupts：stream.interrupts 中各项 value 的独立副本，不暴露随机 ID 作为固定答案。
- 不把暂停当成完成，不吞掉普通异常；异常时也退出流上下文。

```bash
python -m pytest --run-exercises tests/langgraph/test_level10_observability.py -q
```

锁定的 LangGraph 1.2.17 将 v3 标为实验性，可能显示 BetaWarning。本级固定该接口进行练习；v2/v3 是流的输出接口版本，不是 Python SDK 的主版本。v3 没有 stream.updates 属性，节点更新与全量状态投影不可混用。

完成标准：验证正常完成、interrupt 暂停与节点异常，并说明静态回调的状态流为何不等于 LLM token 流。

[官方 streaming](https://docs.langchain.com/oss/python/langgraph/streaming)、[学习路线与后续项目](../README.md)。
