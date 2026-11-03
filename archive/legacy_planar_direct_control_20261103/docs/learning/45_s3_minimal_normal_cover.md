# 45 S3 新法向对 S2 非可行顶点的最小覆盖

日期：2026-09-24。承接第44章，仓库起点 `5e112e76afdd251e1062d78bc9142a0cbb097c5d`。

## 1. 本轮唯一问题

第44章用 exact Farkas certificate 排除了保持 S2 incidence 的 28-facet configuration cone，并明确下一步应从 S3 新法向中寻找最小几何增量，而不是直接使用完整 52 facets。本轮因此只回答：**S3\\S2 的哪些新 halfspaces 是切除 S2 上 endpoint-robust torque 不可行顶点所必需的最小候选集合？**

这一步是几何 triage，不把“切掉旧坏顶点”误写成 RCI 证明。

## 2. 文献接口与创新边界

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, arXiv:2309.06998：用固定 facet orientation、可变 offsets 的 configuration-constrained polytope，把 vertices 表成 offsets 的仿射函数，并通过 LP 联合求 RCI 与 vertex controls。本轮只借用“先选 orientation 再做 configuration LP”的思想；法向选择本身尚不是新理论。

Gupta, Köroğlu, Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, IJ Robust Nonlinear Control 31(5), 2021, DOI `10.1002/rnc.5378`：指出 predefined-complexity RCI 的初始 polytope shape 会影响结果，并建议可用几步 geometric predecessor 获得候选 shape。本轮正是把这一建议具体化为当前 frozen quadrotor benchmark 的 predecessor-derived orientation selection；不能把 fixed-complexity RCI 本身作为创新点。

## 3. 审计定义

沿用第42章 endpoint-exact predecessor。数值 redundancy audit 给出 `S2` 28 facets、`S3` 52 facets。枚举 S2 的四维 vertices；对每个 vertex `x_v` 精确构造 endpoint robust inequalities，并数值求当前 torque interval：

\[
\tau\in[-0.08,0.08],\qquad
h_j^T(A(T)x_v+B\tau)+|h_j^TE|\bar d(T)\le q_j,
\quad T\in\{T_L,T_U\}.
\]

若这些标量不等式的 torque interval 交为空，则称该 S2 vertex 对“一步回到 S2”不可行。

审计得到 98 个 S2 vertices，其中 78 个不可行、20 个存在 admissible torque。随后只考虑 `S3\\S2` 的 38 个新 halfspaces，并建立 set-cover：每个新 halfspace 覆盖它严格切除的非可行 S2 vertices，求覆盖全部 78 个坏顶点所需 halfspaces 的最少数量。

## 4. 结果：最少 10 个 halfspaces，即 5 对对称法向

HiGHS 0-1 MILP 的最优值为 10；选出的 10 条恰好组成 5 对中心对称 halfspaces。代表性正向法向为

\[
[1,3/50,-2943/500000,-981/25000000],
\]
\[
[1,3/50,-8829/500000,-2943/25000000],
\]
\[
[0,1,-2943/10000,-2943/500000],
\]
\[
[0,1,-8829/10000,-8829/500000],
\]
\[
[0,0,1,3/50],
\]

并包含它们的相反法向。完整 rational coefficients 与 RHS 保存于结果 JSON。

因此，在**限定候选池为本次 S3\\S2 38 个新 halfspaces、并限定目标为切掉所有当前 S2 非可行 vertices**时，少于 5 对新法向不能完成该任务；5 对可以完成。

## 5. 这不是 RCI 证明

本轮最重要的限制是：旧 vertices 被切除后，新增 facets 会产生新的 intersections / vertices；这些新 vertices 仍可能没有 admissible torque。因此“5 对”只是下一轮 configuration synthesis 的最小几何候选，不是 RCI 所需 facet complexity 的全局下界。

同样，set-cover optimality 依赖第42章的浮点 redundancy classification、浮点 vertex enumeration 与 HiGHS MILP，因此标记为**数值组合审计事实**，不是 exact-arithmetic theorem。第44章的 Farkas 不可行证书仍是 exact 结论，两者不可混淆。

## 6. 可重复验证

新增 `verification/check_s3_minimal_normal_cover.py`：Fraction 构造 endpoint/Fourier-Motzkin inequalities；HiGHS 做 redundancy、vertex feasibility 与 0-1 minimum set cover。归档结果：`results/s3_minimal_normal_cover_20260924/checks.json`。

运行：

```bash
python verification/check_s3_minimal_normal_cover.py \
  --output /tmp/s3_minimal_normal_cover.json
```

预期审计量：S2 facets=28，S3 facets=52，S2 vertices=98，非可行 vertices=78，新 S3 halfspaces=38，minimum cover=10 halfspaces=5 symmetric pairs。

## 7. 命题状态更新

- **已证明（第44章）**：S2-incidence configuration cone 在当前 torque bound 下不可行，存在 exact Farkas certificate。
- **数值审计**：S2 的 98 个 vertices 中 78 个不能在 endpoint-robust 条件下用 admissible torque 一步回到 S2。
- **数值组合最优**：在 S3\\S2 新 halfspace 候选池中，覆盖这 78 个坏顶点至少需要 10 条，存在 10 条的覆盖，因此该候选池内最优值为 10（5 对）。
- **未证明**：加入这 5 对后得到的 variable-offset configuration polytope 是 RCI。
- **未证明**：5 对是所有可能 orientation family 中的全局最小复杂度。

## 8. 下一轮唯一优先问题

> 只使用 `S2 normals + 本章 5 对新增 S3 normals` 构造扩展 configuration-constrained LP，重新枚举其 configuration vertices，联合求独立 offsets 与 vertex torque controls，并在两个 thrust endpoints 上做 robust RCI certificate。若不可行，优先提取 IIS/Farkas witness，判断失败来自新产生的 vertex chain 还是 torque authority；只有该 38-facet（19 对）候选被排除后才继续增加 S3 normals。
