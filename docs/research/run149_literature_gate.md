# Run 149 文献准入卡：控制平移与推力相关余项的形状分离

日期：2026-10-03。仓库起点为本地 Run148 修正提交 `0f65ef3`；远端 `main=1c49659`。
本轮不继续把零中心 `C0` 当作一般必要 target，而先核查控制输入到底只平移信息集，还是
同时改变其形状。

## 本轮问题

竖直合同使用 `eta=x-hat x`、`e=x-z`、`d=e-eta`，控制器选择修正推力 `deltaT`，实际
推力 `T=barT+deltaT` 又决定物理余项半宽

`r_z(T)=[1043/500+(81/800)T]rho_z`。

需区分两种语义：

1. 用 Run136 在完整执行器上界认证的固定 global residual envelope 时，`deltaT` 是否只
   改变联合信息集的中心，而不改变生成元形状；
2. 保留实际推力条件余项时，同一归一化原语 `rho_z` 的像是否随 `deltaT` 改变，从而形成
   decision-dependent uncertainty，阻断直接套用固定扰动集的 intrinsic-separation 结论。

## 最近邻原始文献与实际阅读

| 工作 | 本轮实际阅读 | 已解决内容 | 对本轮的严格边界 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, 2023, arXiv:2307.04146 | **重读全文 Sections 3.5、4.2--4.3、5.3--5.4，Definition 1、Theorem 1及证明、式(18)--(20)，并复核 Sections 6.5--6.7** | 对固定线性系统、固定加性扰动集 `W`，不同 tight information tubes 的 intrinsic equivalence class 与控制策略无关；控制作用可写成依赖信息集的平移。极端信息多面体用连续凸权重插值控制。 | 本项目若使用固定 Run136 envelope，可把零策略 image 解释为 intrinsic shape 的一个中心化代表；但含 `W(T)` 的 scheduled residual 不满足“固定 `W`”接口，不能直接引用 Theorem 1 得到 policy-independent shape。 |
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901` | **重读全文 Section III-A--C、Definition 2、Theorem 1、式(3)--(12)** | 对每个 noisy output 与当前已知外生 scheduling，全部相容隐藏状态和扰动共享一个输入；给定候选 polytope 的验证和 PWA 输入计算已有。 | 当前 `deltaT` 既是控制又改变余项宽度，不是论文中先于控制给定的外生 scheduling。本文支持 fiber 量词，但不支持把 `T` 当作独立可选顶点。 |
| Wehbeh, Kerrigan, Scaccia, *Generalized Semi-Infinite Programming for Robust Optimal Control with Decision-Dependent Uncertainty*, 2026, arXiv:2609.01538v1 | **重读全文 Introduction、Section II Assumption 1、Lemma 1、Theorem 1/Remark 1、Section IV Assumption 2 与 Theorem 3** | 当 admissible uncertainty set 依赖 control/state decision 时，鲁棒最坏情形是 GSIP；给出在正则条件下转成 existence-constrained SIP 及 adaptive discretization 的框架。 | `r_z(T)` 是最小的 control-dependent uncertainty graph 实例。该文没有给出间歇 output-feedback invariant ensemble、terminal set 或 recursive-feasibility theorem，因此本轮只用它判定问题类别，不实现 GSIP 求解器。 |

## 差异、证明义务与最强基线

本轮只准入当前冻结竖直模型的一步 exact-rational 接口证书：

- 对 miss/success 两类边逐式证明 `e+=eta++d+`；同一个物理余项只能实现一次；
- 固定绝对余项 realization 时，两个 correction 产生的差只能是已知中心平移；
- 固定归一化原语 `rho_z` 且使用 scheduled residual 时，精确量化形状列随 `deltaT` 的变化；
- 证明 Run136 global envelope 在完整实际推力区间上包含所有 scheduled residual，并明确其
  代价是放弃这部分 tightening；
- 不把 Houska 的一般定理、Hempel 的 fiber 量词或 Wehbeh 的 GSIP 转换宣称为创新。

最强固定扰动基线是 Houska 的 translation/intrinsic-shape 分离；最强 decision-dependent
建模基线是 Wehbeh 等 2026。若 exact map 显示即使用 global envelope，`deltaT` 仍改变生成元
形状，固定模板路线被推翻；若 scheduled residual 在完整 correction 区间实际上宽度不变，
则 decision-dependent 分支没有意义，也应停止。

## 课题作用与准入判断

该问题直接决定后续 predecessor 的变量：应优化“固定 shape + 可见中心平移”，还是必须
把控制与扰动图联合放入 GSIP/robust containment。它影响可行性、保守性和计算预算，而非
只增加局部法向。

**准入通过：只实现 control-translation / residual-shape split 的精确接口证书；不准入
RCI、一般 output-feedback synthesis、算法创新或 MPC 递归可行性声明。**
