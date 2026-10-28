# Run192 文献准入卡：Gate A 控制基线证据审计

日期：2026-10-27。

## 本轮问题

仓库是否已经给出一个在已知当前推力、未来推力任意跳变、调度一致扰动
`W(T)`、全部状态硬约束和 `|tau|<=0.08` 下成立的 ancillary feedback/RCI
证书？如果没有，现有负结果究竟否定到哪一层？

## 最近邻与阅读深度

1. Mejari、Mulagaleti、Bemporad，*Data-Driven Synthesis of
   Configuration-Constrained Robust Invariant Sets for Linear
   Parameter-Varying Systems*（L-CSS 2023，arXiv:2309.06998）。重读
   Section III-C、Lemma 3、Problem 1、Section IV；其固定法向、可变 offset、
   vertex control 与状态/输入约束 LP 已覆盖 configuration-constrained RCI
   综合。当前仓库的配置锥探索不是新算法。
2. Mulagaleti、Mejari、Bemporad，*Parameter-Dependent Robust Control
   Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate*
   （IEEE TAC 2025，arXiv:2309.02384）。本轮精读 Problem statement、
   Sections 3.1--3.2、式(14)--(28)与算法步骤。其 PD-RCI 要求已知的下一参数
   集/变化率；仓库当前 `T` 是逐点受限直接输入，不能无依据借用小变化率。
3. Köhler、Soloperto、Müller、Allgöwer，*A computationally efficient
   robust model predictive control framework for uncertain nonlinear systems*
   （2020 extended version，arXiv:1910.12081）。本轮精读 Sections II--III，
   Assumptions 1--6、MPC (11)、Theorem 1及其 shift/terminal proof、
   Proposition 4。该文说明 state/input-dependent uncertainty、ancillary
   incremental feedback、tube tightening与terminal ingredients必须一起满足，
   才能推出递归可行和约束满足；名义稳定或单次 RCI 检查不足。
4. Rungger、Tabuada，*Computing Robust Controlled Invariant Sets of Linear
   Systems*（IEEE TAC 2017，arXiv:1601.00416）。沿用已精读的式(4)--(10)、
   Lemma 1、Theorems 1--2：有限 predecessor 层一般不是 RCI；近似/终止条件
   必须单独说明。

## 严格差异与最强基线

本轮不提出新综合法。严格差异仅是审计仓库冻结四状态横向模型的证据链：
`W(T)=1.880+T*0.45^3/6`，当前 `T` 可知、未来 `T` 任意跳变，并同时检查
状态与力矩权限。最强方法基线是 configuration-constrained vertex-control RCI；
若以后引入经过认证的推力变化率，PD-RCI 才成为合法更强基线。

## 可证伪结果

若现有归档中存在一个可重放的充分 RCI 证书，且覆盖全部 endpoint、扰动、
状态和 torque constraints，则“Gate A blocked”被推翻。若只有特定 `K` 的
reachable-support 反例、有限随机搜索失败、轴对齐盒反例或单一配置锥 Farkas
证书，则不能推出 static feedback、其他相关多面体或系统整体不可行。

## 准入判断

**通过（仅证据审计与方向纠正）**。不准入新 RCI/模板算法，也不继续邻接配置锥
枚举。本轮允许实现一个只读审计器：重放轻量证书、核对归档结论与源码 SHA-256、
明确 Gate A 仍缺的充分证书。其产物不是控制创新。
