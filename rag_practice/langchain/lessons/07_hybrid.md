# Level 7：Advanced RAG · 混合检索与 RRF

**本级只解决：关键词检索和向量检索给出不同排名时，怎样融合候选？**

前置：Level 3 与 Level 6。Advanced RAG 是改进检索、上下文和生成流程的一组方法，不是一套固定产品或必选架构。本级先练一种可确定验收的融合方法。

## A：Reciprocal Rank Fusion

完成 [level07_hybrid.py](../exercises/level07_hybrid.py) 的 `reciprocal_rank_fusion(rankings, rank_constant=60, top_k=5)`。

输入是多份按相关性降序排列的 **chunk ID** 列表，输出 `[{"chunk_id": str, "score": float}, ...]`。

- 单份排名从 1 开始；每个候选从包含它的列表获得 `1 / (rank_constant + rank)` 分，再把这些分数相加。未出现不贡献分数。
- 同一列表重复 ID 只按首次出现的位置贡献一次，后续位置不压缩。例如 `["a", "a", "b"]` 中 b 的 rank 为 3。
- 按融合分数降序排序；完全相同的分数按 chunk ID 字符串升序打破平局。返回最多 top_k 个不同候选。
- rank_constant 是非负整数，top_k 是正整数，否则抛 `ValueError`；空输入也先校验参数。
- `[]` 或全为空列表的输入返回 `[]`。约定 ID 是非空字符串，不修改输入。

例如 rankings=`[["a", "b"], ["b", "c"]]`、rank_constant=0，b 得分 1.5、a 得分 1、c 得分 0.5。

## B：组合两路 retriever

完成 `hybrid_search(question, lexical_retriever, vector_retriever, k=5, rank_constant=60)`。

- 先校验参数并规范化问题；空白问题、k<=0 或 rank_constant<0 抛 `ValueError`，不调用依赖。
- 用规范化问题分别调用两个 retriever 的 `.invoke()` 各一次，结果为 `list[Document]`。
- 复用本级 RRF 函数，按 `metadata["chunk_id"]` 融合，返回最多 k 个 Document。不得用 source 代替 chunk ID：同一文档的不同块应能分别进入排名。
- 每份 Document 都有非空 source、chunk_id；相同 chunk ID 约定内容与 metadata 一致。返回该 ID 首次遇到的文档（先观察关键词列表，再观察向量列表），不修改原对象。
- 一路为空时仍使用另一路；两路都为空返回 `[]`；依赖异常直接传播。

测试注入两路固定结果，不要求实现 BM25 或真实 embedding。真实混合检索的扩展要替换这两个依赖，不能把固定列表称为语义检索质量提升。

## 验收与比较

```bash
python -m pytest --run-exercises tests/rag/langchain/test_level07_hybrid.py -q
```

完成标准：测试通过，并用同一问题集分别记录单路检索和融合后的来源 recall。融合分数不是概率，也不适合直接沿用另一种相似度分数的阈值；是否改善质量要由实验判断。

[RRF 的官方定义](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)。下一步：[Level 8](08_reranking.md)。
