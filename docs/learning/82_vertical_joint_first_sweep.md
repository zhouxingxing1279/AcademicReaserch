# 82. 竖直 joint information candidate 的15模态首次下降层

日期：2026-10-02。本章只证明候选的第一次 descending predecessor 在全部15个 packet
mode 中都含四维正体积内集。它不是 maximal predecessor、固定点、RCI 或 MPC 递归可行性
证书。

## 1. 候选、信息纤维与受限策略

沿用第81章坐标和候选：

```math
s=(\eta_p,\eta_v,e_p,e_v),\qquad d=e-\eta,
```

```math
S_j=E_j\times B_e,\qquad
B_e=\{e:|e_p|\le1,\ |e_v|\le 11/4\}.
```

`E_j` 是 Run 136 六维 estimator-error zonotope 的竖直精确投影。控制器只观测 `d`，
不能读取隐藏 `eta`。本轮固定一个因果且可执行的受限策略：

```math
\delta T=0
```

并要求 observation 区域内每个 `d` 都兼容整个 `E_j`，而非只兼容一个隐藏状态子集。

## 2. 精确 observation 内投影

记支持函数 `h_{E_j}(a,b)`，采样周期 `h=1/50`，全 nominal thrust 区间上由同一 actual
thrust 得到的 residual 半宽为

```math
\bar r_z=411370817/128000000.
```

定义 `D_j^0` 为下列六个 exact-rational 半空间的交：

```math
\begin{aligned}
 |d_p| &\le 1-h_{E_j}(1,0),\\
 |d_v| &\le 11/4-h_{E_j}(0,1)-h\bar r_z,\\
 |d_p+h d_v| &\le 1-h_{E_j}(1,h).
\end{aligned}
```

第一行保证当前 `E_j+d` 的位置约束；第二行同时保证当前速度和下一步最坏 residual 后的
速度约束；第三行保证下一步位置约束。因此对全部 `eta in E_j`、`d in D_j^0` 和共享
physical residual，有 `e` 与 `e+` 均在 `B_e`。`D_j^0` 是零修正、完整 fiber 类的精确
observation projection，但只是一般 predecessor 的保守内投影。

## 3. 逐模态 exact 结果

每个 `D_j^0` 均严格正面积，并包含第81章公共盒
`|d_p|<=1/5, |d_v|<=1/4`。可逆映射 `(eta,d)->(eta,e=eta+d)` 因而给出四维正体积集合

```math
C_j^1=\{(\eta,e):\eta\in E_j,\ e-\eta\in D_j^0\}
\subseteq S_j\cap\operatorname{Pre}_j(S).
```

| mode | `D_j^0` facets | exact area | decimal area | outgoing edges |
|---:|---:|---:|---:|---|
| 0 | 6 | `115411461910160686772599/18432000000000000000000` | 6.261473 | `0->1 miss` |
| 1 | 6 | `970388946206533744722991/165888000000000000000000` | 5.849663 | `1->2 miss` |
| 2 | 6 | `902655722088771633327791/165888000000000000000000` | 5.441356 | `2->3 miss` |
| 3 | 6 | `278569040413637373562597/55296000000000000000000` | 5.037779 | `3->4 miss` |
| 4 | 6 | `769746780065707480722991/165888000000000000000000` | 4.640160 | `4->5 miss`, `4->0 success` |
| 5 | 4 | `73441326249584758711/17280000000000000000` | 4.250077 | `5->6 miss` |
| 6 | 4 | `200580505475187222077/51840000000000000000` | 3.869223 | `6->7 miss` |
| 7 | 4 | `45344799181869615733/12960000000000000000` | 3.498827 | `7->8 miss` |
| 8 | 4 | `9043538271193782461/2880000000000000000` | 3.140117 | `8->9 miss` |
| 9 | 4 | `5794304732523046871/2073600000000000000` | 2.794321 | `9->10 miss`, `9->0 success` |
| 10 | 4 | `127664621398102810963/51840000000000000000` | 2.462666 | `10->11 miss` |
| 11 | 4 | `18544722418738014577/8640000000000000000` | 2.146380 | `11->12 miss` |
| 12 | 4 | `11966549253989010859/6480000000000000000` | 1.846690 | `12->13 miss` |
| 13 | 4 | `81120436332414894793/51840000000000000000` | 1.564823 | `13->14 miss` |
| 14 | 4 | `899947970530621291/691200000000000000` | 1.302008 | `14->0 success` |

全部17条 estimator edge 的 target-facet support 包含以 `Fraction` 精确通过。mode 4/9 的
两个未知后继在计算前固定共享同一个 `deltaT=0`；success measurement noise 与同一
actual-thrust residual 进入相应 estimator update，没有为分支预选不同控制。

## 4. 证据等级与下一门槛

证据等级为 **exact positive-volume inner certificates for all fifteen first-sweep modes**。
它排除了当前候选在第一层必空，但没有证明：

1. `D_j^0` 是最大 observation projection；
2. `C_j^1` 对下一层仍闭合；
3. descending sequence 有非空固定点或有限终止；
4. 水平、姿态、torque、terminal、shift 或 MPC 递归可行性；
5. 当前 boundary-tight input allocation 是最终可机动 nominal MPC 域。

下一步必须让 target 从 `S` 更新为本轮保留集合并执行第二层。关键问题不再是“一步是否
为空”，而是 full-fiber/zero-policy 内证书是否自映射；若第二层空或快速塌缩，再准入
依赖 `d` 的非零 correction policy，而不是直接宣称一般 joint RCI 不存在。
