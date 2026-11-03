# Run185 文献准入卡：单对耦合法向的形状闭合门槛

日期：2026-10-26。续接远端 Run184 `5f2e1415` 的等价本地树。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, 2022，[全文](https://arxiv.org/abs/2208.12554) | **重新精读 §3.4--3.5 的 Theorems 1--2、式(15)--(21)，以及 §4.1--4.2 的 Corollary 4、式(25)--(27)、Remark 5** | 固定法向模板、configuration cone、线性 vertex maps、vertex controls 和可行性 LP 已完整给出。 | “给 box 增加一对斜法向”与相应线性传播不是创新；完整实现必须检查 configuration domain 与所有顶点。 |
| Houska, *Intrinsic Separation Principles*, 2023/Automatica 2026，[全文](https://arxiv.org/abs/2307.04146) | **针对 Run184 新问题重读 §6.3--6.7、式(25)--(30)与 Theorem 3** | 固定复杂度 information ensemble、measurement meta-update、extreme information sets 与 invariant ensemble LP 已是强基线。 | 本轮半径递推最多是完整 `Y/G/Lambda/Z/H/Omega` LP 的准入门槛，不是 information-ensemble 定理。 |
| Scott--Raimondo--Marseglia--Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69 (2016), DOI 10.1016/j.automatica.2016.02.036，[作者版全文](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) | **核对摘要、§1 的问题定位；本轮未重新精读全部降阶算法** | CZ 可精确表示线性映射、Minkowski 和、交集与投影；固定复杂度时需要外包/降阶。 | 若多面体完整 LP 失败，CZ 是下一强基线；不能把“保留相关性”宣称为首次提出。 |
| Robbins--Glunt--Thompson--Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*, 2026 | **仅取得 IEEE/PAC Lab 正式题录与摘要，未取得可核查正文** | 摘要层面是 CZ reachability 驱动的在线 MPC tightening。 | 不据摘要判断定理覆盖或首次性；本轮不作在线 tightening 创新声明。 |

## 本轮问题、差异与最强比较

Run184 的 box 证书使用独立位置/速度半径；position-only measurement 不改变速度半径，故每条边至少增加 `w_v`，沿环得到严格 Farkas 矛盾。本轮只问：在完全相同的 `A/W/V`、15-mode/17-edge 时序下，加入一对

```math
\pm q,\qquad q=p-\kappa v,\qquad \kappa=5h=\frac{1}{10},
```

是否已足以让**形状半径**形成周期闭合。最强比较是 Run184 的同条件 axis-aligned box 半径环。控制、中心区间、meta-ensemble 与 terminal MPC 不在本轮命题中。

选择 `kappa=5h` 是传感器一个 packet 周期对应的 transport direction，不声称在所有斜率中最优。若精确递推仍要求 `r_q` 每周期严格增加，或由 `(r_p+r_q)/kappa` 推出的速度支持超过 `11/4`，则该最小相关模板在进入完整图 LP 前即被否定。

## 准入判断

**通过“单对耦合法向能否打破旧 Farkas 环的精确形状门槛”；不通过“新模板算法”“完整 invariant information ensemble”与“递归可行性”声明。** 该门槛直接决定是否值得构造下一轮更昂贵的 configuration/meta LP，且有明确反例条件。

## 实施后纠正结论

独立复审发现初版把 `p+=(1+h/kappa)p-(h/kappa)q` 的首系数误写为 `1-h/kappa`。纠正后的 interval-support 矩阵为 `[[6/5,1/5],[1/5,4/5]]`，其15步 `q->q` 增益严格大于1。因此固定斜向 `(p,q)` parallelogram 外包不能形成图不变周期。本轮转为 exact obstruction；不据此否定保留 active velocity facets 的六 facet 模板。
