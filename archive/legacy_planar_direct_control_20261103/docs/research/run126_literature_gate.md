# Run 126 文献准入卡：Scott 固定复杂度 CZ 强基线

日期：2026-09-28。仓库基线：`main` 1c49659c；研究基线：`research/run125-terminal-containment`，远端 4aa65ba / 本地 4fdc691，tree 均为 c366c423。

## 最近邻与实际阅读

| 文献 | 本轮阅读层级 | 已解决内容与本轮边界 |
|---|---|---|
| Scott, Raimondo, Marseglia, Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69 (2016) 126–136，[DOI](https://doi.org/10.1016/j.automatica.2016.02.036)，[作者全文](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) | **全文定向重读** Section 3.1、Section 4.1–4.3、Appendix Algorithm 1 与 (A.9)–(A.10)，并核对 Section 5 的比较口径。 | Proposition 4 给等价 rescaling；Proposition 5 给约束 dualization 外包；Section 4.3 的 lift-then-reduce 将 CZ 提升成 zonotope 后安全约减生成元。普通 CZ 外包降阶及其复杂度—精度权衡均已有，不能作为创新。 |
| Robbins, Glunt, Thompson, Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*, ACC 2026, pp. 585–592，[机构记录](https://pure.psu.edu/en/publications/online-constraint-tightening-for-mpc-using-constrained-zonotope-r/)，[IEEE 记录](https://ieeexplore.ieee.org/document/11616451) | 本轮确认摘要、8 页书目信息及章节结构：II Preliminaries、III Error Sets、IV CZ-to-zonotope over-approximation、V Numerical Example；IEEE 在 Introduction 后要求机构/会员访问，**正文仍未取得**。 | 摘要已覆盖 nonlinear error reachability、在线 tightening、无需优化的 CZ-to-zonotope 外包及 LTV MPC 数值例。不得从摘要猜测公式、复杂度或控制方向保护，也不得声称本项目未被覆盖。 |
| Raghuraman, Koeln, *Set operations and order reductions for constrained zonotopes*, Automatica 139 (2022) 110204，[全文](https://arxiv.org/pdf/2009.06039) | 继承 Run 124 对 Section 5 的全文核查，本轮不重复通读。 | 其低复杂度 inner approximation 不能作为可靠后验外包；只用于说明包含方向必须明确。 |
| Dey, Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026，[全文](https://arxiv.org/pdf/2605.23661) | 继承 Run 123 对 Section IV、Algorithm 1、Theorem 2、Appendix IV 的全文核查。 | 在线集合更新后的备份计划、终端追加和递归可行已有一般框架。本轮只复现固定模型的一种外包基线，不提出新递归结构。 |

## 问题、强基线与推翻条件

本轮不提出新算法，只问：在冻结 Run-123 的相同 602 潜变量后验、三条测量、30 步、300 个控制查询方向和硬约束下，Scott 2016 的安全 lift-then-reduce 基线能压到多低复杂度而不使旧移位计划失效？测量带先精确改写为增加三个噪声变量的 CZ；随后按论文 (30)、(A.9)–(A.10) 外包。最强比较对象是经行缩放后重新求解的原 602 变量支持 LP。

以下结果会否定候选价值：外包在任一保护方向低估；低阶 Scott 基线在相同预算下既快又保留全部余量；或控制相关模板的优势仅来自不公平求解容差。终端 mRPI 本轮未审计，因此阶段准入不能写成完整递归可行。

## 准入判断

**通过强基线复现与方向纠正，不通过新算法/创新声明。** Robbins 全文仍不可读，首次性保持未知；Scott 全文足以实现公开、方向正确的替代基线。只有基线在活跃控制约束附近显示普通几何降阶必须保留很高复杂度时，才继续研究“按控制余量保护”的完整方法；本轮结果不能单独构成硕士课题创新。
