# Run178：terminal information-family 排重与方向纠正

本轮从 Run177 检查点接续，先定向核对第 88、89 章、Run154--155 和当前 60-state 自动机语义。
排重发现：仓库已经给出比 `T_0/T_1` 更完整的有限信息抽象合同。15 个 `init` 标签覆盖首次
return 前瞬态，45 个 `(mode,last_return)` 循环标签才是 terminal family；其 51 条循环边必须
在同一因果策略下逐边闭合。Run177 把一次 tick-5 的 success/miss 局部标签误写成下一轮待定义
的完整终端对象，既重复第 88 章，又丢失历史标签，现予纠正。

本轮实际全文定向重读 Houska 的 §§2、3.1--3.3、Propositions 1--3。论文把 information set
及其 ensemble 作为对象，要求 ensemble 对与任意紧集求交闭合，并用 extreme sets/downward
closure 描述最小表示。它支持“终端是信息集之族而不是一个状态盒”的一般接口；但不能替代
本仓库非线性 plant、packet 标签和 actual-thrust-dependent residual 的可靠实例化。

本轮不写代码。准入卡已否决二元 terminal checker：可靠证书必须从全部合法 tick-0 posterior
开始，对每个 source label 的同一当前控制、全部真实状态/扰动/共享物理原语、packet outcome
及下一测量验证真实预测后求交的 `I(h+)` 被 target `K(A(...))` 包含，同时检查状态、输入和
余项 source domain。单个盒包含、有限成员抽样或 success posterior 收缩都不满足该量词。

失败/停止记录：原计划定义可计算 `T_0/T_1`；仓库排重后确认该对象只描述一对局部边，停止
推导和实现。当前证据等级为
`repository_dedup_plus_primary_full_text_contract_correction`，不是 RCI、递归可行性或创新证明。

论文级主线仍未闭合：缺真实非线性 plant 下的 fixed-complexity information-ensemble 表示、
sound containment oracle、45-state terminal fixed point、名义计划移位/终端控制、同预算强基线
及四旋翼闭环。下一唯一问题：冻结最小 `Gamma` 和可靠 source-to-target oracle，先在 60-state
扩展图的一条 miss 与一条 success 边证明逐边模拟；通过后才做 45-state terminal fixed point。
