# Level 4：模型结构化输出与业务约束

**本级只解决：怎样请求结构化对象，并检查调用者的实际约束？**

前置：Level 2。完成 [level04_structured.py](../exercises/level04_structured.py) 的 `generate_plan(model, topic, max_minutes=60)`。

- topic 去掉两端空白；空白 topic 或不在 1–120 的整数 max_minutes 抛 `ValueError`，不得绑定或调用模型。
- 调用模型的 `.with_structured_output(StudyPlan)` 一次，得到可 invoke 的 Runnable。
- 向该 Runnable 发送兼容 chat model 的消息；human 消息需包含规范化 topic 和分钟上限，system 消息给出学习计划任务要求。
- 约定绑定后的模型返回 StudyPlan；输出直接保留该对象。若返回其他类型，抛 `TypeError`，不猜测或修复数据。
- 即使 StudyPlan 的 schema 合法，minutes 超过调用者的 max_minutes 时仍须抛 `ValueError`。不额外调用模型修复，也不静默缩短分钟数。
- 模型绑定和调用异常直接传播。

例如调用者上限 30 分钟，模型给出合法的 60 分钟计划，应判定为业务约束失败；它并未违反 StudyPlan 自身的 1–120 分钟约束。

测试使用仅实现绑定协议的替代模型，不需要 provider SDK。真实模型是否支持指定的 structured output 方式，应按对应集成验证；本级不声称模拟了服务端 JSON schema 约束。

```bash
python -m pytest --run-exercises tests/langchain/test_level04_structured.py -q
```

完成标准：区分输出解析、模型结构化输出接口、业务验证三层责任。

[模型接口](https://docs.langchain.com/oss/python/langchain/models)、[agent 结构化输出](https://docs.langchain.com/oss/python/langchain/structured-output)。下一步：[Level 5](05_tool_protocol.md)。
