# 46 五对新增法向在继承 S3 offsets 下仍非 RCI

日期：2026-09-24。承接第45章，仓库起点 `2f2a74d783626ec59711d18b0a7a65d9eb30b625`。

## 1. 本轮唯一问题

第45章从 `S3\\S2` 中选出 5 对新法向，证明它们在该候选池内是“切除全部 78 个旧 S2 非可行顶点”的最小组合，但明确没有证明扩展集合是 RCI。本轮先做进入 variable-offset configuration LP 前必须完成的边界检查：**若直接采用这些法向在 S3 predecessor 中已有的 offsets，得到的具体扩展 polytope 是否已经具备一步 robust controlled invariance？**

这一步的意义是区分“orientation selection 已足够，只需调 offsets”与“连继承 predecessor offsets 后的新 vertex geometry 仍明显失败”。

## 2. 文献边界

Gupta, Köroğlu, Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, IJ Robust Nonlinear Control 31(5), 2021, DOI `10.1002/rnc.5378`：论文明确指出候选 polytope shape 会影响结果，并建议用若干 geometric predecessor iterations 获得候选 shape；同时其方法不要求固定线性 state feedback，而可为 extreme points 求控制输入。因此，本轮 predecessor-derived orientation/offset 审计属于 baseline construction，不构成方法创新。

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, arXiv:2309.06998：使用 fixed facet orientation、variable offsets 的 configuration-constrained polytope，并通过 LP 联合求 RCI 与 vertex controls。这说明如果继承 offsets 失败，下一步合理动作是独立优化 offsets；但 variable-offset machinery 本身已有文献覆盖。

## 3. 构造

沿用第45章完全相同的 frozen benchmark、endpoint-exact predecessor 和 torque viability test。记第45章选出的 10 个 halfspaces 为 `H_add`，直接保留它们在 S3 中的 RHS，构造

\[
H_{\rm raw}=S_2\cap H_{\rm add}.
\]

原始表示有 28+10=38 条 halfspaces。对其做与第42/45章相同的 HiGHS redundancy elimination，再枚举四维 vertices。对每个 vertex `x_v` 检查是否存在同一个

\[
\tau\in[-0.08,0.08]
\]

使两个 thrust endpoints 上、对扩展集合每个 facet 都满足

\[
h_j^T(A(T)x_v+B\tau)+|h_j^TE|\bar d(T)\le q_j,
\qquad T\in\{T_L,T_U\}.
\]

由第41章 endpoint reduction，该 endpoint 检查对当前 affine-in-T 模型覆盖连续 thrust 区间；但 vertex enumeration/redundancy 仍是浮点数值审计，因此本章不把计数写成 exact theorem。

## 4. 结果

审计得到：

- S2：28 facets；
- 加入 10 个候选 halfspaces 后 raw representation：38 条；
- redundancy elimination 后：30 个 nonredundant facets；
- 扩展 polytope：128 个数值枚举 vertices；
- 其中 96 个不存在 admissible endpoint-robust torque 回到同一扩展集合；
- 只有 32 个通过一步 viability test。

因此

\[
\boxed{S_2+\text{五对选中法向，若直接继承 S3 offsets，则不是 RCI。}}
\]

这个结果还暴露了第45章 set-cover 的关键限制：它只切除了“旧的 78 个坏 S2 vertices”，但加入新 halfspaces 后会产生新的 intersections。当前具体 realization 中 vertex 数从 98 增至 128，且 96 个新集合 vertices 不可行，所以旧顶点覆盖不能替代 configuration synthesis。

另一个值得记录的事实是：10 条新增 halfspaces 在继承 offsets 时只有 2 条对最终 H-representation 提供非冗余贡献（总 facet 数由 28 变为 30）。因此“38-facet template”应严格理解为 **19 对候选 orientations 的 raw template**；具体 offsets 决定其中多少 facets 真正 active。后续不能把 raw orientation 数直接当实际 polytope complexity。

## 5. 证据等级与不能外推的结论

**数值审计结论**：继承 S3 offsets 的该具体 realization 非 RCI；128 个枚举 vertices 中 96 个一步 torque 不可行。

**不能外推**：本章没有排除同一 19 对 orientations 配合独立 variable offsets；也没有排除 configuration incidence 改变后形成的其他 polytope。第44章 exact Farkas certificate 只针对 S2-incidence configuration cone，本章也没有把它扩展成 19 对法向的全局不可行定理。

## 6. 可重复验证

脚本：`verification/check_s2_plus_5pair_fixed_offsets.py`。

运行：

```bash
cd verification
python check_s2_plus_5pair_fixed_offsets.py \
  --output /tmp/s2_plus_5pair_fixed_offsets.json
```

归档：`results/s2_plus_5pair_fixed_offsets_20260924/checks.json`。

预期：`nonredundant_augmented_facets=30`，`augmented_vertices=128`，`nonviable_augmented_vertices=96`。

## 7. 命题状态更新

- **已证明（第44章）**：S2-incidence configuration cone 在当前 torque bound 下不可行，存在 exact Farkas certificate。
- **数值组合最优（第45章）**：在 S3\\S2 候选池内，切除全部旧坏 S2 vertices 至少需 5 对新法向。
- **本章数值排除**：这 5 对法向若直接继承 S3 offsets，具体扩展 polytope 仍非 RCI。
- **仍待解决**：同一 19 对 raw orientations 是否存在 independent offsets + vertex controls 的 configuration-constrained RCI certificate。

## 8. 下一轮唯一优先问题

> 固定 `S2 normals + 第45章五对 orientations`，不继承 S3 offsets；选择一个明确的 configuration domain，建立 vertices 对独立 offsets 的仿射映射，并联合求 offsets 与 vertex torque controls。必须对两个 thrust endpoints 做 robust invariance，且保存 LP primal certificate；若不可行，则提取 IIS/Farkas witness。只有这一 variable-offset 问题被严格排除后，才允许继续增加剩余 S3 normals。
