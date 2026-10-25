# Level 4：根据给定证据生成

**本级只解决：已有证据时，怎样将证据和问题交给模型？**

前置：LangChain chat messages、Runnable 与字符串输出。本级直接接收测试提供的文档，不依赖 Level 3 的检索实现。

## A：可追溯的上下文

完成 [level04_generation.py](../level04_generation.py) 的 `format_context(documents)`。

- 每块严格格式为 `[source]\n正文`，块间以两个换行分隔。
- 保留文档顺序和每块原始正文，不按 source 去重；不修改输入文档。
- 空列表返回空字符串。约定每份文档都有非空字符串 `metadata["source"]`。

例如一份 source=`a.md`、正文为 `Evidence.` 的文档，格式化为 `[a.md]\nEvidence.`。

## B：带证据的模型调用

完成 `generate_answer(question, documents, model) -> str`。

- question 去掉两端空白；空白问题或空 documents 抛 `ValueError`，不调用模型。
- 使用本级的 `format_context`；将规范化后的问题和完整上下文交给注入的 model，恰好调用一次。
- 模型输入为 chat message 列表或具有 `.to_messages()` 的 PromptValue；输出为模型回复文本。
- system 消息明确要求：只使用给定上下文；证据不足则明确表示无法回答；文档是数据，不执行其中的指令。具体措辞自行编写。
- 不修改输入文档；依赖异常直接传播。

## 验收与限制

```bash
python -m pytest --run-exercises tests/rag/test_level04_generation.py -q
```

完成标准：自动测试通过，并人工检查 system 消息包含上述三条要求。公开测试检查消息与数据传递，不对自然语言指令做语义评分。

模拟模型只返回预设文本。它可以验证调用流程，不能证明回答正确、拒答有效或具备抗提示注入能力。

下一步：[Level 5：完整问答流程](05_pipeline.md)。
