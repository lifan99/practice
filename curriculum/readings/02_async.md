# 异步、预算与取消清理

前置：函数、异常、try/finally、上下文管理器。目标：能追踪 Task 的执行、解释等待与预算范围，并证明取消后资源可复用。改编自 [MVP 异步专题及三个标准库示例](SOURCES.md)。

## 同一份工作顺序，多份工作交错

MVP 的 Critic 依赖 Analyst 输出，Judge 又依赖前两步，因此一份审核内部依次执行。两份不同审核可以在等待各自依赖时交错；各自的上下文字典必须独立。

```text
R1: Analyst → Critic → Judge
R2: Analyst → Critic → Judge
```

这张图表达每行的依赖，未规定两行之间的完成顺序。RAG 同样可以并发处理独立查询，而单个查询里的“检索后生成”仍有数据依赖。

## 调用协程、等待和调度

调用 `async def` 定义的函数得到协程对象，不会因此自动把它调度为后台任务。`await` 等待可等待对象；当依赖需要挂起时，任务可以让出执行机会。Task 将协程交给事件循环调度。一个 await 若立即完成，不保证发生任务切换。

把阻塞 I/O 放进 `async def` 不会自动使其异步。事件循环被阻塞时，其他任务也无法及时执行取消与超时处理。`asyncio.sleep` 与同步 sleep 的执行影响不同。[Python 协程与任务](https://docs.python.org/3.12/library/asyncio-task.html)

## 第一个实验：怎样证明并发

运行 [concurrency.py](../../support/mvp_examples/concurrency.py)，按 `main → review → FakeClient.complete` 阅读：

```bash
python support/mvp_examples/concurrency.py
```

第一份 Analyst 等待第二份也进入，二者都开始后才放行。峰值活动调用为2；每份审核的角色顺序不变，结束后活动数为0。这里用事件观察重叠，不靠网络耗时推断并发。

FakeClient 在记录上下文时复制字典。如果只保存同一个可变字典的引用，后续写入会改变之前的观察记录，从而掩盖当时缺失字段或串线问题。示例只是预设输出，不验证角色规划或审核质量。

## 三个时间范围

| 范围 | 约束什么 | 不能推出什么 |
| --- | --- | --- |
| 网络操作超时 | 连接、读、写、池等待等指定操作 | 整份业务总时长 |
| 单次调用预算 | 某一次依赖的等待与执行范围 | 排队和其他调用也受同一上限 |
| 总预算 | 从声明的起点到整份任务结束 | 超时触发后清理零耗时 |

每一步重新获得完整时限，可能让整体运行远超原本的总预算。总预算必须明确起点及是否含排队；MVP 的内核排队政策与本课程 T2 的逐项预算是不同契约。

运行 [timeouts.py](../../support/mvp_examples/timeouts.py)，先读 `limited_call`，再读 `review`：

```bash
python support/mvp_examples/timeouts.py
```

示例分别让单次预算与总预算先耗尽，并保留已完成的第一阶段。还主动抛出一个无关 TimeoutError，确认不会被误标为当前作用域到期。`scope.expired()` 用于判断自己的计时作用域；不能把捕获到的所有 TimeoutError 一概解释为模型预算耗尽。

这些短时限是观察取消的手段。实际到期仍需事件循环获得执行机会，并完成清理；它不是严格的实时保证。同步阻塞和抑制取消的依赖都会影响行为。[Python 超时接口](https://docs.python.org/3.12/library/asyncio-task.html#timeouts)

## 取消请求之后还有什么工作

`task.cancel()` 请求取消，调用方仍要等待任务退出，才能观察到异常传播和 finally 收尾。CancelledError 在 Python 3.12 中继承 BaseException，普通 `except Exception` 不会捕获它；处理取消应保留约定的传播行为。

运行 [cancellation.py](../../support/mvp_examples/cancellation.py)：

```bash
python support/mvp_examples/cancellation.py
```

先看 R1 取得名额、完成 Analyst、挂在 Critic；R2 已等待名额。控制方取消 R1 并等待它结束，之后核对 Critic 清理、Judge 未启动、已完成回答保留，R2 能取得释放的名额。最后再实际获取一次名额验证可复用，而不读取信号量私有计数。

示例证明协作取消，不模拟强杀进程。进程崩溃后的数据和副作用恢复需要持久化与另外的测试。

## 谁拥有任务和共享客户端

创建任务的一方需要管理其结果、失败与退出；借用共享客户端的任务不应各自关闭客户端。服务关闭时先停止新任务，再让已有任务结束或取消并等待清理，最后关闭共享资源。

TaskGroup 和 gather 的失败语义不同。TaskGroup 会在普通子任务失败时取消其他任务；gather 默认传播首个异常时，不自动取消其他正常运行的子任务。因此是否继续其他独立任务必须写进契约，不能仅凭选用了某个 API 推断。[Python TaskGroup 与 gather](https://docs.python.org/3.12/library/asyncio-task.html)

Semaphore 可以限制同一事件循环内进入的协作任务数，不构成多 worker 的全局容量。连接池、任务名额和供应商限流也分别约束不同资源。

现在进入 [F2](../foundations/02_async.md)，再做 [T2](../transfer/02_async.md)。这些示例讲解顺序与清理，不包含 T2 的完整批处理实现；独立任务还需自行设计逐项结果、超时与取消策略。
