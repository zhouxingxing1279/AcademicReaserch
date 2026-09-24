# 39 第二步前驱法向增长：第38章 pairwise template 仍不是 RCI

日期：2026-09-24。承接第38章。仓库起点：`a48d0d048081520cc992d1ce685faa1618e5ed74`。

## 1. 本轮唯一问题

第38章从 hard state box 的一次精确 robust predecessor 推导出 `p-v / v-phi / phi-omega` 三类 pairwise mixed normals，并把下一步设为基于这些 normals 构造 fixed-complexity correlated RCI。

但在真正做 polytope 优化以前必须先回答：**这些一次前驱法向在重复 predecessor 下是否闭合？** 如果不闭合，那么直接固定第38章 pairwise template 会遗漏动力学链条的更深相关性，任何后续“该 template 不可行”的结论都可能只是 facet complexity 不足。

本轮给出一个 exact-rational 反例，证明 `X1 = X ∩ Pre(X)` 本身不是 RCI，并精确指出第二次 predecessor 新增 `v-phi-omega` 相关性。

## 2. 模型

沿用第36–38章：

\[
p^+=p+h v,\qquad v^+=v-hT\phi+h d,
\]
\[
\phi^+=\phi+h\omega,\qquad \omega^+=\omega+\frac hJ\tau,
\]

其中 `h=J=0.02`, `T∈[4.905,14.715]`, `|d|≤dbar(T)`,

\[
\bar d(T)=1.880+T(0.45)^3/6,
\]

硬约束为 `|p|≤5, |v|≤3, |phi|≤0.45, |omega|≤2, |tau|≤0.08`。

第38章已经证明 `X1` 至少包含低推力 velocity predecessor facet

\[
|v-hT_L\phi|+h\bar d(T_L)\le V,
\quad T_L=4.905,\ V=3.
\]

## 3. 精确反例

记

\[
\bar d_L=\frac{6254383}{3200000}=1.9544946875.
\]

考虑状态

\[
p=5,\quad v=-3,\quad
\phi=-\frac{\bar d_L}{T_L}
=-\frac{6254383}{15696000},\quad
\omega=2.
\]

该点满足 hard box；它也满足第38章的一步 predecessor 约束。特别地，低推力 velocity facet 在该点的最坏负扰动方向正好处于边界。

固定允许的 scheduling `T=T_L`，选择允许扰动

\[
d=-\bar d_L.
\]

则

\[
v^+=-3-hT_L\left(-\frac{\bar d_L}{T_L}\right)-h\bar d_L=-3,
\]

而

\[
\phi^+=-\frac{\bar d_L}{T_L}+h\omega.
\]

下一时刻若仍要属于 `X1`，必须再次满足同一个低推力 velocity predecessor facet：

\[
|v^+-hT_L\phi^+|+h\bar d_L\le3.
\]

代入得到

\[
|v^+-hT_L\phi^+|+h\bar d_L
=3+h^2T_L\omega.
\]

因为 `h>0,T_L>0,omega=2>0`，严格违反。当前参数下

\[
h^2T_L\omega
=\frac{981}{250000}
=0.003924.
\]

因此下一时刻左侧精确为

\[
3.003924>3.
\]

### 为什么 torque 无法修复

当前 `tau` 只进入 `omega+`。上述已经违反的 `X1` facet 只依赖 `(v+,phi+)`，而二者都不依赖当前 `tau`。所以不仅 `|tau|≤0.08` 下无解，即使当前 torque 无界，也不能修复这个一步违反。

因此这是 **controller-independent 的 template obstruction**，不是 actuator saturation 造成的反例。

## 4. 第二次 predecessor 为什么产生新法向

把第38章 velocity facet

\[
s(v-hT\phi)\le V-h\bar d(T),\qquad s\in\{-1,+1\},
\]

沿动力学再向后拉一步：

