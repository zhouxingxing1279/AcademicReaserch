# 23 滚动 CZ 的控制方向 Recenter LP：高维反例与安全中心选择

2026-09-23。接续 [22 后验收缩不等于 Tube 收缩](22_recenter_support_budget.md)。本轮把第 22 章的一维反例推进到现有六状态平面四旋翼 affine outer model 的连续 `predict/observe` 历史 CZ，并回答两个问题：

1. 常见的“后验各坐标区间 midpoint”在高维相关 CZ 中是否足以保护控制方向？
2. 若不够，能否把 center selection 写成一个小型 LP，使 center 本身属于 posterior，同时不扩大上一时刻同一测量更新前的 protected-direction error tube？

结论：**坐标 midpoint 只保证坐标投影半径不增，并不保证混合控制方向；center selection 可以直接写成 posterior latent variables 上的 LP。**

## 1. 同时刻测量更新的精确接口

为避免把系统传播造成的 tube 增长误判为 recenter 问题，本章只比较同一 tick 的 measurement update 前后：

\[
X^- \xrightarrow{\text{measurement}} X^+\subseteq X^-.
\]

旧中心为 \(z^-\)，旧方向误差预算

\[
\beta_j=h_{X^-}(p_j)-p_j^\top z^-.
\]

新 posterior 为 constrained zonotope

\[
X^+=\{c+G\xi:A\xi=b,\ \|\xi\|_\infty\le1\}.
\]

要选一个**确实属于 posterior** 的新中心 \(z^+=c+G\xi_c\)，并保护有限控制方向 \(p_j\)，只需满足

\[
h_{X^+}(p_j)-p_j^\top(c+G\xi_c)\le\beta_j,
\]

即

\[
\boxed{p_j^\top G\xi_c\ge h_{X^+}(p_j)-\beta_j-p_j^\top c.}
\]

再加

\[
A\xi_c=b,\qquad -1\le\xi_c\le1,
\]

所有约束对 \(\xi_c\) 都是线性的。若希望尽量靠近普通 point estimate \(z^{\rm tar}\)，可解

\[
\min_{\xi_c,t}\ t
\]

subject to 上述预算约束以及

\[
-t\mathbf 1\le c+G\xi_c-z^{\rm tar}\le t\mathbf1.
\]

因此，在支持值已经查询/认证的前提下，**安全 recenter 是一个 LP，而不是另一个集合传播问题。**

## 2. 为什么 coordinate midpoint 在高维不够

若只对 \(\pm e_i\) 求支持并取每个坐标投影区间 midpoint，则可以让各坐标方向的误差半宽等于 posterior coordinate radius。因为 posterior 投影区间嵌套于 prior 投影区间，所以这些 12 个方向不会扩大。

但高维 CZ 有相关性。对一般 \(p\)，

\[
h_X(p)\neq \sum_i |p_i|h_X(\operatorname{sign}(p_i)e_i),
\]

坐标 midpoint 没有利用 mixed-direction support shrinkage。因此它可能让 \(\pm e_i\) 都安全，却让 MPC 的斜向状态约束、反馈诱导输入法向或终端多面体法向变差。

这说明第 22 章的方向预算不能被“取 posterior 中心”替代；**保护方向必须来自控制问题本身。**

## 3. 六状态 rolling CZ 实验

新增 `verification/check_rolling_recenter_budget.py`，复用：

- `configs/planar_baseline.json`；
- `verification/check_constrained_zonotope.py` 的六状态 affine physical outer model；
- 状态顺序 `(px,pz-2,vx,vz,phi,omega)`；
- 50 Hz 离散步长；
- 姿态每 tick 测量，位置每 5 tick 测量；
- 非零、真值一致的 measurement sequence。

初始真实误差取

\[
(0.015,-0.012,0.04,-0.03,0.003,-0.006),
\]

测量噪声固定为各通道 halfwidth 的 0.3 倍并交替符号，因此 posterior center 确实移动。

protected directions 共 62 个：12 个 signed coordinate directions，加固定种子 `20260923` 产生的 50 个 mixed unit directions。mixed directions 在本轮是压力测试方向；后续必须替换/补充为真实 MPC state/input/terminal normals。

### 3.1 无约束 coordinate-midpoint recenter

26 个 measurement updates 中：

- 19 个 tick 至少一个 protected direction 变差；
- 总计 251 个 direction-update 违反 \(h_{E^+}(p)\le h_{E^-}(p)\)；
- 最大 support 增长约 `1.78694e-3`。

这给出了第 22 章一维反例的高维、滚动 CZ 版本：**absolute posterior 是 measurement intersection 的子集，但按坐标 midpoint 重新定中心仍可扩大 mixed-direction error support。**

### 3.2 budget-constrained center LP

