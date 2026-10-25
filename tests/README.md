# 测试入口

所有命令在仓库根目录运行。默认 pytest 验证提供好的环境与设施，学生任务需要 --run-exercises 才执行；未实现时的 TODO 异常是预期现象。

| 目录 | 对应内容 | 验收命令 |
| --- | --- | --- |
| environment/ | 依赖、离线设施、流接口和MCP传输 | python -m pytest tests/environment -q |
| langchain/ | LangChain 1–10级 | python -m pytest --run-exercises tests/langchain -q |
| langgraph/ | LangGraph 1–10级 | python -m pytest --run-exercises tests/langgraph -q |
| rag/core/ | 手写核心10级与串联检查 | python -m pytest --run-exercises tests/rag/core -q |
| rag/langchain/ | 框架集成9级 | python -m pytest --run-exercises tests/rag/langchain -q |
| rag/workflows/ | 纠正检索工作流 | python -m pytest --run-exercises tests/rag/workflows -q |
| rag/graph/ | 图建模与多跳检索 | python -m pytest --run-exercises tests/rag/graph -q |
| mcp/ | MCP 1–10级 | python -m pytest --run-exercises tests/mcp -q |

每级统一使用 test_levelNN_主题.py，可单独运行；同一目录的集成测试使用 test_integration.py。pytest.ini 使用 importlib 导入模式，允许不同路径有同名测试文件。conftest.py 保留练习开关；rag/core/conftest.py 提供小样本构造器。

公开用例检查行为契约的一部分。绿色环境 CI 不代表练习完成或真实模型质量通过，仍需完成每级解释、边界自查和实验记录。仅安装 requirements-rag-core.txt 时，只运行 rag/core/；完整环境才可收集其他主题。
