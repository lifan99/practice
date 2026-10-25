# C3：余弦与精确 Top-k

目标：实现 [cosine_similarity / top_k_vectors](../level03_vectors.py)，可用 Python 或 NumPy，不得调用 sklearn、向量数据库或现成相似度函数。

## A：相似度

余弦相似度定义为 `dot(x,y)/(norm(x)*norm(y))`，这里 norm 为 L2 范数。两向量维度必须相同且非零，所有元素必须有限，否则 ValueError。任意一方为零向量，本题约定分数0；反方向可以得到负分。数值比较允许浮点误差，输入测试不含导致浮点溢出的极端量级。

例如 [1,0] 与 [3,0] 为1，与 [0,1] 为0，与 [-1,0] 为-1。不修改输入。

## B：精确检索

top_k_vectors(query, vectors, k) 返回 `(输入行号, 分数)` 列表。k>0；先验证 query 和**所有**候选行，即使坏行不在最终前k；按分数降序，同分按原行号升序。k 超过总数取全部，候选为空返回 []，但仍验证 query 和 k。返回分数来自手写余弦函数。

```bash
python -m pytest --run-exercises tests/rag/core/test_core03_vectors.py -q
```

完成后解释：归一化后点积为什么与余弦排序一致？未归一化时给出反例。说明自己的精确检索复杂度，区分计算得分和选择前k的成本；不要求实现 ANN。
