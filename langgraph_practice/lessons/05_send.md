# Level 5：动态 Send 与结果归并

**本级只解决：工作数量由输入决定时，怎样分发独立状态？**

完成 [level05_send.py](../exercises/level05_send.py) 的 build_map_graph(worker)，实际用 Send 为每个输入位置创建 worker 节点任务，不在单个节点里直接循环调用 worker。

- 输入 `{"items": list[int]}`，为每次出现的元素分别调用 worker(value) 一次，包括重复值。
- 每个任务持有自己的 index 和 value；归并到 mapped 列表，每项严格为 `{"index": int, "value": worker结果}`。
- collect 产生按输入位置恢复的 results 列表；不得按值去重或按完成顺序返回。
- 空 items 返回 mapped=[]、results=[]，不调用 worker。
- 不修改输入；同一图不同 invoke 不串结果。普通依赖异常传播。

例如输入 `[3,1,3]`、worker 计算平方，results 为 `[9,1,9]`；mapped 存储顺序不作保证。

```bash
python -m pytest --run-exercises tests/langgraph/test_level05_send.py -q
```

完成标准：解释静态并行与 Send 的区别，指出怎样保留重复项的身份。

下一步：[Level 6](06_checkpoints.md)。
