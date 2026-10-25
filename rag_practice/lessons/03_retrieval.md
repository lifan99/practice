# Level 3：只做向量检索

**本级只解决：输入一个问题，怎样找回相关文档块？**

前置：Level 2、向量与余弦相似度的基本含义。先在测试提供的短文档上练习；无需为了测试本级重新读取或切分文件。

## 任务

完成 [level03_retrieval.py](../level03_retrieval.py) 的两个函数：

1. `build_index(chunks, embeddings)` 返回包含全部 chunks 的 `InMemoryVectorStore`。必须使用注入的 embedding 实例，保留文档来源；空 chunks 抛 `ValueError`；不同调用创建的索引互不影响。
2. `search_index(question, index, k=2)` 去掉 question 两端空白，返回最多 k 个匹配的 Document，按索引的相关性顺序排列，不去重来源。不改写非空问题正文。k 是正整数；k<=0 或问题为空白时抛 `ValueError`，且不查询索引。有效查询无结果时返回 `[]`，索引异常直接传播。

测试使用提供好的 `practice_support.KeywordEmbeddings`：它是固定词表的词频向量，不下载模型，也不能代表真实语义能力。实现中不要硬编码词表或 query 到 source 的映射。

## 验收

```bash
python -m pytest --run-exercises tests/rag/test_level03_retrieval.py -q
```

完成标准：能检索回 `langgraph graph checkpoint` 对应的文档，并解释返回结果为什么仍然是证据，而不是最终答案。同一来源的多个 chunk 可以同时出现。

下一步：[Level 4：根据给定证据生成](04_generation.md)。
