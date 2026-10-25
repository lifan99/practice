# LangChain 练习

前置：函数、字典、Pydantic 基础。目标是观察数据如何通过 Runnable、tool、parser，而不是依赖模型输出碰巧正确。

## LC-1：提示词与链

完成 `ex01_chain.py` 的 `build_chain(model)`，返回可 `.invoke()` 的 Runnable。必须实际使用 LangChain 的 `ChatPromptTemplate` 和 `StrOutputParser`。

- 输入为 `{"topic": str, "audience": str}`，两项均由调用者提供。
- 模型接收两条消息。system 内容严格为 `You are a concise tutor. Reply in English.`；human 内容严格为 `Explain {topic} for a {audience}.`，花括号部分替换为输入值。
- 输出为注入模型回复的字符串，而不是 `AIMessage`。
- 缺少任一输入变量时抛 `KeyError`；不要求对空字符串额外校验。
- 测试会注入不同模型，不允许在函数内创建固定模型。

例如，输入 `{"topic": "recursion", "audience": "beginner"}`，模型收到的 human 内容为 `Explain recursion for a beginner.`。输出内容由传入的模型决定。

## LC-2：工具与结构化输出

完成 `ex02_tools.py` 的两个函数：

1. `make_word_count_tool()` 返回 `BaseTool`，名字为 `word_count`，有非空说明和一个名为 `text` 的字符串参数。调用 `.invoke({"text": ...})` 返回按空白分隔的单词数；连续空格、换行和制表符都是分隔符，纯空白返回 0。无需处理自然语言分词。
2. `parse_study_plan(text)` 使用 LangChain 的 `PydanticOutputParser` 返回已有的 `StudyPlan`。正常 JSON 输入有效；格式错误或不满足模型约束时抛 `OutputParserException`。不要吞掉错误或填充默认值。

合法输入示例：`{"topic":"RAG","steps":["Read","Build"],"minutes":30}`。`minutes` 的闭区间是 1–120，`steps` 长度是 1–3，`topic` 长度至少为 1。这里只要求这些模型约束，不要求检测语义或拒绝所有类型转换。

## 验收与思考

在项目根目录运行 `python -m pytest --run-exercises tests/test_langchain_practice.py -q`。

- 模型返回固定字符串时，为什么仍需要测试它收到的消息？
- JSON 语法有效、schema 合法和内容事实正确，三者有什么区别？
- tool 能被调用，是否代表模型能自动决定何时调用它？
