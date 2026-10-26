# Run182 文献准入卡：局部 lifted cells 的边可组合性

日期：2026-10-26。远端续接点为
`research/run181-mode4-unknown-branch-lifted-cell@46f33d2`；远端 `main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Hempel--Kominek--Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011，DOI `10.1109/CDC.2011.6160901`，[全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **重新下载全文，定向精读 §III-C、式(9)--(14)与 Algorithm 1** | 各 robust facet 的参数解先形成覆盖完整 admissible output set `Y(Omega)` 的 PWA partitions，再用交集细化为共同凸分区；每个分区在线/显式求单值控制。 | “有限输出分区、覆盖、交叠细化和 PWA 策略”不是本项目创新。任意手工 cells 若不证明 successor 落入某个 target cell，就还不是该意义下的可执行分区。 |
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026) 112661，DOI `10.1016/j.automatica.2025.112661`，[预印本](https://arxiv.org/pdf/2307.04146) | **重新下载全文并精读 §4.2、§4.4、§6.1--6.7，Definitions 4--5、Lemma 2、Theorem 3、式(25)--(29)** | 用 configuration-constrained polytopes 参数化固定复杂度 information ensembles；对 extreme vertex polytopes 分配控制，经凸插值得到全 ensemble 策略；式(29)直接给 invariant terminal ensemble，§6.7明确复杂度由 facets、ensemble parameters 与 extreme sets 数控制。 | 固定预算 information-family 和重叠处可实现策略已有强基线。当前非线性、packet-mode、control-dependent residual 的可靠外包仍需项目化，但不能以“cell family”本身声称创新。 |
| Artstein--Rakovic, *Set invariance under output feedback: a set-dynamics approach*, IJSS 42(4), 2011，DOI `10.1080/00207720903428880` | **只取得期刊摘要和作者摘要页，未取得全文** | 摘要确认 output-feedback invariance 应在随观测演化的信息集 set dynamics 上定义。 | 摘要不足以引用其具体定理；本轮只把它列为概念源流，不据此作覆盖或首次性判断。 |
| Rego--Raffo--Scott--Raimondo, *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, Automatica 111 (2020) 108614 | **沿用 Run179 已全文核查的 §§4.1--4.5、Theorems 1--3 与 reduction 复杂度** | 单条已实现 history 的可靠非线性 CZ prediction/update/reduction。 | 仍不解决跨连续 observations 的 target-cell 覆盖；只能作为 ensemble oracle 的单集合传播原语。 |

## 本轮命题、强基线与推翻条件

Run180/181 都使用同一个局部可见盒

```math
D_0=\{(d_p,d_v): |d_p|\leq1/5,\ |d_v|\leq1/4\}.
```

但两轮只检查 successor 的 estimator facets 与真实 tracking box normals，没有检查 successor
`d^+=e^+-eta^+` 是否仍落入某个 target `d`-cell。故“把 mode-0 与 mode-4 两张证书直接扩成
finite cell graph”之前，必须先审计最基本的边可组合性。

本轮允许的精确命题仅为：在相同 `D_0`、相同零修正策略和 Run181 联合 primitive graph 下，
分别求 `0->1 miss`、`4->5 miss`、`4->0 success` 的 `d^+` 坐标支持，并判断是否包含于同一
`D_0`。任一方向支持超过 target bound 即给出精确非包含证书。该结果只否定“现有两张局部
cells 已能直接连边”，不否定其他 translated/larger cells、PWA policy 或 information ensemble。

最强后续基线不是继续手工铺重叠盒，而是 Houska 式 configuration-constrained polytopic
information ensemble；若保留显式输出分区，则至少采用 Hempel 的完整覆盖分区与共同细化。
真正论文义务仍是把 nonlinear packet residual oracle、硬约束、terminal/shift 和同预算比较接入
该基线。

## 准入判断

**通过方向纠正与 exact composability audit；不通过“有限 cell 覆盖本身是新方法”。** 若三条
已认证边全部回到 `D_0`，才允许直接扩展当前 cell 图；若任一边越界，就停止把 Run180/181
当作相互可接续的 nodes，先记录所需最小 target widths，再把下一步改为 information-ensemble
基线或经过综合的 partition，而不是无依据地增加 cell 数。
