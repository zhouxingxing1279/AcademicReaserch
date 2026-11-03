# 48 首个 entirely-simple 19-pair configuration cone 审计

日期：2026-09-24。承接第47章，仓库起点 `8d9908f72bef2c4a831cf687d2422b5bbc52771b`。

## 1. 本轮唯一问题

第47章指出：不能从 inherited-offset realization 的 30 个 active facets 构造 vertex maps 后，让全部 38 个 offsets 任意跨 configuration boundary 变化。本轮只解决一个更窄的问题：

> 对当前 `S2 normals + 第45章五对 orientations` 的 19-pair family，能否先构造一个 38 条 halfspaces 全部 active、且每个 vertex 恰由 4 个 facets 定义的 entirely-simple seed configuration；在该固定 configuration cone 内，endpoint-exact robust-invariance LP 是否可行？

这一步的目标不是排除整个 orientation family，而是第一次合法地执行第47章要求的 single-cone CC-RCI test。

## 2. 文献边界

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818--3823, DOI `10.1109/LCSYS.2023.3346128`, arXiv:2309.06998。

可复用的只是 configuration-constrained 几何参数化：固定 facet orientations、在一个 configuration cone 内用 offsets 参数化 vertices，再联合求 vertex controls。我们的 benchmark 是 model-based、thrust endpoint-exact 的 LPV 模型，并不采用论文的数据驱动 model set，因此不能直接复用其 data-based invariance condition。

## 3. 构造一个明确的 entirely-simple seed

从第42--46章的 `S2` 28 facets 提取 14 对 orientation，再加入第45章筛出的 5 对 orientation，共 19 对。对每个正向代表 `a_k`，构造中心对称 seed

\[
 a_k^T x\le q_k,\qquad -a_k^T x\le q_k.
\]

为了避免 inherited S3 offsets 造成的 8 条冗余 rows，本轮不再沿用 predecessor offsets，而取

\[
 q_k=\widehat{\|a_k\|_2}\left(1+\frac{k+1}{10000}\right),
\]

其中 `||a_k||_2` 先四舍五入到 `1e-8` 后存成有理数。这个构造只是为了获得一个可复现、generic 的 seed configuration，不赋予这些 offsets 物理意义。

数值枚举结果：

- 19 对 orientations / 38 raw halfspaces；
- 38 条全部 nonredundant；
- 160 个 vertices；
- 每个枚举 vertex 恰好 4 条 active facets。

因此在本轮数值几何审计精度下，这是一个 entirely-simple seed，可据此构造 160 个 vertex-affine maps `V_i q`。

证据等级：facet redundancy、vertex enumeration 和 simplicity 判定使用 NumPy/HiGHS，因此这里标记为**数值几何事实**，不是 exact-arithmetic theorem。

## 4. configuration cone 与 robust-invariance LP

对每个 seed vertex 的 active set `I_i`，令

\[
 x_i(q)=V_iq=C_{I_i}^{-1}q_{I_i}.
\]

configuration cone 使用全部

\[
 C_jV_iq\le q_j,
\]

共 `160*38=6080` 条 inequalities。保持中心对称 pair offsets 相等，共 19 条 equality constraints，并要求 `q>=0`。

随后对每个 vertex、每个 target facet 和两个 thrust endpoints `T_L,T_U` 加入

\[
 C_j(A(T)V_iq+B u_i)+|C_jE|\bar d(T)\le q_j.
\]

由于第41章已经证明当前 frozen 模型中该表达式关于 `T` 仿射，两个 endpoints 对连续 `T in [T_L,T_U]` 是精确 robustification，不是 thrust grid sampling。加入 invariance 后 inequalities 共 18240 条；再加入每个 vertex 的 hard-state containment 后总计 19520 条。变量为 38 个 offsets + 160 个 vertex torques，共 198 个。

## 5. 结果

HiGHS feasibility LP 得到：

1. `|u_i|<=0.08` 时 infeasible；
2. 移除 vertex torque bounds、令 `u_i` 无界后仍 infeasible。

因此在**这个明确的 entirely-simple configuration cone** 内，失败不能归因于 `0.08 N m` torque saturation：即使 vertex torque 无界，该 cone 与 endpoint-robust invariance 条件仍不相容。

严格表述为

\[
\boxed{\text{本轮 audited configuration cone 内未找到 CC-RCI，且放宽 torque bound 仍不可行。}}
\]

不能表述为

\[
\text{19-pair orientation family 不存在 RCI}.
\]

原因是其他 offsets 可能属于不同 configuration cones，具有不同 vertex incidence 和 vertex-affine maps。

## 6. 验证与可复现性

新增：

- `verification/check_19pair_cc_seed_cone.py`
- `results/cc_19pair_seed_cone_20260924/checks.json`

运行：

```bash
python verification/check_19pair_cc_seed_cone.py --output results/cc_19pair_seed_cone_20260924/checks.json
```

归档结果：38 active facets、160 vertices、160 个 vertices 均为 4-active 的 numerical entirely-simple seed；198 variables；6080 configuration inequalities；18240 configuration+invariance inequalities；19520 total inequalities；bounded 和 unbounded vertex-torque 两个 LP 均 infeasible。

## 7. 命题状态

- **已证明（承接第41章）**：当前 frozen 模型对 thrust interval 的 robust predecessor / facet inequality 可精确检查两个 thrust endpoints。
- **文献条件**：CC vertex-affine representation 必须限制在对应 configuration cone 内。
- **本轮数值事实**：构造了一个 38-active、160-vertex、numerically entirely-simple 的 19-pair seed configuration。
- **本轮数值排除**：该 cone 的 endpoint-exact CC-RCI LP 在 `|tau|<=0.08` 下不可行；移除 torque bound 后仍不可行。
- **仍未解决**：同一 19-pair orientation family 是否存在其他 configuration cone 可以支持 RCI；当前 infeasibility 尚无 exact Farkas witness。

## 8. 下一轮唯一优先问题

> 对本轮 198-variable LP 提取一个可复核的 infeasibility core / dual-Farkas witness，优先检查能否得到不依赖 torque bounds 的小规模证书，并识别它涉及的 vertex active sets 与 facet chains。若能把证书有理化并 exact-check，则可把“该 configuration cone 不可行”从数值结论升级为严格结论；若不能，则再设计对邻近 configuration cones 的系统审计，而不是直接宣称整个 19-pair orientation family 不可行。
