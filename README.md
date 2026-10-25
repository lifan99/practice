# AI 应用开发分级练习

[![Practice environment](https://github.com/lifan99/practice/actions/workflows/ci.yml/badge.svg)](https://github.com/lifan99/practice/actions/workflows/ci.yml)

面向 AI 应用开发学习者的 LangChain、LangGraph、RAG 与 MCP 独立编程练习。中文任务说明，英文代码与类型标注；提供函数骨架和公开测试，核心实现保留 TODO，不附完整答案。前置为 Python 函数、列表、字典、异常与虚拟环境，异步章节另需 async/await。

## 从哪里开始

默认走 **手写 RAG 基线 → 可用服务 → 评估优化 → 岗位专题选修**。完整顺序与进入下一阶段的证据见[课程主线](curriculum/README.md)，阶段任务见[知识库项目](projects/README.md)。基础完成后立即开始项目，不需要先刷完所有框架章节。

- 学机制：先做 RAG C1–C4、C6–C7，P1 对照时补 C5；C8–C10 由失败分析决定。
- 做工程：P2 使用 [Milvus](projects/knowledge-assistant/milvus.md)提供向量存储，补齐 API、业务数据库、身份边界、版本更新、进程重启和容器；P3 用质量、成本与延迟验证改进。
- 学框架：选择项目实际需要的 LangChain、LangGraph、MCP 或 GraphRAG 单元；重复机制题可按迁移证据跳过。

[基础补学](curriculum/foundations/README.md)按需使用；[独立迁移任务](curriculum/README.md)逐步撤去函数骨架。项目与迁移部分提供任务契约和评审矩阵，尚无项目实现或预置自动验收器。

[基础读物](curriculum/readings/README.md)已复用审核 MVP 的契约、异步、HTTP 与服务边界材料，配有[七个标准库示例](support/mvp_examples/README.md)。在根目录运行 `python support/mvp_examples/run_all.py`。SQL／容器系统讲义与模型原理仍待补建，范围见读物说明。

## 目录怎么找

| 路径 | 内容 | 学习入口 |
| --- | --- | --- |
| curriculum/ | 主修／选修、基础补学、迁移与学习证据 | [学习顺序](curriculum/README.md) |
| projects/ | 同一知识库项目的基线、服务、评估与专题任务 | [项目交付](projects/README.md) |
| langchain_practice/ | 十级组件组合、工具、agent、记忆、可靠性、异步与流 | [LangChain](langchain_practice/README.md) |
| langgraph_practice/ | 十级状态、分支、并行、checkpoint、中断与恢复 | [LangGraph](langgraph_practice/README.md) |
| rag_practice/core/ | 十级手写 RAG：切分、余弦、索引、BM25、评估与融合 | [RAG 手写核心](rag_practice/core/README.md) |
| rag_practice/langchain/ | 九级框架集成：Document、向量存储、Runnable 与桥接 | [RAG 的 LangChain 集成](rag_practice/langchain/README.md) |
| rag_practice/workflows/ | LangGraph 纠正检索工作流 | [RAG 工作流](rag_practice/workflows/README.md) |
| rag_practice/graph/ | 事实图建模、多跳路径、来源证据 | [GraphRAG](rag_practice/graph/README.md) |
| mcp_practice/ | 十级协议、server/client、传输、并发与多服务 | [MCP](mcp_practice/README.md) |
| tests/ | 按主题对应的练习验收；environment/ 为环境检查 | [测试说明](tests/README.md) |
| support/ | 跨主题使用的离线测试设施 | [离线模型与向量](support/offline.py) |

主题目录统一约定：**lessons/ 读题，exercises/ 写代码，support/ 使用提供好的测试设施，data/ 放样本**。每条路径的 README 只负责导航、依赖与运行入口。RAG 先手写核心，再选择框架集成、工作流或知识图谱；不要求先学 LangChain 才能开始 RAG。

## 安装与运行

完整环境使用 Python 3.12，在仓库根目录执行：

```bash
git clone https://github.com/lifan99/practice.git
cd practice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pytest -q
```

PowerShell 使用 py -3.12 -m venv .venv 创建环境，使用 .venv\Scripts\Activate.ps1 激活。锁文件在 Python 3.12 / Linux 验证；requirements.txt 提供依赖范围，升级后需重新验证。

依赖安装后练习可离线运行，无需 API Key。默认测试应为 **8 passed、练习全部 skipped**；CI 绿色表示环境、语法与提供好的离线示例检查通过，不代表学生任务已完成。开启练习验收：

```bash
python -m pytest --run-exercises tests/langchain/test_level01_chain.py -q
python -m pytest --run-exercises tests/langchain -q
python -m pytest --run-exercises tests/langgraph -q
python -m pytest --run-exercises tests/rag/core -q
python -m pytest --run-exercises tests/rag/langchain -q
python -m pytest --run-exercises tests/rag/workflows -q
python -m pytest --run-exercises tests/rag/graph -q
python -m pytest --run-exercises tests/mcp -q
```

TODO 导致的 NotImplementedError 是尚未完成的任务。公开测试通过后，还应能解释数据流、失败路径和工程取舍；具体完成标准见每级任务，不用硬编码示例结果。

仅学手写 RAG 可在独立环境安装 [requirements-rag-core.txt](requirements-rag-core.txt)，只运行 tests/rag/core；核心代码使用标准库，可选 NumPy。其他主题需完整依赖。

## 测试与真实效果

support/offline.py 的词频向量、FakeListChatModel 和各主题 support/ 是提供好的受控设施。它们验证流程，不证明真实语义检索、规划、回答正确性或防提示注入效果。MCP stdio 使用本地测试子进程；HTTP 验收使用进程内 ASGI，不开放端口。

完成最小检索问答后就建立首轮评估，再通过注入接口接真实或本地 embedding、chat model 和按需选用的 reranker。固定问题集比较质量、延迟与费用；记录有答案、无答案和歧义样本。凭据通过环境变量提供，真实服务调用可能收费。RAG 的[实验规范](rag_practice/core/experiments/README.md)与[P1–P3](projects/README.md)给出交付要求。项目服务依赖由学习者在独立环境锁定，当前根锁文件只保证组件练习环境。

## 官方参考

接口核对日期：2026-10-25；运行版本以锁文件为准。

- [LangChain 模型](https://docs.langchain.com/oss/python/langchain/models)
- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [LangChain 检索](https://docs.langchain.com/oss/python/deepagents/retrieval)
- [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/)
