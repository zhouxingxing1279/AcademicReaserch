# Run 136 文献准入卡：成功周期提升的 zonotope 不变多集

日期：2026-09-29。仓库起点为本地 Run 135 提交 `7ff1100`；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。本轮唯一问题是：能否在同一 15 模态 actual-input 误差 inclusion 上，保留生成元相关性并构造 time-uniform 外不变多集，使状态域 tightening 非空。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读层级 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Athanasopoulos, Smpoukis, Jungers, *Invariance in Constrained Switching Systems*, 2017, [arXiv:1702.00598](https://arxiv.org/abs/1702.00598) | **全文定向精读** Sections 2.1--3.2、6，尤其 Assumptions 2--4、Proposition 1、Theorems 1--2、式 (7)--(18) | 图约束系统的 forward reachable multi-set 收敛到 minimal invariant multi-set；逐边可达包含等价于不变性；给出有限和缩放外包，并讨论 T-product lifting。 | 节点多集、有限可达和、缩放尾项和周期提升均不是创新。Theorem 2 要求各边扰动为含原点内点的 C-set；本项目逐拍扰动像秩亏，不能直接套式 (18)。 |
| Kouramas, Raković, Kerrigan, Allwright, Mayne, *On the Minimal Robust Positively Invariant Set for Linear Difference Inclusions*, CDC-ECC 2005, [公开全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc05/pdffiles/papers/1964.pdf) | **全文定向重读** Sections II--V，Theorems 1--4、式 (11)--(23) | 对稳定 LDI，用有限 reachable sums `D_s` 与条件 `R_s subseteq alpha W` 构造 `(1-alpha)^-1 D_s` 外 RPI，并给任意精度条件。 | 其 `W` 也是 full-dimensional C-set，且采用公共 disturbance set/LDI convexification；逐拍秩亏、标签相关扰动不能无条件代入。 |
| Hassaan, Pati, Shen, Yong, *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, 2021, DOI [10.1016/j.ifacol.2021.08.482](https://doi.org/10.1016/j.ifacol.2021.08.482) | **仓库既有全文精读；本轮定向对照** Section 3.1.1 | 使用缺测语言和 time-varying hyperbox error tubes；未来数据模式未知时取允许模式最坏值。 | 每拍/每相位 box 是必须比较的低成本基线；但对有符号 reset 动力学逐拍取绝对值会丢失周期内抵消，不能据其发散否定真实几何集合。 |

全文门槛由前两篇原文定理与假设复核满足。检索未支持“成功周期提升＋mode-0 盒＋年龄 zonotope”为首次性；它是图提升和 zonotope 传播的直接组合，本轮不作创新声明。

## 2. 严格差异、直接推论与强基线

本轮不使用 Athanasopoulos/Kouramas 的缩放公式。对仓库确定的三种返回周期 `L in {5,10,15}`，直接形成标签相关的精确 lifted pair `(M_L,V_L)`；只在成功后的 mode 0 用坐标盒外包，随后 0--14 龄全部以有符号生成元传播。逐边 miss image 是下一年龄 zonotope 的等式，success image 由三个 lifted box inclusion 证回 mode 0。

这是现有 invariant-multi-set、T-product lift 和 zonotope 支持函数的直接特化。最强同合同基线为：Run 135 的共同度量椭球、逐拍 time-varying hyperbox，以及直接 forward reachable multi-set/更紧 polytope 或 CZ 外包。尚未满足同计算预算的性能比较。

## 3. 推进价值与推翻条件

该问题决定估计误差能否在 residual/state domain 内给 ancillary 层留下非空余量。以下任一结果会推翻候选：

- 三个返回周期中任一 lifted image 不能证入 mode-0 盒；
- 17 条原图边中任一 miss 等式或 success 包含失败；
- 任一年龄的坐标支持超过原状态区间半宽；
- 结论依赖逐拍绝对值递推，或把非空 state tightening 误写成完整闭环 residual-domain 自洽。

## 4. 准入判断

**作为证据链修复和可执行估计器接口：通过。作为论文创新：不通过。**

理由：它直接回答 Run 135 的阻塞，并可把 scalar/common-metric 的假失败纠正为几何证书；但组成模块及其不变性逻辑已有直接近邻。允许实现精确有理数 verifier，禁止宣称控制约束、递归可行性或性能优势已经成立。

## 5. 本轮停止条件

一旦得到 17/17 逐边包含和全部模式非空状态 tightening，停止继续细化估计集合；下一轮恢复 control-dependent joint ancillary RCI，并显式消费各模式 zonotope 支持。若只得到有限时域变紧而没有 time-uniform 逐边闭合，则本轮判不通过。
