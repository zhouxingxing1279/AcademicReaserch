# Run153：`last_return` 自动机语义与初始化审计

日期：2026-10-11；分支 `research/run153-last-return-automaton-gate`。

本轮只从 Run152 短检查点接续，定向读取配置中的 15-mode/17-edge 图、初始化合同和 Run148
三 return seed。全文精读 Yang--Ozay 2021 §4.1--4.4、Algorithm 1、Propositions 2--5，
核对 string automaton、因果输入串和产品系统不变性之间的逻辑边界。

核心纠正：`last_return={5,10,15}` 不足以描述真实初始化。首次 success 前没有上一周期，
必须加入 `init` 哨兵。把原图提升为 `(mode,last_return)` 后共有 60 状态、68 边，从
`(0,init)` 出发全部可达：15 个首次-return前瞬态状态和 45 个循环状态。miss 保持记忆，
三种 success 把记忆写为 5/10/15。更新只读已实现的 packet outcome，故离散层是确定且因果的。

这并未证明有限信息抽象。Run148 三 seed 是固定零修正下从真实初始化出发的首次 return 像，
只能作为三个循环标签的必要样本，不能取代 `(0,init)` 初始集，也不能覆盖同标签的多周期历史。
Yang--Ozay 的有限自动机编码缺测语言和决策时刻；其安全结论仍依赖产品系统对所有允许 return
string、扰动及中间状态闭合。因此本轮文献准入仅通过语义修正，不准入共同外包求解器或 RCI
声明，未新增代码。

验证采用配置直接枚举图提升与 BFS 可达性；这只是有限图事实。下一唯一问题：正式定义每个
`(mode,last_return)` 标签对应的全部历史语言，并在固定 global residual 下写出从
`(0,init)` 初始化的 monotone common-outer-cover 算子；只有该算子和硬约束语义确定后才可
实现一次迭代，不能从三个 post-success seed 直接启动循环 fixed point。

回归时 `READ_PAPERS.md` 的新增记录使五份历史 artifact 的来源哈希按设计失配；重建后删除
该单一哈希字段逐份比较，数值、集合和结论 5/5 完全一致，仅更新绑定哈希。最终
`verification/` 207/207、`tests/` 39/39 通过，五项相关模块定向 31/31 通过；Python
compileall、全部结果 JSON 解析和 `git diff --check` 通过。
