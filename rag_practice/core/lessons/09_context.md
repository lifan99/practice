# C9：重排与完整证据预算

目标：实现 [rerank / pack_context](../exercises/level09_context.py)。重排模型通过回调注入，不要求实现 cross-encoder 训练；去重、打分调用、排序、预算选择自行完成。

## A：重排

question.strip() 非空，k>0，非法时 ValueError，先于 scorer。按 chunk_id 保留首次出现，每个唯一块调用 score(清理后问题,正文) 一次。分数有限，否则 ValueError，负分合法；返回新 SearchHit，score 为新分数。降序，同分保留候选顺序，最多k。空列表不调用 scorer。不改原对象。

## B：token 预算

输入 chunks 约定已去重、正文非空。budget>0，否则 ValueError。按输入顺序尝试加入整块，调用 **level06_pipeline.format_context(当前已选块+[候选块])** 后，把完整渲染文本交给 count_tokens。统计值必须是非负整数（bool 不算），否则 ValueError。

不超过 budget 就保留，否则跳过继续；不截断块，也不求全局最优组合。头部的 chunk_id/source、换行分隔符都计入。每个候选需要按完整候选上下文重新计数，不能假设各块 token 数可直接相加。空输入 []，不调用 counter；依赖异常传播。

测试注入计数器以验证选择逻辑，它不等于真实 tokenizer。实际接模型时要使用对应 tokenizer；本级 budget **只约束证据上下文**，完整模型窗口还需预留 system、问题、历史、工具schema、消息包装和输出空间。

```bash
python -m pytest --run-exercises tests/rag/core/test_level09_context.py -q
```

完成后展示一个只算正文长度会低估预算的例子。比较重排前后支持答案的证据是否被保留，不把上下文减少自动视作质量提升。
