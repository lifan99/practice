# RAG 学习路径

按能力分为四条路径：**手写核心 → LangChain 集成 → 工作流／知识图谱扩展**。每条路径都有独立的 README、lessons/ 和 exercises/，测试在 tests/rag/ 的同名目录。没有按版本并列的重复入口。

| 路径 | 目标 | 前置 | 入口 |
| --- | --- | --- | --- |
| core/ | 手写切分、余弦、精确索引、BM25、问答、指标、融合与预算，共10级 | Python；向量／词频基础逐级引入 | [开始学习](core/README.md) |
| langchain/ | 用 Document、Runnable、向量存储接入框架，并桥接核心接口，共9级 | 基础 Python；建议完成手写核心再对照 | [任务目录](langchain/README.md) |
| workflows/ | 用 LangGraph 编排证据评估、改写、重试与拒答 | RAG 流程、评估与 LangGraph 基础 | [任务目录](workflows/README.md) |
| graph/ | 手写事实图、局部多跳路径，并回溯原文证据，共2级 | 字典、集合、有向图 | [任务目录](graph/README.md) |

core/ 无需先学 LangChain。workflows/ 的图节点是执行步骤；graph/ 的图节点是实体，两种分支可独立学习。GraphRAG 仅覆盖局部图检索教学范围，不含自动实体抽取、社区摘要与全局检索。

## 文件约定

```text
rag_practice/
├── README.md
├── core/          # 手写算法与普通函数接口
├── langchain/     # 框架组件和输入输出桥接
├── workflows/     # 纠正检索工作流
├── graph/         # 事实图、图检索及其 data/
└── data/          # 文本语料与 source 级评估样例
```

在各分支内，lessons/ 放任务契约，exercises/ 放实现骨架；core/types.py 是共享数据结构，core/experiments/ 是综合实验要求。只修改当前任务的 exercises/ 文件，按说明运行对应测试。

## 验收入口

在仓库根目录使用完整锁定环境：

```bash
python -m pytest --run-exercises tests/rag/core -q
python -m pytest --run-exercises tests/rag/langchain -q
python -m pytest --run-exercises tests/rag/workflows -q
python -m pytest --run-exercises tests/rag/graph -q
```

只学 core/ 可仅安装 requirements-rag-core.txt，然后只运行 tests/rag/core。没有 --run-exercises 时学生任务被跳过；默认环境检查通过不证明练习完成。

## 数据与评估口径

[data/](data/) 的三份 Markdown 和 [evaluation_queries.json](data/evaluation_queries.json) 用于组件连通性与 source 级评估；[graph/data/](graph/data/) 用于事实图练习。小语料、词频向量和固定模型回复不能证明真实质量。

手写核心保留原文字符偏移，并使用 chunk 级标签；LangChain 文档读取题先清理首尾空白，其评估题按 source 计召回。二者是不同的处理约定，跨接口对照前先统一正文与标签口径。字符预算和 token 预算也应分别记录。

完成核心后进行[综合对比实验](core/experiments/README.md)，再替换真实模型或数据库，报告证据支持、失败样本、延迟和成本。持久化、增量更新、权限、部署与 ANN 是后续工程扩展。
