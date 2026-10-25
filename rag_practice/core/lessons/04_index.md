# C4：自有索引与检索前过滤

目标：实现 [build_index / search_index](../exercises/level04_index.py)，使用 [VectorIndex](../types.py)。不使用框架向量存储。

## A：建库

- chunks 非空、chunk_id 不重复，否则 ValueError，且不调用 embedding。
- embed_documents 按原顺序接收全部正文，恰好一次，返回与 chunks 等长的向量序列。
- 输出向量维度一致、非空、所有元素有限，否则 ValueError；保存为独立 tuple 快照，使回调后来修改列表不会改变索引。chunks 也保存为 tuple，原列表可独立修改。
- 不训练 embedding；其输入输出接口由你控制。不同 build 调用没有共享全局可变状态。

## B：查询

question.strip() 非空、k>0，否则 ValueError，先于回调调用。index 约定是有效建库结果，测试也可直接构造有效对象。

allowed_sources=None 表示全部；set 表示仅候选来源在其中的块，空集表示无候选。**先过滤，再做 Top-k**。无候选直接 []，不调用 embed_query；否则将清理后问题交给 embed_query 一次，校验维度与数值，并复用 C3 的精确相似度能力。

返回 SearchHit，按分数降序、同分按原索引顺序；最多k，不按 source 去重。负分和零分仍可返回，没有默认相似度阈值。过滤是检索策略练习，不等于完整用户认证／授权系统。

```bash
python -m pytest --run-exercises tests/rag/core/test_level04_index.py -q
```

完成后展示一个“先 Top-k 再过滤”会丢失合法候选的例子。说明 embedding 模型变化后旧向量是否仍可比较，以及索引应记录哪些模型版本信息。
