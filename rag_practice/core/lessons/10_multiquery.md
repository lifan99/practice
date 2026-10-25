# C10：有界多查询检索

目标：实现 [multi_query_search](../exercises/level10_multiquery.py)，用普通函数组合 query 扩展与 C8 的融合。rewrite 可以是真实模型，也可以是受控回调；本级手写执行规则，不评价改写的语义质量。

- question.strip() 非空，max_queries>0、k>0、rank_constant>=0，否则 ValueError，先于所有依赖调用。
- 原始清理后问题总是第一条，计入 max_queries。max_queries=1时不调用 rewrite。
- 其他情况调用 rewrite(清理后问题) 一次，约定返回 list[str]；各项 strip，忽略空白，与已保留 query 按区分大小写的字符串去重。最多保留 max_queries 条（包括原始问题），不额外改写。
- 按保留顺序每条 query 调 retrieve 一次，无共享隐式缓存；不同 query 即使命中相同块也保留独立排名。
- 必须复用 **level08_hybrid.reciprocal_rank_fusion(rankings,k,rank_constant)**，返回其结果。无扩展仍查原始问题；全部空命中返回 []。依赖异常传播，不修改回调结果。

```bash
python -m pytest --run-exercises tests/rag/core/test_level10_multiquery.py -q
```

完成后记录单查询与多查询的 Recall、MRR、NDCG、检索次数，并检查改写是否偏离原意。固定问题与相同预算下比较；更多查询不保证更好。最终进入[综合实验](../experiments/README.md)。
