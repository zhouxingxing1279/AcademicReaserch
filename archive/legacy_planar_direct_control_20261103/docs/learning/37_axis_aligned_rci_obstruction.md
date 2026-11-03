# 37 轴对齐 RCI 盒的结构性不可能性：certificate baseline 必须保留状态相关性

日期：2026-09-24。承接第36章，仓库基线提交 `1001c84700005baf7705175d3bc5d2ccfd698286`。

## 1. 本轮唯一问题

第36章已经证明：现有 static-K 失败不能解释为执行器物理不可能；下一步应建立 scheduling-consistent `W(T)` 下的 certificate-based ancillary/RCI baseline。

在进入 LMI/polyhedral co-design 前，先回答一个更基础的证书类选择问题：**能否把四状态横向误差 tube 直接取成 origin-centered axis-aligned Cartesian box，并把其作为 RCI baseline？**

这是阻塞点，因为若该集合类本身与位置积分器不相容，再继续搜索 box halfwidth 或 feedback gain 只会重复得到假阴性。

## 2. 模型

沿用第36章四状态模型

\[
p^+=p+h v,
\]
\[
v^+=v-hT\phi+h d,
\]
\[
\phi^+=\phi+h\omega,
\]
\[
\omega^+=\omega+\frac hJ\tau,
\]

其中 `h=0.02`, `J=0.02`, `T in [4.905,14.715]`，且 scheduling-consistent residual 满足

\[
|d|\le \bar d(T)=1.880+T(0.45)^3/6.
\]

考虑 Cartesian candidate

\[
\mathcal E_B=[-P,P]\times[-V,V]\times[-\Phi,\Phi]\times[-\Omega,\Omega],
\]

其中所有 halfwidth 非负，且集合包含原点。控制器允许是任意 causal map `tau=kappa(x,T)`；因此下面的否定不依赖 static K。

## 3. 命题：任何非零速度宽度的 axis-aligned box 都不能 RCI

**命题 37.1.** 若 `h>0` 且 `P<infinity`，上述 Cartesian set 若对系统 robust control invariant，则必须 `V=0`。

**证明。** 由于 Cartesian product 独立组合所有坐标，若 `V>0`，状态

\[
(p,v,\phi,\omega)=(P,V,0,0)
\]

属于 `E_B`。但位置后继与控制、推力和扰动都无关：

\[
p^+=P+hV>P.
\]

故一步即离开 `[-P,P]`，与 RCI 定义矛盾。因此必须 `V=0`。QED。

这不是 hard-domain `[|p|<=5,|v|<=3]` 本身不可行；被否定的是**把整个 Cartesian product 当成 invariant tube cross-section**。

## 4. 非零 residual 又排除了 V=0 的退化盒

**命题 37.2.** 在当前 residual contract `bar d(T)>0` 下，不存在非空 origin-centered axis-aligned Cartesian RCI box。

**证明。** 由命题37.1，RCI 必须有 `V=0`。于是集合中包含

\[
x=(0,0,0,0).
\]

固定任一允许 `T`，选择允许扰动 `d=bar d(T)>0`。则

\[
v^+=h\bar d(T)>0.
\]

而 `V=0` 要求 `v^+=0`。当前 tick 的 `tau` 只进入 `omega^+`，不能改变 `v^+`，所以不存在 causal torque choice 可以避免该违反。QED。

低推力 `T=4.905` 下精确有理数为

\[
\bar d(T_L)=6254383/3200000\approx1.9544946875,
\]

因此从零状态、正最坏 residual 一步得到

\[
v^+=6254383/160000000\approx0.0390898934>0.
\]

## 5. 一个直接数值见证

即使不使用一般证明，hard-domain halfwidth `P=5,V=3` 的 Cartesian corner `(p,v)=(5,3)` 在一步后为

\[
p^+=5+0.02\times3=5.06,
\]

精确违反量为 `3/50=0.06 m`。这与 feedback gain、`W(T)` 的具体大小甚至 disturbance 是否为零均无关。

