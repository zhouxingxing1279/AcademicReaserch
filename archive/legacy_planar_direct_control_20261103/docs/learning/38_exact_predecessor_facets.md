# 38 一步鲁棒前驱的精确混合法向：RCI 模板不能只加入 p-v braking facets

日期：2026-09-24。承接第37章。

## 1. 本轮唯一问题

第37章证明 axis-aligned Cartesian RCI box 在当前横向四状态模型上结构性不可能，并提出下一步至少加入 `p-v` braking facets。但“至少加入 p-v”仍不是一个充分合理的 template：当前动力学是 `p <- v <- phi <- omega <- tau` 的积分链，且 `v` 同时受 scheduling-dependent residual 影响。

本轮只回答：**从当前 hard box 做一次精确 robust controlled-predecessor，究竟会自然产生哪些法向？** 这决定下一轮 polyhedral RCI co-design 应固定哪些 normals，避免凭经验选 facet。

仓库起点：`c87aae7369dc6fe3500478c81a3db462c24aa5c3`。

## 2. 模型与硬约束

沿用第36–37章

\[
p^+=p+h v,\quad v^+=v-hT\phi+h d,
\]
\[
\phi^+=\phi+h\omega,\quad \omega^+=\omega+\frac hJ\tau,
\]

其中 `h=J=0.02`, `T in [4.905,14.715]`, `|d|<=dbar(T)`，

\[
\bar d(T)=1.880+T(0.45)^3/6.
\]

硬域为

\[
|p|\le5,\ |v|\le3,\ |\phi|\le0.45,\ |\omega|\le2,\ |\tau|\le0.08.
\]

`T` 按当前 LPV 语义是已知 scheduling quantity；`d` 是未知 additive residual。

## 3. 一步 robust predecessor 的解析形式

要求后继仍落在 hard state box。

### 3.1 位置约束

因为 `p+` 不受当前 torque、T、d 影响，精确条件是

\[
|p+h v|\le5.
\]

因此第37章所说的 `p-v` mixed facet 不是启发式，而是 hard box 一步前驱的精确 facet。

### 3.2 速度约束

固定已知 T，对所有 `|d|<=dbar(T)` 要求 `|v+|<=3`，等价于

\[
|v-hT\phi|+h\bar d(T)\le3.
\]

这必然引入 `v-phi` mixed normals。只给 `p-v` 相关性而让 `(v,phi)` 继续独立，仍会保留 hard-box corner `v=3, phi=-0.45`，该 corner 在正最坏 residual 下立即违反速度约束。

更重要的是，不需要对连续 T 做网格化。对固定 `(v,phi)`，

\[
f(T)=|v-hT\phi|+h\left(1.880+T(0.45)^3/6\right)
\]

是 T 的凸函数，因此在闭区间 `[T_L,T_U]` 上的最大值必在端点取得。故整个 thrust interval 的一步 robust velocity predecessor **精确等价**于同时检查

\[
|v-hT_L\phi|+h\bar d(T_L)\le3,
\]
\[
|v-hT_U\phi|+h\bar d(T_U)\le3.
\]

绝对值展开后就是有限组线性 halfspaces。

### 3.3 姿态角约束

精确条件为

\[
|\phi+h\omega|\le0.45,
\]

因此还必须出现 `phi-omega` mixed normals。仅 `p-v` 和 `v-phi` 仍不足以使 template 对 predecessor 运算闭合。

### 3.4 角速度与输入

最后一维是 controlled predecessor：

\[
\exists |\tau|\le0.08:\quad
|\omega+(h/J)\tau|\le2.
\]

由于 `h/J=1`，当前 hard interval `|omega|<=2` 中每一点都至少存在一个 admissible torque 使下一步仍在该 interval；这一层本身不新增 state-state mixed normal。但在更小 RCI candidate 上，输入权限仍必须进入 vertex/facet certificate，不能从后续 co-design 中删除。

