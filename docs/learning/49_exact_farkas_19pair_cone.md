# 49 19-pair audited configuration cone 的 exact Farkas 证书

日期：2026-09-24。承接第48章，仓库起点 `568b0481c3783dc554ecc43c1634de7dc759e039`。

## 1. 本轮唯一问题

第48章在一个明确的 38-active-facet、160-vertex entirely-simple seed configuration 上得到 CC-RCI LP infeasible，并且删除 `|tau|<=0.08` 后仍 infeasible；但该结论来自浮点 HiGHS。本轮只解决：

> 能否从第48章 unbounded-torque LP 中提取小规模 Farkas witness，并用有理数精确复核，从而把“该 configuration cone 不可行”升级成严格数学结论？

## 2. 文献与方法边界

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818--3823, DOI `10.1109/LCSYS.2023.3346128`：本项目继续只复用其 configuration-constrained H/V 参数化思想；本章不把 CC-RCI machinery 当创新。

Farkas lemma 对线性不等式系统提供线性不可行证书。Gleixner et al., *Iterative Refinement for Linear Programming*（2015 preprint, Optimization Online: https://optimization-online.org/wp-content/uploads/2015/06/4948.pdf）第4节明确讨论了 infeasible LP 的高精度 Farkas proof，并指出 exact rational arithmetic 可用于任意精度/精确验证。HiGHS 仅用于发现稀疏 support；最终证书不依赖求解器容差。

## 3. 证书形式

将第48章 audited cone 中所需的有效不等式统一写为

\[
 a_k^T z\le b_k,
\]

其中 `z` 包含 38 个 offsets 与 160 个 vertex torques。若存在 `y_k>=0` 使

\[
 \sum_k y_k a_k=0,\qquad \sum_k y_k b_k<0,
\]

则任意可行 `z` 都会推出

\[
 0=\sum_k y_k a_k^Tz\le\sum_k y_kb_k<0,
\]

矛盾，因此系统不可行。

## 4. 从 19520-row LP 到 25-row exact core

对第48章 **unbounded vertex torque** LP 构造归一化 Farkas auxiliary LP，数值搜索得到一个仅 25 条原始 inequalities 的 support。它由：

- 4 条 configuration-cone inequalities；
- 20 条 endpoint-robust invariance inequalities；
- 1 条 hard-state inequality；
- **0 条 torque-bound inequalities**；
- **0 条 pair-offset equality 的正/负展开行**；
- **0 条 q>=0 bound rows**。

20 条 invariance rows 中，16 条对应 `T_L=4.905`，4 条对应 `T_U=14.715`；共涉及 18 个不同 vertex maps。

数值 dual ray 只用于确定 support。随后重新从 rational facet normals、active sets、`A(T),B,E,dbar(T)` 构造这 25 条 rows。每个 `C_I^{-1}` 用 SymPy rational inverse 计算，所有后续系数和 multipliers 都转换为 `Fraction`。

## 5. exact 结果

25 个 multipliers 全部严格为正。代表性的系数包括

\[
100/27,\;1/9,\;500000/8829,\;4000000/79461,\;\ldots,\;1.
\]

完整列表保存在 verifier 中。精确求和得到

\[
\boxed{\sum_{k=1}^{25} y_k a_k=0}
\]

对全部 198 个决策变量逐分量严格成立，同时

\[
\boxed{\sum_{k=1}^{25} y_k b_k=-\frac{3069803}{88290}<0.}
\]

因此由 Farkas lemma：

\[
\boxed{\text{第48章 audited 19-pair configuration cone 的 endpoint-robust CC-RCI 系统严格不可行。}}
\]

这不再是 HiGHS tolerance 下的数值观察。

## 6. 更强的原因分类

证书完全没有使用 vertex torque bounds，所以即使每个 vertex torque 无界，矛盾仍成立。更强的是，证书也没有使用 pair-offset equalities 或 `q>=0` bounds。因此本次 obstruction 不是 `0.08 N m` 饱和、中心对称 offset tying 或 offset 非负性单独造成的；它来自该 audited incidence/configuration inequalities、endpoint robust invariance 与 hard-state containment 的组合。

但是不能外推为整个 19-pair orientation family 不可行：其他 offsets 可能跨越 configuration boundary，产生不同 active sets 和 `V_i`，本证书中的 25 rows 随之不再是对应 cone 的完整有效描述。

## 7. 验证

新增：

- `verification/check_19pair_cc_exact_farkas.py`
- `results/cc_19pair_exact_farkas_20260924/checks.json`

运行：

```bash
python verification/check_19pair_cc_exact_farkas.py \
  --output results/cc_19pair_exact_farkas_20260924/checks.json
```

脚本会重建第48章 seed、核对 witness 涉及 vertex 的 active sets，然后使用 exact rational arithmetic 断言 `y^T A == 0` 和 `y^T b == -3069803/88290`。

## 8. 命题状态

- **已证明**：当前 frozen 模型的 thrust robustification 可精确归约到 endpoints（第41章）。
- **已证明（本轮）**：第48章 audited configuration cone 的 CC-RCI inequalities 严格不可行；存在 25-row rational Farkas certificate。
- **已证明（本轮）**：该 certificate 不依赖 torque bounds、pair-offset equalities 或 q-nonnegativity rows。
- **仍未解决**：同一 19-pair orientation family 的其他 configuration cones 是否可行；本证书不是 orientation-family-global obstruction。

## 9. 下一轮唯一优先问题

> 以本轮 25-row witness 涉及的 18 个 active sets 为中心，构造跨越其 configuration boundary 的最小邻接 cone 搜索：每次只改变一个 vertex/facet incidence，重新生成合法 entirely-simple seed 与 CC-RCI LP，并记录 Farkas support 是否持续存在。目标是判断 obstruction 是单一 cone 特有，还是能传播到一个可证明的邻域；在没有覆盖/全局证书前，不宣称整个 19-pair orientation family 不可行。
