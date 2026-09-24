# 50 由 exact Farkas circuit 缩小邻接 configuration-cone 搜索

日期：2026-09-24。承接第49章 exact 25-row Farkas certificate，起点 `bbf22e9c65b3461b6118d334355102e9f21f5e7d`。

## 1. 本轮唯一问题

第49章已经严格排除了一个 audited 19-pair configuration cone，但下一轮若直接枚举 witness 涉及的 18 个 vertex active sets 周围所有 incidence boundary，组合量仍然较大。本轮先回答：

> 第49章 25-row Farkas support 是否已经是 support-minimal 的正线性 circuit？若是，哪些 configuration inequalities 对该矛盾真正不可删除，从而哪些 boundary 才值得优先跨越？

这是邻接 cone 搜索的必要筛选问题，不改变 RCI 模型或 thrust endpoint 合同。

## 2. 文献边界

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818--3823, DOI `10.1109/LCSYS.2023.3346128`，继续提供 configuration-constrained polytope 的固定法向/可变 offset 与 vertex-map 框架。本章不把该框架当创新。

本轮新增内容是对**我们自己的第49章不可行证书**做 oriented-matroid/linear-circuit 意义上的最小性审计：对选中的 inequality coefficient rows 计算 exact rational rank，并利用已知严格正 Farkas multiplier 判断该 support 是否为 circuit。

## 3. exact circuit 判据

第49章 25 条不等式写成

\[
a_k^Tz\le b_k,\quad k=1,\ldots,25,
\]

且已有严格正有理向量 `y` 满足

\[
y^TA=0,\qquad y^Tb=-3069803/88290<0.
\]

本轮重新用 rational facet normals、active-set inverse 与 `Fraction/SymPy` 构造 25 个 coefficient rows，得到

\[
\boxed{\operatorname{rank}_{\mathbb Q}(A)=24.}
\]

因此 `A^T` 的 nullspace 维数恰为 1。又因为第49章的唯一已知 null vector `y` 的 25 个分量全部严格非零，所以不存在任何 proper subset 的 rows 仍线性相关：否则将得到一个带零分量、与 `y` 不成比例的第二个 null vector，与 nullity=1 矛盾。

故这 25 rows 构成一个**support-minimal positive linear circuit**。这比“找到了一个稀疏 Farkas support”更强：对这一特定矛盾，25 条中的每一条都不可删除。

## 4. 对邻接 cone 搜索的直接含义

25-row circuit 中只有 4 条 configuration-cone inequalities：

- vertex 15: active `[0,6,11,19]`, entering facet `5`；
- vertex 17: active `[0,6,19,33]`, entering facet `5`；
- vertex 60: active `[1,7,10,18]`, entering facet `4`；
- vertex 62: active `[1,7,18,32]`, entering facet `4`。

因为它们也具有严格正 multiplier，四条都对当前 circuit 必不可少。于是：

> 若只跨越一个与这四条无关的 configuration boundary，而上述四条仍作为新 cone 的有效 inequalities 保留，则第49章这组 25 条有效 inequalities 仍然给出同一个 Farkas 矛盾；这种 boundary 不可能消除**该 exact obstruction**。

因此邻接搜索不再需要围绕 18 个 witness vertices 无差别展开，第一优先级严格缩小到这四个 certificate-critical boundaries。

注意这不是说跨越其中任意一个 boundary 就会得到可行 RCI；它只说明要破坏当前 exact circuit，至少必须使其中一条 critical configuration inequality 不再属于新 cone 的有效 certificate system。

## 5. 单 boundary 的局部 flip 候选

在每个 critical boundary 上，将 entering facet 加入原 4-active set，得到 5-row boundary incidence；枚举删除一条旧 facet 后仍保持 4x4 normal matrix 非奇异的 active set。exact determinant 检查得到每个 boundary 3 个 nondegenerate replacements，共 12 个：

- v15 / enter 5: `[0,5,11,19]`, `[0,5,6,19]`, `[0,5,6,11]`；
- v17 / enter 5: `[0,5,19,33]`, `[0,5,6,33]`, `[0,5,6,19]`；
- v60 / enter 4: `[1,4,10,18]`, `[1,4,7,18]`, `[1,4,7,10]`；
- v62 / enter 4: `[1,4,18,32]`, `[1,4,7,32]`, `[1,4,7,18]`。

这些只是**局部非退化 flip candidates**。要成为真正邻接 configuration cone，还必须构造一个全局 entirely-simple seed，使所有 vertex incidences 一致，并重新生成完整 `Eq<=0`、endpoint-robust invariance 与 hard-state constraints。

## 6. 验证与证据等级

新增 `verification/check_19pair_farkas_circuit.py`。脚本复用第48/49章的 seed construction 和 exact row reconstruction，检查：

1. 25-row coefficient matrix 的 rational rank 精确等于 24；
2. 第49章全部 multipliers 严格为正；
3. `y^TA=0` 与 `y^Tb=-3069803/88290` 继续 exact 成立；
4. 四个 critical 5-row boundary incidences 各有 3 个 non-singular 4-row replacements。

结果归档 `results/cc_19pair_farkas_circuit_20260924/checks.json`。

其中 rank、nullity、circuit minimality 和 12 个 determinant 非零判断均为 exact rational 结论；但“12 个 candidate 中哪些能扩展成合法邻接 cone”仍未证明。

## 7. 命题状态

- **已证明**：第49章 audited cone 严格 infeasible。
- **已证明（本轮）**：第49章 25-row support 是 support-minimal positive linear circuit，rank=24、left nullity=1。
- **已证明（本轮）**：当前 exact circuit 只依赖 4 条 configuration inequalities；若不使至少一条失效，就不能破坏这一证书。
- **已证明（本轮）**：四个 critical boundary 共给出 12 个 nondegenerate local active-set replacements。
- **未解决**：这些 local flips 中哪些对应真实可达的 neighboring entirely-simple configuration cones；跨越后是否出现新的 Farkas certificate 或可行 primal RCI。

## 8. 下一轮唯一优先问题

> 只围绕本章四个 certificate-critical boundaries 构造真正的 neighboring entirely-simple seeds。优先测试 12 个 nondegenerate local flips（利用中心对称性去重），对每个成功构造的邻接 cone 重建完整 CC-RCI LP：若可行保存 primal certificate；若不可行提取并有理化新的 Farkas witness。不要再对与当前 circuit 无关的 configuration boundaries 做盲目枚举。
