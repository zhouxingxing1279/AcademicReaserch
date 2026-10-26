# Run181 文献准入卡：mode-4 未知 success/miss 分叉的联合法向证书

日期：2026-10-26。仓库续接点为远端
`research/run180-mode0-miss-lifted-cell@9f8d46a`；本轮不以落后的 `main` 为研究基线。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 与本轮严格差异 |
|---|---|---|---|
| Hempel--Kominek--Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011，DOI `10.1109/CDC.2011.6160901`，[全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **重新下载全文并精读 §III-A--C、Definition 2、Theorem 1、式(3)--(14)与 Algorithm 1** | 对每个 noisy output 只选一次输入，并对全部相容隐藏状态、扰动及 LPV 顶点逐 facet 保证不变；输入可在线求解或显式写成 PWA。 | 本轮 successor label 在当前输入后才揭示，且两支共享 actual-thrust-dependent residual；Hempel 的 scheduling 在控制时可知、过程扰动集固定。 |
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026) 112661 | **复核仓库已保存的 §4.2、§4.4、§6.1--6.7 全文阅读记录；本轮未重新取得正文** | information ensemble、固定配置多面体和 extreme-information-set control 的一般框架。 | 不给出本仓库 15-mode 四旋翼 residual graph 的数值 cell 或逐边证书。 |
| Robbins et al., *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis*, 2026 | **只核对 IEEE 正式题名/摘要与作者出版目录；全文未取得** | 摘要明确以 CZ reachability 在线计算 MPC tightening。 | 摘要不足以核查其定理、复杂度和 terminal/shift 义务；本轮不据此作首次性或优越性声明。 |
| Lucia--Ernesto--Castelan, *Set-theoretic output feedback control: a bilinear programming approach*, Automatica 2023，DOI `10.1016/j.automatica.2023.110861` | **沿用 Run141 已核查的全文 §2--5、Definitions 2--3、Propositions 1--2、Algorithm 1** | 静态输出反馈与嵌套 one-step controllable sets保证约束和有限步 UUB；rank-deficient output 不能读取隐藏状态。 | 当前只验证一个冻结正体积 cell，不综合反馈增益或完整嵌套集合族。 |

## 差异、最强基线与证明义务

最强同条件基线是 Hempel 的 observation-fiber robust polyhedral condition；Run144 已给出
mode 4/9/14 的正体积内前驱存在性，但没有把 mode 4 的两条未知后继展开成 Run180 风格的
联合 `(eta,e)` 全部 target-normal 行，也没有在同一证书中显式记录 success measurement noise
与两支共用的 actual-thrust residual。

本轮只允许回答以下实现问题：冻结 source 为 Run136 mode-4 `eta` 精确投影乘
`|d_p|<=1/5, |d_v|<=1/4`、`e=eta+d`，冻结同一仿射 fiber policy `deltaT=0`，分别对
`4->5 miss` 与 `4->0 success` 的 estimator facets 和 tracking box normals 求 exact-rational
支持。两支必须先共享同一控制；每支内部的 `eta` 与 `e` 必须共享同一物理 residual realization；
success 还必须显式传播同一测量噪声 realization。必须同时核查 source domain、输入盒和图边。

任一 target normal 超界、需要按隐藏 `eta` 或未来 packet label 选输入、把 estimator error
误当未来 plant disturbance，或 success 中测量创新没有在真实 tracking error 中抵消，都会推翻
这个 cell。通过也只得到双边一步证书，不得到 45-state terminal family、RCI 或递归可行性。

## 准入判断

**作为证书完备性与回归门槛通过；作为新算法/创新命题不通过。** 共享 observation-fiber 输入和
逐 facet 验证已被 Hempel 覆盖；本轮价值是把第一个未知 packet 分叉可靠接到真实配置并暴露
是否存在某一分支的精确阻塞。若通过，下一步才有资格把这种 cell 扩展到有限覆盖并处理 cell
重叠处的策略一致性；若失败，应停止扩展并保留最小反例。
