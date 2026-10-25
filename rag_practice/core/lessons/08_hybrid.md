# C8：两路召回与 RRF

目标：实现 [reciprocal_rank_fusion / hybrid_search](../level08_hybrid.py)。把 C4 的向量检索、C5 的 BM25 各包装为 `Callable[[str], list[SearchHit]]`，再组合；不得用框架 EnsembleRetriever。

RRF 契约：每个不同 chunk_id 从每个出现它的列表首次出现位置 r（从1起）得到 `1/(rank_constant+r)`，跨列表求和。单列表重复项仍占原位置，不能先去重压缩排名。忽略输入的原始 score，不把 BM25 与余弦直接相加。

输出 SearchHit.score 为融合分；chunk 为该 ID 首次遇到的对象。按融合分降序，同分按 ID 字符串升序。k>0、rank_constant>=0，否则 ValueError，即使输入为空也要校验。允许空列表，不修改输入。输入约定同ID内容和来源一致。

hybrid_search 先校验清理后问题和两个数值参数，再按 lexical、dense 顺序各调用一次，复用本模块 RRF。两路都空返回 []，单路空仍融合另一条，异常传播。本题为确定性顺序调用，异步并发可作为后续工程练习。

```bash
python -m pytest --run-exercises tests/rag/core/test_core08_hybrid.py -q
```

完成后在相同问题集比较 BM25、向量、混合检索。记录融合分不等于概率，也不能沿用余弦阈值；融合未提高指标时也如实报告。
