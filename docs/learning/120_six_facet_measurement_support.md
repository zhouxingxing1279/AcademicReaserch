# 120. 六 facet configuration 与位置测量的精确支持映射

日期：2026-10-27。Run185 证明固定 `(p,q)` parallelogram 在 success 保留 `q` 半径时不能周期闭合；本章恢复被删去的显式速度 facets，检查该关键前提是否仍成立。

## 1. 六 facet configuration triple

令 `q=p-kappa*v`、`kappa=1/10`，按法向角度循环排列

```math
Y=\begin{bmatrix}
1&0\\0&1\\-1&\kappa\\-1&0\\0&-1\\1&-\kappa
\end{bmatrix},
```

对应 `+p,+v,-q,-p,-v,+q`。相邻法向对
`(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)` 各自给出一个精确线性 vertex map `Lambda_i`。按 CCTMPC Theorem 2 构造

```math
G=\operatorname{stack}_i(Y\Lambda_i-I),\qquad Gy\le0,
```

删除恒零行后共有24行。参考 offsets `y=1` 的六个顶点依次为

```math
(1,1),\ (-9/10,1),\ (-1,0),\ (-1,-1),\ (9/10,-1),\ (1,0),
```

全部逐行满足 `Yx<=1`。这些映射是既有 configuration-constrained polytope 方法的直接实例，不是本项目创新。

对中心对称 offsets `(r_p,r_v,r_q,r_p,r_v,r_q)`，configuration cone 等价地包含三角关系

```math
|r_p-\kappa r_v|\le r_q\le r_p+\kappa r_v.
```

等号允许重复 vertex，即 configuration cone 的边界；Theorem 2 的凸包表示仍给出安全外包。

## 2. 位置 strip 求交后的紧支持

对 success measurement 的中心化位置 cap `|p|<=a`，保留预测约束

```math
|v|\le r_v,\qquad |p-\kappa v|\le r_q.
```

分别最大化 `p`、`v` 和 `q=p-kappa*v`，得到精确恒等式

```math
h_p=\min(a,r_q+\kappa r_v),\qquad
h_v=\min(r_v,(a+r_q)/\kappa),\qquad
h_q=\min(r_q,a+\kappa r_v).
```

检查器同时枚举六条边界线的全部15个两两交点，保留真实可行顶点，并用有理数支持最大值独立重放这三个公式。

## 3. 严格反例：Run185 的 unchanged-q 前提不再成立

取可靠安全盒中的预测形状

```math
r_p=1,\qquad r_v=11/4,\qquad r_q=1,
```

它严格满足预测 configuration 条件。success 的位置噪声半宽是 `a=1/50`。若机械地只把 `r_p` 改为 `1/50` 而保留 `r_q=1`，则

```math
r_q> a+\kappa r_v=\frac1{50}+\frac1{10}\frac{11}{4}=\frac{59}{200},
```

所以原 `q` facet 已冗余，raw offsets 离开所选六边形 configuration cone。对真实交集重新求支持得到

```math
(h_p,h_v,h_q)=\left(\frac1{50},\frac{11}{4},\frac{59}{200}\right),
```

`q` 支持严格减少 `141/200`，新 offsets 位于 configuration cone 边界。故显式 velocity facets **确实能够**通过位置测量阻断 Run185 的局部 unchanged-`q` 放大机制。

## 4. 证据边界与下一步

证据等级为 `exact_six_facet_measurement_support_map`。当前只证明一个中心对称形状和中心化 strip 的精确局部映射；尚未构造 measurement-dependent center、`Z/H/Omega`、15-mode/17-edge graph、source-shared controls、硬输入或终端条件。因此不能据此宣称存在 invariant information ensemble、降低闭环保守性或 MPC 递归可行。

下一轮唯一问题：把上述 canonical support 分支提升为对连续 measurement centers 有效的六-facet `Z/H/Omega` meta-template，并在 control-before-packet 时序下构造完整15-mode/17-edge LP；输出 exact primal 或 Farkas 证书。若必须使用非凸 min/disjunction 且固定预算下不能由有限 extreme meta-polytopes覆盖，则停止该模板。
