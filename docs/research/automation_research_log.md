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

### 研究问题

按第24章要求，先尝试合成不依赖学习的六状态 ancillary feedback，再让真实 `K^T q_u` 决定 recenter 候选是否有控制意义。

### 文献核对

新增核对 Mayne–Seron–Raković (Automatica 2005) bounded-disturbance robust MPC，以及 Raković–Kerrigan–Kouramas–Mayne (TAC 2005) mRPI outer approximation。它们确认“稳定 K + RPI/tube tightening”是经典基线，不是创新；有限 reachable sum 不能未经尾项处理就当 RPI。

### 代码实验

新增 `verification/check_ancillary_lqr_rpi.py`。按 `planar_baseline.json` 的 Q/R 标度在 hover LTI 上求 DARE/LQR，得到 `rho(A+BK)=0.9778088237`。对 mRPI 计算 1000 项 Minkowski sum，并使用离散 Lyapunov P-范数对无限尾项做外包。

**语义一致的全域 LTI 合同**必须保留旧水平独立扰动 `dx=4.3107340625`。结果：

- `vx` support 4.37810 > 3，margin = -1.37810；
- `phi` support 0.70752 > 0.45，margin = -0.25752；
- `tau` support 0.16244 > 0.08，margin = -0.08244。

因此该 LQR/RPI 不满足硬约束。

随后主动测试一个危险错误：把第12章保留 `-T*phi` 后的较小 residual `dx=2.1034840625` 塞回固定 `-g*phi` LTI。数值上所有 state/input margin 居然都变正，其中 `tau` support=0.079264，仅比0.08小约7.36e-4。这是一个非常容易误判为成功的**假阳性**。

但它不是合法证书：较小 residual 的前提正是中心动力学保留 `-T*phi`；固定 hover A 则必须把 `-(T-g)phi` 放回不确定项。详见第25章与 `results/ancillary_lqr_rpi_20260923/checks.json`。

### 被否定/收缩

- 否定：通过调 LQR 权重即可在旧独立盒 LTI 上闭合六状态 terminal tube。第12章已有任意策略长期否证，本轮又给出标准 LQR/RPI 的直接硬约束失败。
- 否定：可以把 reduced residual 与 fixed hover LTI 组合。这会制造数值假阳性。
- 暂停：finite-control-normal recenter gate。在合法完整 ancillary controller 出现前不再扩展。

### 新的高优先候选

提升 `correlation-preserving joint tube`：显式保留 `q=(T-g)phi` 或 `T phi` 的输入—状态相关性，比较 independent box / McCormick polytope / CZ joint latent representation。目标不是“CZ更紧”的口号，而是证明在同一源域上

\[
R_{joint}\subseteq R_{corr-outer}\subseteq R_{independent-box}
\]

并在真实 state/input normals 上得到严格 support 改善，同时维持固定复杂度和 recursive-feasibility 接口。

### 下一轮

构造最小 `deltaT-phi-vx` 联合一步/多步模型，实际代码比较独立盒、McCormick 与 CZ/联合潜变量外包；必须同时找严格包含正例和“相关性方法并不更紧”的边界/反例。只有这一层成立，才推进六状态 terminal/tube 合成。
