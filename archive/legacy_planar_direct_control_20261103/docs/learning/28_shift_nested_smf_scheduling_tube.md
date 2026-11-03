# 28 Rolling CZ-SMF 的 shift-nesting：固定预测映射下无需额外 update gate

2026-09-24。接续第27章。本轮直接检查递归可行性链条所需的跨时刻未来姿态区间关系，而不是继续做单步 support tightening。

## 1. 关键集合命题

设滤波后验为 `X_k`，固定的一步外包预测算子

\[
\mathcal P(S)=F S\oplus W,
\]

且下一时刻 measurement update 是合法集合求交，因此

\[
X_{k+1}\subseteq \mathcal P(X_k).
\]

预测 horizon 使用同一个 `P`：

\[
X_{i|k}=\mathcal P^i(X_k).
\]

Minkowski 和与线性映射都关于集合包含单调，所以对所有 `i>=0`

\[
\boxed{X_{i|k+1}\subseteq X_{i+1|k}.}
\]

证明只有两步：由 measurement update 得到 `X_{k+1} subset P(X_k)`；对两边重复应用单调算子 `P^i` 即得结论。

因此任意线性 projection/support 也自动满足

\[
h_{X_{i|k+1}}(p)\le h_{X_{i+1|k}}(p).
\]

特别地，姿态 scheduling interval

\[
I_{i|k}=[-h_{X_{i|k}}(-e_\phi),h_{X_{i|k}}(e_\phi)]
\]

满足

\[
\boxed{I_{i|k+1}\subseteq I_{i+1|k}.}
\]

## 2. 对第27章 decision-conditioned tightening 的意义

第27章给出给定 thrust decision `d` 和姿态 interval `I=[ell,u]` 时的精确 robust support

\[
H(d;I)=\max\{r_zd-r_x(g+d)\ell,\ r_zd-r_x(g+d)u\}.
\]

若 shifted candidate 在 `k+1` 沿用上一时刻后续的 control decision，即

\[
d_{i|k+1}=d_{i+1|k},
\]

那么由 `I_{i|k+1} subset I_{i+1|k}` 和 support 对集合包含的单调性，立即得到

\[
\boxed{H(d_{i|k+1};I_{i|k+1})\le H(d_{i+1|k};I_{i+1|k}).}
\]

因此在**固定预测映射、固定 disturbance contract、shifted control 不变**的前 `N-1` 个 stage，新的 SMF measurement 只会维持或放松旧 tightening，不会让旧 shifted candidate 因 scheduling bound 变差而失效。

这比“每次更新后额外做 feasibility gate”更具体：在上述条件成立时，gate 对前 `N-1` stages 是冗余的。

## 3. 代码审计

新增 `verification/check_shift_nested_scheduling_tube.py`。它复用仓库六状态 affine outer model、CZ `predict/observe`、非零 truth-consistent measurements，并在每个时刻从 posterior 生成 horizon 8 的 `phi` projection intervals。

固定 seed `20260924`，26 ticks，共检查

\[
25\times 8=200
\]

个 shifted interval inclusions。结果：

- violations: **0 / 200**；
- max violation: **0**；
- 400 个 interval endpoints 中 200 个出现严格收缩；
- endpoint 平均收缩 `2.744e-4 rad`；
- 最大 endpoint 收缩 `5.60e-4 rad`。

运行：

```bash
python verification/check_shift_nested_scheduling_tube.py \
  --output /tmp/shift_nested.json --seed 20260924 --horizon 8
```

数值 LP 只用于审计 support；上述 nesting 命题本身来自集合包含，不依赖这 200 个样例。

## 4. 一个重要的边界：为什么这还不是完整递归可行性定理

这个结论只覆盖前 `N-1` 个 shifted stages。完整 MPC proof 还缺：

1. **terminal append**：必须证明旧 terminal state 经 terminal controller 后进入新 terminal set；
2. **decision-dependent prediction map**：若未来集合传播本身依赖优化控制 `d`，必须对相同 shifted decision 比较同一个 map `P_d`，不能把不同控制下的集合直接声称嵌套；
3. **adaptive disturbance/model contract**：若 `W_k`、模型中心或 outer approximation algorithm 在两次 MPC solve 之间改变，需要额外 monotonic compatibility 条件；
4. **复杂度压缩**：若 CZ reduction 是外包且每次独立重算，`reduce(P(S))` 未必保留跨时刻 nesting，除非 reduction operator 本身具有所需的 inclusion/monotonic property。

第4点尤其重要：**exact CZ history 天然 shift-nested，不代表 fixed-complexity compressed CZ 也天然 shift-nested。** 这把“固定复杂度 CZ 压缩如何不破坏 recursive feasibility”重新提升为真正的理论缺口。

## 5. 与文献边界

Köhler et al. (2021) 已经对 set-membership parameter update 与 tube update 给出 monotonic/non-increasing 条件以保证 recursive feasibility；Hanema et al. (2021) 已利用 state/scheduling relation 构造 future scheduling tubes 并证明 recursive feasibility/stability。因此“nested uncertainty helps recursive feasibility”不是创新。

本轮更有价值的定位是：对当前 CZ-SMF state-estimation 接口，**exact prediction/update 本身已经给出所需 shift nesting**。因此后续不应把精力放在为 exact CZ 设计额外 gate，而应研究实际工程必需的 fixed-complexity reduction 是否破坏这个性质，以及如何构造 certificate-preserving reduction。

## 6. 候选创新重新排序

### A. Certificate-preserving fixed-complexity CZ reduction — 提升为主候选

目标不是单纯最小化 volume/generator count，而是设计 reduction `R`，使控制相关方向或整个集合满足可用于 shift proof 的关系，例如

\[
R(X_{i|k+1})\subseteq R(X_{i+1|k})
\]

或较弱但足够的有限 control-normal support non-expansion。需要同时保证 outer inclusion `X subset R(X)` 与固定复杂度。

### B. Certified SMF-to-scheduling-tube interface — 保留为系统接口

exact CZ 下 nesting 已闭合；其价值主要是把 certified support 投影接入 decision-conditioned MPC，而不是 nesting 本身。

### C. Exact-CZ update feasibility gate — 降级

固定 prediction map 下前 `N-1` stages 不需要该 gate。只有 reduction、model/tube update 或 terminal append 改变 contract 时才需要。

## 7. 下一轮证明义务

下一轮应主动构造反例：找两个嵌套 CZ `A subset B`，分别独立做常用 fixed-order zonotope/CZ outer reduction 后，检查是否可能出现

\[
h_{R(A)}(p)>h_{R(B)}(p)
\]

在真实 MPC normals 上成立。若能找到，说明 naive reduction 会破坏 exact-CZ 的 shift nesting；随后比较两条修复路线：

- ancestor-capped support reduction：要求新 reduced set 的 control-normal caps 不超过上一 horizon 对应 caps；
- nested template reduction：共享固定 normals/template，只更新单调 support bounds。

只有这一步形成“反例 + 修复 + fixed complexity + recursive-feasibility compatibility”，才具备更像论文贡献的理论结构。