同样 26 个 updates 中，LP 每次都找到 posterior member center；19 个 tick 必须偏离 coordinate-midpoint target，最大 \(\ell_\infty\) 调整约 `1.51334e-3`。重新计算全部 62 个方向后，数值容差 `1e-7` 下违反数为 0。

这只是数值验证。当前脚本中的 support LP 和 center LP 使用 SciPy/HiGHS 浮点求解；第 21 章已经给出支持上界/成员点的有理数认证接口，但本轮尚未把 center-LP 的整个可行性证书也转成精确算术。因此不能把“0 violations”写成一般性定理证明。

复现：

```bash
python verification/check_rolling_recenter_budget.py \
  --output /tmp/rolling_recenter.json --seed 20260923
```

归档摘要：`results/rolling_recenter_budget_20260923/checks.json`。

## 4. 与 recursive feasibility 的关系：本轮只闭合了一半

本轮严格区分两个层次。

**已证明的有限方向命题：** 若 support 值准确，且 center LP 可行，则对所列 \(p_j\)，同一 measurement update 后

\[
h_{E^+}(p_j)\le h_{E^-}(p_j).
\]

证明就是 LP 约束本身。

**尚未证明：** 这不等价于完整 MPC recursive feasibility。完整 shift proof 还需要：

1. protected directions 覆盖真实 state tightening、\(K E\) 引起的 input tightening 与 terminal normals；
2. 从 tick \(k\) 到 \(k+1\) 的 dynamics/disturbance propagation 与 measurement contraction 正确组合；
3. shifted nominal trajectory 的动态一致性；
4. terminal append 条件；
5. 若 support 只得到上下界而非精确值，要用第 21–22 章的 certified sufficient inequalities。

因此本轮没有声称 recursive feasibility 已闭合。

## 5. 文献核对后的创新边界进一步收缩

Andrade, Normey-Rico, Raffo (IEEE Access 2024) 已直接提出 **Tube-Based MPC Based on Constrained Zonotopes**，并在 24-state tiltrotor UAV + suspended load 的 HIL 环境验证。它使用 zonotope reachable sets 与 constrained-zonotope admissible/nominal sets来降低高阶系统计算成本。因此“CZ + Tube MPC + UAV”也明确不是创新。

Dey & Bhasin 2026 的 *Output Feedback MPC with Adaptive Tubes* 更接近本项目：adaptive observer 同时更新 state/model/initial-condition point estimates 与集合，并让 tightening、terminal ingredients、tube geometry 随估计变化，同时声称 recursive feasibility 与 robust exponential stability。因此“输出反馈 + evolving estimate + adaptive tube”也不能作为宽泛创新点。

本项目剩余可能有差异的对象变得更窄：

> **对 constrained-zonotope state posterior，不完整重算 tube geometry，而只在 MPC 当前需要的有限 support directions 上建立 anytime-certified shrinkage budget，并把 nominal/observer recenter 本身作为 posterior-member LP；support 证书不足时拒绝或限制 recenter。**

这个表述仍需全文排重，尤其要逐式比较 Dey & Bhasin 2026 的 observer/tube update 和 Andrade et al. 2024 的 CZ tube containment。当前不能宣称首创。

## 6. 三个候选及去留

### A. protected-direction posterior-member recenter LP — 保留

- 新意候选：把 point-estimate update 转成由 control normals 和 certified support shrinkage 约束的小 LP。
- 优点：直接堵住第 22 章的 center-drift proof hole；可与第 21 章 anytime support query 联动。
- 风险：若真实 MPC normals 很多，support 查询成本可能抵消收益；Dey & Bhasin 近邻可能已有等价结构。

### B. coordinate-midpoint recenter 作为安全默认 — 否定

高维 mixed-direction 实验已给反例。它只能保护坐标投影，不能作为一般 Tube MPC recenter 规则。

### C. 完整 CZ tube 每步重算 — 作为强基线，不作为当前创新

Andrade et al. 2024 已说明 CZ-based Tube MPC/UAV 可行。后续实验必须比较本项目“有限控制方向 + certified query + center LP”与完整 CZ/zonotope tube 重算的时间和保守性。

## 7. 下一步

下一轮优先把随机 mixed directions 替换为**真实 MPC normals**。当前 `planar_baseline.json` 的 `K` 和 terminal certificate 仍为空，因此不能假装已有完整控制器。应先从仓库已证明的姿态/有限时域约束和候选反馈中抽取可认证 normals，形成：

- state constraint normals；
- candidate feedback 下的 input normals \(K^\top q_u\)；
- 已有 terminal polytope normals。

然后构造一个真正的 shifted-candidate failure：unrestricted recenter 使至少一个 tightened input/state inequality 失效，而 budget center 保留旧 candidate。只有这一步通过，方向预算才真正进入 recursive-feasibility proof，而不只是几何现象。
