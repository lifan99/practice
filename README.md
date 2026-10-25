# AI 应用开发分级练习

[![Practice environment](https://github.com/lifan99/practice/actions/workflows/ci.yml/badge.svg)](https://github.com/lifan99/practice/actions/workflows/ci.yml)

LangChain、LangGraph、RAG 与 MCP 的独立编程练习。中文任务说明，英文代码与类型标注；提供函数骨架和公开测试，核心实现保留 TODO，不附完整答案。前置为 Python 函数、列表、字典、异常与虚拟环境，异步章节另需 async/await。

## 目录怎么找

| 路径 | 内容 | 学习入口 |
| --- | --- | --- |
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

依赖安装后练习可离线运行，无需 API Key。默认测试应为 **8 passed、练习全部 skipped**；CI 绿色表示环境和语法检查通过，不代表学生任务已完成。开启练习验收：

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

完成基础后可通过注入接口接真实 embedding、chat model 和 reranker，再用固定问题集比较质量、延迟与费用。记录有答案、无答案和歧义样本；凭据通过环境变量提供，真实调用可能收费。RAG 的[综合实验](rag_practice/core/experiments/README.md)给出记录要求。

## 官方参考

接口核对日期：2026-10-25；运行版本以锁文件为准。

- [LangChain 模型](https://docs.langchain.com/oss/python/langchain/models)
- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [LangChain 检索](https://docs.langchain.com/oss/python/deepagents/retrieval)
- [MCP Python SDK](https://py.sdk.modelcontextprotocol.io/)