\[
s\{v^+-hT'\phi^+\}
=s\{v-hT\phi+h d-hT'(\phi+h\omega)\}.
\]

即使固定 `T=T'=T_L`，表达式也出现

\[
-h^2T_L\omega.
\]

所以第二次 predecessor 必然产生同时耦合 `v,phi,omega` 的 mixed normal。第38章的 pairwise normals 是一次 predecessor 的精确结构，但**不是 repeated-predecessor closed family**。

类似地，继续反向传播时，积分链会把更深的动态相关性带入 facet normal。由此不能把“第38章三类 pairwise normals”直接当成最终 RCI template 的充分 shape prior。

## 5. 文献核查与创新边界

### Gupta, Köroğlu, Falcone (2021)

*Computation of Robust Control Invariant Sets with Predefined Complexity for Uncertain Systems*, IJ Robust and Nonlinear Control 31(5):1674–1688, DOI `10.1002/rnc.5378`。

论文针对 rationally parameter-dependent systems 与 additive disturbances 计算预定义复杂度的原点对称 polytopic RCI，并不要求控制输入预先采用固定线性反馈；其正文明确说明初始 polytope shape 会影响最终结果。因此，本轮“错误/不足的初始 facet family 会限制 certificate”与该文方法边界一致；fixed-complexity correlated RCI 本身不能作为创新。

### Mulagaleti, Mejari, Bemporad (2025)

*Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate*, IEEE TAC 70(2):1259–1266, DOI `10.1109/TAC.2024.3454528`。

该文利用 scheduling parameter 的实时测量，联合计算 parameter-dependent RCI 与 parameter-dependent vertex control law，并用 configuration-constrained polytopes 保持固定 facet orientation、让 offsets 随 scheduling parameter 变化；还显式利用 parameter variation-rate bound 降低保守性。

这对本项目尤其重要：我们的 thrust `T` 也是已知 scheduling quantity。因此“让 RCI/tube 随 T 变化”已经有直接 LPV-RCI 近邻，不能作为独立创新声明。当前真正未闭合的是：如何把这种强 LPV baseline 与 SMF posterior / output-feedback uncertainty 以及 Tube-MPC shift-compatible tightening 接起来。

## 6. 命题状态

### 已证明

1. `X1=X∩Pre(X)` 不是当前模型的 RCI；
2. 反例使用 exact rational arithmetic，严格违反量为 `981/250000`；
3. 违反与当前 torque 无关，因此不能归因于 actuator saturation；
4. repeated predecessor 从第二步开始产生 `v-phi-omega` deeper-chain normal，第38章 pairwise family 不闭合。

### 被否定

> “只固定第38章 `p-v / v-phi / phi-omega` pairwise normals 就已经获得 predecessor-closed RCI template。”

该命题错误。

### 尚未证明

- 一个有限 fixed-orientation normal family 是否足以在当前 hard constraints 内形成非空 RCI；
- parameter-dependent offsets 是否能显著减少所需 facet complexity；
- arbitrary thrust jump 与有界 thrust-rate 两种信息模式下各自的最小可认证 baseline；
- SMF posterior 如何在不破坏 shift proof 的前提下进一步收紧 tube。

## 7. 可重复验证

新增：

- `verification/check_first_predecessor_not_rci.py`
- `results/first_predecessor_not_rci_20260924/checks.json`

运行：

```bash
python verification/check_first_predecessor_not_rci.py --output /tmp/first_predecessor_not_rci.json
```

脚本仅使用 Python 标准库 `fractions.Fraction`，并断言直接计算的 facet violation 与闭式 `h^2 T_L omega` 完全相等，不依赖浮点优化器。

## 8. 下一轮唯一优先问题

> **明确 thrust scheduling 的信息合同：在“每步可测但可任意跳变”这一当前最弱假设下，构造 repeated-predecessor 的有限深度 normal family，并检查何时出现 normal growth/收敛；同时与允许 `|T_{k+1}-T_k|≤rho` 的 PD-RCI 合同严格区分。**

原因：2025 TAC 近邻表明 parameter-rate 信息会直接改变 PD-RCI 保守性。若仓库没有物理上可证明的 thrust-rate bound，就不能为了得到更大的 invariant set 随意采用 bounded-rate 假设。下一轮先闭合这个信息合同，再决定使用 common RCI、PD-RCI 还是 configuration-constrained tube；不要先做 CZ 几何比较。
