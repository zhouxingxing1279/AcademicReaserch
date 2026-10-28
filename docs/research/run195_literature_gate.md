# Run195 文献准入卡：调度可见 19-pair 配置锥复核

日期：2026-10-28。

## 本轮问题

仓库第 48--51 章已对一个审计过的 19-pair configuration cone 给出不可行与精确
Farkas 证书，但旧 LP 在每个状态顶点只配置一个力矩，并要求该力矩同时覆盖两个推力端点。
Run193 已冻结更准确的信息时序：当前推力在选力矩前可见。因此本轮只问：把每个顶点的
力矩改为端点相关的 `tau(v,T_low)` 与 `tau(v,T_high)` 后，该同一 19-pair 锥是否仍不可行？

## 最近邻与实际阅读

1. Mulagaleti, Mejari, Bemporad, *Parameter-Dependent Robust Control Invariant Sets for LPV
   Systems With Bounded Parameter-Variation Rate*, IEEE TAC 2024,
   DOI `10.1109/TAC.2024.3454528`, arXiv `2309.02384`。
   **全文定向阅读引言、定义(4)--(6)、Proposition 2 及证明、式(14)--(27)、Sections
   3.2--3.4。** 论文明确令调度参数在控制前可测，控制律为 `u(x,p)`；其 PD vertex law
   为本轮端点相关力矩的直接近邻。
2. Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust
   Invariant Sets for LPV Systems*, IEEE L-CSS 2023, arXiv `2309.06998`。
   **全文定向阅读引言、Lemma 3 的证明(77)--(81)、Sections IV--V 的式(85)--(88)。**
   该 CC-RCI 基线为每个集合顶点配置单一输入并共同覆盖所有调度顶点；仓库旧 19-pair
   LP 正是这一更保守量词。
3. Abbas et al., *Generalized Tube Model Predictive Control for Linear Parameter-Varying
   Systems with Bounded Rate of Parameter Variation*, Automatica 2019。
   **核查作者公开摘要、问题设置与递归可行性定理的可用正文摘录；未完成全文精读。**
   它把调度预览/未来调度集合纳入 tube MPC，但不直接给出本轮固定 19-pair 锥的证书。

## 严格差异、强基线与可证伪标准

本轮不提出新 RCI 算法，也不搜索新法向。严格差异仅是修正旧 19-pair LP 的控制量词：
集合 offset 仍与推力无关，但每个状态顶点在两个已知当前推力端点分别选择力矩；未来扰动
继续按对应 `W(T)` 最坏覆盖。最强同条件基线是完整 parameter-dependent CC/RCI 联合综合，
而不是旧的共享顶点输入 LP。

若修正后的完整 LP 可行，则旧证书失效，必须转向构造该候选的显式控制律。若不可行，仍
必须给出在扩展变量空间中逐系数为零、右端严格为负的精确 Farkas 证书；仅有 HiGHS
`infeasible` 不足以形成结论。任何结果都只适用于该 19-pair 锥，不能排除其他法向、
parameter-dependent offsets、非线性控制或六状态安全基线。

## 准入判断

**通过旧强基线的量词纠错与独立复核；不通过创新、一般 RCI 不存在性、六状态安全或
递归可行性声明。**

