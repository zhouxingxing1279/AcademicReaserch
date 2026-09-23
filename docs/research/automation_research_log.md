# 自动研究日志

## 2026-09-23 — 任意多等式 CZ 支持查询认证

第 20 章固定后验实验只能对单等式 CZ 重建原始顶点。本轮补齐一般历史 CZ 的 primal/dual 认证接口。对 \(\mathcal Z=\{c+G\xi:A\xi=b,\|\xi\|_\infty\le1\}\)，任意乘子给上界
\[
U=p^\top c+\lambda^\top b+\|p^\top G-\lambda^\top A\|_1,
\]
任意经精确核验成员给下界。固定 seed=20260923 的 600 个随机多等式有理数 CZ 全部通过上下界审计；不能推广成任意病态实例的成功定理。详见第 21 章。

---

## 2026-09-23 — 后验收缩与 observer/nominal center 漂移

设 \(E^-=X^--z^-\)、\(E^+=X^+-z^+\)。protected direction \(p\) 上 tube 不扩大当且仅当
\[
h_{X^+}(p)-p^\top z^+\le h_{X^-}(p)-p^\top z^-.
\]
等价 center-shift budget 为 \(-p^\top\delta z\le\Delta h_p\)。精确一维反例否定“posterior shrinkage 自动推出 recentered tube shrinkage”。10,000 个嵌套区间中任意 posterior center 有 11.5% 失败。详见第 22 章。

---

## 2026-09-23 — 六状态 rolling CZ 与 posterior-member recenter LP

第 23 章把一维反例推进到六状态 rolling CZ。62 个压力方向中，coordinate-midpoint recenter 在 26 次 measurement update 的 19 个 tick 出现 251 个 mixed-direction violations，最大 support 增长约 `1.78694e-3`；posterior-member budget LP 将数值违反降为 0。但这些 mixed directions 当时并非真实 MPC normals，因此只证明几何现象，不证明 recursive-feasibility failure。

---

## 2026-09-23 — 真实已认证 control normals 门：第 23 章候选被降级

使用 state/domain box、姿态 terminal faces 与已认证姿态反馈诱导的共18个真实法向重跑 rolling posterior：26次 updates 中 `violation_ticks=0`、`direction_violations=0`。因此否定“第23章已证明 unrestricted recenter 会破坏本项目 Tube MPC recursive feasibility”。Ping (2015) 又说明 estimation-set update 前的 feasibility gate 已有直接近邻。下一步必须先独立合成完整六状态 ancillary controller。

---

## 2026-09-23 — 六状态 ancillary LQR/RPI：发现模型合同假阳性

固定 hover LTI 上 LQR 得 `rho(A+BK)=0.9778088237`。语义一致的全域扰动 `dx=4.3107340625` 下，mRPI 在 `vx/phi/tau` 三个硬约束方向失败；若错误使用保留 `-T*phi` 才成立的 reduced residual，则所有 margin 看似转正，形成危险假阳性。因此下一步转向 `deltaT*phi` correlation-preserving joint tube。详见第25章。

---

## 2026-09-24 — 单乘积相关性：McCormick 已 support-exact，CZ-vs-McCormick 候选被否定

### 研究问题

验证第25章提出的 independent box / McCormick / CZ-joint 三路比较是否真的存在第三层几何优势。

### 理论结果

对 `d=deltaT in [-a,a]`, `phi in [-b,b]`, `q=d*phi` 与线性方向 `c=(cd,cphi,cq)`，exact support 在四个源域角点取得。独立 q-box 的 support 为

\[
h_{box}=|c_d|a+|c_\phi|b+|c_q|ab.
\]

若三项均非零，则独立最优符号兼容当且仅当 `sign(cq)=sign(cd*cphi)`。不兼容时精确 gap 为

\[
h_{box}-h_{exact}=2\min(|c_d|a,|c_\phi|b,|c_q|ab).
\]

McCormick 四面体/多面体正是单 bilinear graph 在 rectangle 上的 convex hull；线性 support 对集合与 convex hull 相同，所以 `h_McCormick=h_exact`。普通 CZ 可表示同一个 bounded polytope，但不能仅靠表示变化进一步减小 support。

### 代码验证

新增 `verification/check_bilinear_correlation_hull.py`，seed=20260924，10,000 个随机方向：

- McCormick vs exact 最大误差 `3.55e-15`；
- 解析 gap 公式最大误差 `3.55e-15`；
- 5002/10000 方向 independent box 严格更松；
- 平均 gap `0.3100087410`，本批最大 `3.1570853516`。

对物理映射 `y=[deltaT, -g*phi-deltaT*phi]`：纯 horizontal direction `(0,1)` 的 exact 与 independent 都为 `6.62175`，gap=0，直接否定“保留乘积相关性必然缩小 vx tightening”。mixed direction `(-1,1)` 则 exact=7.11225、independent=11.52675，gap=4.4145；相反 `(1,1)` gap 又为0。

### 文献核对

新增 McCormick (1976)、Müller–Serrano–Gleixner (SIAM J. Optim., stronger bilinear separation over nonrectangular projections)、Kochdumper–Althoff (Acta Informatica 2023, constrained polynomial zonotopes)。文献边界明确：box 单乘积 convexification 与 polynomial set representation 都已有成熟理论。

### 被否定/收缩

- 否定：“CZ joint representation 比 McCormick box hull 更紧”作为创新。对当前单乘积线性 support 不成立。
- 否定：“保留 deltaT*phi 相关性会自动降低 vx tightening”。纯 vx 一步 support 没有收益。
- 降级：constrained polynomial zonotope 作为创新。已有 quadratic-map 闭包理论，只能作为实现工具。

### 保留候选

转向 **SMF-conditioned bilinear support**：只有当 SMF/历史约束能把 bilinear variables 的联合可行域从 rectangle 收缩成非矩形 `P_k` 时，才可能比 box McCormick 进一步降低 support。Müller 等的二维投影结果正是强近邻。

### 下一轮最关键模型审计

`deltaT` 是控制决策，不是普通被估状态。下一轮必须先判断 SMF posterior 是否真的能合法地产生 `(deltaT,phi)` 联合域；若不能，就不能把 posterior correlation 强行用于 future control decision。应改写成 decision-dependent/scheduling tube：给定候选 `deltaT_i` 后只传播 `phi` uncertainty，或使用 admissible control sequence 的 robust bilinear envelope。只有模型语义先闭合，才进入多步 Tube MPC。
