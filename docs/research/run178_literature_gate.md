# Run178 文献准入卡：terminal information-family 排重

| 工作 | 本轮实际阅读 | 已解决内容 | 与本轮严格边界 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, *Automatica* 183 (2026) 112661，DOI `10.1016/j.automatica.2025.112661`，[预印本](https://arxiv.org/pdf/2307.04146) | **全文定向重读 §§2、3.1--3.3，Propositions 1--3 及 extreme-set/downward-closure 构造** | 用集合值信息状态和 information ensemble 表示不确定信息；定义对任意紧集求交的闭合性，并给出最小表示/向下闭包接口。 | 不直接给出本仓库非线性 plant、packet automaton、固定复杂度 `Gamma` 或 actual-thrust-dependent residual 的可靠包含 oracle。 |
| Baras--Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, IEEE TAC 43(1), 1998，DOI `10.1109/9.654887` | 复核 Run177 对 §IV-A、Lemma 4、Theorems 9--11 的全文记录 | 完整历史诱导的信息状态和输出反馈动态规划已有一般理论。 | 不提供有限历史压缩的项目级模拟证书。 |
| Yang--Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 54(5), 2021 | 复核 Run153 对 §§4.1--4.4、Algorithm 1、Propositions 2--5 的全文记录 | 缺测 string/product 模式和中间安全义务已有直接基线。 | 连续有界噪声、非线性联合信息集和终端外包仍须另证。 |

## 差异、强基线与判定

最强方法基线是 Houska 的 information ensemble；最强仓库基线是第 88 章 `alpha/K/A` 五项
充分合同和 Run154 的 15 个 transient/45 个 recurrent 标签划分。Run177 所提 `T_0/T_1`
只是 tick-5 两条局部边的标签，不能替代 60-state 扩展图，也不是未解决的新定义。

**准入不通过：停止两族 terminal 模板及其 checker；准入通过：纠正重复并下推缺口。** 本轮
不作创新声明。最强同条件比较必须保留同一非线性 plant、测量时序、共享 observation-fiber
控制、扰动/执行器界、60-state 标签和全部循环边。一个单盒包含或 success 后 posterior 变小
不能证明 terminal closure。

推进价值在于避免沿错误对象继续实现。候选有限表示会被以下任一结果推翻：初始化 posterior
无法可靠覆盖；一条合法 miss/success 边违反 source-to-target 包含；压缩/凸化新增 fiber 无
共享可行控制；或硬约束/source domain 失败。只有先冻结 `Gamma` 和 sound inclusion oracle，
才可启动 45-state fixed point。
