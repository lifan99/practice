# Level 1：状态节点与条件分支

**本级只解决：怎样根据状态选择一个执行分支？**

完成已有 [ex01_routing.py](../ex01_routing.py) 的 build_graph，使用 StateGraph 返回 CompiledStateGraph。

- 输入 `{"question": str}`，执行 normalize、classify，然后只进入 billing 或 general 节点并结束。
- normalize 去掉问题两端空白，空白输入抛 ValueError。
- classify 按大小写不敏感的子串规则匹配 refund；包含时 category=billing，否则 general。
- answer 分别为 `Contact billing support.` 或 `Contact general support.`。
- 输出保留规范化问题、category、answer 和真实执行顺序 trace，例如 `["normalize","classify","billing"]`。
- 不修改输入，重复调用不串状态。

```bash
python -m pytest --run-exercises tests/test_langgraph_practice.py -k 'routing or empty_question' -q
```

完成标准：测试通过，能指出节点返回值和边各自负责什么。下一步：[Level 2](02_retry.md)。
