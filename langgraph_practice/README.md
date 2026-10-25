# LangGraph 练习

前置：函数、TypedDict、条件判断。所有节点运行普通 Python 函数，无需 LLM。必须用 `StateGraph` 构建并编译图，不要用包装器模拟 `.invoke()`。

## LG-1：条件分支

完成 `ex01_routing.py` 的 `build_graph()`，返回已编译的图。

输入为 `{"question": str}`，执行顺序为 `normalize`、`classify`，然后只能进入 `billing` 或 `general` 其中一个响应节点并结束。

- `normalize` 去掉 question 两端空白；空白输入抛 `ValueError`。
- `classify` 按大小写不敏感的子串规则分类：包含 `refund` 为 `billing`，否则为 `general`。`refunds` 也算匹配。
- billing 回答严格为 `Contact billing support.`；general 回答为 `Contact general support.`。
- 输出保留规范化后的 question，包含 category、answer，以及按实际执行顺序记录的 trace。
- 每次调用互不影响；不得直接修改调用者传入的字典或列表。

例如输入 `{"question": "  REFUND please  "}`，结果应包含 question=`REFUND please`、category=`billing`、trace=`["normalize", "classify", "billing"]`。

## LG-2：有界重试

完成 `ex02_retry.py` 的 `build_retry_graph(checker, max_attempts)`。`max_attempts` 是正整数；小于等于 0 时在构图时抛 `ValueError`。题目不要求处理错误类型。

- 调用输入固定为 `{"attempts": 0, "done": False}`。
- 每次尝试调用 `checker(n)`，n 从 1 开始连续递增，且每次尝试仅调用一次。
- 首次返回 True 时停止，输出 `done=True`、`status="success"` 和实际 attempts。
- 最后一次仍返回 False 时停止，输出 `done=False`、`status="exhausted"`、`attempts=max_attempts`。
- 不允许超过尝试上限；checker 抛异常时直接传播，不把异常视为 False。
- 返回的图应可重复调用，计数保存在每次输入的状态中。

例如 checker 在第 2 次返回 True、上限为 3，最终 attempts=2；始终返回 False、上限为 1，最终 attempts=1。

图运行还有独立的 `recursion_limit`。大上限实验可用 `graph.invoke(initial_state, config={"recursion_limit": 1000})`；达到框架递归限制不等于实现了业务重试上限。

## 验收与思考

运行 `python -m pytest --run-exercises tests/test_langgraph_practice.py -q`。

- 节点返回部分状态时，其他字段如何保留？
- 默认列表更新与 reducer 累积列表的行为有什么区别？
- 写出重试循环的不变量，说明它为什么一定终止。
