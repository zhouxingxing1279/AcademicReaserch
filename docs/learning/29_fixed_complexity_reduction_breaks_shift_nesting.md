# 29 固定复杂度 outer reduction 会破坏 shift support nesting：反例与修复条件

2026-09-24。接续第28章。本轮不再假设“outer reduction 可能有问题”，而是构造可复现反例，并把修复目标压缩为 MPC 真正需要的有限 control-normal support 条件。

## 1. 问题

第28章已经证明 exact rolling CZ 在固定预测映射下满足

\[
A:=X_{i|k+1}\subseteq B:=X_{i+1|k}.
\]

工程实现需要固定复杂度，通常独立计算外包 `R(A)`、`R(B)`。仅有

\[
A\subseteq R(A),\qquad B\subseteq R(B)
\]

并不能推出 `R(A) subset R(B)`，甚至不能推出真实 MPC normal `p` 上

\[
h_{R(A)}(p)\le h_{R(B)}(p).
\]

## 2. 一个更强的反例构造：A 甚至只是 B 的缩放

令中心为零的 zonotope

\[
B=\{G\xi:\|\xi\|_\infty\le1\},\qquad A=\alpha B,\ 0<\alpha<1.
\]

为了排除“集合本身复杂”的干扰，只改变 A 的**表示**：把第一根 generator `g` 拆成 `s` 根 `alpha*g/s`。因为独立系数的和仍恰好覆盖 `[-alpha,alpha]g`，该 split representation 与 `alpha B` 是同一个集合。

对 A、B 分别应用经典 generator-box outer reduction：按 `||g||_1-||g||_inf` 排序，保留一根 generator，把其余 generators 用逐坐标绝对值和构造 axis-aligned box。该操作分别保证 outer inclusion，但 generator ranking 依赖表示。

固定 seed `20260924`，10,000 个随机二维 B，`alpha in [0.65,0.98]`，split=2..6。检查坐标 normals 与仓库姿态 terminal family 中的 mixed normal `p=(4,1)`。

结果：

- 326 / 10,000 个嵌套 pair 在 `p=(4,1)` 上出现 support reversal；
- `+/-e1,+/-e2` 上 0 reversal，这是 boxification 保留 coordinate support 的负对照；
- 最坏样例：`alpha=0.9564107538`，exact support 本来严格缩小：

\[
h_A(p)=9.802623 < h_B(p)=10.249386,
\]

但独立 reduction 后变成

\[
\boxed{h_{R(A)}(p)=14.634527 > 10.249386=h_{R(B)}(p)},
\]

reversal gap 为 `4.385141`。

因此“每一步都安全外包”与“跨时刻 shift-compatible”是两个不同证明义务。

## 3. 为什么这个反例对 MPC 有意义

它不是随机 support direction 才出现的现象。`(4,1)` 正是仓库已有姿态 terminal polytope 使用的 mixed normal 形状。因此 fixed-complexity reduction 若只优化 generator 数/体积而不保护 control normals，可能把 exact posterior 带来的 tightening improvement 反转，从而破坏 shifted-candidate proof 所需的 monotone tightening。

但本轮仍不声称已经构造完整六状态闭环失效：二维随机 generator family 只证明 reduction operator 的一般缺陷。下一步必须把同样审计接入 rolling 六状态 CZ 的真实 reduction。

## 4. 修复路线 A：control-normal cap intersection

若上一 horizon 已认证 cap

\[
\beta_j^{old}=h_{R(B)}(p_j),
\]

而 exact 新集合满足 `A subset B subset R(B)`，则必有

\[
h_A(p_j)\le\beta_j^{old}.
\]

先做任意 outer reduction `R_0(A)`，再定义

\[
\widetilde R(A)=R_0(A)\cap\bigcap_j\{x:p_j^Tx\le\beta_j^{old}\}.
\]

由于 `A` 同时包含于 `R_0(A)` 和所有旧 cap halfspaces，严格有

\[
A\subseteq\widetilde R(A),
\qquad
h_{\widetilde R(A)}(p_j)\le\beta_j^{old}.
\]

这给出**外包含 + control-normal shift compatibility**的直接定理。CZ 对 halfspace intersection 有现成表示工具，因此理论上可实现。

缺点也很明确：每次追加 halfspace 会增加 constraints/generators。若随后再做不受约束的 reduction，刚证明的 caps 又可能被破坏。因此它还没有闭合“固定复杂度”这一项。

## 5. 修复路线 B：共享 H-template / support ledger

取固定 MPC normals

\[
H=[p_1^T;\ldots;p_m^T]
\]

并维护

\[
\mathcal T(\beta)=\{x:Hx\le\beta\}.
\]

对 exact set X 令 `beta_j=h_X(p_j)`。若 `A subset B`，support 单调性自动给

\[
\beta(A)\le\beta(B),
\]

因此 template sets 满足

\[
\mathcal T(\beta(A))\subseteq\mathcal T(\beta(B)).
\]

这是固定 facet complexity、天然 monotone 的表示。对 MPC tightening 而言，它比强行维护完整低阶 CZ 更直接，因为优化器最终只消费这些 normals 的 support。

问题是 prediction/update 仍需要一个可传播的 state set；纯 support ledger 不能自动替代 CZ-SMF。因此更现实的系统结构是：

1. CZ-SMF 负责 state consistency 与 measurement intersection；
2. fixed-complexity reduction 负责可计算传播；
3. 独立的 certified control-normal support ledger 负责 recursive-feasibility caps；
4. reduction 若超出 ledger cap，则用 exact/CZ support query + cap intersection 修复，或 fallback 到旧安全表示。

这比“设计一个对所有集合都单调的神奇 CZ reduction”更可能实现。

## 6. 文献边界

Scott et al. (Automatica 2016) 已给 CZ lower-complexity enclosure；Raghuraman & Koeln (Automatica 2022, DOI 10.1016/j.automatica.2022.110204) 系统研究 CZ set operations/order reductions；Girard (HSCC 2005) 是经典 zonotope reachability/order-reduction基础。因此普通 order reduction 不是创新。

2026 ACC 的 *Exact Representation Complexity Reduction for Constrained Zonotopes with Applications to Dynamic Systems and Control* 又进一步研究**不改变集合本身**的冗余检测/删除。它很重要，因为 exact redundancy removal 天然不会破坏 nesting，但只能删除表示冗余，不能保证长期传播后的复杂度始终落在固定预算内。因此它可作为本项目压缩流水线的第一阶段，而不能替代真正的 outer reduction。

本项目候选差异只能是：**把 fixed-complexity reduction 的误差约束到 MPC recursive-feasibility 所需的有限 control normals，并与 certified support ledger 联动。** 首次性仍需继续全文排重。

## 7. 可证伪条件与下一步

主候选只有同时满足以下四项才保留：

1. outer inclusion；
2. 固定/有界 representation complexity；
3. 对真实 state/input/terminal normals 的 shifted support non-expansion；
4. 相比 static worst-case tube 有严格 tightening 改善且总计算成本可接受。

下一轮必须把 reduction 真正接入第28章 rolling 六状态 CZ，比较：naive generator-box reduction、cap-intersection repair、shared support ledger。若真实 rolling CZ 上 naive reduction 从不触发 mixed-normal reversal，或 repair 的 constraint growth/LP 成本抵消收益，则降低该候选优先级。

## 8. 复现

```bash
python verification/check_reduction_shift_monotonicity.py \
  --pairs 10000 --seed 20260924 \
  --output /tmp/reduction_shift_monotonicity.json
```

归档结果：`results/reduction_shift_monotonicity_20260924/checks.json`。
