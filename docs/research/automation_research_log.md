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

### 研究问题

检查第 23 章是否把“随机 mixed-direction 几何反例”过早解释成了“本项目 MPC shifted candidate 会失败”。只允许使用仓库已经有严格来源的 control normals，不人为挑选一个方便制造反例的六状态反馈增益。

### 使用的真实法向

- 六状态 state/domain box 的 12 个 signed coordinate normals；
- `theory/05` 已证明有限姿态终端多面体的 4 个 faces：`±(1,0)`、`±(4,1)`；
- 同一证书反馈 `K_a=[8/25,4/25]` 对 torque tightening 诱导的 `±K_a`。

共 18 个方向。完整 `planar_baseline.json` 仍有 `K=null`、`terminal_certificate=null`，所以不存在可诚实使用的 translational feedback/input normals。

### 代码实验

新增 `verification/check_control_normals_recenter.py`，复用第 23 章相同的六状态 affine outer model、truth、测量时序和非零 truth-consistent measurement rule。

实际运行结果：26 次 updates、18 个真实已认证方向，`violation_ticks=0`、`direction_violations=0`，最大 growth 仅 `3.33e-16` 数值舍入量。归档于 `results/control_normals_recenter_20260923/checks.json`。

### 新文献边界

Ping (2015), *Dynamic Output Feedback Robust Model Predictive Control via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems* 明确指出 estimation-error set 刷新后主 MPC 下一时刻可行性可能丢失，并使用辅助 feasibility condition；失败时继承旧 controller parameters。结合 Köhler et al. 的 monotonic/non-increasing RAMPC 条件与 Dey/Bhasin 2026 adaptive tubes，说明“估计集合更新前加 recursive-feasibility gate”本身也不是创新。

### 被否定/收缩

- 否定：“第 23 章已证明 unrestricted recenter 会破坏本项目 Tube MPC recursive feasibility。”
- 保留但降级：“finite control-normal certified update gate”仅是候选；必须等完整六状态控制器产生真实 `K^T q_u` 与 terminal normals 后再检验。
- 否定研究捷径：不能为了制造 recenter failure 而先挑一个未认证的 K。

### 下一轮

优先回到控制基础：从 04/05/08/09 的有限时域、姿态 RPI、硬输入约束结果出发，尝试合成一个满足硬约束的六状态 ancillary feedback/terminal family。只有它通过独立证书后，才重新测试 recenter 候选。如果真实 normals 仍不触发问题，应主动放弃 center-budget 作为主要创新，转向 CZ 压缩/外包对真实 tightening 保守性的可证明改进。
