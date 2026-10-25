# RAG 分级练习

每一级只增加一个主要能力：**文档 → 切分 → 检索 → 生成 → 组合 → 评估**。所有代码都是待完成的练习，不附完整答案。先完成当前级，再进入下一级；不要求先掌握数据库部署或真实模型服务。

## 从哪里开始

基础准备：Python 函数、字典、列表、Path 和类型标注。第 1–3 级无需 chat model；第 4 级开始需要 LangChain messages / Runnable，可先完成仓库的 LangChain 练习。整个基础路径不要求先学 LangGraph。

| 级别 | 本级要回答的问题 | 题目 | 代码 |
| --- | --- | --- | --- |
| 1 · 文档 | 如何保留内容与来源？ | [任务说明](lessons/01_documents.md) | [level01_documents.py](level01_documents.py) |
| 2 · 切分 | 如何从字符窗口过渡到递归切分？ | [任务说明](lessons/02_chunking.md) | [level02_chunking.py](level02_chunking.py) |
| 3 · 检索 | 如何只找证据、不生成答案？ | [任务说明](lessons/03_retrieval.md) | [level03_retrieval.py](level03_retrieval.py) |
| 4 · 生成 | 给定证据后如何组织模型输入？ | [任务说明](lessons/04_generation.md) | [level04_generation.py](level04_generation.py) |
| 5 · 组合 | 如何处理检索、生成与无证据分支？ | [任务说明](lessons/05_pipeline.md) | [level05_pipeline.py](level05_pipeline.py) |
| 6 · 评估 | 如何测量召回并比较切分配置？ | [任务说明](lessons/06_evaluation.md) | [level06_evaluation.py](level06_evaluation.py) |

每级的说明给出前置知识、输入输出契约、边界情况、独立测试命令和完成标准。第 2 级有先后两道小题，第 6 级另有参数对比实验。

## 如何运行

先按照[总说明](../README.md)安装依赖，然后在仓库根目录执行：

```bash
# Start with level 1 only.
python -m pytest --run-exercises tests/rag/test_level01_documents.py -q

# After completing level 1, move to level 2.
python -m pytest --run-exercises tests/rag/test_level02_chunking.py -q

# Run all RAG acceptance checks when ready.
python -m pytest --run-exercises tests/rag -q
```

初始 `NotImplementedError` 是待完成练习的标记。默认 `python -m pytest -q` 跳过全部练习，只验证运行环境，不能证明你已经完成某级。公开测试通过后，还应对照契约检查边界，并完成本级解释或观察任务。

测试尽量隔离不同级别：第 3 级直接使用提供好的 Document，第 4 级直接使用给定证据，第 5 级用替代生成函数检查组合逻辑，第 6 级用固定 retriever 检查指标。这样某一级的失败不会迫使你同时调试整条链。最终串联时仍需完成前面的组件。

## 数据与范围

- [data/](data/) 包含三份短 Markdown 文档；第 1 级只读取 `.md` 文件。
- [evaluation_queries.json](data/evaluation_queries.json) 给出第 6 级组件实验的问题与相关来源，加载后把来源列表转成 set。
- `practice_support.KeywordEmbeddings` 是本地词频向量；`FakeListChatModel` 返回预设文本。两者用于流程验证，不代表真实语义检索或生成质量。
- 通过 context 传递 source 不证明模型实际引用了它，也不证明回答正确。基础题仅对空检索结果实现确定性拒答。

旧的 `ex01_index.py`、`ex02_qa.py` 保留为导入兼容入口。请修改相应的 `levelXX_*.py`，不要在旧文件重复实现。

## 基础路径完成后的扩展

以下是可选项目方向，不是当前六级已提供的实现或测试：结构化文档切分与表格处理、真实 embedding 和 chat model、重排与混合检索、持久化与增量更新、LangGraph 工作流。每次只选一个方向，给出可观察的改进目标后再增加组件。
