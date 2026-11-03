# 116. 局部 lifted-cell 证书不等于可组合 cell graph

日期：2026-10-26。本章纠正第 114--115 章之后的直接扩展方向：两轮已认证 estimator 与
tracking target normals，但尚未认证 successor 可见坐标进入下一 source cell。

## 被遗漏的 target-cell 义务

两轮 source 都使用

```math
D_0=\{(d_p,d_v): |d_p|\leq1/5,\ |d_v|\leq1/4\},\qquad d=e-\eta.
```

若把这些局部证书当作 cell graph 的 nodes，则每条边还必须满足 `d^+ in D_0`，或显式落入
另一个已定义 target cell。只证明 `eta^+` 进入 mode projection、`e^+` 进入 tracking box 并不
蕴含这项条件。

## 两条 miss 边的精确非包含

零修正 miss 下

```math
d_p^+=d_p+h d_v,\qquad d_v^+=d_v,\qquad h=1/50.
```

因此 `0->1 miss` 和 `4->5 miss` 都有

```math
h_{d_p^+}=\frac15+\frac1{50}\frac14=\frac{41}{200}
>\frac15,
\qquad h_{d_v^+}=\frac14.
```

位置方向恰好超出 `1/200`。所以即使 Run180/181 的 estimator/tracking normals 全部闭合，
相同 centered `D_0` 也不能作为这两条 miss 边的 target cell。

## mode-4 success 的精确可见像

从 Run181 的同一组联合 `(eta^+,e^+)` primitive columns 逐列作差，保留同一 success innovation，
得到 `4->0 success` 的可见坐标支持

```math
h_{d_p^+}=\frac{2624143}{7200000},\qquad
h_{d_v^+}=\frac{1548143}{1600000}.
```

相对 `D_0` 的超量分别为

```math
\frac{1184143}{7200000},\qquad
\frac{1148143}{1600000}.
```

success 的两个方向均严格越界，且速度半宽约为 `0.9676`，远大于原 `1/4`。物理 residual
在 `d=e-eta` 中按共享 realization 抵消；这里没有把 estimation error 或 residual 当作独立未来
扰动。按联合生成元分解，越界来自 source `eta`、source `d` 与测量创新的合法传播；其中
source `eta` 对上述位置/速度支持分别贡献约 `0.13946` 与 `0.62759`，不可省略。

## 文献排重与方向纠正

Hempel--Kominek--Werner 的显式 output-feedback controller 已要求各 PWA 分区覆盖完整 admissible
output set，并通过公共细化获得单值策略；Houska 的 configuration-constrained polytopic
information ensemble 进一步给出固定模板、extreme-set controls、全 ensemble 插值和 invariant
terminal ensemble。故“继续手工增加 overlapping cells”不是可辩护的创新路线。

本章只证明：**Run180/181 当前 cells 不能直接作为相互接续的 cell-graph nodes。** 它不证明
有限 cover 不存在，也不排除 translated/larger cells、PWA policy 或 Houska 型 information
ensemble。证据等级为
`exact_visible_successor_support_noncontainment_certificate`。

下一唯一问题：停止手工 cell 枚举；在当前竖直 15-mode 线性/可靠 residual-envelope 合同上，
先复现一个 Houska 式 configuration-constrained polytopic information-ensemble terminal baseline，
明确模板参数、extreme information sets、逐边 packet graph 和输入/状态约束。只有该强基线闭合
后，才讨论 nonlinear CZ oracle 或同预算几何优势。