## 6. 这改变了什么

### 已证明

1. 在当前横向模型中，任何有限 `P`、正 `V` 的 origin-centered axis-aligned Cartesian tube 都不可能是一阶 RCI；
2. 非零 residual 进一步排除 `V=0` 的退化情况；
3. 因此后续 certificate synthesis 若把 RCI 形状限制为独立 coordinate box，其 infeasibility **没有资格**被解释为 controller/actuator infeasibility。

### 没有证明

本轮完全没有否定：

- 带 `p-v` 相关面的 polyhedral RCI；
- constrained zonotope / zonotope RCI；
- ellipsoidal RPI/RCI；
- parameter-dependent `E(T)`；
- gain-scheduled controller；
- 完整六自由度四旋翼安全性。

特别是，第36章已给出满足硬约束的有限时域控制序列，所以本轮的 negative result 必须严格解释为**集合参数化类不合适**。

## 7. 文献核查与创新边界

### Hanema, Lazar, Tóth — Heterogeneously parameterized tube model predictive control for LPV systems (2019/Automatica 2020)

预印本：https://arxiv.org/abs/1910.08449

论文考虑可测 scheduling 的 constrained LPV system，明确指出 tube parameterization 决定 complexity/performance trade-off，并给出保证 recursive feasibility 与 closed-loop stability 的 parameterization 条件。其 scheduling tube 还使用 shifted inclusion 关系处理下一时刻预测。这说明“tube parameterization 不能任意选”已有成熟理论背景；本章的 box obstruction 只是针对当前四旋翼降阶模型的一个精确筛选结论，不声称一般理论创新。

与本项目差异：该文主要处理 scheduling 的 multiplicative uncertainty；当前项目还存在 additive `W(T)`，后续还要接 SMF/output-feedback posterior。

### Gupta, Köroglu, Falcone — Computation of robust control invariant sets with predefined complexity for uncertain systems (2021)

DOI: `10.1002/rnc.5378`。

该文针对 rationally parameter-dependent systems + additive disturbances，计算预定义复杂度的 polytopic RCI set；重要的是它不要求固定 state-feedback 结构，而可为 RCI 顶点求 admissible control，再形成 PWA controller。这与第36章“不要把 static-K failure 写成 plant impossibility”的结论高度一致，也给出下一阶段更合适的 baseline 类型。

因此，本项目不能把“采用 correlated polytope/CZ 而不是 box”本身作为创新；真正待研究的是：在 scheduling-consistent disturbance contract、output-feedback SMF 信息以及真实 MPC normals 下，是否存在额外且可证明的保守性改进。

## 8. 可重复验证

新增：

- `verification/check_axis_aligned_rci_obstruction.py`
- `results/axis_aligned_rci_obstruction_20260924/checks.json`

脚本只用 Python 标准库 `fractions.Fraction`，检查：

- `(P,V)=(5,3)` corner 的一步位置越界；
- 一般 invariance inequality 强制 `V=0`；
- 当前低推力 residual 非零，并使零状态下一步 `v^+>0`。

运行：

```bash
python verification/check_axis_aligned_rci_obstruction.py \
  --output /tmp/axis_aligned_rci_obstruction.json
```

归档结果使用 exact rational arithmetic，不依赖浮点 solver。

## 9. 下一轮唯一优先问题

不再尝试 axis-aligned RCI box，也不恢复 CZ geometry comparison。下一轮只做：

> **选择一个最小的 correlated polyhedral template（至少包含 p-v braking facets），在 scheduling-consistent `W(T)` 下建立 controller/RCI co-design 的可认证 feasibility problem，并检查全部 state + torque constraints。**

优先参考 Gupta–Köroglu–Falcone 的 predefined-complexity RCI 思路；若实现上需要先固定 normals，则 normals 必须由 double-integrator braking geometry/controlled-predecessor 推导，而不是随机选取。只有得到第一个可认证 correlated ancillary/RCI baseline 后，才有资格重新讨论 CZ-SMF 是否进一步降低 tightening。
