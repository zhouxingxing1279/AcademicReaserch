# Run184 文献准入卡：box information-ensemble 图 LP

日期：2026-10-26。续接远端 Run183 `893046dc` 的等价本地树。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, 2023/Automatica 2026，[全文](https://arxiv.org/pdf/2307.04146) | **重新精读 §6.1--6.7，尤其式(25)--(30)、Theorem 3及证明** | `Y/G/Lambda`、`Z/H/Omega`、extreme-set controls、meta-level measurement outer approximation 与 invariant ensemble LP 已完整给出。 | 这些均是强基线，不是创新；原式时序是测量后控制，不能不经修改地用于仓库的 control-before-edge 图。 |
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, 2022，[全文](https://arxiv.org/pdf/2208.12554) | **定向重读 §2.1--2.3、§3.1--3.4** | 固定 facet、configuration cone、vertex maps 和 vertex controls；给出可表示 tube/policy 类的保守性比较框架。 | box template 的 configuration/vertex maps 是直接实例，不构成新方法。 |
| Dey--Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026, arXiv:2605.23661 | **本轮仍仅有题名、摘要和问题陈述，未据此引用定理** | 摘要层面声称在线估计集合驱动 tube、收紧与递归可行性。 | 首次性保持未知；本轮只复现更早且正文可核查的 Houska 强基线。 |

## 差异、最强基线与推翻条件

Houska 式(29)对 posterior ensemble 的 extreme sets 选 control 后传播；当前 mode graph 明确 current
control 先于 successor packet outcome。故最强同条件基线必须是“每个 source 一组 extreme
controls和一个 predicted ensemble，之后才按 edge 做 miss identity 或 success measurement
intersection”，不能为每条 edge 分配 current control。

本轮只允许实现这个因果适配和最小 box/meta-template。若 mode 4/9 需要 edge-specific control、
success 不能在 transition 后表达、或 exact rational replay 出现正违反量，则候选基线失败。
即使可行，也只证明冻结二维线性合同下的 invariant information-ensemble 充分证书，不证明
scheduled residual 优势、完整 MPC shift、六状态/六自由度保证或算法首次性。

## 准入判断

**通过“时序正确的 box 强基线复现”；不通过“新 information-ensemble 算法”与“直接照搬式
(29)”。** 该问题直接决定终端/递归可行性链条能否从局部 cell 证书转入固定预算强基线，具有
继续实现的价值。

## 实施后结论

准入后的498变量/2772约束LP由HiGHS判为不可行；进一步的21行精确Farkas聚合给出
`0<=-572143/800000`。因此本轮可靠结论是“纯axis-aligned box模板不通过”，而不是一般
information-ensemble方法不通过。失败机制是position-only measurement不改变box的velocity
radius，非零过程扰动在每条边严格累积；下一模板必须保留position--velocity相关性。
