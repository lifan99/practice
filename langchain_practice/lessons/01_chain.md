# Level 1：提示词与字符串输出

**本级只解决：怎样把输入字典送进模型，并拿到字符串？**

前置：函数、字典、类型标注。完成已有的 [ex01_chain.py](../ex01_chain.py) 的 `build_chain(model)`；必须使用 `ChatPromptTemplate` 和 `StrOutputParser`，返回真正的 Runnable。

- 输入为 `{"topic": str, "audience": str}`。
- 模型收到两条消息：system 严格为 `You are a concise tutor. Reply in English.`，human 为 `Explain {topic} for a {audience}.`，其中变量替换为输入内容。
- 输出是模型回复的字符串；使用调用者注入的模型。
- 缺少任一变量时抛 `KeyError`，不要求拒绝空字符串。

例如输入 `{"topic":"recursion","audience":"beginner"}`，human 内容应为 `Explain recursion for a beginner.`。

```bash
python -m pytest --run-exercises tests/test_langchain_practice.py -k test_chain -q
```

完成标准：测试通过，能区分输入字典、PromptValue、AIMessage 和最终字符串。固定回复模型不能证明提示词有效，所以测试也会检查模型收到的消息。

下一步：[Level 2](02_tools_parser.md)。
