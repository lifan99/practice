# Level 5：组合为完整问答流程

**本级只解决：怎样把检索和已有的回答能力接起来，并处理没有证据的情况？**

前置：Level 4；检索能力通过参数注入，不在本级重新建立索引。

## 任务

完成 [level05_pipeline.py](../exercises/level05_pipeline.py) 的 `answer_question(question, retriever, model)`，返回 `{"answer": str, "sources": list[str]}`。

- question 去掉两端空白；空白时抛 `ValueError`，不调用任何依赖。
- 使用 `.invoke(question)` 调用 retriever 一次，返回 `list[Document]`。
- 空结果返回 `{"answer": "I don't know based on the provided documents.", "sources": []}`，不调用生成函数或模型。
- 有结果时复用 `level04_generation.generate_answer`，传入规范化问题、全部命中文档、原样传入的模型，各一次。
- sources 是供生成步骤使用的来源，按首次出现顺序去重。它不表示模型逐个引用过这些来源。
- 不修改命中文档；检索或生成异常直接传播，不伪装成无答案。

测试用替代函数隔离本级的生成依赖，因此能单独检查组合逻辑；最终实际运行仍需要完成 Level 4。

## 验收

```bash
python -m pytest --run-exercises tests/rag/langchain/test_level05_pipeline.py -q
```

完成标准：成功、无命中、空白问题和依赖失败四条路径都符合契约。再将 Level 3 的索引 retriever 接入本级，观察一次完整调用。

目前只对“没有命中”做确定性拒答。有命中仍可能证据不足；这是后续真实模型实验需要评估的行为。

下一步：[Level 6：检索评估与参数实验](06_evaluation.md)。
