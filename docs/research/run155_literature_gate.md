# Run155 文献准入卡：同标签仿射凸化交换律

日期：2026-10-11。起点为远端 Run154 `ee769f2`（本地等树提交 `9d327d7`）；远端
`main=1c49659`，起点工作树干净。

| 最近邻 | 本轮实际阅读 | 已解决内容与边界 |
|---|---|---|
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011，DOI `10.1109/CDC.2011.6160901`，[全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **重新精读 §III-A--C、Definition 2、Theorem 1、式 (3)--(14)** | 对每个 noisy output 与当前 scheduling，只能选择一个依赖该可见量的输入，并对整条相容状态纤维及全部扰动保证不变；输入约束也是同一量词的一部分。其 PWA 控制来自凸参数分区，但论文不直接构造 OFCI 集。 |
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026) 112661，DOI `10.1016/j.automatica.2025.112661`，[预印本](https://arxiv.org/pdf/2307.04146) | **定向复核 §6.4--6.5、Definition 7、Theorem 3 与证明（Run154 已逐页精读，本轮核对极端信息集的凸权重控制）** | configuration-constrained/extreme information polytopes、每个 extreme information set 的控制及凸权重插值已经覆盖一般方法。仿射像与凸包交换只是该构造的基础凸分析，不是新算法。 |
| Yang--Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 2021，[作者全文](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) | 复核 Run153 的 §4.1--4.4/Propositions 2--5 阅读记录；**本轮未重新读正文** | 缺测 string automaton/产品图必须保留离散历史标签；不同标签可有不同控制与集合。 |

## 差异、强基线和反证条件

最强一般基线仍是 Houska 的 polytopic information ensemble；Hempel 给出同一 observation
fiber 的共享输入量词。本轮只问一个实现合同：固定 global residual、线性边动力学、凸硬约束
以及**同一 source 标签上的一张 affine-in-`d` 策略**时，是否需要逐点重验凸化新增的
`d=e-eta` fibers。

结论是一个已有凸分析的直接特化：对同一边映射，闭环映射变成仿射映射，所以它与有限并集
的凸包以及凸扰动 Minkowski 和交换；输入像同样交换。它不覆盖 scheduled `W(T)`、非仿射/
分片不一致策略、非凸约束、不同边映射在应用前的错误混合，也不提供任何集合自包含。

**准入通过，但仅允许写成项目实施引理和标签纪律，不准入算法或创新声明，不写数值求解器。**
若存在同标签 constituent sets 上均可行、但其凸包上 affine policy 违反凸输入/状态约束或同一
固定边后继不在 constituent images 的凸包中，即推翻本引理；这只能在上述凸性/仿射/固定扰动
假设之一被破坏时发生。最强同条件比较基线就是 Houska 的 extreme-set convex interpolation。

## 对 Run148 的语义纠正

Run148 的三条首次 return seeds 分别进入 `(0,5)`、`(0,10)`、`(0,15)`，在 Run153 的
`last_return` 产品图中不是同一个标签。把三者先取共同凸包虽可作为 mode-only 的更粗安全外包，
却会主动抹掉本来要验证的 return-history 区分，不能作为 45-state recurrent family 的模板。
第一个非平凡、语义正确的同标签凸化应在**第二个周期**发生：对每个目标 `(0,r')`，汇集来自
三个前一 `last_return` 标签且下一 return length 同为 `r'` 的三条历史像，再在该目标标签内凸化。
