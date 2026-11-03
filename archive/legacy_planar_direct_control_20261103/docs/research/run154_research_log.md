# Run154：历史完备共同外包算子审计

日期：2026-10-11；分支 `research/run154-history-envelope-operator-gate`。

本轮从 Run153 短检查点接续，只读取 60-state 语义、当前共享原语边映射及 vertical joint
predecessor 合同。定向精读 Houska 2026 §4.2--4.3、§6.3--6.5、Definitions 5--7、
Theorems 1/3 与证明，并复核 Baras--Patel 和 Yang--Ozay 的既有全文记录。

核心结果是修正共同外包的量词。对预先固定的因果策略，含真实 `(0,init)` 初始集的前向历史
包络算子是单调的，其 Kleene 迭代给出该策略下的最小 reachable envelope。若每层重新选择
不同策略，则层层可行不对应一张可执行控制器；一般也不存在未指定 policy class 的跨策略最小
闭包。对三 return seed 一次取凸包还会生成新的 observation fibers，必须在这些 fibers 上
重新证明共享输入、执行器约束和逐边闭合。

另一区分是 transient initialization 与 recurrent terminal：`init` 层15状态只负责首次
return 前安全，terminal family 可限制于45个循环状态；但必须覆盖所有首次 return image，
并在循环子图的51条边（42 miss、9 success）上闭合。本轮只形成这套合同，不实现数值迭代，
因为 policy class、固定复杂度外包 `Gamma` 和新增 fiber 的输入量词尚未冻结。

证据等级为项目特化的 fixed-policy monotone envelope contract，是已有 information-ensemble
理论的直接特化，不作创新声明。下一唯一问题：选定可审查的最小 policy/template class——优先
竖直 affine-in-`d` correction 加 exact lifted convex hull——并先证明凸化后新增 fibers 上的
输入可行与单步包含公式；通过后才实现从真实初始化开始的第一轮传播。

验证方面，文献表更新使五份历史 artifact 的来源哈希按设计变化；重建后删除该单一字段逐份
比较，数值、集合和结论 5/5 完全一致。最终 `verification/` 207/207、`tests/` 39/39、五项
相关模块定向 31/31 通过；Python compileall、全部结果 JSON 解析和 `git diff --check` 通过。
