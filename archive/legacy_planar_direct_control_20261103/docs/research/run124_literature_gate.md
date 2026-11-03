# Run 124 文献准入卡：非零重定心与固定复杂度外包

日期：2026-09-28。仓库基线：`main` 1c49659c；研究基线：`research/run123-two-time-shift` 47b46b1。

## 最近邻与实际阅读

| 文献 | 本轮阅读层级 | 已解决内容与本轮边界 |
|---|---|---|
| Scott, Raimondo, Marseglia, Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69 (2016) 126–136，[DOI](https://doi.org/10.1016/j.automatica.2016.02.036)，[作者全文](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) | **全文定向精读** Section 3.1、Section 4（pp. 129–131，Propositions 4–5、lift-then-reduce）及 Section 5 的估计递推。 | Section 4 明确构造满足原 CZ 包含于低复杂度 CZ 的外包；因此“CZ 安全降阶”不是创新。其目标主要是几何/Hausdorff 质量，并未自动给出本仓库旧解移位所需的逐方向余量和终端兼容性。 |
| Raghuraman, Koeln, *Set operations and order reductions for constrained zonotopes*, Automatica 139 (2022) 110204，[DOI](https://doi.org/10.1016/j.automatica.2022.110204)，[全文](https://arxiv.org/pdf/2009.06039) | **全文定向精读** Section 5（pp. 5–8）及相关定理/算法。 | Section 5 的降阶对象是低复杂度**内近似**。它可用于可行域/集合运算，但不能替代可靠状态后验的 outer compression；否则真值包含方向颠倒。 |
| Robbins, Glunt, Thompson, Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*, ACC 2026, pp. 585–592，[机构记录](https://pure.psu.edu/en/publications/online-constraint-tightening-for-mpc-using-constrained-zonotope-r/) | 仅取得机构摘要和书目信息，**未取得全文**。 | 摘要已覆盖在线 CZ 可达分析、zonotope 外包和 MPC 收紧，并宣称比既有免优化外包更紧。它是后续同预算强基线；不能据摘要声称其未覆盖控制方向保护。 |
| Dey, Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026，[arXiv](https://arxiv.org/abs/2605.23661) | 继承 Run 123 对 Section IV、Algorithm 1、Theorem 2 和 Appendix IV 的全文核查；本轮未重复通读。 | 一般的在线估计集/tube 更新、备份集合和旧解移位已有递归可行性框架。本轮只审计冻结 Run-119 合同中“有限方向压缩 + 非零重定心”的遗漏证明义务。 |

## 问题、基线和推翻条件

最强同条件基线是 Run 123 的 602 潜变量精确支持查询、中心对齐旧 nominal 后继、旧计划移位和 Run 121 固定 mRPI 终端。候选压缩固定为 300 行 H-template：每一行来自 30 阶段乘 8 个状态方向和 2 个输入方向的闭环逆传播方向。它必须同时满足：后验外包含、所有旧候选余量、零 nominal 终端以及固定 mRPI 终端包含。

候选被以下任一结果推翻：H-template 丢失受保护方向支持；非零重定心 LP 只有零解；名义动态/硬约束失败；或虽通过 300 条阶段约束，却不能继承 Run 121 的终端 mRPI 包含。最后一项不能用“终端 nominal 为零”替代。

## 准入判断

**通过“证明义务审计和反例验证器”，不通过新算法/创新声明。** Scott 2016 已覆盖 outer reduction，Dey–Bhasin 2026 已覆盖 adaptive-tube 递归结构；本轮实现只用于判定仓库候选能否闭合。Raghuraman–Koeln 2022 的内近似明确禁止作为可靠后验压缩。若阶段余量通过而终端包含未闭合，应停止宣称完整准入，不靠数值小位移掩盖。
