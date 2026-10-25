# Level 3：Runnable 并行组合与路由

**本级只解决：怎样把单条链组织成多个分支？**

前置：Level 1。完成 [level03_composition.py](../level03_composition.py) 的两个函数。

## A：两路分析

`build_parallel_analysis(summary_model, keywords_model)` 返回使用 `RunnableParallel` 的 Runnable。

- 输入为 `{"text": str}`；缺少 text 抛 `KeyError`。
- summary 分支的 system 内容为 `Summarize the text.`；keywords 分支为 `List three keywords.`。两者的 human 内容均为原始 text，不改写。
- 两个模型各调用一次，回复均经 `StrOutputParser`，返回 `{"summary": str, "keywords": str}`。
- 返回链支持 `.invoke()` 和 `.batch()`，不修改输入；普通依赖异常直接传播。
- 不要求具体调度顺序或延迟指标，也不解析关键词字符串为列表。

## B：显式路由

`build_router(routes, default)` 返回 Runnable；routes 非空时实际使用 `RunnableBranch`，空 routes 时允许直接转发到 default。

- 输入为 `{"route": str, "payload": 任意值}`；缺少任一键抛 `KeyError`。
- 若 route 在 routes 中，只执行匹配分支，否则只执行 default；分支收到 payload 本身，不是外层字典。
- 不执行未选中的分支。routes 可以为空；不修改输入字典。
- 不使用模型判断 route，不在本级引入分类质量问题。

```bash
python -m pytest --run-exercises tests/langchain/test_level03_composition.py -q
```

完成标准：测试通过，能解释并行组合与条件路由的区别。再用 config 的 tags/metadata 观察一次调用如何传到分支，而不把标签当成模型提示词。

下一步：[Level 4](04_structured.md)。
