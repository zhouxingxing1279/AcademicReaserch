# Run 121 文献准入卡：修复冻结算例的终端证书

日期：2026-09-28。基线：`main` 1c49659c；未合并研究分支 `research/run120-proof-quality-run119` 2a0b3d5。此轮只修复已有 Run 119 终端 RPI 支持证书的可执行核验，不提出新控制算法。

## 最近邻与本轮实际阅读

| 文献 | 核查深度 | 与本轮关系 |
|---|---|---|
| Köhler, Kötting, Soloperto, Allgöwer, Müller, *A robust adaptive model predictive control framework for nonlinear uncertain systems*, IJ Robust Nonlinear Control 31 (2021), DOI [10.1002/rnc.5147](https://doi.org/10.1002/rnc.5147)，[作者全文](https://www.ist.uni-stuttgart.de/de/institut/team/PDFs_MA-Seiten/JK/Adaptive_Nonlin.pdf) | 阅读正文 II–III，特别是 Assumptions 6–7、Theorem 2 及证明的候选移位，另核查 III-F 的终端讨论。 | 其未知量是模型参数及加性扰动，使用有限复杂度超盒、标量 tube；Theorem 2 的递归可行性需要单调更新、嵌套、收紧及兼容终端条件。仅有 RPI 集不能代替整套移位证明。 |
| Mayne, Raković, Findeisen, Allgöwer, *Robust output feedback model predictive control of constrained linear systems*, Automatica 42 (2006), DOI [10.1016/j.automatica.2006.03.005](https://doi.org/10.1016/j.automatica.2006.03.005) | 本轮核查出版方页面和摘要；全文未取得，本轮不对其证明细节作排除性判断。 | 已有带有界状态/输出扰动的输出反馈 tube MPC 与收紧名义约束。 |
| Robbins, Glunt, Thompson, Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*, ACC 2026, pp. 585–592，[机构记录](https://pure.psu.edu/en/publications/online-constraint-tightening-for-mpc-using-constrained-zonotope-r/) | 本轮只取得机构摘要及书目信息；全文、定理和算法未核查。 | 已有 CZ 可达集在线收紧与免优化 zonotope 外包。不能据摘要声称其没有控制余量准入机制。 |

## 准入判断

**通过修复证据，不通过新颖性声明。** 本轮唯一命题是：Run 119 所用固定四状态合同中的无限扰动和 `S=⊕_{i≥0}F^iW`，可用有理数有限前缀与矩阵幂收缩上界证明五个状态/输入方向严格处于硬界内。该级数尾界是标准几何级数推论，不构成研究创新。Run 120 的可执行脚本使用 139 项前缀和粗尾界，运行时在 `px` 方向断言失败；Run 120 文本已有 600 项前缀的修正规格，但尚无通过的执行记录。

同条件比较基线是固定 mRPI 终端合同，并非上述文献的完整控制器。若有任一严格界失败，则当前冻结终端合同不能认证，Run 119 的「准入」不能升级；即便五界通过，Run 119 基线 OCP 和测量行删除分类仍是数值观察，且多轮重定心/测量更新的递归可行性仍未证明。
