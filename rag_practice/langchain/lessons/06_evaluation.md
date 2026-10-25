# Level 6：检索评估与参数实验

**本级只解决：怎样用固定问题集判断检索有没有找回应有的证据？**

前置：集合、均值；评估器接受注入的 retriever，可独立于索引实现进行测试。本级不使用 LLM 评分。

## A：来源召回率

完成 [level06_evaluation.py](../exercises/level06_evaluation.py) 的 `recall_at_k(retrieved_sources, relevant_sources, k)`。

- 分母为所有相关来源的数量；分子为前 k 条结果中出现过的不同相关来源数。
- 先按原始结果位置取前 k 条，重复来源不额外增加命中数。
- k 为正整数；k<=0 或 relevant_sources 为空时抛 `ValueError`。
- 检索结果为空且相关集合非空时返回 0.0；k 超出结果长度时使用全部结果。

例如结果 `["a", "a", "b"]`、相关来源 `{"a", "b"}`，k=2 时为 0.5，k=3 时为 1.0。

## B：固定问题集评估

完成 `evaluate_retrieval(cases, retriever, k)`。每个 case 是 `{"question": str, "relevant_sources": set[str]}`，返回：

```python
{
    "mean_recall": 0.75,
    "per_query": [
        {"question": "first question", "recall": 1.0},
        {"question": "second question", "recall": 0.5},
    ],
}
```

- 按输入顺序保留每个问题的结果；question 去掉两端空白。
- 每个问题调用 retriever 一次，取返回 Document 的 source，复用本级 `recall_at_k`。
- mean_recall 为每个问题 recall 的不加权算术均值；重复问题作为独立 case 计入。
- 空 cases、k<=0、任意空白问题或空相关集合都抛 `ValueError`；所有输入须在首次检索前校验完毕。
- 约定文档都有非空字符串 source；依赖异常直接传播，不修改输入。

## 验收与实验

```bash
python -m pytest --run-exercises tests/rag/langchain/test_level06_evaluation.py -q
```

测试通过后，使用 [evaluation_queries.json](../../data/evaluation_queries.json) 的固定问题集做一次真实组件串联实验。JSON 中的相关来源列表需要转成 set。

在相同数据、embedding 和问题集下，分别比较 `(chunk_size, chunk_overlap)` 为 `(80, 0)`、`(80, 20)`、`(160, 30)`，k 取 1 和 2。自行建立一张记录表，填写分块数量、平均来源召回率和具体漏检例子。这里只比较给定配置，不预设哪个配置一定获胜，也不要求观察到性能差异。

完成标准：测试通过，实验记录可复现，并能说明“来源被找到”“支持答案的具体句子被找到”“最终答案正确”为什么是三个不同判断。

本问题集仅是组件连通性样例，规模小、关键词明显，不能支持真实质量结论。完成后再加入自然语言改写、有多个相关来源和无答案的问题；无答案问题不纳入本题的 recall 均值，可另行评估拒答。

下一阶段：[Level 7：混合检索与 RRF](07_hybrid.md)。也可以根据兴趣选择 [LangGraph RAG](../../workflows/lessons/01_corrective.md) 或 [GraphRAG 图谱建模](../../graph/lessons/01_knowledge_graph.md)，依赖关系见 [学习路径](../../README.md)。
