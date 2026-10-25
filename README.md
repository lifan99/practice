# LangChain / LangGraph / RAG 练习

[![Practice environment](https://github.com/lifan99/Practice/actions/workflows/ci.yml/badge.svg)](https://github.com/lifan99/Practice/actions/workflows/ci.yml)

适合会使用 Python 函数、类型标注、字典和虚拟环境的学习者。说明用中文，代码用英文。这里是独立练习：函数签名和测试已经准备好，核心实现以 `NotImplementedError` 标记，没有附答案。

LangChain 练习组件组合，LangGraph 练习有状态工作流，RAG 练习用外部文档支持回答。RAG 是一种架构，不是与前两者并列的 Python 库；本项目用 LangChain 组件实现它。

## 安装与检查

使用 Python 3.12。克隆仓库并安装已验证的依赖：

```bash
git clone https://github.com/lifan99/Practice.git
cd Practice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pytest -q
```

Windows PowerShell 中，创建虚拟环境使用 `py -3.12 -m venv .venv`，激活使用 `.venv\Scripts\Activate.ps1`，其余 Python 命令相同。

依赖安装需要联网；安装完成后，所有基础练习与测试均可离线运行，不需要 API Key。`requirements-lock.txt` 锁定本次在 Python 3.12 / Linux 下验证的依赖版本；`requirements.txt` 提供允许升级的兼容版本范围，升级后应重新验证。

默认测试只检查运行环境，练习测试全部跳过。初始结果应为 **3 passed, 55 skipped**；这不代表练习已经完成。GitHub Actions 的绿色状态同样只表示环境检查和 Python 语法检查通过。

## 练习顺序

| 顺序 | 文件 | 完成后的可观察结果 |
| --- | --- | --- |
| 1 | [langchain_practice/ex01_chain.py](langchain_practice/ex01_chain.py) | 将输入字典转为消息，调用模型，输出字符串 |
| 2 | [langchain_practice/ex02_tools.py](langchain_practice/ex02_tools.py) | 暴露带 schema 的工具，验证结构化学习计划 |
| 3 | [langgraph_practice/ex01_routing.py](langgraph_practice/ex01_routing.py) | 同一工作流按输入进入不同节点 |
| 4 | [langgraph_practice/ex02_retry.py](langgraph_practice/ex02_retry.py) | 成功时停止，失败时在次数上限内终止 |
| 5 | [rag_practice/ex01_index.py](rag_practice/ex01_index.py) | 加载、切分文档并建立可检索向量索引 |
| 6 | [rag_practice/ex02_qa.py](rag_practice/ex02_qa.py) | 将证据交给模型、返回来源、计算检索召回率 |

各目录的 README 提供精确输入输出约定和边界条件。只需修改练习文件；`practice_support.py` 是提供好的测试设施。

```bash
python -m pytest --run-exercises tests/test_langchain_practice.py -q
python -m pytest --run-exercises tests/test_langgraph_practice.py -q
python -m pytest --run-exercises tests/test_rag_practice.py -q
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
