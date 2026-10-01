# Run 138 文献准入卡：显式 ancillary 输入预算只作为 existence probe

日期：2026-10-02。仓库起点为本地 Run 137 `e3ae26d`；远端 Run 137 `310a2a0` 与本地 tree `ee0fd07` 一致。唯一问题是：如何冻结不隐藏执行器权限、又不把任意固定切分误称为最终 Tube MPC 收紧的输入合同。

## 最近邻原文

| 文献 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Lorenzetti, Pavone, *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, 2020, [arXiv:1911.07360](https://arxiv.org/abs/1911.07360) | **全文定向重读** Sections IV-A--B、IV-E--F，式 (8)、(12)--(13)、Proposition 1 | 用 `u=bar u+K(hat x-bar x)`；coupled-error RPI 的 correction 投影通过 Pontryagin difference 形成 nominal input set，并证明 robust constraint satisfaction。 | 最强 LTI 基线。最终 nominal input tightening 必须来自认证 correction support；固定输入切分只能是前置 benchmark。 |
| Köhler, Müller, Allgöwer, *Robust output feedback MPC using online estimation bounds*, 2021, [arXiv:2105.03427](https://arxiv.org/abs/2105.03427) | **全文源码定向重读** “Homothetic tube-based MPC”“Simplified constraint tightening”、两组 terminal assumptions/theorems及 shift proof | 在联合 state/input constraints 中对反馈律和 estimation/tracking bounds 统一收紧；terminal conditions封闭递归可行性。 | 非线性 feedback-dependent input 应整体核查，不能把静态预算等同 RCI 或 terminal 证书。 |

## 差异、比较基线与推翻条件

本轮没有新算法主张。严格差异只是把当前实际执行器盒与 `d_z(T)` 写成一个 exact-rational、可执行的预算合同，防止后续 RCI solver 隐式使用 full nominal range 或未声明 correction authority。最强比较基线仍是 Lorenzetti--Pavone coupled RPI 的 input projection；Köhler的 joint nonlinear constraint 是语义更强的对照。

以下任一结果推翻“可直接作为最终分配”：nominal torque 无内点、thrust boundary authority 无严格余量、Minkowski 和越过 actual box，或分配依赖非因果的同拍 residual cancellation。当前候选前两项已经发生，因此只能标为 existence probe。

## 准入结论

**通过 exact input-budget prerequisite；不通过最终 nominal allocation 与算法创新准入。** 允许新增配置字段、精确验证器和回归测试；禁止把边界 balance 升级为 causal policy、RCI 或可机动 MPC 可行性，也不在本轮启动高维 RCI 求解器。下一步只在该最有利预算下回答 augmented RCI existence；若存在，再由实际 correction support 反推 nominal 域。
