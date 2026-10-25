# Level 2：工具 schema 与输出解析

**本级只解决：怎样向外描述一个函数，并验证模型输出的形状？**

前置：Level 1、Pydantic。完成已有的 [level02_tools.py](../exercises/level02_tools.py)，保留提供的 StudyPlan 模型。

1. `make_word_count_tool()` 返回 BaseTool，名字为 `word_count`，说明非空，有名为 text 的字符串参数。`.invoke({"text": ...})` 返回按空白分隔的单词数；连续空格、换行、制表符均为分隔符，空串或纯空白返回 0。不要求中文分词。
2. `parse_study_plan(text)` 使用 `PydanticOutputParser` 返回 StudyPlan。格式错误或违反模型约束时抛 `OutputParserException`，不吞掉错误或补默认值。

约束：topic 长度至少 1，steps 长度为 1–3，minutes 在闭区间 1–120。合法示例为 `{"topic":"RAG","steps":["Read","Build"],"minutes":30}`。本级不要求拒绝 Pydantic 允许的类型转换，也不要求判断内容是否正确。

```bash
python -m pytest --run-exercises tests/langchain/test_level02_tools.py -k 'word_count or plan_parser' -q
```

完成标准：测试通过，并解释“工具可被程序调用”“模型发起工具调用”“JSON schema 合法”分别说明了什么。

下一步：[Level 3](03_composition.md)。
