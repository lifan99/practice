# Level 4：静态并行与汇合

**本级只解决：怎样同时执行多个独立节点，再生成完整结果？**

完成 [level04_parallel.py](../exercises/level04_parallel.py) 的 build_parallel_review(reviewers)。reviewers 为名字到 `(text)->feedback` 回调的映射，不能为空；名字需匹配 `[a-z][a-z0-9_]*`，无效时构图即抛 ValueError。

- 输入 `{"text": str}`，prepare 去掉两端空白，空白时 ValueError，不调用任何 reviewer。
- 为每个名字建立独立节点，分别调用对应回调一次，传相同的规范化文本；各节点在同一并行阶段运行。
- 将各节点的 `{"name":名字,"feedback":回调文本}` 更新合并进 reviews 列表，不发生同键并发写冲突。
- collect 等待所有 reviewer 完成，产生按名字升序排列的 report，各行严格为 `name: feedback`，以换行连接。
- reviews 的存储顺序不作保证，但必须各有一项；不修改输入，不用全局列表收集结果。
- 回调异常直接传播，不把未完成的报告当成成功结果。

```bash
python -m pytest --run-exercises tests/langgraph/test_level04_parallel.py -q
```

测试用同步屏障验证两个独立回调确实可以同时运行，不用毫秒耗时猜测并行。完成标准：解释共享状态的 reducer 与最终报告排序为什么是两个不同问题。

下一步：[Level 5](05_send.md)。
