# Run 47 — configuration seed boundary

- 仓库起点：`88b030d4870f254536d339d83c7b23363cde2675`
- 本轮问题：第46章 19-pair raw orientation family 是否能从 inherited-offset realization 直接建立一个允许 38 个 offsets 任意独立变化的单一 vertex-affine CC-LP？
- 文献：Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), DOI 10.1109/LCSYS.2023.3346128, arXiv:2309.06998。论文的 vertex maps 只在 `E q <= 0` configuration cone 内保证 H/V 表示等价，附录构造以 entirely-simple seed 为前提。
- 已得结论：不能把 fixed orientation + variable offset 误写成跨 configuration boundary 的全局自由 offset 参数化。第46章 seed 有 38 raw rows、30 active facets、8 redundant rows；若 offset 变化激活这些 rows 并改变 incidence，原 seed 的 vertex maps 不再自动构成 certificate。
- 失败/纠正：原“直接对 38 offsets 做一个 configuration LP”的任务表述过宽，必须先固定 seed configuration 与其 cone。
- 验证：`verification/check_cc_seed_activation_boundary.py` 对第46章归档计数做结构一致性检查；结果 `results/cc_seed_activation_boundary_20260924/checks.json`。
- 证据等级：CC cone 适用域来自文献理论；38/30/8 是第46章数值几何事实。本轮没有宣称 19-pair orientation family 不可行。
- 下一轮唯一优先问题：构造一个明确的 entirely-simple 19-pair seed configuration，生成 `V^i` 和 `E q<=0`，然后只在该 cone 内求 endpoint-exact RCI LP；不可行时只排除该 cone，不能外推整个 orientation family。
