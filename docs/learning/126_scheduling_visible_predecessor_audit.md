# 126 当前推力可见的 robust predecessor：量词纠正与旧精确算术缺陷

日期：2026-10-28。范围仅限四状态横向—姿态降阶基准。

## 1. 唯一问题

冻结时序规定当前推力 `T_k` 在施加力矩前可知，而未来推力可在
`[4.905,14.715] N` 内任意跳变。旧 predecessor 实现使用

\[
\exists\tau_k\ \forall T_k,
\]

即两个推力端点共享同一个力矩。真实信息权限应为

\[
\forall T_k\ \exists\tau_k(x_k,T_k).
\]

本轮比较两种量词的前四层 predecessor，不搜索新模板，也不把有限层当作 RCI。

## 2. 调度可见端点投影

给定目标多面体 `S={x:Hx<=q}`，对每个端点 `T_j` 和目标行 `r_i`，消除扰动后得到

\[
r_i^T A(T_j)x+r_i^TB\tau_j
+|r_i^TE|\left(1.880+T_j\frac{0.45^3}{6}\right)\le q_i.
\]

调度可见投影必须在每个端点内部单独对标量 `tau_j` 做 Fourier--Motzkin 消元；把低推力
下界与高推力上界交叉配对，会重新引入不存在的共同力矩约束。对区间内部的 `T`，端点控制
作仿射插值后，状态行、输入项和扰动 support 都关于 `T` 仿射，故端点成立可覆盖连续区间。
这只是当前仿射合同的已有 LPV 凸性工具，不是新算法。

## 3. 旧 checker 的精确算术缺陷

`check_projected_predecessor_layers.py` 声称使用 `Fraction` 构造全部行，但硬盒法向通过
`e[i]=1` 写入 Python `int`。其 `canon` 随后执行 `x/s`；当 `s` 也是 `int` 时，Python 产生
`float`。因此第一层 redundancy 后保留的行已经混入浮点数，后续 Fourier--Motzkin 行不能再
称为 exact-rational construction。

新 checker 用 `F(1)`/`F(-1)` 构造硬盒，并回归检查所有保留系数和 RHS 均为 `Fraction`。
旧工件与修正后前四层的非冗余 facet 数恰好仍同为 `16,28,52,102`；这只能说明该缺陷在本次
数值冗余审计中未改变 facet 数，不能恢复旧工件的“精确行构造”证据等级。

证据等级：旧实现缺陷为可执行的 **COUNTEREXAMPLE**；修正后候选行构造为 **DERIVED**；
冗余与多面体包含仍为 HiGHS `NUMERIC_CHECK`。

## 4. 前四层结果

| depth | 共同力矩 unique candidates | 调度可见 unique candidates | 两者非冗余 facets |
|---:|---:|---:|---:|
| 1 | 17 | 17 | 16 |
| 2 | 31 | 31 | 28 |
| 3 | 99 | 85 | 52 |
| 4 | 903 | 489 | 102 |

双向 LP 包含的最大 violation 不超过 `4.45e-16`，在冻结 `1e-7` 容差下，前四层两种量词的
保留多面体相同。调度可见投影显著减少了未消冗余候选行，但尚未扩大这四层的集合。

该结果**不能推出**所有深度相同、有限收敛、RCI 存在、力矩反馈已经实现、六状态安全或
MPC 递归可行。Gate A 仍为 blocked。

## 5. 文献边界与方向判断

Mulagaleti--Mejari--Bemporad 已明确采用 `u=u(x,p)` 的 PD-RCI，并覆盖允许后继参数；
Mejari--Gupta--Piga 已综合 gain-scheduled RCI controller。因此调度可见控制不是创新。
Mejari--Mulagaleti--Bemporad 的 configuration-constrained vertex-control LP仍是直接强基线。

本轮结果说明不能继续沿用旧共同力矩量词，但单纯纠正量词也没有在前四层扩大 viability
集合。下一步仍必须取得一个充分的调度可见 correlated controller/RCI 证书，或对明确策略/
集合类别给出反证；不回到局部 configuration-cone 邻接枚举。

## 6. 复现

```bash
python -m unittest verification/test_scheduling_visible_predecessor.py
python verification/check_scheduling_visible_predecessor.py \
  --max-depth 4 --output /tmp/run193_checks.json
```

归档：`results/scheduling_visible_predecessor_20261028/checks.json`。
