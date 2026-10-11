# Run152：有限信息抽象的充分性合同

日期：2026-10-11；分支 `research/run152-finite-information-abstraction-gate`。

本轮仅从 Run151 短检查点接续，定向读取当前 mode graph、初始化、policy contract、Run148
三 return seed checker，以及 Baras--Patel 原文相关章节。未通读历史分支。

核心纠正有两点。第一，当前 `mode` 已是连续丢包年龄，所谓 `return-age` 若含义相同只是
重复标签；三条 success 边均回到 mode 0。要保存 return history，最小离散扩展应是上一
周期长度 `last_return in {5,10,15}`，而不是再次记录 current age。第二，不同历史产生不同
shape 并不足以否定有限抽象：保守控制只需一个覆盖同标签全部历史、逐边闭合且满足硬约束的
共同外包。Run148 的三个 seed 正好说明“标签不决定精确 shape”，同时也已构造其凸包，故
不能将 shape difference 误写成不可行证明。

据此在第88章给出五项 simulation contract：初始化覆盖、可见历史一致性、共享输入/原语的
逐边 posterior 模拟、状态输入硬约束及终端闭合。它可通过归纳推出真实信息集始终被抽象集合
覆盖，但尚不包含 nominal plan shift 和终端名义控制，不能升级为 MPC 递归可行性。

本轮没有写数值求解器或新增测试，因为准入只到语义合同。定向复核 Run148 时，首次测试因
`READ_PAPERS.md` 新增本轮阅读记录导致五份历史 artifact 的源文件散列失配；直接执行核心
checker 仍通过。逐份重建五份 JSON，并删除该单一散列字段后与旧归档逐字段比较，数值、集合
和结论 5/5 完全一致。最终 `verification/` 207/207、`tests/` 39/39 通过；Python compileall、
全部结果 JSON 解析及 `git diff --check` 通过。

下一唯一问题：把 mode graph 扩成 `(mode,last_return)`，以 Run148 三 seed
为初始化像，先对固定 global residual 检查所有同索引历史的共同外包能否在 17 条物理边的
扩展图上闭合；若不能，在声明失败前给出硬约束/共享输入导致的精确反证。