## 4. 精确边界见证

使用有理数算术：

1. `p=5,v=3` 时
   \[
   p^+=5.06=253/50,
   \]
   越界 `3/50=0.06`。

2. `phi=0.45,omega=2` 时
   \[
   \phi^+=0.49=49/100,
   \]
   越界 `1/25=0.04`。

3. `v=3,phi=-0.45,d=+dbar(T)` 时：
   - `T=4.905`: `v+ = 493317583/160000000 ~= 3.08323489375`，越界约 `0.08323489375`；
   - `T=14.715`: `v+ = 507920749/160000000 ~= 3.17450468125`，越界约 `0.17450468125`。

所以“第37章后只增加 p-v braking facets”本身会留下明确的一步反例。

## 5. 命题状态

### 已证明

- hard box 的一步 robust predecessor 必然含 `p-v`、`v-phi`、`phi-omega` 三类 mixed facets；
- 对当前 affine `dbar(T)`，速度 predecessor 对连续 thrust interval 的 robustification 精确化为两个 thrust endpoints，不需要 sampling；
- 只加入 `p-v` braking facets 而保持其余坐标独立，不是 predecessor-closed template。

### 尚未证明

- 上述一步 predecessor 本身是 RCI；
- 反复 predecessor 后 normals 是否有限闭合；
- 存在满足全部硬约束的 fixed-complexity correlated RCI；
- output-feedback/SMF posterior 下的递归可行性；
- CZ 相对该 correlated baseline 的严格改进。

因此本轮只完成 **normal selection 的理论闭合**，没有提前声称 RCI 已构造成功。

## 6. 文献核查

Gupta, Köroğlu, Falcone, *Computation of Robust Control Invariant Sets with Predefined Complexity for Uncertain Systems*, International Journal of Robust and Nonlinear Control 31(5), 2021, 1674–1688, DOI `10.1002/rnc.5378`。

该文正文明确处理 rationally parameter-dependent systems + additive disturbances + polytopic state/input constraints，并计算预定义复杂度、原点对称的 polytopic RCI；其方法不预先限制为固定线性 state feedback，而是在 RCI extreme points 上求 admissible controls，再可离线构造 PWA controller。论文还明确指出 candidate polytope 的初始 shape 可利用对 RCI 几何的先验知识选择。

与本项目的关系：本轮从当前四旋翼降阶模型的 exact one-step predecessor 推导 normals，正是给 predefined-complexity polytope 提供非任意的 shape prior。但“预定义复杂度 correlated polytope RCI”已经被该文覆盖，不能作为我们的创新点。

与本项目的差异：我们的 T 是在线可测 scheduling quantity，additive bound 本身依赖 T；最终还要接 SMF/output-feedback posterior 及 Tube MPC shift proof。当前一步 endpoint reduction 只解决 baseline 的有限 robust facet representation。

## 7. 可重复验证

新增：

- `verification/check_hard_box_predecessor_facets.py`
- `results/hard_box_predecessor_facets_20260924/checks.json`

脚本用 `fractions.Fraction` 复核全部 corner witness 和 `dbar(T)` 数值。运行：

```bash
python verification/check_hard_box_predecessor_facets.py --output /tmp/predecessor_facets.json
```

归档结果为 exact rational arithmetic；本轮不依赖优化器。

## 8. 下一轮唯一优先问题

> **用第38章导出的 `p-v / v-phi / phi-omega` predecessor normals 建立第一个 fixed-complexity correlated polytope candidate，并做真正的 robust controlled-invariance feasibility certificate：对 T 的允许范围、d in W(T) 和全部 state/input constraints，验证每个 candidate extreme point 是否存在 admissible scheduling-dependent torque。**

如果该 template 不可行，先用 predecessor/vertex counterexample 判断是 facet complexity 不足还是 actuator authority；不要恢复随机 K 搜索，也不要提前转向 CZ geometry comparison。
