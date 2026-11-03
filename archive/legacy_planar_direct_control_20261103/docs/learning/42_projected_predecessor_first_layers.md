# 42 endpoint-exact predecessor 的 torque 投影与前四层 facet 审计

日期：2026-09-24。承接第41章，仓库起点 `ad828718205f643bab6d71134cc1a43f5b9aa21b`。

## 1. 本轮唯一问题

第41章只枚举了 raw row pullback，没有执行 `exists tau` 投影，因此 `5,8,14,25,44,76` 不能解释为真正 RCI facet 数。本轮只做一件事：对当前 arbitrary-jump thrust 合同，在两个精确 thrust endpoints 上构造

\[
S_{n+1}=X\cap\operatorname{Pre}(S_n),\qquad S_0=X,
\]

显式消去标量 torque，并做 LP redundancy audit，检查前若干层真正的 nonredundant facets，以及 hard torque 何时进入边界。

## 2. frozen 横向模型与量词

沿用第41章

\[
x^+=A(T)x+B\tau+Ed,
\quad x=[p,v,\phi,\omega]^T,
\]

`h=0.02`, `J=0.02`, 因而 `B=[0,0,0,1]^T`；`T in {4.905,14.715}` 已由第41章证明与连续区间 robustification 精确等价。扰动满足

\[
|d|\le \bar d(T)=1.880+T\,0.45^3/6.
\]

硬约束为

\[
|p|\le5,\ |v|\le3,\ |\phi|\le0.45,\ |\omega|\le2,
\quad |\tau|\le0.08.
\]

本章仍采用 common-current-control 信息结构

\[
\exists \tau\in[-0.08,0.08]\ \forall T\in\{T_L,T_U\}\ \forall d.
\]

## 3. 精确 torque elimination

若 `S_n={x:r_j^T x<=q_j}`，对每个 endpoint 和每个 facet 消去 disturbance 后得到

\[
a_i^Tx+b_i\tau\le c_i.
\]

其中 `a_i=r_j^T A(T)`, `b_i=r_j^T B`,

\[
c_i=q_j-|r_j^TE|\bar d(T).
\]

再加入 `tau<=0.08` 与 `-tau<=0.08`。由于 torque 是标量，Fourier-Motzkin elimination 在这里是精确投影：保留所有 `b_i=0` 行；对每个 `b_l<0` 和 `b_u>0` 的组合加入

\[
(b_u a_l-b_l a_u)^Tx\le b_u c_l-b_l c_u.
\]

因此投影步骤没有采样或近似。随后与 X 相交。

## 4. 前四层实际结果

实现先用 `fractions.Fraction` 生成 endpoint robustification 与 Fourier-Motzkin 投影的精确有理系数，再用 HiGHS LP 判断候选 inequality 是否由其余 inequalities 蕴含。为避免第5层开始出现的大系数尺度造成假 infeasible，LP 前逐行缩放；最终 facet count 因 redundancy test 使用浮点 LP，故本节计数标记为 **numerically audited**，不是 exact-arithmetic theorem。

| n | projection/intersection 后 unique candidates | LP nonredundant facets |
|---:|---:|---:|
| 1 | 17 | 16 |
| 2 | 31 | 28 |
| 3 | 135 | 52 |
| 4 | 1193 | 102 |

前四层均非空，且原点满足所有保留 inequalities。真正投影后的 facet family 在这四层仍未闭合：`16 -> 28 -> 52 -> 102`。因此第41章 raw-normal growth 不是纯粹由未投影的伪约束造成；至少在前四层，复杂度增长在 `exists tau` 后仍存在。

但不能从四层数据推出“facet 数指数发散”或“最大 RCI 不存在”。第5层 unique candidates 已达到 6655；逐 facet LP redundancy audit 在当前自动化预算内过慢，因此本轮在 n=4 截止，而不是用不稳定/未完成计算宣称第5层结论。

## 5. 哪些 hard constraints 首先产生真实收缩

`S_1` 的 16 个 facets 包括原 hard box，以及由 hard state constraints 回拉得到的：

