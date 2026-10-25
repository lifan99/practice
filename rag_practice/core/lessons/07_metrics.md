# C7：手写检索指标

目标：实现 [四个评估函数](../level07_metrics.py)，不使用 sklearn、RAGAS 等指标实现。所有 k>0，否则 ValueError。这里评估单位为 **chunk_id**；不要混用旧框架练习的 source 级标签。

## 指标契约

保留结果的原排名位置，前k截断后不压缩重复项；同一 ID 只有首次出现能贡献命中或 gain，后续重复位置仍占排名。未知 ID 的相关度为0。

- Recall@k：前k不同相关ID数量／相关ID总数。相关集合为空约定0，不把无答案问题计为“召回成功”。
- Reciprocal rank@k：第一个相关结果位置的倒数（从1起）；未命中或相关集合为空返回0。**MRR 是多个问题该值的均值**。
- NDCG@k：本题相关度为整数0–3，其他值抛 ValueError；gain=`2**grade-1`，位置 r 的折扣为 `log2(r+1)`。DCG 为前k折扣gain之和，IDCG 为全部标签按相关度降序后取前k的理想值；IDCG=0时返回0，否则 DCG/IDCG。空标签合法。不同工具可能使用线性gain，不能直接混比数值。

例：[a,a,b]、相关集合{a,b}、k=2，recall=0.5，reciprocal rank=1。三项衡量覆盖和排名，不衡量最终答案是否事实正确。

## 固定集评估

evaluate(cases,retrieve,k) 接收 `{"question":str,"relevance":{chunk_id:grade}}` 列表。cases 非空、所有问题 strip 后非空、所有等级合法、k>0；**整个列表先校验，再开始检索**，非法 ValueError。

按输入顺序每个问题调用 retrieve 一次；重复问题作为独立 case，不缓存。grade>0 的 ID 视为相关，分别复用本模块三个指标，返回 `{"recall":宏平均,"mrr":宏平均,"ndcg":宏平均}`。不修改 cases，回调异常传播。空标签样本三项记0并计入宏平均；请在真实报告中另外分组呈现有答案与无答案样本，评估拒答另需专门指标。

```bash
python -m pytest --run-exercises tests/rag/core/test_core07_metrics.py -q
```

完成后构造两个 Recall 相同但 MRR 不同的结果；说明 chunk ID 随切分配置变化时，为什么必须重新映射证据区间标签。更细的真实效果实验见[实验要求](../experiments/README.md)。
