# 44 S2 configuration-constrained RCI 的精确 Farkas 排除证书

日期：2026-09-24。承接第43章，仓库起点 `4224482bd92dc5448d962d64cb083be7e4f7cb2a`。

## 1. 本轮唯一问题

第43章只排除了 `alpha*S2` 的统一缩放。本轮固定第42章 `S2` 的 28 个法向，允许 14 对对称 facets 的 offsets 独立变化，并保持第42章数值审计得到的 `S2` vertex incidence（configuration cone）。问题是：在该 configuration-constrained parameterization 中，是否存在 offsets 与 vertex torque controls，使集合在两个 thrust endpoints 和 additive disturbance 下 RCI？

这是进入 Tube MPC baseline 前的阻塞点：若该 LP 可行，就得到有限复杂度 correlated RCI；若不可行，则必须区分是 configuration/template 限制还是 actuator authority。

## 2. 文献接口与创新边界

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters / ACC 2024, arXiv:2309.06998：固定 facet orientation、改变 offsets，并在有效 configuration domain 内把 vertices 表成 offsets 的仿射函数，从而用单个 LP 联合求 RCI 与 vertex controls。本轮采用的是这一类 machinery 的 model-based 特例；它不是本项目创新点。

Gupta, Köroğlu, Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, IJ Robust Nonlinear Control 31(5), 2021, DOI `10.1002/rnc.5378`：对带 additive disturbance 的 uncertain systems 计算预定义复杂度 RCI，并允许 extreme points 使用不同 admissible controls。论文还明确指出 candidate polytope shape 会影响最终结果。因此本轮的价值是为当前 frozen quadrotor lateral benchmark 建立可信 baseline / 排除证书，而不是宣称 fixed-complexity RCI 新颖。

## 3. LP 结构

沿用第41--43章系统

\[
x^+=A(T)x+B\tau+Ed,\qquad T\in\{T_L,T_U\},\quad |d|\le\bar d(T),\quad |\tau|\le0.08.
\]

令 14 对对称 offsets 为 `q`。在保持 `S2` incidence 的 configuration cone 内，每个 vertex 都有

\[
x_v(q)=V_v q.
\]

对每个 vertex `v` 分配一个 common-current torque `u_v`。对每个 endpoint 和每个 target facet `h_j`，robust invariance 是线性的：

\[
h_j^T(A(T)V_vq+B u_v)+|h_j^TE|\bar d(T)\le q_j.
\]

同时加入 configuration inequalities、hard-state containment 和 `|u_v|<=0.08`。完整 LP 的不可行性可以由下面仅四条 invariance rows 加一个 torque bound 的子系统精确证明，因此不依赖浮点 solver 的 infeasible status。

## 4. 精确 Farkas 子证书

从完整 LP 中抽取四条 endpoint-robust vertex inequalities。只保留其中出现的变量

\[
z=[q_3,q_6,q_{13},u_{26}]^T.
\]

四条不等式 `a_i^T z <= b_i` 的非零系数分别为

\[
-\frac{2943}{5000}q_6+\frac{2943}{10000}q_{13}
\le-\frac{6731149}{160000000},
\]

\[
\frac{981}{100000}q_3-\frac{2943}{10000}q_{13}
\le-\frac{6731149}{160000000},
\]

\[
-q_3+50q_6-50q_{13}-u_{26}\le0,
\]

\[
\frac{2943}{10000}q_{13}+\frac{2943}{500000}u_{26}
\le-\frac{6731149}{160000000}.
\]

取严格非负 Farkas multipliers

\[
y=\left[\frac5{11},\frac6{11},\frac{2943}{550000},1\right]^T.
\]

加权相加后，三个 offset 系数精确抵消，只剩

\[
\frac{2943}{5500000}u_{26}
\le -\frac{6731149}{80000000}.
\]

输入约束 `u26 >= -0.08=-2/25` 等价于

\[
-u_{26}\le\frac2{25}.
\]

再乘 `2943/5500000` 与上式相加，左侧恒等于 0，而右侧为

\[
-\frac{370024843}{4400000000}
\approx-0.0840965552<0.
\]

得到矛盾

\[
0\le-\frac{370024843}{4400000000}<0.
\]

因此该 configuration-constrained LP **严格不可行**。

## 5. 结论的准确范围

**命题44.1（已证明）**：固定 `S2` 的 28 个 normals，并限制 offsets 位于保持第42章 `S2` vertex incidence 的 configuration cone 时，不存在满足当前 endpoint-exact disturbance guarantee 与 `|tau|<=0.08` 的 RCI vertex-control certificate。

**命题44.2（已证明）**：与第43章不同，本轮 infeasibility certificate 显式使用 `u26 >= -0.08`；因此 actuator authority 已进入不可行性的最小子证书。若删除该 torque lower bound，上述 Farkas contradiction 消失。

**没有证明**：所有使用相同 28 normals、但允许跨越到不同 combinatorial configuration 的 polytopes 都不可行。configuration-constrained 方法只在固定 incidence domain 内给出 affine vertex map；不能把本章结论扩大成整个 fixed-normal family 的不可能性。

**没有证明**：增加 S3/S4 normals 一定可行，也没有证明 0.08 N m 本身使任何 RCI 都不存在。

## 6. 可重复验证

新增 `verification/check_s2_configuration_farkas.py`，仅使用 Python `Fraction`。脚本逐项检查 Farkas multipliers、offset 系数精确抵消、剩余 torque coefficient 和最终负 RHS。运行：

```bash
python verification/check_s2_configuration_farkas.py \
  --output /tmp/s2_configuration_farkas.json
```

归档结果：`results/s2_configuration_farkas_20260924/checks.json`。

## 7. 命题状态更新

- **已证明**：`alpha*S2` 的所有 `0<alpha<=1` homothetic candidates 失败（第43章）。
- **已证明**：保持 `S2` incidence 的 14-offset configuration-constrained LP 也不可行；存在 4 个 invariance rows + 1 个 torque bound 构成的 exact Farkas certificate。
- **已证明**：本轮失败不再只是 uniform-offset parameterization 问题；当前 torque authority 参与证书。
- **未证明**：相同 S2 normals 的其他 configuration cones 是否存在可行 RCI。
- **未证明**：加入 S3/S4 新 normals 后是否可行。

## 8. 下一轮唯一优先问题

> 不立即宣称 S2-normal family 全部失败。先检查第44章 Farkas 子证书在加入 S3 的新 normals 后是否能够被打破：从 S3 的 52 个存活 facets 中选择直接切断证书所用 offending vertices / active chains 的最小新增 normal 集，构造扩展 configuration LP，并要求 endpoint-exact RCI certificate。若仍不可行，继续提取 exact/solver-verifiable IIS/Farkas witness；若可行，则得到第一个有限复杂度 correlated RCI baseline，并记录最小新增 facet complexity。