\[
\pm(p+0.02v)\le5,
\]

\[
v-0.0981\phi\le2.96091,\quad
v-0.2943\phi\le2.957930464\ldots
\]

及其负向对应行，以及

\[
\pm(\phi+0.02\omega)\le0.45.
\]

所以第一层收缩首先由 position、velocity、attitude hard state constraints 产生；这与第38章的一步 predecessor 结构一致。

### torque bound 首次进入 nonredundant boundary：n=2

`S_1` 中有 `phi+0.02 omega<=0.45`。再回拉一步得到

\[
\phi+0.04\omega+0.02\tau\le0.45
\]

及其负向行。存在 `|tau|<=0.08` 等价地产生可达边界

\[
|\phi+0.04\omega|\le0.45+0.02(0.08)=0.4516.
\]

这对称 pair 在 `S_2` 的 LP redundancy audit 后仍保留。因此 **hard torque bound 从 n=2 起已经真实参与 projected predecessor geometry**。它不是“第2层使集合为空”的 blocker；前四层集合仍非空。正确结论只是：从 n=2 开始，不能再把 normal growth 解释成纯 state-chain 几何，actuator authority 已进入边界。

## 6. 对第39章结论的修正/加强

第39章证明 pairwise normal family 在第二次 predecessor 下不闭合。本章进一步表明：即使执行精确 scalar-input projection 和 redundancy elimination，deeper-chain correlated facets 仍然存活；因此不能通过“这些 deeper normals 最终会被 torque projection 消掉”来挽救 pairwise template。

另一方面，本章没有证明 full-complexity sequence 最终不收敛。当前可信状态是：

- **已证明**：endpoint robustification 和 scalar-torque Fourier-Motzkin projection 的公式是精确的；`|phi+0.04 omega|<=0.4516` 的 torque-bound 来源可解析推导。
- **数值审计**：n=1..4 nonredundant facet counts 为 `16,28,52,102`，各层非空。
- **未证明**：n>=5 的 exact irredundant H-representation、有限收敛、最大 RCI 非空性。

## 7. 文献边界

Blanchini, *Set invariance in control*, Automatica 35(11), 1999, DOI `10.1016/S0005-1098(99)00113-2`，是 set invariance/controlled invariance 的经典综述；本章的 predecessor fixed-point 思路属于标准集合不变性工具，不构成创新。

Rungger and Tabuada, *Computing Robust Controlled Invariant Sets of Linear Systems*, IEEE TAC 62, 2017（文献综述中可检索到该工作），以及 Gupta, Köroğlu, Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, IJ Robust Nonlinear Control, 2021，均说明 RCI computation / complexity control 已有成熟近邻。Gupta 等还明确允许不预设固定 feedback structure。因此本章的贡献定位仍是 **为当前 quadrotor frozen abstraction 建立可信 baseline certificate machinery**，而不是宣称 predecessor 或 polyhedral projection 新颖。

## 8. 可重复验证

新增：

- `verification/check_projected_predecessor_layers.py`
- `results/projected_predecessor_layers_20260924/checks.json`

运行：

```bash
python verification/check_projected_predecessor_layers.py \
  --max-depth 4 \
  --output /tmp/projected_predecessor.json
```

依赖 Python 3、SciPy。脚本从 `configs/planar_baseline.json` 读取 frozen hard bounds；模型系数使用 `Fraction` 生成，LP 只用于 redundancy classification。

## 9. 下一轮唯一优先问题

> **不要直接硬算第5层 6655 个逐行 LP。改为构造一个可认证的低复杂度 H-template synthesis：以 n=1..4 真正存活 facets 的法向簇为候选，求最大对称/非对称 template offsets 与 vertex/torque controls，并用 endpoint-exact inequalities 给出 RCI certificate；若不可行，输出 Farkas/LP infeasibility witness，区分“template complexity 不足”与“0.08 N·m actuator authority 不足”。**

这一步会第一次给出可用于 Tube MPC 的有限复杂度 correlated RCI baseline；在此之前仍不讨论 CZ 比 box/polytope 的最终保守性优势。