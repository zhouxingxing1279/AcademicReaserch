# Run 146 文献准入卡：完整纤维类的第二下降层

日期：2026-10-03。仓库起点为远端 Run 145 提交 `08bc927`，tree
`6904217adda44d922855e6e6dc943e31907e61f3`；远端 `main=1c49659`。

## 本轮问题

以 Run 145 的

`C_j^1={(eta,e): eta in E_j, d=e-eta in D_j^0}`

作为新 target，执行第二次 exact predecessor。当前只准入 `complete eta fiber + shared
zero correction` 类：每个保留的 `d` 必须兼容整个 `E_j`，mode 4/9 的 success/miss
分叉使用同一个当前输入 `deltaT=0`。本轮要么给出15个 mode 的第二层正体积内证书，要么
定位第一个严格空 predecessor，并将否定范围限制在该候选/策略类。

## 最近邻原始文献与本轮实际阅读

| 工作 | 本轮阅读层级 | 已解决内容 | 本轮严格边界 |
|---|---|---|---|
| Rungger, Tabuada, *Computing Robust Controlled Invariant Sets of Linear Systems*, TAC 2017, DOI `10.1109/TAC.2017.2672859`，[作者预印本](https://arxiv.org/pdf/1601.00416) | **重读 pp.1--6、式 (4)--(10)、Theorems 1--2** | `R_{i+1}=pre(R_i) intersect X` 的下降序列、有限终止判据，以及外/内 RCI 近似。文中明确一般有限层不是 RCI。 | 其控制可读取完整状态；本轮必须先对同一可见 `d` 的隐藏 `eta` 纤维 robustify。第二层非空仍不能升级为 RCI；第二层空也只否定当前内证书类。 |
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901`，[全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **精读 Section III-A--C、Definition 2、Theorem 1、式 (3)--(11)** | 对每个 noisy output，与该输出相容的全部状态和扰动共享一个输出反馈输入；给定 polytope 的验证及在线/显式控制计算。 | 本轮完整 `E_j` 纤维和共享输入是该量词的受限实例，不是创新。其 scheduling 当前可知且外生；本项目 packet successor 未知、actual thrust 与 residual 共用同一输入决策。 |
| Houska, *Intrinsic Separation Principles*, 2023, arXiv:2307.04146，[全文](https://arxiv.org/pdf/2307.04146) | **定向重读 Sections 5.3、6.1--6.5 及式 (38)、(43)** | information ensemble、预计算 information tube 和 extreme-information-set control 给出一般有限维凸近似框架。 | 当前 `E_j x D_j` 完整纤维模板只是更保守的固定形状近似；若它塌缩，不能否定保留 `eta|d` 相关性的 information ensemble。 |

## 差异、证明义务、基线和推翻条件

最强同条件基线是 Houska 的多面体 information ensemble；最直接量词基线是 Hempel 的
noisy-output fiber。当前实现不求一般最大 predecessor，只把 Run 145 的 exact `D_k^0`
facets 通过两类可见误差动力学反拉回：

- miss：`d_p^+=d_p+h d_v`, `d_v^+=d_v`；
- success：`d^+=A_d d + (1,L)(q+n)`，其中完整隐藏纤维给出
  `|q|<=h_Ej(1,h)`，测量噪声 `|n|<=nbar`。

每条 target facet 必须对同一个 `q+n` 区间取 exact support，随后与 source `D_j^0`
相交。estimator `eta` 边已由 Run 145 独立包含，但本轮仍须核对17条 graph edge 和
mode 4/9 的共享输入语义。

本问题直接决定是否继续完整纤维 fixed-point 支线。通过标准是15个第二层集合均有严格
正面积；反例标准是某 mode 的 exact 对偶/宽度矛盾。若塌缩，下一步必须转向保留
`eta|d` 相关性的 joint template 或分段策略，不能靠调整参数掩盖，也不能宣称一般 joint
information RCI 不存在。

## 准入判断

**通过一次受限第二下降层验证；不通过算法创新、一般不可行、固定点、RCI 或 MPC
递归可行性声明。** 该轮若发现严格塌缩，其价值在于停止错误的完整纤维支线并确定下一种
必要的集合表示，而不是把局部否证包装成贡献。
