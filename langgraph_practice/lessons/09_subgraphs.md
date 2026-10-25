# Level 9：子图与状态接口

**本级只解决：父子工作流的字段不同，怎样保持边界并复用逻辑？**

完成 [level09_subgraphs.py](../level09_subgraphs.py)。

## A：文本子图

build_normalizer_subgraph 使用 StateGraph，输入 raw 字符串，输出 clean（只去两端空白）和 word_count（按空白分词）。空白输入 ValueError；不修改输入。子图有 strip、count 两个顺序节点。

## B：父图适配

build_report_graph(normalizer) 返回父图，输入 `{"document":str,"request_id":str}`。request_id 是调用者标签，原样保留。

- normalize 节点调用传入子图一次，只传 `{"raw":document}`；把 clean 映射成父状态 text，word_count 映射到同名父字段。
- report 节点生成 `request_id: N words`，N 为子图返回的 word_count。
- 保留父状态 document、request_id；子图私有键 raw、clean 不出现在父图输出。
- 不在父图重算清理或词数来代替子图；子图异常传播，不修改输入。

```bash
python -m pytest --run-exercises tests/langgraph/test_level09_subgraphs.py -q
```

测试父图时注入独立编译的子图，以隔离 A 的完成状态。完成标准：解释直接共享 state key 与显式映射两种集成方式。本题不声称实现了多 agent 协作，只验证子工作流组合。

下一步：[Level 10](10_observability.md)。
