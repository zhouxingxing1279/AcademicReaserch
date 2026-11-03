# Run 129 文献准入卡：等式修正的携证 Scott 消元

日期：2026-09-29。当前分支 `research/run129-certificate-carrying-scott` 从尚未推送的 Run 128 提交 `c1dd18f` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。研究对象仍是冻结四状态合同，不外推到完整六自由度四旋翼。

## 最近邻与本轮实际阅读

| 文献 | 阅读层级与本轮定位 | 已解决内容及边界 |
|---|---|---|
| Scott, Raimondo, Marseglia, Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69 (2016) 126--136，[DOI](https://doi.org/10.1016/j.automatica.2016.02.036)，[作者全文](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) | **全文定向重读** Appendix (A.9)--(A.10) 及其前后的生成元删除步骤；复核 Section 4.3 的 lift-then-reduce。 | 对 `G=[T\ V]`、`R=T^{-1}V`，选中残余列 `v` 后以 `T(I+diag|r|)` 替代 `[T\ v]`，并用逆缩放更新剩余坐标；给出可靠外包和几何体积启发式。算法不维护到外部目标集的包含 witness，也不保证 terminal inner-containment。 |
| Kopetzki, Schürmann, Althoff, *Methods for Order Reduction of Zonotopes*, CDC 2017, 5626--5633，[DOI](https://doi.org/10.1109/CDC.2017.8264508)，[作者全文](https://mediatum.ub.tum.de/doc/1442501/1442501.pdf) | **全文精读** Introduction、Section II 的 box/transformation methods、Section III 的 PCA/clustering/constrained optimization、Section IV 的约束与评价。 | 系统比较 zonotope 外包约减并优化体积或几何误差；没有 CZ equality slice，也没有相对于给定终端内集的逐行包含证书。故几何最优不等于本合同下的控制准入。 |
| Sadraddini, Tedrake, *Linear Encodings for Polytope Containment Problems*, CDC 2019，[DOI](https://doi.org/10.1109/CDC40024.2019.9029363)，[作者全文](https://groups.csail.mit.edu/robotics-center/public_papers/Sadraddini19.pdf) | **全文定向重读** Section IV-A Theorem 3 及其反例，并沿用 Run 128 对 Theorems 1--2 的核查。 | 仿射生成元映射及逐行 `l1` 预算是 zonotope-in-zonotope 的充分证书，但一般不必要。它允许证明本轮 witness 的可靠性，却不允许由 witness 失败推出真实不包含。 |
| Diaconescu et al., *Zonotope-Based Elastic Tube Model Predictive Control*, arXiv:2509.19824v2 (2026)，[全文](https://arxiv.org/abs/2509.19824) | **全文定向精读** Sections 3.1 与 3.4 的 Lemma/Proposition/Corollary 及预计算包含矩阵。 | 该工作已在 zonotopic tube MPC 中用固定仿射生成元映射和行范数条件，并预计算 inclusion matrix 以减少在线变量。因此“携带/预计算包含证书”本身不是本轮创新；其对象是缩放 zonotope，不是 Scott CZ 消元和 equality 修正。 |

Raghuraman--Koeln 2022 的内近似降阶、Run 127 的 539-generator 严格终端反例、Run 128 的通用 AH/CZ 巨型 LP 审计继续作为已核查边界。检索未发现直接给出“沿 Scott 消元链、利用 CZ 等式修复到固定外部 zonotope 的行预算”的原始论文，但检索不完备，因此首次性仍标未知，不作创新声明。

## 本轮命题与结构化 witness

令固定终端内近似为

\[
S_{602}=Y[-1,1]^{602},
\]

Scott 链上的当前 CZ 为

\[
R_m=\{G_m\xi:\|\xi\|_\infty\le 1,\ A_m\xi=b_m\}.
\]

从未压缩后验的显式映射 `G_605=Y C_605` 出发，按 Scott 的列替换同步传播系数矩阵 `C_m`，从而保持 `G_m=Y C_m`。若忽略 CZ 等式，Sadraddini--Tedrake 型充分条件是每个目标系数行 `c_j` 满足 `||c_j||_1<=1`；Scott 对基列的放大会立即使某些行超出 1，因此朴素携证规则预期首步失败。

等式提供一个不改变 equality slice 上物理点的修正自由度。对任意 `Q`，

\[
C_m\xi=(C_m+Q A_m)\xi-Qb_m
\qquad(A_m\xi=b_m).
\]

故下式是 `R_m subseteq S_602` 的充分证书：对每个目标行 `j` 存在 `q_j` 使

\[
\|c_j+q_j^\top A_m\|_1+|q_j^\top b_m|\le 1.
\]

每行只需优化 3 个自由变量及绝对值辅助变量；与 Run 128 的 160--180 万变量通用 LP 不同，它复用已知 Scott 列谱系，并可只检查朴素预算超限的行。该判据是已知仿射生成元包含证书在当前结构上的直接特化，而非独立理论贡献。

## 强基线、价值与可推翻条件

最强同条件基线依次为：605-generator 后验到 `S_602` 的构造性精确包含；不使用 equality 修正的谱系行 `l1` witness；Run 128 的通用 AH/CZ 充分证书；以及 Run 127 对 539-generator 候选的真实不包含证书。本轮只能在同一冻结 Scott 链、同一 `Y`、同一等式和同一硬终端集合下比较。

这个问题直接决定普通 Scott 降阶能否成为完整 MPC terminal gate，而非只保护有限阶段方向。以下任一结果会推翻候选路线：

1. 第一次非平凡消元已无可靠 equality-adjusted witness；
2. 小 LP 的构造、求解或可靠复核不能进入现有在线预算；
3. 即使 witness 可行，也不能与 Scott 外包的实际 binary64 实现建立足够小的残差裕量；
4. 近邻正文已经覆盖完全相同的结构和闭环证明义务。

证书失败只能记作“该充分 witness 未证”，不能记作集合不包含；真实不包含仍须全方向分离证书。若至少一个 `m<605` 可证，则得到一个有控制意义的低成本终端准入机制候选；但在闭环递归可行、同预算优势和四旋翼验证完成前，仍不足以构成硕士课题创新。

**准入判断：通过一个有边界的实现审计，不通过创新声明。** 允许测试先行实现最小验证器：验证谱系恒等、逐行小 LP 证书和至少一次非平凡消元；若首步结构失败即停止，不退回巨型 LP或有限方向枚举。
