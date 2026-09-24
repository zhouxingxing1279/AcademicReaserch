# 自动研究记录：S2 homothetic template obstruction

日期：2026-09-24
起点：`7397ce81daa534ccd65bbac46e9d2be1bdc8bcb2`

## 本轮问题

第42章要求构造有限复杂度 correlated RCI。本轮先检验最低成本候选 `P_alpha=alpha S2, 0<alpha<=1`，判断简单统一缩放是否足以获得 RCI。

## 阅读文献

1. A. Gupta, H. Koroglu, P. Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, International Journal of Robust and Nonlinear Control, 31(5), 1674-1688, 2021. DOI: `10.1002/rnc.5378`. 论文证明/构造的是预定义复杂度 RCI，并允许 extreme-point controls；它提示 shape selection 重要，但不提供本项目特定 S2 的可行性结论。
2. M. Mejari, S. K. Mulagaleti, A. Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters / ACC 2024, arXiv:`2309.06998`. 使用 fixed orientation + variable offsets 的 configuration-constrained polytope 和 vertex controls；说明下一轮独立 offset synthesis 有直接成熟方法近邻，因此不能把该参数化本身当创新。

## 已得到结论

构造 S2 exact vertex

`x*=(-5,0,-6254383/15696000,2)`

以及 S2 retained facet

`r=(-1,-1/25,981/500000,0)`, `q=39993745617/8000000000`。

在 `T_L=981/200`，该 facet 的 nominal slack coefficient 为 `5940463/4000000000`，而最坏 disturbance support 为 `6254383/4000000000`，严格缺口 `981/12500000=7.848e-5`。因为 `r^T B=0`，torque 无法改变该一步违反。对 `alpha*S2`，必要条件要求 `alpha>=6254383/5940463≈1.052844`，故所有 `0<alpha<=1` 均被严格排除。

## 失败尝试/边界

没有把该结论扩大成“S2 normals 不可行”。统一缩放失败只证明单参数 offset family 太弱；独立 offsets 会改变顶点和 slack，仍可能得到 RCI。也不能把该失败归因于 torque saturation，因为 witness row 对当前 torque 完全不敏感。

## 验证

`verification/check_s2_homothetic_rci_obstruction.py` 使用标准库 Fraction 精确复算全部有理数并断言 gap；结果归档于 `results/s2_homothetic_rci_obstruction_20260924/checks.json`。

## 下一轮唯一优先问题

固定 S2 的 28 个 normals，按 configuration-constrained polytope 有效配置域允许对称 facet pairs 独立 offsets，联合求 vertex torque controls，并对两个 thrust endpoints 做 robust certificate。若 LP 不可行，必须保存 Farkas/infeasibility witness 后才升级 S3/S4 normals。
