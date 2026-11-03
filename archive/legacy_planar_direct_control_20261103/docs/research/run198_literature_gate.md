# Run198 文献准入卡：固定 affine-offset 综合的 SOCP 能力门

日期：2026-10-29。

## 本轮唯一问题

Run197 已把每条标量区间二次条件精确写成 `2 x 2` LMI。本轮只核查：冻结的
38-facet、160-vertex affine-offset 综合能否在当前仓库环境中以可复现的锥规划求解，并且
其规模与求解能力边界能否独立审计。

## 最近邻与实际阅读

1. Mulagaleti、Mejari、Bemporad，*Parameter-Dependent Robust Control Invariant Sets for LPV
   Systems With Bounded Parameter-Variation Rate*, IEEE TAC 70(2), 2025，DOI
   `10.1109/TAC.2024.3454528`，[作者全文](https://ipg.idsia.ch/preprints/mejari2025a.pdf)。
   **重读式(28)、SDP(33)、算法步骤4与Section IV求解环境。** 论文用YALMIP/MOSEK求解一般
   PD-RCI SDP；fixed normals、configuration constraints及S-procedure均可能引入保守性。
2. Fawzi，*On Representing the Positive Semidefinite Cone Using the Second-Order Cone*,
   Mathematical Programming 175 (2019)，DOI `10.1007/s10107-018-1233-0`，
   [开放正文](https://link.springer.com/article/10.1007/s10107-018-1233-0)。**精读Introduction
   式(1)、Theorem 1及表示范围。** `2 x 2` PSD cone与三维Lorentz cone精确同构；该事实不
   延伸到一般`3 x 3` PSD cone。
3. Goulart、Chen，*Clarabel: An Interior-Point Solver for Conic Programs with Quadratic
   Objectives*, Mathematical Programming Computation, 2026，DOI
   `10.1007/s12532-026-00320-7`，[开放正文](https://link.springer.com/article/10.1007/s12532-026-00320-7)。
   **定向精读Sections 2.1--2.2。** 论文明确给出解/不可行解释并支持nonnegative、Lorentz、
   PSD与zero cones；是下一步可锁定的开源求解器候选，但当前环境未安装。

## 严格差异、最强基线与可证伪标准

本轮不提出新RCI算法。最强方法基线仍是Mulagaleti等的fixed-normal PD-RCI SDP；本轮只把
Run197的`2 x 2` LMI逐条精确转换成SOCP，并审计当前环境。对
`Q=[[q00,q01],[q01,q11]]`，精确等价约束为

`norm([2*q01,q00-q11],2) <= q00+q11`。

恒等式
`(q00+q11)^2-(4*q01^2+(q00-q11)^2)=4 det(Q)`
由纯有理数checker核对。若矩阵阶数不是2、右端未约束非负或该恒等式失败，则SOCP转换无效。
若环境没有真锥求解能力，则HiGHS LP、有限网格或局部非线性优化都不能替代完整区间证书。

## 准入判断

**通过“精确SOCP等价、问题规模与求解依赖门审计”；不通过“当前环境执行数值综合”。**
因此本轮不实现伪求解器，也不报告19-pair可行或不可行。数值可行性保持`OPEN`，Gate A仍
`blocked`。下一步必须先提供锁定版本的SOCP solver，再求解并独立复核全部6080条区间条件。
