# Run197 文献准入卡：标量调度区间的精确二次 SDP 合同

日期：2026-10-29。

## 本轮唯一问题

Run196 已用纯有理反例否定 affine-offset PD-RCI 的 endpoint-only 认证。本轮只回答其直接后继：
在冻结的单一标量推力区间上，19-pair 固定 active-set family 的每条二次 vertex/facet 条件，
能否不采样、也不引入通用多约束 S-procedure 的额外间隙，精确转成凸约束？

## 最近邻与实际阅读

1. Pólik, Terlaky, *A Survey of the S-Lemma*, SIAM Review 49(3), 2007,
   pp.371--418，DOI `10.1137/S003614450444614X`，
   [作者存档页](https://optimization-online.org/2004/10/968/)。**定向精读 Theorem 2.2
   （S-lemma）及其 Slater 条件、Section 3 的 S-procedure 形式。** 对单个二次约束，若存在
   严格可行点，则区间内二次非负等价于存在一个非负乘子，使相应全局二次型 PSD；不是只有
   充分性。
2. Mulagaleti, Mejari, Bemporad, *Parameter-Dependent Robust Control Invariant Sets for LPV
   Systems With Bounded Parameter-Variation Rate*, IEEE TAC 70(2), 2025,
   DOI `10.1109/TAC.2024.3454528`，
   [作者全文](https://ipg.idsia.ch/preprints/mejari2025a.pdf)。**重读式(26)--(28)、
   Remarks 4--5与SDP(33)。** 其多维多面体调度集用通用 S-procedure 给充分 LMI，作者明确
   记录潜在 duality gap；这不妨碍本轮对单变量单区间约束使用精确 S-lemma 特化。
3. Gupta, Mejari, Falcone, Piga, *Computation of Parameter Dependent Robust Invariant Sets for
   LPV Models with Guaranteed Performance*, Automatica 151 (2023) 110920，
   DOI `10.1016/j.automatica.2023.110920`，
   [作者条目](https://manasdm.github.io/publication/j8-aut23/)。**复核 Run196 已精读的
   Definition 1、式(11)、多项式条件(20)--(21)与 Polya LMI (37)--(40)。** 它确认
   参数相关集合必须覆盖完整当前参数域和全部未来参数；Polya 是一般多项式充分路线，不是
   本轮一维二次精确表示的首次性来源。

## 严格差异、强基线与可证伪标准

本轮不提出 PD-RCI 新算法。最强基线仍是 Mulagaleti 等的 fixed-normal PD-RCI SDP。本轮仅
把其一般参数二次条件在仓库的**一个标量推力区间**上专门化。令归一化调度 `s in [-1,1]`，
`f(s)=a s^2+b s+c`。由于 `1-s^2>0` 在 `s=0`，S-lemma 给出精确等价：存在
`lambda>=0`，使

`Q=[[c-lambda,b/2],[b/2,a+lambda]] >= 0`。

反证标准很直接：若系数恒等式、乘子非负或 PSD 主子式任一失败，则该 LMI 不是有效证书；
而即使全部通过，也只认证一条冻结二次条件。完整综合仍受 fixed configuration cone、共同
后继 core 与四状态局部模型限制。

## 准入判断

**通过“精确标量区间 LMI 合同与独立有理证书检查器”；不通过“19-pair 数值可行”、
“Gate A 通过”“六状态安全”或“递归 MPC 可行”声明。** 本轮先冻结可靠综合接口，不安装
新 SDP 依赖；下一轮才运行 6080 条 LMI 的数值综合并把返回候选送回 Run196 全区间验证器。
