# 41 arbitrary-jump thrust 下 robust predecessor 的精确端点归约

日期：2026-09-24。承接第40章。仓库起点：`93c2e7e64b0b24b3985bdc738976d20304e1ff4c`。

## 1. 本轮唯一问题

第40章已证明当前 frozen planar benchmark 只能认证：当前推力可测，而未来每一步 `T_i` 可在 `[T_L,T_U]` 内任意跳变。本轮只回答：**对这个合同，连续 thrust interval 的 robust predecessor 是否能无损地只检查两个端点？**

结论：对仓库当前的离散 LPV 模型、仿射 residual 半径和 polyhedral target，答案是肯定的；这是精确等价，不是 thrust gridding。

## 2. 模型与集合

横向误差子系统写成

\[
x^+=A(T)x+B\tau+Ed,
\quad x=[p,v,\phi,\omega]^\top,
\]

其中 `h=0.02`，

\[
A(T)=\begin{bmatrix}
1&h&0&0\\
0&1&-hT&0\\
0&0&1&h\\
0&0&0&1
\end{bmatrix},
\quad B=[0,0,0,h/J]^\top,
\quad E=[0,h,0,0]^\top .
\]

扰动满足

\[
|d|\le \bar d(T)=d_0+cT,
\]

其中当前 benchmark 的 `d_0=1.880`、`c=0.45^3/6>0`，故半径对 T 仿射。

令目标多面体

\[
S=\{x:Hx\le q\}.
\]

robust controlled predecessor 定义为

\[
\mathrm{Pre}(S)=\{x:\exists\tau\in U_\tau,\ \forall T\in[T_L,T_U],\ \forall |d|\le\bar d(T),\ A(T)x+B\tau+Ed\in S\}.
\]

量词顺序对应 common-RCI baseline：选择当前 torque 后，对当前允许的 scheduling/disturbance 鲁棒。若以后允许 controller 显式读取当前 T 后再选 torque，则应改成 `forall T exists tau(T)`，那是另一信息结构，本章不偷换量词。

## 3. 命题 41.1：一步 predecessor 精确端点化

对 H 的第 j 行 `r_j^T`，消去标量扰动后的必要充分条件为

\[
r_j^T A(T)x+r_j^TB\tau+|r_j^TE|\bar d(T)\le q_j
\quad \forall T\in[T_L,T_U].
\]

因为 `A(T)=A_0+T A_1` 且 `dbar(T)=d_0+cT`，左端对 T 是仿射函数

\[
g_j(T)=\alpha_j(x,\tau)+\beta_j(x)T.
\]

仿射函数在闭区间上的最大值必在端点取得，因此

\[
g_j(T)\le q_j\ \forall T\in[T_L,T_U]
\iff
g_j(T_L)\le q_j\ \land\ g_j(T_U)\le q_j.
\]

对每一行成立，故整个 robust predecessor 与只检查 `{T_L,T_U}` 完全相同。输入约束若本身与 T 无关，不改变该结论。证毕。

### 重要边界

这个结论依赖两个结构：`A(T)` 对 T 仿射，且 disturbance support `sigma_D(r_j^TE,T)=|r_j^TE| dbar(T)` 对 T 仿射。若以后 residual envelope 改成非凸/非仿射函数，或执行器模型产生同一步 T 的高阶乘积，不能自动继续使用端点化。

## 4. 命题 41.2：任意有限 repeated predecessor 仍可逐层精确端点化

若 `S_n` 是 polytope，则命题41.1说明 `Pre(S_n)` 可由 `T_L,T_U` 两组有限线性不等式和 torque 投影得到，因此仍为 polyhedron；再与 hard polytope X 求交仍为 polytope。归纳可得

\[
S_{n+1}=X\cap\mathrm{Pre}(S_n)
\]

的每一步连续 scheduling robustification 都可精确替换为两个 endpoint systems。

注意这不是声称“固定 open-loop endpoint trajectory 足以代表反馈控制”。正确说法是：**每一层 predecessor 的 universal T quantifier 可由该层两个 endpoint inequalities 精确替换**。控制变量的存在量词和投影仍必须保留。

## 5. 多步 reachability 的补充解释

对固定初态和固定控制序列，N 步状态中的每个线性 functional 对独立变量 `(T_0,...,T_{N-1})` 是 multi-affine：矩阵乘积中每个 `T_i` 只在 `A(T_i)` 中出现一次；第 i 步 disturbance 半径依赖 `T_i`，而该 disturbance 的后续传播只依赖 `T_{i+1:}`。因此其最大值也在 hyperrectangle 的 `2^N` 个 endpoint sequences 上取得。这与逐层 predecessor 证明一致，但后者更适合 RCI 量词结构。

