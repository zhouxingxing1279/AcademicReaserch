# Run196 文献准入卡：参数相关 offset 的端点认证边界

日期：2026-10-29。

## 本轮唯一问题

Run195 的精确证书只否定参数无关 offset 的固定 19-pair configuration cone。下一候选允许
facet offset 随当前可见推力仿射变化。由于未来推力可在全区间任意跳变，本轮先问：是否还能
像 Run195 一样只检查当前推力两个端点并得到连续区间的可靠不变性证书？这决定后续综合器与
独立验证器的最小接口；若答案为否，就不应先写一个错误的 endpoint LP。

## 最近邻与实际阅读

1. Mulagaleti, Mejari, Bemporad, *Parameter-Dependent Robust Control Invariant Sets for LPV
   Systems With Bounded Parameter-Variation Rate*, IEEE TAC 70(2), 2025,
   DOI `10.1109/TAC.2024.3454528`，[作者全文](https://ipg.idsia.ch/preprints/mejari2025a.pdf)。
   **全文定向精读 Definition/Problem、Proposition 2、式(14)--(15)、(21)--(28)、SDP(33)及
   Section IV-A。** 定义要求当前切片对全部允许后继参数切片求交；固定法向、仿射 offset
   产生仿射顶点，配合仿射 LPV 动力学/vertex control 后，式(27)是关于当前参数的可能非凸
   二次不等式。作者用 S-procedure/LMI (28) 给充分条件，并明确固定法向、configuration 与
   S-procedure 都可能引入保守性。
2. Gupta, Mejari, Falcone, Piga, *Computation of Parameter Dependent Robust Invariant Sets for
   LPV Models with Guaranteed Performance*, Automatica 151 (2023) 110920,
   DOI `10.1016/j.automatica.2023.110920`，[全文](https://arxiv.org/pdf/2009.09778)。
   **全文定向精读 Sections 3--5，Definition 1、Problems 1--2、Lemma 3、式(11)、
   (14)--(28)、多项式条件(20)--(21)及LMI条件(37)--(40)。** 式(11)同样覆盖全部未知
   `xi(t+1)`，并把参数相关条件写成多项式矩阵不等式，再以 Polya 松弛得到充分 LMI；没有把
   参数相关集合的认证退化为当前参数端点检查。
3. Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust
   Invariant Sets for LPV Systems*, IEEE L-CSS 7 (2023),
   DOI `10.1109/LCSYS.2023.3346128`。**本轮仅复核仓库既有全文笔记，没有新增全文阅读。**
   其参数无关 set/vertex-input 条件关于调度仿射，端点/顶点化是 Run195 的强基线；它不覆盖
   参数相关顶点与 LPV 动力学相乘后的二次项。

## 严格差异、强基线与可证伪标准

本轮不提出 PD-RCI 新算法。最强同条件基线是上述 PD-RCI 的全参数多项式/SDP 充分条件。
本轮严格目标只是审计一个更弱但关键的认证主张：对标量调度、仿射 offset 与仿射动力学，
端点检查是否足以覆盖区间内部。若能构造有理数例子，使两个端点全部满足但某个内部点违反
共同后继目标，则 endpoint-only LP 被精确推翻；后续固定候选至少必须检查二次函数的区间
最大值。该反例不能推翻 PD-RCI、SDP/Polya 充分条件或不同集合法向。

## 准入判断

**通过“认证接口纠错与精确反例”；不通过“PD-RCI 创新算法”“19-pair 参数相关候选
不可行”“六状态安全”或“递归 MPC 可行”声明。** 该工作直接防止 Gate A 采用不可靠证书，
并为下一轮综合器冻结独立的全区间候选核查接口。
