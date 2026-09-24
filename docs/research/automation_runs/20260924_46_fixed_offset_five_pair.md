# 自动研究记录：46 fixed-offset five-pair obstruction

- 仓库起点：`2f2a74d783626ec59711d18b0a7a65d9eb30b625`
- 本轮问题：第45章选出的 5 对 S3 新法向，在直接继承 S3 offsets 时是否已经形成 RCI？
- 关键文献：Gupta, Köroğlu, Falcone (2021), DOI `10.1002/rnc.5378`；Mejari, Mulagaleti, Bemporad, arXiv:2309.06998。
- 结论：否。raw 38 halfspaces 经 redundancy elimination 后为 30 facets；数值枚举 128 vertices，其中 96 个没有 admissible endpoint-robust torque 一步回到同一集合。
- 证据等级：数值几何审计；endpoint reduction 本身沿用第41章证明，但 redundancy/vertex enumeration 使用 HiGHS/浮点运算。
- 失败尝试/排除：不能把第45章“覆盖旧坏顶点”解释为 RCI；新增 halfspaces 产生新的 intersections/vertices。也不能把 raw 38 halfspaces 直接称为实际 38-facet polytope，因为继承 offsets 时仅 30 facets nonredundant。
- 新增代码：`verification/check_s2_plus_5pair_fixed_offsets.py`。
- 原始结果：`results/s2_plus_5pair_fixed_offsets_20260924/checks.json`。
- 理论记录：`docs/learning/46_fixed_offset_five_pair_obstruction.md`。
- 仍缺证明：同一 19 对 orientations 配合 independent offsets 与 vertex controls 是否存在 configuration-constrained RCI。
- 下一轮唯一优先问题：建立上述 variable-offset configuration LP；可行则保存 primal certificate，不可行则提取 IIS/Farkas witness。未排除前不增加剩余 S3 normals。
