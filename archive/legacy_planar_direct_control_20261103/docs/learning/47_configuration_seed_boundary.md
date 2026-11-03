# 47 Variable-offset CC-RCI 前必须固定 configuration seed

日期：2026-09-24。承接第46章，仓库起点 `88b030d4870f254536d339d83c7b23363cde2675`。

## 1. 本轮唯一问题

第46章留下的任务表述为：固定 `S2 normals + 五对 orientations`，允许 offsets 独立变化，建立 vertex-affine configuration LP。这里存在一个必须先闭合的逻辑前提：**“38 条 raw halfspaces 的 offsets 独立变化”是否能由从第46章 inherited-offset realization 构造的一套 vertex-affine map 全局覆盖？**

答案是否定的。这个结论不是 RCI 不可行性，而是对下一步 certificate domain 的严格限定。

## 2. 文献核查

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818–3823, DOI `10.1109/LCSYS.2023.3346128`, arXiv:2309.06998。

论文的 CC 参数化为

\[
\mathcal S(q)=\{x:Cx\le q\},
\]

并不是对任意 `q` 都直接使用同一 vertex map。它从一个 configuration 构造 vertex maps `V^i` 和 configuration cone

\[
\mathbb S=\{q:E q\le0\},
\]

然后只对 `q in S` 保证

\[
\mathcal S(q)=\operatorname{ConvHull}\{V^i q\}.
\]

其附录 Proposition 2 进一步以 entirely-simple seed polytope 为构造前提。因此 fixed orientation + variable offset 的 LP machinery 的关键是**保持所选 configuration domain**，而不是允许 offsets 任意跨越 facet/vertex incidence 改变的边界。

这与本项目的区别也必须说清：我们现在是 model-based endpoint-exact benchmark，不使用论文的数据驱动 model set；可复用的是 CC polytope 的几何参数化思想，而不是其 data-driven invariance condition。

## 3. 仓库当前 seed 的结构事实

第46章已经审计：

- raw halfspaces：38；
- inherited S3 offsets 下 redundancy elimination 后 active facets：30；
- 因而当前 seed 有 8 条 raw rows 是冗余的；
- 当前具体 realization 有 128 个数值 vertices，其中 96 个一步 torque 不可行。

因此 `38 raw orientations` 与 `当前 configuration 的 30 active facets` 不能混为一谈。

## 4. 命题：单个 inherited-seed CC map 不能认证任意 38-offset 变化

设当前 seed 为 `q0`，其 38 个 H-rows 中存在 8 个严格冗余 rows。由 seed configuration 构造的 vertex-affine maps `V^i q` 与 cone `E q<=0` 的保证域，是保持该 configuration 的 offsets 子集。

若某个 offset 变化使原本冗余的 row 成为真正 facet，则 facet/vertex incidence 已发生改变。此时该点若不属于原 cone，就不能继续援引原 seed 的

\[
\mathcal S(q)=\operatorname{ConvHull}\{V^i q\}
\]

作为 certificate。要覆盖该 realization，必须重新构造相应 configuration 的 vertex maps/cone，或使用能够显式处理多个 configuration 的方法。

所以：

\[
\boxed{\text{“19 对 orientations 独立 offsets”不是一个无条件的单 CC-LP 搜索域。}}
\]

正确的问题应是：先选择一个 entirely-simple seed configuration，构造 `(V^i,E)`，然后只在 `E q<=0` 内联合优化 offsets 和 vertex torques。

## 5. 为什么这不是措辞修正

如果忽略这个边界，可能出现两类错误：

1. LP 得到的 `q` 已经激活 seed 中原本冗余的 orientation，却仍用旧 vertex maps 检查 invariance；此时 vertex certificate 不再有已证明的几何依据。
2. 一个 configuration cone 内 LP infeasible，被错误外推为整个 19-pair orientation family infeasible。第44章已经明确展示过这种外推是不允许的。

因此下一步必须把“orientation family 是否可行”和“某一个 configuration cone 是否可行”分开报告。

## 6. 最小验证

新增 `verification/check_cc_seed_activation_boundary.py`。脚本读取第46章归档结果，断言 `38 raw - 30 active = 8 redundant rows`，并把“single-seed free-38-offset claim”标记为 false。

归档：`results/cc_seed_activation_boundary_20260924/checks.json`。

这不是数值 RCI certificate；它是对第46章已有数值几何事实与 CC 理论适用域的一致性检查。

## 7. 命题状态

- **已证明/文献条件**：CC vertex-affine representation 只在由所选 configuration 构造的 cone 内得到保证；entirely-simple seed 是所引用构造的前提。
- **仓库数值事实**：第46章 inherited-offset realization 的 38 raw rows 中仅 30 条 nonredundant，存在 8 条冗余 rows。
- **本轮排除**：不能从该 seed 构造一套 vertex maps 后，把 38 个 offsets 当作可任意跨 configuration boundary 的自由变量，并仍称其为同一个 CC certificate。
- **仍未解决**：是否存在某个明确、entirely-simple 的 19-pair configuration cone，使 endpoint-exact RCI LP 可行。

## 8. 下一轮唯一优先问题

> 对当前 19-pair orientation family 构造一个明确的 entirely-simple seed：优先从第46章 realization 做最小 offset perturbation，消除 degeneracy/冗余造成的 configuration 歧义；枚举其 active sets，生成 vertex-affine maps `V^i` 与 `E q<=0`。随后才在这个固定 cone 内联合求 offsets 与 vertex torques，并做两个 thrust endpoints 的 robust invariance LP。若不可行，只能排除该 cone；若要排除 orientation family，必须继续审计其他可达 configuration cones 或给出独立的全局不可行证明。
