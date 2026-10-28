# Run194 文献准入卡：S4 同心模板的 vertex-control RCI 门槛

日期：2026-10-28。

## 本轮问题

Run193 得到的第四层调度可见 predecessor 多面体 `S4` 是否能通过同心缩放
`alpha*S4`（`0<alpha<=1`）和当前推力可见的顶点力矩控制，形成一个充分 RCI 证书？
这不是继续增加 predecessor 深度，而是直接检查一个控制器/集合类别的无限时域自包含条件。

## 最近邻与实际阅读

1. Rungger, Tabuada, *Computing Robust Controlled Invariant Sets of Linear Systems*,
   IEEE TAC 2017, DOI `10.1109/TAC.2017.2672859`, arXiv `1601.00416`。
   **全文定向重读定义、式(4)--(10)、有限确定讨论、Lemma 1、Theorems 1--2及证明。**
   向下 predecessor 有限层通常不是 RCI；只有相邻层相等或论文给出的内近似停止条件才能
   升级为不变集。
2. Mulagaleti, Mejari, Bemporad, *Parameter-Dependent Robust Control Invariant Sets for LPV
   Systems With Bounded Parameter-Variation Rate*, IEEE TAC 2024,
   DOI `10.1109/TAC.2024.3454528`, arXiv `2309.02384`。
   **重读 Sections 1、3.1--3.4、定义、PD vertex-control 参数化和 SDP 充分条件。**
   当前调度可测时允许 `u=u(x,p)`；任意后继参数仍须统一覆盖。
3. Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust
   Invariant Sets for LPV Systems*, IEEE L-CSS 2023,
   DOI `10.1109/LCSYS.2023.3346128`。
   **重读 Section III-C、Lemma 3、Problem 1、Sections IV--V。** 固定法向、可变 offset
   和 vertex inputs 的单 LP 综合已经存在。
4. Mejari, Gupta, Piga, *Data-Driven Computation of Robust Invariant Sets and Gain-Scheduled
   Controllers for LPV Systems*, IEEE L-CSS 2023。
   **全文阅读 pp.1--6，重点 Problem 1、Section III-C、Theorem 1和算法。** 其增益调度控制
   与本轮 vertex control 都是强基线，但数据驱动模型集合不是本轮对象。

## 严格差异、强基线与可证伪标准

本轮不提出新表示或综合算法。固定 Run193 `S4` 的法向与 offset，只允许一个尺度 `alpha`，
并给予最有利的端点可见 vertex torque。最强比较基线是直接 configuration-constrained/PD-RCI
联合综合；因此本轮只能判定该 homothetic `S4` 类，不能排除其他法向、非同心 offset、PWA
或 PD-RCI 集合。

若找到 `S4` 的一个精确顶点，使某个推力端点下两条目标 facet 对全部 `alpha>0` 给出互斥
力矩上下界，则该候选类被精确否定。若不存在这种见证，再进入全顶点 LP 搜索并保持
`NUMERIC_CHECK` 等级。

## 准入判断

**通过受限候选类的充分 RCI 门槛审计；不通过创新、RCI 不存在性、六状态安全或递归可行性
声明。**
