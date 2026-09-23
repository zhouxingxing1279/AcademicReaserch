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

### 研究问题

把第 22 章从 1D 推到现有六状态平面四旋翼 affine outer model。重点检查：coordinate-wise posterior midpoint 是否足以保护高维控制方向；若不足，是否能把安全 center selection 写成小型 LP。

### 新文献边界

- Andrade, Normey-Rico, Raffo, IEEE Access 2024：已经直接提出 constrained-zonotope-based Tube MPC，并在 24-state tiltrotor UAV + suspended load HIL 场景验证。因此“CZ + Tube MPC + UAV”不是创新。
- Dey, Bhasin, arXiv 2026 `2605.23661`：Output Feedback MPC with Adaptive Tubes。adaptive observer 的 state/model/initial-condition point estimates 与集合共同更新，并在线改变 tightening、terminal ingredients 与 tube geometry；作者建立 recursive feasibility 与 robust exponential stability。因此“output feedback + evolving estimate + adaptive tube”也不是足够窄的创新。

### 新理论接口

新 posterior 写成
\[
X^+=\{c+G\xi:A\xi=b,\|\xi\|_\infty\le1\}.
\]
旧方向误差预算 \(\beta_j=h_{X^-}(p_j)-p_j^\top z^-\)。若强制新 center 是 posterior member，\(z^+=c+G\xi_c\)，则保护方向只需线性约束
\[
p_j^\top G\xi_c\ge h_{X^+}(p_j)-\beta_j-p_j^\top c.
\]
连同 \(A\xi_c=b, |\xi_c|\le1\)，并最小化相对普通 point estimate 的 \(\ell_\infty\) 偏差，得到一个 LP。

该结果的价值在于：support query 与 center selection 分离；前者可沿第 21 章认证，后者只在 posterior latent coordinates 中求解。

### 代码验证

新增 `verification/check_rolling_recenter_budget.py`，复用 `check_constrained_zonotope.py` 的六状态 affine physical outer model。使用非零、真值一致 measurement sequence；62 个 protected directions = 12 signed coordinate + seed=20260923 的 50 个 mixed unit directions。

数值压力结果：

- 26 个 measurement updates；
- unrestricted coordinate-midpoint recenter 有 19 个 tick 出现 mixed-direction tube 增长；
- 共 251 个 direction-update violations；
- 最大 support 增长 `1.7869429222420186e-3`；
- budget-center LP 在 19 个 tick 必须调整 midpoint target；
- 最大 center \(\ell_\infty\) 调整 `1.5133355513984384e-3`；
- 对全部 62 directions 重新检查后，数值容差 `1e-7` 下 0 violations。

结果归档 `results/rolling_recenter_budget_20260923/checks.json`。

### 重要限制

本轮 support LP 与 center LP 仍为浮点 HiGHS。实验已实际复现同一方程和固定种子，但不是精确算术证明。第 21 章的 support certification 尚需与 center LP 的可行性 certificate 合并。

更重要的是，本轮只比较**同一 tick measurement update 前后**，刻意排除了 dynamics/process propagation。因此它证明/反驳的是 recenter geometry，不是完整 MPC recursive feasibility。

### 被否定的候选

“coordinate midpoint 是高维 CZ 的安全默认 center”被否定。它可以保护坐标投影，但不能保护 mixed control directions。

### 保留候选

保留更窄的：**control-normal-aware posterior-member recenter LP + anytime certified support budget**。若真实 MPC 只需要有限 state/input/terminal normals，则无需每次完整重建 tube geometry。

### 下一轮

`planar_baseline.json` 的 `K` 和 terminal certificate 仍为空，不能伪造完整控制器。下一轮应从仓库已有姿态/terminal 证书中提取真实 state normals、candidate-feedback input normals 与 terminal normals，构造一个真正的 shifted-candidate inequality failure；然后检查 budget center 是否保留旧 candidate。只有完成这一步，方向预算才能进入 recursive-feasibility proof。
