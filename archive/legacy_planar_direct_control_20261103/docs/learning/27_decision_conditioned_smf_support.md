# 27 控制决策不进入 SMF posterior：decision-conditioned support 的精确凸接口

2026-09-24。接续第26章。本轮首先完成模型语义审计：`deltaT` 是 MPC 未来控制决策，不是未知状态，因此不能构造虚假的 `(deltaT,phi)` SMF joint posterior。正确接口是：**SMF 只认证未来 `phi` 集合；MPC 在给定/优化 `deltaT` 时，对该集合做 decision-conditioned robust support。**

## 1. 当前模型下的精确单步接口

取当前小角度水平映射

\[
a_x=-(g+d)\phi,\qquad d=\delta T,
\]

并允许同时考虑 vertical thrust contribution。对输出方向 `r=(r_z,r_x)`，若 SMF/预测器给出认证区间

\[
\phi\in[\ell,u],
\]

则给定控制决策 `d` 的最坏线性贡献为

\[
H(d)=r_zd+\max_{\phi\in[\ell,u]}[-r_x(g+d)\phi].
\]

由于对 `phi` 仿射，精确值只需两个端点：

\[
\boxed{H(d)=\max\{r_zd-r_x(g+d)\ell,\ r_zd-r_x(g+d)u\}.}
\]

等价地，令 `c=(ell+u)/2`, `rho=(u-ell)/2`，

\[
H(d)=r_zd-r_x(g+d)c+|r_x(g+d)|\rho.
\]

关键点是：`H(d)` 是两个关于 `d` 的仿射函数的最大值，因此是凸的。无需把 `d` 当随机变量，也无需为 `d*phi` 构造 McCormick joint posterior。

## 2. 可直接嵌入 MPC 的 epigraph

引入变量 `t`：

\[
t\ge r_zd-r_x(g+d)\ell,
\]
\[
t\ge r_zd-r_x(g+d)u.
\]

则最小化/约束 `t` 就精确实现该 stage 的 robust support。只要 `[ell,u]` 是合法外包，这个接口就是安全的。

这给出一个比第26章更干净的模型合同：

1. SMF/CZ 负责认证 `phi`（以及后续需要的 state projection）；
2. `deltaT` 始终保留为优化变量；
3. robustification 通过 support epigraph 与 MPC 决策耦合；
4. 不存在“SMF 估计未来控制”的语义错误。

## 3. 为什么 SMF 可以降低保守性，但条件必须说清楚

全域静态基线使用 `phi in [-b,b]`，其 support 为

\[
H_{global}(d)=r_zd+|r_x(g+d)|b.
\]

若认证 posterior/prediction interval `[ell,u]` 是 `[-b,b]` 的子集，则集合包含直接给出

\[
H_{post}(d)\le H_{global}(d).
\]

严格改善并非无条件：只有当前最坏全域端点被 posterior 排除、且对应系数非零时才严格小于。这个结论比“SMF 集合变小所以 MPC 一定更好”更精确。

本轮固定 seed `20260924` 的 10,000 个随机严格子区间/控制/方向测试中，全部出现正 support reduction；平均 reduction `2.3876276223`，最大 `43.5594018269`，但这是随机压力测试，不是闭环性能定理。

## 4. 与现有文献的边界

这一接口本身不能作为“decision-dependent robust MPC”新方法声明。已有文献已经覆盖：

- Bujarbaruah, Nair, Borrelli (ECC 2020)：set-membership refinement + state-dependent uncertainty envelope + robust MPC；
- Hanema et al. (IET CTA 2021)：nonlinear system 的 LPV embedding，利用 state/scheduling relation 构造 future scheduling tube，并证明 recursive feasibility/stability；
- Abbas (Automatica 2024)：利用 future scheduling-parameter uncertainty bounds 构造 anticipated scheduling tubes，目标就是降低只用全局/rate bounds 的保守性；
- Fleming & Hawari (IEEE L-CSS 2024)：gain-scheduled tube MPC，可利用 LPV parameter rate bounds，并证明 recursive feasibility/exponential stability。

因此本项目若有贡献，不能是“未来参数区间进入 tube”本身，而必须落在 **CZ-SMF 如何产生可认证的未来 scheduling/state support，并以有限 control normals/anytime certificates 接入四旋翼输入相关动力学** 上。

## 5. 代码验证

新增 `verification/check_decision_conditioned_support.py` 与归档 `results/decision_conditioned_support_20260924/checks.json`。

复现：

```bash
python verification/check_decision_conditioned_support.py \
  --output /tmp/decision_conditioned.json --seed 20260924 --cases 10000
```

结果：

- exact endpoint enumeration 与 center-radius 公式最大误差 `3.55e-15`；
- 10,000/10,000 随机严格 posterior intervals 相对全域 `[-0.45,0.45]` 得到严格 support reduction；
- posterior 平均宽度约为全域宽度的 `0.3319`；
- 平均 support reduction `2.3876`。

限制：这是单 stage、标量 `phi` projection 的验证；尚未证明多步预测区间嵌套、recursive feasibility 或 terminal invariance。

## 6. 候选创新重新排序

### A. Certified SMF-to-scheduling-tube interface — 保留

从 rolling CZ-SMF 得到每个预测步的 certified `phi` support interval，而不是人为设置 scheduling bounds；只对真实 MPC normals 查询。若能进一步保证 shift 时未来区间满足适当嵌套，就可能形成递归可行性接口。

### B. Decision-conditioned exact support epigraph — 作为方法组件，不单独宣称创新

它解决第26章的模型语义错误且计算很轻，但属于 robust/LPV MPC 已有思想范围。

### C. `(deltaT,phi)` SMF joint posterior — 否定

`deltaT` 是未来控制决策，普通 SMF 不应估计它。除非控制策略本身被参数化并把其不确定性明确建模，否则这种 joint posterior 是伪造相关性。

## 7. 下一轮最关键证明义务

下一轮应从现有 rolling CZ 的 `phi` 投影出发，构造 horizon-wise intervals `[ell_i|k,u_i|k]`，并检查 shift 后是否满足支持嵌套：

\[
[\ell_{i|k+1},u_{i|k+1}]\subseteq[\ell_{i+1|k},u_{i+1|k}]
\]

或至少在真实 control normals 上满足 support non-expansion。若不满足，应寻找反例并明确需要哪种 set-update gate / terminal fallback。只有这一跨时刻条件闭合后，decision-conditioned tightening 才能进入 recursive-feasibility theorem，而不只是单步保守性改善。
