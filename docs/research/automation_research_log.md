# 自动研究日志

## 2026-09-23 — 任意多等式 CZ 支持查询认证

第 20 章固定后验实验只能对单等式 CZ 重建原始顶点。本轮补齐一般历史 CZ 的 primal/dual 认证接口。对 \(\mathcal Z=\{c+G\xi:A\xi=b,\|\xi\|_\infty\le1\}\)，任意乘子给上界，任意经精确核验成员给下界。固定 seed=20260923 的 600 个随机多等式有理数 CZ 全部通过上下界审计；不能推广成任意病态实例的成功定理。详见第 21 章。

---

## 2026-09-23 — 后验收缩与 observer/nominal center 漂移

设 \(E^-=X^--z^-\)、\(E^+=X^+-z^+\)。protected direction \(p\) 上 tube 不扩大当且仅当 \(h_{X^+}(p)-p^\top z^+\le h_{X^-}(p)-p^\top z^-\)。精确一维反例否定“posterior shrinkage 自动推出 recentered tube shrinkage”。详见第 22 章。

---

## 2026-09-23 — 六状态 rolling CZ 与 posterior-member recenter LP

62 个压力方向中 coordinate-midpoint recenter 出现 mixed-direction violations；posterior-member budget LP 消除数值违反。但随机 mixed directions 并非真实 MPC normals，因此只证明几何现象。详见第23章。

---

## 2026-09-23 — 真实 control normals 门：recenter 候选降级

使用 state/domain box、姿态 terminal faces 与已认证姿态反馈诱导的18个真实法向重跑 rolling posterior：26次 updates 中零违反。Ping (2015) 又说明 estimation-set update 前 feasibility gate 已有近邻。详见第24章。

---

## 2026-09-23 — 六状态 ancillary LQR/RPI：模型合同假阳性

固定 hover LTI 上 LQR 稳定，但语义一致的全域扰动下 mRPI 在 vx/phi/tau 三个硬约束方向失败；错误使用 reduced residual 则 margin 看似转正。下一步转向 `deltaT*phi` correlation。详见第25章。

---

## 2026-09-24 — 单乘积相关性：McCormick 已 support-exact

对 `d=deltaT`, `phi`, `q=d*phi`，单矩形域上线性 support 的 McCormick relaxation 已是 exact convex hull；普通 CZ 改写不会进一步缩紧。10,000 随机方向验证解析 gap 公式。纯 horizontal direction 无收益，mixed direction 可有大 gap。详见第26章。

---

## 2026-09-24 — 控制决策语义闭合：SMF 只估 phi，deltaT 保持 MPC decision

### 研究问题

第26章留下最关键语义问题：`deltaT` 是未来控制决策，不是被估状态。若直接构造 `(deltaT,phi)` SMF joint posterior，会把控制变量伪装成不确定变量。本轮寻找合法且仍能利用 SMF 收缩信息的 robustification 接口。

### 理论结果

对当前小角度项

\[
a_x=-(g+d)\phi,\quad d=\delta T,
\]

若 SMF/预测器只认证 `phi in [ell,u]`，则任意 mixed output direction `(rz,rx)` 在给定 `d` 下的精确 support 是

\[
H(d)=\max\{r_zd-r_x(g+d)\ell,\ r_zd-r_x(g+d)u\}.
\]

这不是 bilinear nonconvex robust counterpart：对 `d` 而言它是两个仿射函数的最大值，因此可用两个 epigraph 线性不等式精确嵌入 MPC。`deltaT` 从始至终保持优化变量，不进入 SMF posterior。

若 `[ell,u] subset [-b,b]`，集合单调性给出 `H_post(d)<=H_global(d)`。严格改善只在全域最坏端点被 posterior 排除且相关系数非零时成立，不应写成无条件性能改善。

### 代码验证

新增 `verification/check_decision_conditioned_support.py`，seed=20260924，10,000 个随机严格 posterior intervals、thrust decisions 和 directions：

- endpoint exact 与 center-radius 公式最大误差 `3.55e-15`；
- 10,000/10,000 本批随机严格子区间相对全域 phi box support 严格降低；
- posterior 平均宽度比 `0.3319193`；
- 平均 support reduction `2.3876276`，最大 `43.5594018`。

这些数值只验证单 stage support，不证明 recursive feasibility。

### 文献核对

新增/强化三类近邻：Bujarbaruah–Nair–Borrelli (ECC 2020) 已用 set-membership refinement 处理 state-dependent uncertainty；Hanema et al. (IET CTA 2021) 已从 state/scheduling relation 构造 future scheduling tubes 并证明 recursive feasibility/stability；Abbas (Automatica 2024) 已用 anticipated scheduling uncertainty bounds 降低 LPV-MPC 保守性；Fleming–Hawari (IEEE L-CSS 2024) 已研究 gain-scheduled tube MPC 并证明 recursive feasibility/exponential stability。

### 被否定/收缩

- 否定：`(deltaT,phi)` 普通 SMF joint posterior。`deltaT` 是未来决策，不应被估计。
- 降级：decision-conditioned support epigraph 作为独立创新。它是精确、实用的接口，但 scheduling/LPV robust MPC 已有强近邻。
- 收缩：“SMF posterior 更窄就一定提升闭环性能”。目前只能严格说 support 不增；性能与可行域改善仍需 MPC 层证明/实验。

### 保留候选

**Certified CZ-SMF-to-scheduling-tube interface**：从 rolling CZ-SMF 为每个预测步只计算真实 MPC normals 所需的 `phi`/state support，形成可审计 future scheduling bounds；再研究这些 bounds 在 receding-horizon shift 后的嵌套条件，使 decision-conditioned tightening 能进入 recursive-feasibility proof。

### 下一轮关键证明义务

构造 horizon-wise `[ell_{i|k},u_{i|k}]` 并验证/否证

\[
[\ell_{i|k+1},u_{i|k+1}]\subseteq[\ell_{i+1|k},u_{i+1|k}].
\]

若 measurement posterior 更新与预测使该包含失败，则必须给出反例，并确定需要 monotone envelope、update gate 还是 old-tube fallback。下一轮应直接用 rolling CZ 代码做跨时刻验证，而不是继续静态随机区间。
