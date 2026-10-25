# Level 9：用 LangGraph 编排可纠正的 RAG

**本级只解决：第一次检索的证据不合格时，怎样有界地改写并重试？**

前置：Level 5、Level 6、仓库的 LangGraph 分支与重试练习。这里的图是工作流图，节点表示步骤；它不要求知识图谱，也不等于 GraphRAG。

## 输入输出与依赖

完成 [level09_workflow.py](../level09_workflow.py) 的 `build_adaptive_rag(...)`。必须用 `StateGraph` 返回真正的 `CompiledStateGraph`，不使用模拟 `.invoke()` 的包装器。

构图参数：

- retriever：`.invoke(query) -> list[Document]`。
- grader：`(original_question, documents) -> bool`，判断这批证据是否足够。
- rewriter：`(current_query) -> str`，产生下一次检索的 query。
- generator：`(original_question, accepted_documents) -> str`。
- max_rewrites：非负整数，表示最多改写多少次；负数在构图时抛 `ValueError`。

测试使用本地函数。真实模型可包进这些依赖；基础验收不测试模型的判断质量。

## 行为契约

图输入为 `{"question": str}`，节点名称依次使用 initialize、retrieve、grade，以及按条件执行的 rewrite、generate、abstain。

- initialize 去掉问题两端空白，空白时抛 `ValueError`；设置本次独立运行的 query、attempts=0、rewrites=0 和空 trace。
- 每次 retrieve 调用 retriever 一次，更新 documents，attempts 加一。
- grade 对非空 documents 调用 grader 一次，传原始规范化问题；空 documents 直接判定不合格，不调用 grader。
- 合格时进入 generate，只用当前合格文档和原始问题生成一次；answer 为其输出，status=`success`，sources 按合格文档的首次来源顺序去重。
- 不合格且还能改写时进入 rewrite；用当前 query 调用 rewriter 一次，对输出去掉两端空白，空白输出抛 `ValueError`；有效时 rewrites 加一，重新检索。
- 不合格且改写上限已到时进入 abstain；answer=`I don't know based on the provided documents.`、status=`abstained`、sources=`[]`，不生成答案。
- trace 记录实际节点执行顺序，包括 initialize 和最终节点。不能把上一轮不合格证据传给 generator；不得修改调用者字典或文档。依赖异常直接传播。
- 同一图可重复调用，状态不串联；最多检索 `max_rewrites+1` 次。框架 recursion_limit 独立于业务上限。

例如第一次不合格、改写一次后合格，trace 为 `["initialize","retrieve","grade","rewrite","retrieve","grade","generate"]`。

## 验收

```bash
python -m pytest --run-exercises tests/rag/test_level09_workflow.py -q
```

完成标准：测试通过，能分别展示直接成功、改写后成功、达到上限拒答三条路径。实际质量实验还应记录检索次数、grader 错判和改写偏离原问题的情况。

本题使用明确规则控制流程，是可纠正检索工作流的教学版本。它不是包含自主工具选择、规划和长期记忆的完整 agent。

[LangGraph 官方 RAG 示例](https://docs.langchain.com/oss/python/langgraph/agentic-rag)。下一条独立分支：[Level 10](10_knowledge_graph.md)。
