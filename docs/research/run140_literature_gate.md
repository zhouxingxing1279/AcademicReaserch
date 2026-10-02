# Run 140 文献准入卡：hover 邻域 partial-information ancillary 合同

日期：2026-10-02。仓库起点为 Run 139 本地提交 `8116839`；远端同内容提交
`50f3da1`，两者 tree 均为 `d2e010f1731ded8feda8c258cbe2a45eed5cea10`。
远端 `main` 为 `1c49659`。

## 1. 本轮问题与最近邻

本轮不求 augmented RCI，而是把 Run 139 的六项缺口实例化为一个可审查的
hover-neighborhood existence-probe：控制只依赖当前可见的
`(mode,d=hat x-z,z,bar u)`，在未知下一 packet outcome 和共享扰动原语实现之前选定；
15 个年龄模式、17 条边、实际推力、物理余项、测量噪声及初始化切片均须显式冻结。

| 文献 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901`, [全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **全文精读 Sections II--III，Definition 1--2、Theorem 1、式 (3)--(11)** | 对每个噪声输出及已知 LPV scheduling，选择一个只依赖输出/调度的输入，并对与该输出一致的全部状态、过程扰动和测量噪声保证多面体不变；给出验证及在线/显式 PWA 控制计算。 | 当前 policy 也必须在 observation fiber 上统一，不能读取隐藏 `eta`。其 `theta` 当前可测且外生，而本项目实际推力由 correction 决定、下一 packet outcome 未知，所以不能直接套用其 LPV 顶点定理。 |
| Baras, Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, IEEE TAC 43(1), 1998, [作者全文](https://terpconnect.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf) | **全文定向精读 Section IV-A--B，Lemma 4、Theorems 9--11、15--16** | 用 observation history 诱导的信息状态把 output-feedback robust game 转为 information-state feedback game，并给出有限/无限时动态规划必要与充分条件。 | 精确 sufficient statistic 通常是集合/函数值信息状态，而不只是点估计偏差 `d`。本轮有限 policy class 只能是保守 existence probe，不能声称等价于一般 output-feedback controller。 |
| Yang, Ozay, *Efficient Safety Control Synthesis with Imperfect State Information*, CDC 2020, [作者全文链接](https://web.eecs.umich.edu/~necmiye/pubs/YangO_cdc20.pdf) | **仅核查摘要；全文抽取失败** | 以 estimated-state dynamics 上的 perfect-information safety game 给出两个保守近似，并区分只知初始测量与精确初态两类条件。 | 支持“有限估计状态近似一般 partial-information game 时须标注保守性”；未用其定理作本轮证明。 |
| Yang, Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, ADHS 2021, DOI `10.1016/j.ifacol.2021.08.481`, [作者全文链接](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) | **核查摘要与问题陈述；正文抽取失败** | 用 automaton 描述 missing-measurement language，并利用 causality 构造 product system，把 partial-information safety game 化为 full-information game。 | 15-mode bounded-dropout automaton 与其问题结构相近；模式扩张及因果 policy 不是创新。其离散/有限安全综合没有直接给出本项目连续六状态、控制相关余项的证书。 |
| Ning, *Data-Driven Synthesis of Robust Positively Invariant Sets: From State Feedback to Output Feedback*, 2026, [arXiv:2608.23412](https://arxiv.org/abs/2608.23412) | **仅核查摘要及 problem formulation** | 对 LTI observer-based output feedback，从 noisy offline data 综合 observer/feedback gain 与 ellipsoidal RPI。 | 是截至本轮检索日的新增近邻，但仍先冻结 observer-based closed loop；不处理当前 observation-fiber controlled RCI、packet automaton 与 feedback-dependent residual graph。 |

检索截至 2026-10-02，关键词覆盖 output-feedback controlled invariance、imperfect
state information、missing measurements、information-state robust control 及 2024--2026
新增工作。没有用摘要作“未被覆盖”的首次性证明。

## 2. 严格差异、直接推论与最强基线

Hempel 等 Definition 2 已给出本轮核心量词：对同一输出一致的全部隐藏状态，输入必须相同。
Baras--Patel 又表明一般精确信息结构应保留 observation history 诱导的信息状态。因此：

1. `forall observation -> exists one input -> forall hidden eta/disturbance/edge` 是既有
   output-feedback invariance 原理的直接特化，不是创新；
2. 15-mode automaton 是已知 missing-data product construction 的实例化，也不是创新；
3. 本轮新增价值仅是把仓库的物理/估计模型接成可执行合同：同一实际推力
   `T=bar T+delta T` 决定跟踪动力学与余项半宽；成功测量时，同一物理余项和下一测量
   噪声在 `eta+` 与 `d+` 之间分配，禁止独立笛卡尔复制；
4. 最强同条件基线不是 full-state vertex RCI，而是 Hempel 风格的 observation-fiber
   output-feedback CI；一般信息状态动态规划是更强但计算不可比的概念基线。

## 3. 推翻条件、课题作用与停止点

若所冻结公式不能逐式恢复 `e+=eta++d+`，若同一 success edge 中的物理余项/测量噪声
被重复为独立原语，若 policy 能读取 `eta` 或下一 packet outcome，或若初始化不包含
`S_0 x {d=0}`，合同即失败。若 nominal hover box、Run 136 的 `eta` 投影与候选 `d`
不能共同保证 `x=z+eta+d` 留在物理源域，则后续 RCI 应报告不可行，不能缩小已冻结噪声。

该合同推进的是“估计证书 -> 控制层可执行问题”的接口；它本身不提供 RCI、输入内点、
terminal set、recursive feasibility、性能或创新贡献。合同 ready 后的第一求解基线应是
mode-indexed observation-piecewise-affine policy；若失败，只能否定该 policy/certificate class。

## 4. 准入结论

**通过合同实例化与精确代数验证；不通过 RCI 综合和创新声明。**

允许修改配置、contract gate 和 exact verifier，使真实配置从 `blocked` 变为 `ready`，并
逐边验证模式/量词/共享原语标识及 `e+=eta+d` 的分裂恒等式。禁止在本轮报告高维集合
可行或不可行。
