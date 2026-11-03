# Run 122 文献准入卡：独立复现 Run 119 数值基线

日期：2026-09-28。仓库基线：`main` 1c49659c；研究基线：`research/run121-literature-and-certificate` 8d073c0。

## 本轮阅读与最近邻

| 文献 | 本轮核查范围 | 已解决内容与边界 |
|---|---|---|
| Köhler, Kötting, Soloperto, Allgöwer, Müller, *A robust adaptive model predictive control framework for nonlinear uncertain systems*, IJ Robust Nonlinear Control 31 (2021), DOI [10.1002/rnc.5147](https://doi.org/10.1002/rnc.5147)，[作者全文](https://www.ist.uni-stuttgart.de/de/institut/team/PDFs_MA-Seiten/JK/Adaptive_Nonlin.pdf) | 重读 Section II 的 Assumptions 1–2、Problem (6)、Theorem 1 及其候选移位证明；定向核查 Section III-C Theorem 2 的候选构造。 | 已用集合传播的过逼近、参数集非扩张、传播算子单调性和终端条件证明在线更新下的递归可行与约束满足。其对象主要是参数集合与加性扰动；Run 119 的单次表示删行准入不等于这些跨时刻条件。 |
| Mayne, Raković, Findeisen, Allgöwer, *Robust output feedback model predictive control of constrained linear systems*, Automatica 42 (2006), DOI [10.1016/j.automatica.2006.03.005](https://doi.org/10.1016/j.automatica.2006.03.005) | 检索到作者 PDF 链接，但本轮抓取失败；只使用出版信息与摘要，不引用定理细节。 | 已覆盖有界估计误差、不变误差集合、名义约束收紧和输出反馈 tube MPC；不是本轮可声称的新意。 |
| Robbins, Glunt, Thompson, Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*, ACC 2026, pp. 585–592 | 继承 Run 121 的机构摘要核查；全文仍未取得。 | 摘要已明确在线 CZ 可达收紧和免优化 zonotope 外包。不能依据摘要判断是否覆盖基于旧计划余量的表示删减准入。 |

## 准入结论

**通过复现，不通过新算法或首次性声明。** 本轮只把 Run 119 已记录的数值观察变成可执行基线：从冻结的 `F,G,D0` 重建 600 生成元旧预测和一个新扰动生成元，按正确时序构造两条独立位置测量行；用 HiGHS 求后验支持，用 SLSQP 解固定 30 步名义 OCP，并重新计算每个状态/输入面的真实余量和两种纯删行的支持损失。

最强否证条件是：无法重现 Run 114 的六个后验支持、SLSQP 计划不满足终端等式或收紧约束，或两种删行不再出现 Run 119 所述的拒绝/准入分离。即便全部重现，也只提高数值证据的可复核性；不证明跨时刻递归可行性、稳定性或四旋翼非线性闭环优势。
