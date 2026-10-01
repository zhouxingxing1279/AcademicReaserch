# Run 139 文献准入卡：增广 RCI 的量词与信息合同

日期：2026-10-02。起点为 Run 138 本地提交 `595523e`；其 tree 与远端
`research/run138-ancillary-allocation-probe` 的 tree
`10b21cdd6c7a51c0486ee22a9513d9c34576dbe5` 一致。远端 `main` 仍为
`1c49659`。

## 1. 本轮问题与最近邻

本轮问题不是提出新的不变集算法，而是判断仓库所写的“构造或严格否定 15-mode
augmented `(eta,d=hat x-z)` RCI”是否已经是一个可执行、可证伪的数学问题。

| 文献 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Lorenzetti, Pavone, *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, 2020, [arXiv:1911.07360](https://arxiv.org/abs/1911.07360) | **全文定向重读** Sections IV-B、IV-E--G，式 (8)、(12)--(15)、Propositions 1--2 | 先固定可实现反馈 `u=bar u+K(hat x-bar x)`，再令 `xi=(x-hat x,hat x-bar x)` 成为自主受扰系统；对该固定闭环求 RPI，并由 `[H H]R`、`[0 K]R` 收紧状态和输入。 | “augmented RPI”必须先给定反馈及其可用信息；RPI 不是在每个状态重新自由选择控制的 RCI。
| Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for LPV Systems*, 2023, [arXiv:2309.06998](https://arxiv.org/abs/2309.06998) | **全文定向精读** Section III-C、Lemma 3、Problem 1、Section IV | RCI 的量词为对状态/调度存在 admissible control，使后继对全部扰动/模型仍在集合；vertex controls 及其凸插值显式定义 invariance-inducing policy。 | 若本轮选择 controlled-invariant 语义，必须冻结 `forall state -> exists causal input -> forall disturbance`，并给出 controller parameterization；不能把 solver 内部逐场景输入当作 causal policy。
| Wehbeh, Kerrigan, *State-Dependent Uncertainty Modeling in Robust Optimal Control Problems through Generalized Semi-Infinite Programming*, 2025, [arXiv:2503.10389](https://arxiv.org/abs/2503.10389) | **全文定向精读** Sections II--IV、Theorems 1--2 | 将依赖状态/控制的 uncertainty set 写成 generalized SIP，并强调 robust constraint 只对与同一 decision/trajectory 相容的 uncertainty 量化。 | 当前 `T=bar T+delta T` 同时决定 dynamics 与 `d_x(T),d_z(T)`；必须保留同一实际 `T` 与共享 residual primitive，不能把 `A(T)`、`W(T)` 独立笛卡尔化。

## 2. 严格差异与最强基线

Run 138 只冻结了 actual/nominal/correction input boxes。当前配置仍有
`mpc.K=null`、`mpc.L_by_mode=null`、`mpc.terminal_certificate=null`，也没有：

1. 选择固定反馈 RPI 还是 controlled RCI 的量词；
2. `delta u` 的因果信息集合和 policy class；
3. 用于 `delta T z_phi` 的 nominal state/reference domain；
4. 逐条 dropout edge 的 mode transition contract；
5. 同一 residual/measurement primitive 在 `eta` 与 `d` 更新中的共享映射；
6. 非空性的初始化要求，例如 mode 0 必须包含 `(eta,d)=(S_0,0)`。

因此当前“augmented RCI”不是单一数学命题。Lorenzetti--Pavone 的固定反馈
coupled-error RPI 是最强、最直接的线性基线；Mejari--Mulagaleti--Bemporad 的
vertex-control RCI 是更宽的 controlled-invariant 基线。两者的可行或不可行不能相互替代。

## 3. 推翻条件与课题价值

若仓库已经在其他当前原始文件中冻结了上述六项，或能从 Run 138 配置唯一推出它们，
则本轮“问题未实例化”的判断被推翻。实际核查没有发现这些字段；尤其不能从输入盒唯一
推出 policy、nominal `z_phi` 域或 disturbance coupling。

该纠正直接阻止两类错误：把某个固定 `K` 失败升级为 arbitrary-policy 不存在；或让每个
disturbance realization 选择不同控制，从而把非因果可行误报为 RCI。它推进的是证据链的
控制层接口，而不是新的不变集算法或性能贡献。

## 4. 准入结论

**通过“可执行合同门槛与回归检查”准入；不通过高维 RCI 求解和创新声明准入。**

本轮允许新增一个只读 contract verifier：它必须在当前配置上明确返回 `blocked`，并列出
缺失的量词、policy、nominal-domain、mode-edge、shared-primitive 与 initialization 合同；
完整 fixture 应返回 `ready`。在这些条件冻结前，不运行局部 NLP/SDP/GSIP，也不把任何
solver infeasible 解释为不变集不存在。