## 6. normal growth：端点化解决连续性，但没有解决复杂度

验证脚本从 hard-box 四个正坐标 normals 出发，仅做精确 row pullback `r <- r A(T)`，对 `T_L,T_U` 枚举并用有理数去重。深度 1..6 的不同正向 normals 数为：

| depth | unique normals |
|---:|---:|
| 1 | 5 |
| 2 | 8 |
| 3 | 14 |
| 4 | 25 |
| 5 | 44 |
| 6 | 76 |

这不是最终 `Pre` 投影后的 facet 数，因此**不能**据此宣称 RCI facet 必然指数增长；它只证明 raw endpoint pullback family 在前六层没有有限闭合迹象，并给下一轮 redundancy/projection 分析提供可重复基线。

第39章的 deeper-chain normal 现在有更清楚的来源：例如 velocity row `[0,1,0,0]` 回拉为 `[0,1,-hT,0]`；再次回拉会在 omega 分量产生 `-h^2 T`，所以 pairwise family 不闭合。

## 7. 文献核查与创新边界

1. Mulagaleti, Mejari, Bemporad, *Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate*, IEEE TAC 70(2), 2025, DOI `10.1109/TAC.2024.3454528`, arXiv:2309.02384。其核心是利用 scheduling transition/rate 信息构造 parameter-dependent RCI；第40章已说明当前 benchmark 没有可用的非平凡 rate bound。
2. Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters, 2024, arXiv:2309.06998。论文使用 fixed-orientation configuration-constrained polytopes，并通过 LP 合成 RCI 与 vertex controls；因此“固定法向 polytope + LPV vertex checking”不是我们的创新点。
3. Abbas, *Linear parameter-varying model predictive control for nonlinear systems using general polytopic tubes*, Automatica 160 (2024) 111432, DOI `10.1016/j.automatica.2023.111432`。该工作利用未来 scheduling uncertainty/tubes 构造 general polytopic invariant tubes，说明利用更强 future scheduling information 降保守性已有直接近邻。

本章可复用的是 polytopic LPV 的 convex-vertex 思想，但这里给出了针对 frozen quadrotor abstraction 与 T-dependent disturbance support 的精确 predecessor 推导。**端点化本身不作为创新点**；它只是把后续 certificate 从连续 T 严格有限化。

## 8. 可重复验证

新增 `verification/check_endpoint_predecessor_reduction.py` 与 `results/endpoint_predecessor_reduction_20260924/checks.json`。脚本只使用 Python 标准库 `fractions.Fraction`：

```bash
python verification/check_endpoint_predecessor_reduction.py \
  --output /tmp/endpoint_predecessor.json
```

它检查：A(T) row pullback 的 T 仿射性；当前 dbar(T) 的仿射性；深度1..6 endpoint pullback normal counts；并保存精确分数参数。脚本不是证明本身，证明是第3-4节；脚本用于防止实现与公式漂移。

## 9. 命题状态

### 已证明

- 当前模型的一步 polyhedral robust predecessor 对连续 T 区间可精确归约到 `T_L,T_U`；
- repeated predecessor 可逐层使用相同端点归约，不需要 thrust grid；
- raw pullback normal family 在深度1..6分别有 5,8,14,25,44,76 个不同方向（精确枚举事实）。

### 被排除

- “为了覆盖 arbitrary-jump T，必须对连续 thrust 做数值网格采样”：错误；当前仿射合同下两个端点已经精确。
- “端点化意味着第38章 pairwise template 已闭合”：错误；第39章反例仍成立。

### 尚未证明

- 经过 hard-set intersection、torque existential projection 和 redundancy elimination 后，真正 predecessor facet family 是否趋于有限 closure；
- arbitrary-jump endpoint systems 下是否存在 nonempty correlated RCI；
- 若存在，其最小有效 template 与 CZ/ellipsoid 的 tightening 比较。

## 10. 下一轮唯一优先问题

> **对 endpoint-exact predecessor 真正执行 torque existential projection 与 redundancy elimination，计算 `S_n=X∩Pre(S_{n-1})` 的前若干层，并判定 facet family 是稳定、持续增长还是集合变空；同时记录是哪一个 hard input/state constraint 首先成为阻塞。**

只有这一层完成后，才有资格选择 fixed-complexity correlated RCI template 并与 CZ-SMF 接口比较。