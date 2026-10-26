# Run187 文献准入卡：连续测量中心的 meta 表示门槛

日期：2026-10-27。基线为远端 Run186 `2047ee6`（本地同树 `7215ef45`）。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026), 112661；arXiv:2307.04146 | **重读 §4.1--4.2、§6.2--6.5、式(7)、(25)--(27)及 Theorem 3 证明** | 传感器不是按未来测量值枚举，而是 information ensemble `V={X | exists eta: eta-CX subset V}`；若 measurement-compatible sets 能写成 `Z_1 y<=v`，则 posterior 在 meta 层求交。精确 `min` 非联合凸，式(25)给出安全凸外包。 | “连续 measurement centers 导致必须枚举无限分支”不成立；本轮只能核查六 facet 的 measurement row，不能把 Houska 的 measurement-after-update 控制时序直接套到当前 control-before-packet 图。 |
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, Automatica 163 (2024), 111494；arXiv:2208.12554 | **重读 §3.4--3.5、Theorems 1--2 与 vertex representation 条件** | 在 configuration cone 内，`P(y)=conv_i Lambda_i y`，因此 facet offsets 是真实支持，可用于精确宽度判定。 | 六 facet `Y/G/Lambda` 仍是现有基线；测量宽度坐标只是其直接推论。 |
| Hempel--Kominek--Werner, *A Bundle Method for Output Feedback MPC*, CDC-ECC 2011 | **定向复核 §III-C、式(9)--(14)与 Algorithm 1 的输出纤维覆盖义务（仓库已有全文记录）** | 输出反馈策略必须对完整输出纤维单值，并覆盖连续观测域；有限分区/公共细化已有基线。 | 若后续不用 information ensemble 而显式分区 measurement centers，必须证明完整覆盖，不能靠采样中心。 |
| Robbins--Glunt--Thompson--Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations* (2026) | **仅核对正式摘要；未取得正文** | 摘要层面涉及 CZ reachability 驱动的在线收紧。 | 不据摘要判断首次性或 theorem coverage；本轮不作 CZ tightening 声明。 |

## 严格差异、最强基线与证伪条件

Run186 把 success strip 固定在中心零点并推导单个集合的 canonical supports。本轮只问：对任意
measurement center `eta`，是否能在不枚举 `eta` 的情况下精确判定一个 configuration-constrained
六边形是否与某个噪声半宽 `a` 的位置观测纤维相容。

对 `P(y)={x|Yx<=y}`，若 `+p/-p` facets 在 Run186 configuration 内给出真实支持，则

```math
\max_{x\in P(y)}p=y_0,\qquad \min_{x\in P(y)}p=-y_3.
```

存在 `eta` 使 `|eta-p|<=a` 对所有 `x in P(y)` 成立，当且仅当

```math
y_0+y_3\le2a.
```

因此 Houska 的 measurement block 可取 `Z_1=(e_0+e_3)/2`、`v=a`。最强基线正是 Houska
式(25)，不是逐中心 support formula。若 configuration cone 内存在反例，使上述支持等式或
相容性等价失效，则停止该行；若等价成立，也只说明连续中心已被一个 meta coordinate 精确
消去，不说明完整 `Z_2/H/Omega`、15-mode 图或递归可行性已闭合。

## 准入判断

**通过“六 facet sensor-ensemble measurement row 的精确复现”；不通过“连续中心有限化是创新”、
“已构造完整 meta-template”与“已证明 invariant information ensemble”。** 本轮不直接扩展完整
LP，因为在选择剩余 `Z_2` 与固定-complexity `H/Omega` 前复制 Run184 会把任意模板选择误当作
理论结论。
