# RAG 学习路径

RAG 机制沿 **手写核心 → 项目服务 → 评估优化** 一条主线学习。读取、切分、检索、问答与指标只在 core/ 实现一套；LangChain 的组件和类型适配集中在 [langchain_practice/](../langchain_practice/README.md)。

| 定位 | 内容 | 前置 | 入口 |
| --- | --- | --- | --- |
| 主线：core/ | 手写文档读取、切分、余弦、精确索引、BM25、问答、指标、融合与预算，共10级 | Python；向量／词频基础逐级引入 | [开始学习](core/README.md) |
| 选修：workflows/ | 用 LangGraph 编排证据评估、改写、重试与拒答 | 核心问答与评估、LangGraph 基础 | [纠正检索工作流](workflows/README.md) |
| 选修：graph/ | 手写事实图、局部多跳路径，并回溯原文证据，共2级 | 字典、集合、有向图 | [GraphRAG](graph/README.md) |

core/ 无需先学框架。workflows/ 的图节点是执行步骤；graph/ 的图节点是实体。两项专题可独立选择：前者学习检索流程控制，后者学习关系查询。GraphRAG 目前覆盖局部图检索，不含自动实体抽取、社区摘要与全局检索。

## 从哪里开始

先读 [C1／C2 前置知识](knowledge.md)，按当前练习补充数据类、Path、文件类型、UTF-8、字符串空白、列表与排序、切片、循环控制和正则匹配。小例子可独立运行，不附练习完整解答。

C1–C4、C6–C7 后开始 [P1 基线项目](../projects/knowledge-assistant/01_baseline.md)，加入 C5 做词法基线。服务化与持久化进入 [P2](../projects/knowledge-assistant/02_service.md)；按失败归因选择 C8–C10，在 [P3](../projects/knowledge-assistant/03_evaluation.md)验证收益。不必等所有进阶题完成才做首轮评估。

项目需要 LangChain 时，在掌握消息与 Runnable 后完成 [LangChain L11 桥接](../langchain_practice/lessons/11_rag_bridge.md)，将已有 C6 接到框架边界。需要检索纠正、恢复或关系查询时，再选择 workflows/ 或 graph/。完整先修与迁移要求见[课程主线](../curriculum/README.md)。

## 从手写索引到 Milvus

项目向量存储主线为 [Milvus Standalone](../projects/knowledge-assistant/milvus.md)。完成核心索引、指标与 P1 后，在 P2 的独立项目环境接入；使用相同 chunks、向量与候选范围对照精确检索。权限、版本、删除、持久化与服务重启按接入任务验收，core 本身保持纯 Python 数据结构与普通函数。

## 文件怎么找

```text
rag_practice/
├── README.md
├── knowledge.md   # C1／C2 前置知识与独立小示例
├── core/          # 唯一机制主线：types.py、lessons/、exercises/、experiments/
├── workflows/     # 选修：纠正检索工作流
├── graph/         # 选修：事实图、多跳检索及其 data/
└── data/          # 三份 Markdown 小语料
```

lessons/ 放任务契约，exercises/ 放代码骨架；core/types.py 定义共享数据结构，core/experiments/ 放综合实验要求。测试在 tests/rag/ 的对应目录。阅读当前任务后修改对应 exercises/ 文件，并单独运行该级测试。

## 验收入口

在仓库根目录使用完整锁定环境：

```bash
python -m pytest --run-exercises tests/rag/core -q
python -m pytest --run-exercises tests/rag/workflows -q
python -m pytest --run-exercises tests/rag/graph -q
```

只学 core/ 可仅安装 requirements-rag-core.txt，并只运行 tests/rag/core。没有 --run-exercises 时练习被跳过；默认环境检查通过不证明练习完成。框架桥接的测试入口见 LangChain L11。

## 数据与评估

[data/](data/) 的三份 Markdown 用于组件连通性；[graph/data/](graph/data/) 用于事实图练习。小语料、词频向量和固定模型回复不能证明真实质量。

核心保留原文字符偏移，以 chunk_id 标记相关性；桥接沿用正文、ID、来源与偏移，不额外清理原文。切分变化后需重新核对标签；字符预算与 token 预算分别记录。

从最小闭环就开始[基线与对比实验](core/experiments/README.md)，报告证据支持、失败样本、延迟和成本。持久化、更新删除、权限与部署按 P2 的规格独立实现；ANN 在容量需求出现后选修。
