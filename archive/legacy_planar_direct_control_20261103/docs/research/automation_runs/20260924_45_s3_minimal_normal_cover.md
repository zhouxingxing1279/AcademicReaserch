# Run 45 — S3 minimal normal cover

- 起点：`5e112e76afdd251e1062d78bc9142a0cbb097c5d`。
- 唯一问题：在第44章 S2-incidence Farkas obstruction 后，寻找 S3 新法向中切除全部 S2 一步 torque-不可行 vertices 的最小子集。
- 文献：Mejari–Mulagaleti–Bemporad, arXiv:2309.06998；Gupta–Köroğlu–Falcone, IJRNLC 2021, DOI 10.1002/rnc.5378。
- 结果：第42章数值 H-representation 下，S2 有 98 vertices，其中 78 个不能用 `|tau|<=0.08` 在两个 thrust endpoints 与 residual guarantee 下回到 S2；S3\\S2 有 38 个新 halfspaces。0-1 set-cover 最优值为 10 halfspaces，恰为 5 对中心对称 normals。
- 状态：这是数值组合审计，不是 RCI 证明；第44章 exact Farkas certificate 不受影响。
- 失败/边界：不能由“切掉旧坏顶点”推断 augmented polytope RCI，因为新增 facets 会生成新 vertices；也不能宣称 5 对是全局最小 orientation complexity。
- 验证：`verification/check_s3_minimal_normal_cover.py`；结果 `results/s3_minimal_normal_cover_20260924/checks.json`。
- 下一轮唯一优先问题：用 S2 normals + 这 5 对 S3 normals 构造 38-facet variable-offset configuration LP，重新建立 vertex maps 并求 endpoint-exact RCI certificate；若不可行则提取 IIS/Farkas witness。
