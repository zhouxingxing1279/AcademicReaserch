# Run186 文献准入卡：六 facet configuration 与测量支持映射

日期：2026-10-27。基线为远端 Run185 `302600a5`。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, Automatica 163 (2024), arXiv:2208.12554 | **精读 §3.4--3.5、Definition 6、Lemma 1、Theorems 1--2、式(4)--(8)，并重读 Corollary 4、式(15)--(18)** | configuration domain 是多面锥；在固定 vertex configuration 内，facet offsets 到全部 vertices 有线性映射，vertex controls 给出一步鲁棒传播的充要条件。 | 六法向的 `Y/G/Lambda` 及逐 vertex 支持传播均是现有方法的直接实例，不得称为创新。 |
| Houska, *Intrinsic Separation Principles*, Automatica (2026), arXiv:2307.04146 | **精读 §6.2--6.5、式(25)--(27)及 Theorem 3 的构造和证明开头** | 用 `Y/G/Lambda` 表示极端信息集，用 `Z/H/Omega` 表示 ensemble；measurement meta-update 与 extreme-set controls 已形成完整框架。 | 本轮单个形状的测量支持映射不是 invariant information ensemble；后续必须另证 `Z/H/Omega`、所有 packet edges 与因果控制权限。 |
| Badalamenti--Mulagaleti--Villanueva--Houska--Bemporad, *Efficient Configuration-Constrained Tube MPC via Variables Restriction and Template Selection*, CDC 2025, DOI 10.1109/CDC57313.2025.11312697, arXiv:2505.14440 | **精读 §3.1--3.2、§4.1、Problem (19)、Algorithm 1、Proposition 3 与 §5 的 10-state quadrotor说明** | 已系统给出逐次增加 facet 的 template refinement、非增性能指标和复杂度折中，并在四旋翼模型上验证。 | “给 box 手工增加一对斜法向”已被更强的一般算法覆盖；本轮只准入可审计基线接口，不作 template-design 首次性声明。 |
| Robbins--Glunt--Thompson--Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*, 2026 | **仅核对 IEEE 正式题录与摘要；未取得正文** | 摘要层面覆盖 CZ reachability 驱动的在线收紧。 | 不据摘要判断定理覆盖或首次性；本轮不作在线 tightening 声明。 |

## 严格差异、最强基线与证伪条件

Run185 的固定 `(p,q)` parallelogram 丢弃了显式 `+/-v` facets，因此 success 位置条带只能重置 `p` offset、不能收缩 `q` offset。本轮保留

```math
Yx\le y,\qquad Y=\begin{bmatrix}
1&0\\0&1\\-1&\kappa\\-1&0\\0&-1\\1&-\kappa
\end{bmatrix},\qquad \kappa=\frac1{10},
```

并只问两个已有框架内的接口问题：六边形的完整 configuration/vertex maps 是否精确；位置 strip 求交后，active velocity facets 是否会改变紧的 `q` 支持。最强同条件比较是 Run185 的 parallelogram outer recurrence。

若紧支持仍严格保留 predicted `q` offset，或者所谓收缩依赖采样而非精确 LP/support 恒等式，则停止该六-facet 支线。若能严格收缩，也只通过“值得构造完整 graph/meta LP”的准入，不等价于图不变、硬约束、终端或递归可行性。

## 准入判断

**通过“六-facet configuration 与 measurement-support 基线接口”；不通过“增加斜 facet 是创新”“已经闭合 information ensemble”与“已经降低 MPC 保守性”。**
