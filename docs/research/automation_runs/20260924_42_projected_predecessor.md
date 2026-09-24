# 自动研究记录：第42轮 projected predecessor

- 仓库起点：`ad828718205f643bab6d71134cc1a43f5b9aa21b`
- 本轮问题：对第41章 endpoint-exact robust predecessor 真正执行 `exists tau` 投影、hard-set intersection 与 redundancy audit。
- 文献：Blanchini, *Set invariance in control*, Automatica 35(11), 1999, DOI `10.1016/S0005-1098(99)00113-2`；Rungger & Tabuada, *Computing Robust Controlled Invariant Sets of Linear Systems*, IEEE TAC 62, 2017；Gupta, Köroğlu, Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, IJ Robust Nonlinear Control, 2021。
- 已证明：对 scalar torque，加入 `|tau|<=0.08` 后的 Fourier-Motzkin elimination 给出精确 state-space projection；第2层解析地产生 torque-limited facet `|phi+0.04 omega|<=0.4516`。
- 数值证据：逐行缩放后的 HiGHS redundancy audit 给出 n=1..4 的 nonredundant facet counts `16,28,52,102`，四层均非空且包含原点。候选 unique inequalities 分别为 `17,31,135,1193`。
- 失败/限制：第5层在完整 redundancy audit 前已有 6655 个 unique candidates，逐 facet LP 超出本轮计算预算；因此没有宣称第5层 facet 数、有限收敛、集合为空或最大 RCI 不存在。
- 排除结论：第39章 deeper-chain normals 并不会在前四层被 torque projection 全部消掉；pairwise template 仍不足。
- 代码/结果：`verification/check_projected_predecessor_layers.py`；`results/projected_predecessor_layers_20260924/checks.json`；完整推导见 `docs/learning/42_projected_predecessor_first_layers.md`。
- 下一轮唯一优先问题：基于 n=1..4 存活法向簇构造低复杂度 H-template RCI synthesis，联合求 offsets 与 admissible vertex/torque controls；若 LP 不可行，输出可核查 infeasibility witness，以区分 template complexity 不足与 torque authority 不足。
