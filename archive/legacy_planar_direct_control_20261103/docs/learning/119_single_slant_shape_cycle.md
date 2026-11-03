# 119. 固定单斜向 parallelogram 的精确形状阻断

日期：2026-10-26。Run184 已证明 axis-aligned box information ensemble 因独立速度半径逐边增长而不可行。本章检查新增一对法向 `q=p-(1/10)v` 后，仅用 `(p,q)` 两组条带形成的固定方向 parallelogram 外包是否闭合。

## 1. 独立坐标推导

令 `h=1/50`、`kappa=1/10=5h`。由

```math
p^+=p+hv,\qquad v^+=v+h\delta T+w,\qquad q=p-\kappa v
```

及 `v=(p-q)/kappa`，得到

```math
\begin{bmatrix}p^+\\q^+\end{bmatrix}
=\begin{bmatrix}6/5&-1/5\\1/5&4/5\end{bmatrix}
\begin{bmatrix}p\\q\end{bmatrix}
+\begin{bmatrix}0\\-\kappa h\end{bmatrix}\delta T
+\begin{bmatrix}0\\-\kappa\end{bmatrix}w.
```

共同输入只平移中心。对独立 `p/q` 条带取支持外包时必须取绝对值，因此半径递推是

```math
\begin{bmatrix}r_p^+\\r_q^+\end{bmatrix}
=M\begin{bmatrix}r_p\\r_q\end{bmatrix}
+\begin{bmatrix}0\\\kappa\bar w\end{bmatrix},\qquad
M=\begin{bmatrix}6/5&1/5\\1/5&4/5\end{bmatrix},
```

其中 `w_bar=572143/8000000`。初版错误地把 `M[0,0]` 写成 `4/5`；该错误会在第一条 miss 边少计 `2nu/5=1/125`，故原周期和余量结论全部撤回。

## 2. 长 return 的系数阻断

success 位置条带最多把 `r_p` 重置为 `nu=1/50`，但此 parallelogram outer update 保留 predicted `r_q`。对5、10、15步 return，`M^N` 的 `q->q` 系数分别为

```math
\frac{2096}{3125},\qquad
\frac{17562857}{9765625},\qquad
\frac{187604137722}{30517578125}.
```

5步系数小于1，但10、15步均大于1。特别地，若 mode 0 的 slant radius 为任意 `R>=0`，15步后

```math
r_q^{15}-R
=(M^{15})_{qp}\nu+
\left(\frac{187604137722}{30517578125}-1\right)R
+\text{非负扰动项}>0.
```

因此不存在非负有限 `R` 使合法15步 success 回到同一 `(nu,R)` 外形。该结论不依赖求解器容差，也不需要选择中心或控制。

## 3. 对错误候选的最小反例

把初版错误递推得到的 `R=805322658983099/5546041676000000` 代回正确动力学：

- 第一条 miss 的位置半径已欠包 `1/125`；
- 第5步即有 `r_q^5>R`，无法走 `4->0 success`；
- 第5步派生速度半径 `(r_p^5+r_q^5)/kappa` 已严格超过 `11/4`。

原测试误通过的原因是所谓 transform test 仅重复断言同一个错误矩阵，没有从 signed coordinate identity 检查。修复后的测试固定 signed state/input transform、第一 miss 反例与5/10/15步增益。

## 4. 证据边界与方向纠正

证据等级为 `exact_fixed_slant_parallelogram_shape_obstruction`。它只否定固定方向、独立 `(p,q)` 条带半径、success 不缩 `r_q` 的外包。它没有否定：

- 在原 box 上保留 active `+/-v` facets 的六边形；
- mode-dependent/rotating slant normals；
- CZ 或一般 Houska information ensemble；
- 中心、输入、终端与 MPC 递归可行性。

下一轮唯一问题：保留 `+/-p,+/-v` 并加入 `+/-(p-kappa v)`，先精确构造六 facet configuration/vertex maps 和 measurement outer map；检查 active velocity facets 是否能阻断上述 `q->q` 放大。若仍不闭合，再给 exact Farkas 证书，而不是继续改变斜率调参。
