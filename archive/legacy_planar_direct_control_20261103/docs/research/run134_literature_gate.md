# Run 134 文献准入卡：控制相关推力下的 ancillary 合同

日期：2026-09-29。仓库起点为本地 Run 133 提交 `d6f12e6`；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。本轮原问题是选择保持 paired `(A(T),W(T))` 的非轴对齐 RPI/RCI 证书。准入前先核查：实际推力在允许 ancillary correction 后究竟是不是外生 scheduling variable。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读层级 | 已解决内容 | 对本轮候选的约束 |
|---|---|---|---|
| Mulagaleti, Bemporad, *Learning Quasi-LPV Models and Robust Control Invariant Sets with Reduced Conservativeness*, 2025, DOI [10.1109/LCSYS.2025.3569637](https://doi.org/10.1109/LCSYS.2025.3569637), [arXiv:2505.07287](https://arxiv.org/abs/2505.07287) | **全文精读** Introduction、Section 2.1、Propositions 1--2、Section 3.1、Proposition 3 与 Corollary 1 | 对 self-scheduling qLPV 模型构造 configuration-constrained polytopic RCI；利用候选 RCI 内 scheduling 的 state dependence 缩小 multiplicative uncertainty hull；支持 vertex controls。 | 非轴对齐 polytope、configuration constraints、vertex control 和利用 self-scheduling 相关性均已有直接近邻，不能作为创新。论文只提示可扩到 `p(x,u)`，未实例化本项目的间歇 SMF estimation error 与推力余项联合图。 |
| Wehbeh, Kerrigan, *State-Dependent Uncertainty Modeling in Robust Optimal Control Problems through Generalized Semi-Infinite Programming*, 2025, [arXiv:2503.10389](https://arxiv.org/abs/2503.10389) | **全文精读** Sections II、V，含 planar quadrotor 案例 | 以 GSIP 表示 state/control-dependent uncertainty；四旋翼案例保留 reference thrust 与 motor uncertainty 的耦合，比较 uniform 或不保持包含的近似。 | 支持“不丢失控制相关 uncertainty graph”的建模原则；但对象是有限时域 robust optimal control，不是不变集、间歇输出反馈或递归可行性证书。 |
| Wehbeh, Kerrigan, Scaccia, *Generalized Semi-Infinite Programming for Robust Optimal Control with Decision-Dependent Uncertainty*, 2026, [arXiv:2609.01538v1](https://arxiv.org/abs/2609.01538) | **全文精读** Introduction、Sections II--IV、Theorems 1--3、Algorithm 1、Sections V--VI | 将适当正则的 GSIP 转为 existence-constrained SIP，以 adaptive discretization 和 worst-case separation oracle求解；把状态轨迹并入不确定变量处理 state-dependent uncertainty。 | 是式 (71.3) 的强语义/求解基线，但论文保证要求有限子问题全局求解；实验使用多起点局部优化。它没有给出本项目的 RCI 或 old-plan shift theorem。 |
| Hanema, Lazar, Tóth, *Heterogeneously Parameterized Tube Model Predictive Control for LPV Systems*, 2020, [arXiv:1910.08449](https://arxiv.org/abs/1910.08449) | **全文定向重读** Introduction、LPV problem setting | 对当前可测、未来未知且外生的 scheduling signal 构造 heterogeneously parameterized tubes 与递归可行 MPC。 | 强 LPV tube baseline；其外生 scheduling 假设不覆盖由 `delta T=kappa(e-eta,...)` 决定的实际推力。 |

全文门槛由四篇正文满足。2026 文献版本日期为 2026-09-01；本轮没有凭摘要推断首次性。

## 2. 与近邻严格不同的证明义务

本轮不是再提出一个 generic qLPV/GSIP/RCI 方法。需要解决的是特定六状态 output-feedback 合同：

1. 实际推力 `T=bar T+delta T` 同时进入横向误差矩阵、垂向控制通道和 `d_x(T),d_z(T)`；
2. `delta u` 由 `hat x-z=e-eta` 产生，必须量化 mode-dependent estimator error；
3. 横向误差还有 `-delta T z_phi`，因此不能只在 e-space 里声称闭合；
4. 证书必须同时给出硬输入分配、15-mode 边不变性，以及之后可供 nominal terminal 层使用的 tightening。

Mulagaleti--Bemporad 的 polytopic RCI 与 Wehbeh 系列的 GSIP 都可作为工具，但将其与 SMF、MPC 拼接本身不是贡献。最强同条件 baseline 是：在相同模型、sensor/dropout language、residual graph 与 input budget 下，对联合图使用 configuration-constrained polytope/vertex control 或 GSIP separation，并保存独立可查证的最坏点证书。

## 3. 推进价值与推翻条件

冻结合同直接决定能否构造可靠 `S_c^j`、定义 state/input tightening，并继续 common nominal terminal synthesis。以下任一结果会推翻候选路线：

- 不允许 `delta T` 时仍声称存在紧致全六状态 RPI；命题 71.1 已严格否定；
- 把 actual `T` 当独立外生信号，忽略 `T=bar T+delta T`；
- 缺少 `E_eta^j` 却把 state posterior 或 measurement noise 直接当未来 process disturbance；
- 只靠局部 NLP success、有限采样成员检查或 Monte Carlo 声称 robust invariance；
- 安全外包后的 tube 使 tightened state/input domain 为空。

## 4. 准入结论

**直接实现 exogenous paired-endpoint RPI：不通过。六状态控制相关合同审计与 torque-only 不可能性证明：通过。**

原因是旧问题的量词仍然错误：允许 thrust correction 后 scheduling 是 controller-dependent；不允许 thrust correction又被 vertical residual 精确否定。此时选择 ellipsoid、polytope 或 CZ 形状并求解，只会得到另一份错误模型的可行/不可行记录。

本轮不写控制代码。式 (71.1) 与命题 71.1 是解析结果，不需要采样验证；在 estimator-error family 尚未冻结时，编写 RCI 求解器无法产生可解释结论。

## 5. 下一轮唯一问题

从现有 rolling SMF 与 15-mode bounded-dropout automaton 构造或否定 time-uniform、mode-indexed estimator-error family `E_eta^j`，明确 prediction/intersection/reduction 及 actual-input 时序，并逐边给出可靠包含证书。完成后才把它代入式 (71.3) 选择非轴对齐 ancillary certificate。
