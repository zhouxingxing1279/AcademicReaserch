# Run 145 文献准入卡：15 模态竖直 joint predecessor 首次下降层

日期：2026-10-02。仓库起点为 Run 144 本地提交 `64cf2a0`，远端提交
`b3a9953`；两者 tree 均为 `78d4be8db83ddb09b27407379bfa0723612a8317`。
远端 `main=1c49659`。

## 本轮问题

在 Run 144 的正确坐标 `s=(eta_pz,eta_vz,e_pz,e_vz)`、15 模态/17 边、可见
`d=e-eta` 和 actual-input residual 合同下，对候选

`S_j=E_eta,vertical^j x {|e_pz|<=1, |e_vz|<=11/4}`

执行一次下降 predecessor 核查。逐模态必须给出可审查的 observation 内投影与四维正体积
内集，或给出空集证书；一次非空不得升级为固定点或 RCI。

## 最近邻原始文献与本轮实际阅读

| 工作 | 本轮阅读层级 | 已解决内容 | 本轮严格边界 |
|---|---|---|---|
| Rungger, Tabuada, *Computing Robust Controlled Invariant Sets of Linear Systems*, TAC 2017, DOI `10.1109/TAC.2017.2672859`，[作者预印本](https://arxiv.org/pdf/1601.00416) | **全文定向重读 pp.1--6，式 (4)--(10)、递减迭代 (5)、Theorems 1--2 与 Remark 1** | `R_0=X, R_{i+1}=pre(R_i)∩X` 收敛到 maximal RCI，但有限层一般不是 RCI；给出 constraint-relaxed outer certificate 和 disturbance-inflated inner certificate 的停止条件。 | 本轮只有第一次下降层，且控制只读取 observation fiber，不满足该文 full-state feedback 假设；因此只能报告非空内证书，不能引用收敛或不变性结论。 |
| Houska, *Intrinsic Separation Principles*, arXiv:2307.04146, 2023，[全文](https://arxiv.org/pdf/2307.04146) | **定向重读 Sections 4.2、6.1--6.5，Definition 4、式 (7)、(24)--(27)** | information ensemble 保存未来可能信息集；configuration-constrained/extreme vertex polytopes 把信息集合及其控制有限维化，一个 extreme information set 配一个输入。 | 一般 information-set predecessor 与 finite-dimensional convex approximation 已被覆盖。本轮只给冻结 packet graph 与零修正 policy class 下的 exact rational 内投影，不是新算法。 |
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901`，[全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **重读 Section III-A--C、Definition 2、Theorem 1、式 (3)--(10)** | 对每个 noisy output，全部相容状态和扰动必须共享一个 output-feedback input；给定 polytope 可用 Farkas 条件验证。 | 本轮每个 mode 的 success/miss 后继必须共享当前 `deltaT`；但其 LPV scheduling 外生，本轮 residual 半宽由同一 actual thrust 决定。 |

## 严格差异、证明义务与最强基线

最强同条件方法基线是 Houska 的 polytopic information ensemble。当前实现只是一个可复核
的受限实例：对每个 mode 固定 `deltaT=0`，只保留使完整隐藏 fiber `E_j` 在当前与下一步
tracking box 中都安全的 `d` 多边形 `D_j^0`。因此

`C_j^1={(eta,e): eta in E_j, d=e-eta in D_j^0}`

是 `S_j∩Pre_j(S)` 的内集，而非整个 predecessor。还必须核查全部17条 estimator edge 对
目标 `E_k` 的包含，且 residual 半宽必须由同一 actual thrust 上界生成。

这只是已有 predecessor 理论的直接实例化。它的价值在于决定当前候选是否在任一模态
“第一层即空”，从而决定是否值得继续固定点综合；它本身不构成硕士课题创新。

推翻条件包括：任一 `D_j^0` 面积为零/为空；任一 estimator edge 包含失败；mode 4/9 为
success 与 miss 选择不同输入；或把一次下降层写成 RCI。最强负结果只能否定这个
`complete-fiber + zero-correction` 内证书类，不能否定一般 joint information RCI。

## 准入判断

**通过受限的一次下降层验证；不通过创新声明、最大 observation projection、固定点迭代或
完整 RCI 声明。** 若15个 mode 全部非空，下一轮才准入真正会改变 target sets 的第二层
或固定点策略设计；在此之前不接入 terminal/recursive-feasibility 证明。
