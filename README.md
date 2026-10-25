# LangChain / LangGraph / RAG 练习

[![Practice environment](https://github.com/lifan99/practice/actions/workflows/ci.yml/badge.svg)](https://github.com/lifan99/practice/actions/workflows/ci.yml)

适合会使用 Python 函数、类型标注、字典和虚拟环境的学习者。说明用中文，代码用英文。这里是独立练习：函数签名和测试已经准备好，核心实现以 `NotImplementedError` 标记，没有附答案。

LangChain 练习组件组合，LangGraph 练习有状态工作流，RAG 练习用外部文档支持回答。RAG 是一种架构，不是与前两者并列的 Python 库；本项目用 LangChain 组件实现它。

## 安装与检查

使用 Python 3.12。克隆仓库并安装已验证的依赖：

```bash
git clone https://github.com/lifan99/practice.git
cd practice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pytest -q
```

Windows PowerShell 中，创建虚拟环境使用 `py -3.12 -m venv .venv`，激活使用 `.venv\Scripts\Activate.ps1`，其余 Python 命令相同。

依赖安装需要联网；安装完成后，所有基础练习与测试均可离线运行，不需要 API Key。`requirements-lock.txt` 锁定本次在 Python 3.12 / Linux 下验证的依赖版本；`requirements.txt` 提供允许升级的兼容版本范围，升级后应重新验证。

默认测试只检查运行环境，练习测试全部跳过。初始结果应为 **4 项环境检查通过，练习测试全部 skipped**；这不代表练习已经完成。GitHub Actions 的绿色状态同样只表示环境检查和 Python 语法检查通过。

## 学习入口

| 主题 | 当前练习范围 | 入口 |
| --- | --- | --- |
| LangChain | 10 级：基础组件、并行与路由、结构化输出、多工具 agent、记忆、可靠性、异步、流式输出 | [LangChain 分级练习](langchain_practice/README.md) |
| LangGraph | 条件分支、有界重试 | [LangGraph 练习](langgraph_practice/README.md) |
| RAG | 11 级：基础六级、Advanced RAG、LangGraph RAG、GraphRAG 局部图检索 | [RAG 分级练习](rag_practice/README.md) |

各主题的 README 提供每级前置知识、输入输出约定、独立测试命令与完成标准。LangChain 基础两级可作为 RAG 生成部分的准备；RAG 基础和知识图谱分支不要求先学 LangGraph，工作流分支则需要。先选一条路径，逐级完成即可。

原有 LangChain 基础文件和测试入口保持可用。只需修改对应练习文件；practice_support.py 和 LangChain 的 offline_models.py 是提供好的测试设施。

```bash
python -m pytest --run-exercises tests/test_langchain_practice.py -q
python -m pytest --run-exercises tests/langchain -q
python -m pytest --run-exercises tests/test_langgraph_practice.py -q
python -m pytest --run-exercises tests/rag/test_level01_documents.py -q
python -m pytest --run-exercises tests/rag -q
python -m pytest --run-exercises -q
```

**加上 `--run-exercises` 后，尚未完成的练习测试会失败，这是预期现象。** 看到 `NotImplementedError` 表示还未完成该函数，不是环境损坏。先跑环境检查，再按顺序使对应测试通过。公开测试只覆盖部分行为；完成后请对照契约自行检查边界情况。

可以通过 `-k` 聚焦单个任务，例如 `python -m pytest --run-exercises tests/test_langchain_practice.py -k test_chain -q`。

每个主题另有简短思考题。完成标准是：对应公开测试通过，能解释自己的数据流与失败路径。无需为了通过测试硬编码示例结果。

## 模拟与真实模型的区别

`FakeListChatModel` 返回预设文本，不会理解提示词；提供的词频 embedding 只用于检验向量检索流程，不能代表真实语义检索质量。问答测试检查上下文和来源传递，不证明回答事实正确，也不证明模型一定遵守拒答或防注入指令。

可选拓展：基础练习完成后，换用真实 chat model 与 embedding model，对有答案、无答案、歧义问题分别评估。自行选择 provider 并安装对应集成包，通过环境变量提供凭据；不要将密钥写入代码。真实调用可能收费，不属于默认测试流程。

## 官方参考

接口文档核对日期：2026-10-25。依赖版本仍以本项目锁文件为准。

- [LangChain 模型接口](https://docs.langchain.com/oss/python/langchain/models)
- [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [LangChain 检索与 RAG](https://docs.langchain.com/oss/python/deepagents/retrieval)
- [LangChain Core API](https://reference.langchain.com/python/langchain-core/)
