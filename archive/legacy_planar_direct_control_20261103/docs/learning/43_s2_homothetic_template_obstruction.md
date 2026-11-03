# 43 S2 法向模板的 homothetic RCI 排除证书

日期：2026-09-24。承接第42章，仓库起点 `7397ce81daa534ccd65bbac46e9d2be1bdc8bcb2`。

## 1. 本轮唯一问题

第42章建议从 `S1..S4` 存活法向构造有限复杂度 H-template RCI。本轮先检验最自然、也最容易被误用的候选：保持 `S2` 的全部 28 个 nonredundant facets，仅统一缩放 offsets，即

\[
P_\alpha=\alpha S_2,\qquad 0<\alpha\le1.
\]

问题是：缩小第42章已经得到的 correlated polytope，能否直接获得一个 RCI baseline？如果答案为否，就证明下一轮必须真正独立优化 offsets / vertex controls，而不能把 predecessor 截断集做简单 homothetic contraction。

## 2. 系统与信息结构

完全沿用第41--42章 frozen lateral model：

\[
x^+=A(T)x+B\tau+Ed,
\quad x=[p,v,\phi,\omega]^T,
\]

`h=0.02`, `T in [4.905,14.715]`, `|tau|<=0.08`，且

\[
|d|\le \bar d(T)=1.880+T\,0.45^3/6.
\]

使用 common-current-control 量词 `exists tau forall T,d`。第41章已证明对该模型连续 thrust robustification 精确归约到两个 endpoints。

## 3. 一个 S2 的精确顶点和精确 facet

第42章 `S2` 的 irredundant H-representation 中存在 facet

\[
r^Tx\le q,
\]

其中

\[
r=\left[-1,-\frac1{25},\frac{981}{500000},0\right],
\qquad
q=\frac{39993745617}{8000000000}.
\]

考虑 `S2` 顶点

\[
x^\star=\left[-5,0,-\frac{6254383}{15696000},2\right]^T.
\]

它由 `-p<=5`、`-p-0.02v<=5`、`omega<=2` 与上述 facet 的交点得到，因而不是浮点搜索构造的近似点。

## 4. 命题：任何 alpha<=1 的统一收缩都不是 RCI

**命题 43.1（已证明）** 对当前 frozen model 和 common-current-control 信息结构，`P_alpha=alpha S2` 对所有 `0<alpha<=1` 都不是 robust control invariant。

**证明。** 取 `P_alpha` 中的点 `alpha x*`，并只检查允许的低推力 endpoint

\[
T_L=4.905=\frac{981}{200}.
\]

对目标 facet `r^T x <= alpha q`，由于 `r^T B=0`，当前 torque 对该一步约束完全没有作用。将最坏 disturbance support 消去后，必要条件为

\[
\alpha\bigl(q-r^T A(T_L)x^\star\bigr)
\ge |r^TE|\bar d(T_L).
\]

精确有理数计算给出

\[
q-r^T A(T_L)x^\star
=\frac{5940463}{4000000000},
\]

而

\[
|r^TE|\bar d(T_L)
=\frac{6254383}{4000000000}.
\]

两者之差为

\[
\frac{6254383-5940463}{4000000000}
=\frac{981}{12500000}
=7.848\times10^{-5}>0.
\]

因为 `alpha<=1`，左侧至多等于 `5940463/4000000000`，严格小于所需 disturbance support。因此 `alpha x*` 在允许的 `(T_L,d)` 下必然离开 `P_alpha`。又因 `r^T B=0`，任何满足或不满足 `|tau|<=0.08` 的当前 torque 都无法修复这一违反。证毕。

等价地，要让这个单一 witness facet 成立，至少需要

\[
\alpha\ge\alpha_{crit}
=\frac{6254383}{5940463}
\approx1.052844>1,
\]

与“在 hard-domain 内收缩 `S2`”相矛盾。

## 5. 这说明什么、不说明什么

本章严格排除的是 **S2 offsets 的统一缩放**，不是排除 `S2` 的 normal family 本身。不同 facets 独立改变 offsets 后，顶点位置和 disturbance slack 都会改变，仍可能存在 fixed-normal RCI。因此下一步应求

\[
P(q)=\{x:Hx\le q\}
\]

中的独立 `q_i`，并联合 admissible vertex controls，而不是继续搜索单个 scale `alpha`。

同样，本章的 witness 是 torque-independent 的，所以这里的失败不能归因于 `0.08 N m` torque saturation；它是 **uniform-offset parameterization 不足** 的证书。这第一次把“template parameterization 不足”和“actuator authority 不足”明确分开。

## 6. 文献与创新边界

Gupta, Koroglu, Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, IJ Robust Nonlinear Control 31(5), 2021, DOI `10.1002/rnc.5378`：论文允许预定义复杂度的 0-symmetric polytope，并强调初始 shape 会影响所得 RCI；其方法不强制固定 state-feedback，而在 extreme points 求 admissible controls。因此“固定复杂度 polytope + vertex control”本身不是创新。

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters / ACC 2024：采用 fixed facet orientation、variable offset 的 configuration-constrained polytope，并通过 vertex representation 与 LP 联合求 RCI 和 vertex controls。这直接支持下一轮从单一 alpha 升级为独立 offsets，但也意味着这种 parameterization 本身不能作为创新点。

本项目当前潜在贡献仍应来自 **SMF 在线可靠集合信息如何以可证明方式改变 Tube MPC tightening / feasible set，同时维持递归可行性**；本章只是建立不含人为弱 baseline 的控制侧 certificate machinery。

## 7. 可重复验证

新增：

- `verification/check_s2_homothetic_rci_obstruction.py`
- `results/s2_homothetic_rci_obstruction_20260924/checks.json`

运行：

```bash
python verification/check_s2_homothetic_rci_obstruction.py \
  --output /tmp/s2_homothetic.json
```

脚本只使用 Python 标准库 `fractions.Fraction`，并断言 slack、disturbance support 和严格 gap 的闭式值；没有 LP solver、网格或随机种子。

## 8. 命题状态

- **已证明**：`alpha*S2`, `0<alpha<=1` 全部不是 RCI；存在 torque-independent exact witness。
- **已证明**：失败不能由增大当前 torque authority 修复，因为 offending row 的 `r^T B=0`。
- **未证明**：使用同一 S2 normal family、但独立优化 offsets 后是否存在 RCI。
- **未证明**：若 fixed-normal LP 不可行，是否需要加入 S3/S4 normals，或最终由 actuator authority 限制。

## 9. 下一轮唯一优先问题

> 固定第42章 S2 的 28 个法向，但允许每个对称 facet pair 独立 offsets；按 configuration-constrained polytope 的有效配置域构造 vertex-affine representation，联合求 offsets 与 vertex torque controls，并在两个 thrust endpoints 上做 exact robust certificate。若不可行，输出具体的 LP/Farkas infeasibility witness；只有在 S2-normal family 被严格排除后，才升级到 S3/S4 normals。
