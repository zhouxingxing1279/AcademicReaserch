# Run 137 文献准入卡：联合 ancillary RCI 前的名义推力预留

日期：2026-10-01。仓库起点为 Run 136 本地提交 `6e389c1`；远端 `main` 为 `1c49659`，远端 Run 136 快照 `3c3944f` 与本地 tree `8bc8945` 一致。本轮唯一问题是：能否把 15-mode estimator zonotope 直接接入实际推力相关联合 `(e,eta)` ancillary RCI。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读层级 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Lorenzetti, Pavone, *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, 2020, [arXiv:1911.07360](https://arxiv.org/abs/1911.07360) | **全文定向精读** Sections IV-B、IV-E--IV-G，式 (8)、(12)--(15)、Proposition 1 | 将 estimation error 与 estimate-to-nominal control error 组成增广状态，计算单个 RPI 并同时收紧 state/output 与 input。 | “联合误差图 + RPI + input tightening”已有直接 LTI 基线，不能作为创新。 |
| Köhler, Müller, Allgöwer, *Robust output feedback MPC using online estimation bounds*, 2021, [arXiv:2105.03427](https://arxiv.org/abs/2105.03427) | **全文定向重读** pp. 9--10，Assumption 7、Theorem 4 及 shift proof | 在线 estimation bound 与 tracking bound 共同进入 tightened constraints；terminal ingredients 封闭递归可行性。 | estimator bound 可直接消费，但仍必须先有合法的 control-error/constraint contract。 |
| Mulagaleti, Bemporad, *Learning Quasi-LPV Models and Robust Control Invariant Sets with Reduced Conservativeness*, 2025, [arXiv:2505.07287](https://arxiv.org/abs/2505.07287) | **全文定向重读** Section 2.2.2 Proposition 2、Section 3.1、Corollary 1 | configuration-constrained polytope、vertex control 与 self-scheduling qLPV RCI。 | 非轴对齐联合 RCI、vertex policy 和 scheduling correlation 已有方法学近邻。 |
| Wehbeh, Kerrigan, *State-Dependent Uncertainty Modeling in Robust Optimal Control Problems through GSIP*, 2025, [arXiv:2503.10389](https://arxiv.org/abs/2503.10389) | **全文定向重读** Sections II--IV、Theorems 1--2、Section V planar quadrotor | 用 GSIP 保留 state/control-dependent uncertainty，而非全局统一外包。 | 可表达 `T=bar T+delta T` 与 `d_z(T)` 的联合图；其有限时域求解不是 RCI/shift 证明。 |

## 2. 排重、严格差异与强基线

联合 `(e,eta)` RPI、在线 estimation bound、qLPV RCI 和 decision-dependent uncertainty 建模均已有直接近邻，故“建立 12 维联合图”创新准入不通过。当前仓库的严格差异只是一个更前置的 benchmark 合同问题：配置只给实际输入区间，没有单独名义输入收紧；若 nominal MPC 直接复用完整实际推力区间，则 endpoint constant plans 使垂向误差无法由合法 correction 抵消。

最强基线是 Lorenzetti--Pavone 的增广 RPI 加 input tightening；本轮必须先给它分配非空 correction authority，之后才有资格比较 configuration-constrained polytope、GSIP、CZ 或其他集合类。

## 3. 推进价值与推翻条件

该问题直接决定联合 RCI 求解是否语义可行。以下任一事实会推翻本轮候选结论：

- 配置已存在独立 nominal thrust bounds 且完全落入必要预留区间；
- 当前 vertical residual 不允许常值最坏符号序列；
- actual thrust 不受 `[4.905,14.715]` 硬约束；
- 推导没有保持同一 actual `T` 同时进入 correction limit 与 `d_z(T)`。

仓库核查表明前三项均不成立；精确验证器显式保持最后一项。

## 4. 准入判断

**作为合同纠正与精确必要条件：通过。作为联合 RCI 算法或论文创新：不通过。**

因此允许实现一个 exact-rational verifier，证明 full-range nominal candidate 不可能支持非空紧致 vertical ancillary RCI，并给出必要 nominal thrust reserve。禁止继续运行高维 RCI 优化器，直到配置冻结独立 nominal input set；优化器在错误输入分配上的 infeasible 只会重复证明合同错误。

## 5. 停止条件

得到端点漂移 witness 和非空必要区间后立即停止。本轮不搜索 K、不构造 12 维 polytope/CZ，也不进入 terminal/shift；下一轮先把 nominal thrust/torque allocation 写入配置，再在 hover 附近做最小的 mode-indexed augmented-error RCI existence baseline。
