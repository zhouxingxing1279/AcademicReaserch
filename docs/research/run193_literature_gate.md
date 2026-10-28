# Run193 文献准入卡：当前调度可见的 robust predecessor 量词纠正

日期：2026-10-28。

## 本轮问题

冻结合同声明当前推力 `T_k` 在施加力矩前已知，但旧 projected-predecessor checker 将同一个
`tau_k` 同时用于两个推力端点。两者分别对应

\[
\exists\tau\;\forall T
\quad\text{与}\quad
\forall T\;\exists\tau(T).
\]

本轮只问：按真实时序允许控制读取当前 `T_k` 后，前四层 endpoint-exact robust predecessor
是否改变？该问题直接决定后续 vertex/PWA RCI 综合应采用哪一种信息权限。

## 最近邻与阅读深度

1. Mulagaleti、Mejari、Bemporad，*Parameter-Dependent Robust Control Invariant Sets for LPV
   Systems With Bounded Parameter-Variation Rate*（IEEE TAC 2025，
   https://arxiv.org/abs/2309.02384）。本轮重读 Definition/Problem statement 式(4)--(6)、
   Sections 3.1--3.2、式(12)--(25)及算法步骤。其定义明确使用 `u=u(x,p)`：当前参数先测得，
   控制可依赖当前参数，同时必须覆盖允许的全部后继参数。PD vertex controls 和参数相关集合均
   已有，不是本项目创新。
2. Mejari、Mulagaleti、Bemporad，*Data-Driven Synthesis of Configuration-Constrained Robust
   Invariant Sets for Linear Parameter-Varying Systems*（L-CSS/ACC 2024，
   https://ipg.idsia.ch/preprints/mejari2023e.pdf）。本轮重读 Section III-C、Lemma 3及证明、
   Problem 1、Sections IV--V。其固定 configuration 的 vertex-control LP 是直接强基线；
   但正文式(16)采用与调度参数无关的 vertex input，属于更保守策略类。
3. Mejari、Gupta、Piga，*Data-Driven Computation of Robust Invariant Sets and Gain-Scheduled
   Controllers for Linear Parameter-Varying Systems*（L-CSS 2023，
   https://arxiv.org/abs/2309.01814）。本轮核对全文问题陈述与 gain-scheduled controller
   量词；它利用可用 scheduling measurement，说明调度可见反馈也不是新机制。
4. Hanema、Tóth、Lazar，*Tube-based anticipative model predictive control for linear
   parameter-varying systems*（CDC 2016，DOI 10.1109/CDC.2016.7798472）。本轮仅核对机构页
   摘要：当前 scheduling 精确测量、未来 scheduling 用集合描述，并采用 gain-scheduled
   vertex controls；未取得正文，故不引用其定理。

## 严格差异、最强基线与可证伪结果

本轮没有算法首次性。严格差异只是把仓库冻结四状态模型的 predecessor 量词与已声明的信息
时序对齐。最强同条件基线是允许 `tau=tau(x,T)` 的 common-set RCI；更强的 PD-RCI 还允许
集合本身依赖当前 `T`。

若 endpoint-local projection 在某层产生比 shared-torque projection 更大的多面体，则旧审计
存在可量化保守性；若前四层经独立冗余消除后相同，只能说明这四个有限层上量词差异没有改变
集合，不能推出所有层相同，更不能推出 RCI 存在。

## 准入判断

**通过（合同纠正与有限层基线审计）**。不通过新 RCI 算法、无限时域不变性、六状态安全或
递归可行性声明。允许新增独立 checker、回归测试与结果工件；禁止借此恢复 CZ 几何支线。
