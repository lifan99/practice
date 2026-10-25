# Level 10：同步与异步文本流

**本级只解决：怎样增量传递模型输出，并在提前停止时释放流？**

前置：迭代器、生成器、Level 9。完成 [level10_streaming.py](../level10_streaming.py) 的两个函数。

- `stream_text(model, messages)` 返回同步迭代器，实际使用 model.stream。
- `astream_text(model, messages)` 返回异步迭代器，实际使用 model.astream；调用者直接 `async for`，不先 await 此函数的返回值。可以改为带 yield 的 async def，或返回内部异步生成器。
- 创建迭代器时不调用模型；第一次请求输出时才打开底层流。不得先收集完整回复再逐字符输出。
- 本题只处理 AIMessageChunk 的字符串 content，空串跳过，其他字符串（包括纯空格）原样且按顺序产出。
- 遇到列表等非字符串 content 时抛 `TypeError`，不静默丢弃。多模态和 content blocks 解析属于扩展。
- 流中途抛异常时直接传播，保留此前已经产出的内容，不重新调用模型。
- 消费完成、异常或外层迭代器提前关闭时，关闭底层流：若支持 close/aclose，须分别调用或 await。不得修改 messages。

块不一定是单个字符或 token，调用者也不应依赖具体块大小。本题是模型文本流练习；原生 agent 事件流还有额外协议，不在这里假定所有事件都长成 AIMessageChunk。

```bash
python -m pytest --run-exercises tests/langchain/test_level10_streaming.py -q
```

完成标准：分别展示首块、增量输出、中途异常、提前 close/aclose 四种行为。

[模型接口](https://docs.langchain.com/oss/python/langchain/models)、[agent 流式接口](https://docs.langchain.com/oss/python/langchain/streaming)。后续项目见[学习路线](../README.md)。
