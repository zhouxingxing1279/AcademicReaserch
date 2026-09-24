# 自动研究日志

## 2026-09-23 — 任意多等式 CZ 支持查询认证
第 20 章固定后验实验只能对单等式 CZ 重建原始顶点。本轮补齐一般历史 CZ 的 primal/dual 认证接口。固定 seed=20260923 的 600 个随机多等式有理数 CZ 全部通过上下界审计；详见第21章。

---
## 2026-09-23 — 后验收缩与 observer/nominal center 漂移
精确一维反例否定“posterior shrinkage 自动推出 recentered tube shrinkage”。详见第22章。

---
## 2026-09-23 — 六状态 rolling CZ 与 posterior-member recenter LP
62 个压力方向中 coordinate-midpoint recenter 出现 mixed-direction violations；posterior-member budget LP 消除数值违反。但随机 mixed directions 并非真实 MPC normals。详见第23章。

---
## 2026-09-23 — 真实 control normals 门：recenter 候选降级
18个真实法向重跑 rolling posterior 零违反；更新前 feasibility gate 已有近邻。详见第24章。

---
## 2026-09-23 — 六状态 ancillary LQR/RPI：模型合同假阳性
固定 hover LTI 上 LQR 稳定，但语义一致的全域扰动下 mRPI 在 vx/phi/tau 三个硬约束方向失败；错误使用 reduced residual 则产生假正 margin。详见第25章。

---
## 2026-09-24 — 单乘积相关性：McCormick 已 support-exact
单矩形域上线性 support 的 McCormick relaxation 已是 exact convex hull；普通 CZ 改写不会进一步缩紧。详见第26章。

---
## 2026-09-24 — 控制决策语义闭合
`deltaT` 保持 MPC decision，SMF 只认证 `phi`；给定 `phi` interval 后 robust support 是两个关于 `deltaT` 的仿射函数最大值，可精确 epigraph。详见第27章。

---
## 2026-09-24 — exact rolling CZ 的 shifted scheduling nesting
固定预测算子和合法 measurement intersection 下，证明 `X_{i|k+1} subseteq X_{i+1|k}`；六状态 rolling CZ 数值审计 200 次 shifted inclusions 零违反。详见第28章。

---
## 2026-09-24 — fixed-order reduction 可破坏 shift support nesting
构造 `A subset B` 的表示等价反例后独立 reduction，在真实 mixed terminal normal 上出现 support reversal；说明 outer inclusion 本身不足以支撑 recursive-feasibility shift proof。详见第29章。

---
## 2026-09-24 — control-normal ledger reality check
六状态 rolling posterior 上，当前 terminal normals `±(4,1)` 的 exact CZ 与 coordinate box support 无实质差异，而诊断 mixed normals 有明显差异；“CZ 更紧”不能替代真实 MPC-normal tightening 证据。详见第30章。

---
## 2026-09-24 — 语义一致 LPV ancillary 候选
保留 thrust scheduling 的四状态 LPV 模型中生成 hover-DARE feedback；rolling CZ 在其真实 torque normal 上出现 support reduction，但控制器当时尚未完成硬约束认证。详见第31章。

---
## 2026-09-24 — common-quadratic LPV stability certificate
为第31章 K 找到整个 thrust interval 有效的 common-P contraction certificate；但 nominal/LPV stability 不等于 additive-disturbance RPI 可行。详见第32章。

---
## 2026-09-24 — finite reachable support 否定旧 K
在允许的固定高推力路径上，语义一致 residual 的 finite reachable torque support 于第50项超过 0.08；仅 aero bound 也于第69项超过。因此旧 K 不能作为当前 disturbance contract 的 robust ancillary controller。详见第33章。

---
## 2026-09-24 — 约束感知 ancillary synthesis
static-K 启发式搜索没有闭合 joint state/input constraints；失败不能升级为 actuator impossibility。详见第34章。

---
## 2026-09-24 — vertex-consistent residual
采用 `d_x(T)=1.880+T*0.45^3/6` 修正统一高推力 residual 的额外保守性；30,000 点 static-K 搜索仍无样本同时通过 finite state+torque necessary checks，但不是不存在证明。详见第35章。

---
## 2026-09-24 — controller-independent actuator authority audit
移除固定反馈结构后，global residual 首个数值 torque-feasible horizon 为381；按已知T条件化后为160，约降低58%。详见第36章。

---
## 2026-09-24 — axis-aligned RCI box 结构性不可能
当前积分链不存在非空 origin-centered axis-aligned Cartesian RCI box；只否定 box certificate class。详见第37章。

---
## 2026-09-24 — hard-box 一步 robust predecessor 精确 correlated normals
一次 predecessor 精确产生 p-v、v-phi、phi-omega mixed normals；连续 thrust 的一步 velocity robustification 可精确缩为两个 thrust endpoints。详见第38章。

---
## 2026-09-24 — 第二次 predecessor 证明 pairwise normal family 不闭合
exact-rational 反例证明 `X1=X∩Pre(X)` 不是 RCI；第38章 pairwise family 在第二次 predecessor 产生 `v-phi-omega` deeper-chain normal。当前 torque 无法修复该一步违反，因此是 template obstruction 而非 actuator saturation。详见第39章。

---
## 2026-09-24 — thrust scheduling 信息合同闭合
当前 benchmark 只蕴含 `T∈[4.905,14.715] N` 的逐点约束；任何 universal `rho<9.81 N/tick` 均被合法 endpoint alternation 否定，而 `rho=9.81` 不缩小下一 scheduling set。故 baseline 必须采用 measured-current / arbitrary-future-jump scheduling。详见第40章。

---
## 2026-09-24 — arbitrary-jump predecessor 精确端点化

本轮证明 frozen 横向 LPV 模型的一步 polyhedral robust predecessor 可无损地把连续 `T∈[T_L,T_U]` 替换为两个 endpoints。原因是 `A(T)` 与 residual 半径 `dbar(T)` 都对 T 仿射；对任一 target facet 消去 `|d|<=dbar(T)` 后，robust inequality 左端仍是 T 的仿射函数，区间最大值必在端点。由 polyhedron closure 归纳，repeated predecessor 每一层都可同样端点化；这不是 thrust grid。

同时用 Fraction 精确枚举 raw row pullbacks：深度1..6不同正向 normals 数为 `5,8,14,25,44,76`。该计数没有执行 torque existential projection、hard-set intersection 和 redundancy elimination，因此只作为 normal-growth 诊断，不能升级为 facet-complexity 定理。

文献边界：Mulagaleti–Mejari–Bemporad 的 PD-RCI 已覆盖 bounded-rate parameter-dependent RCI；Mejari–Mulagaleti–Bemporad 已覆盖 fixed-orientation configuration-constrained LPV RCI；Abbas 2024 已使用 future scheduling uncertainty/tubes 构造 general polytopic invariant tubes。因此端点化和 fixed-normal LPV RCI 都只作为 baseline 技术，不宣称创新。

新增第41章、`verification/check_endpoint_predecessor_reduction.py` 和 `results/endpoint_predecessor_reduction_20260924/checks.json`。

下一轮唯一优先问题：对 endpoint-exact predecessor 真正执行 torque existential projection 与 redundancy elimination，计算 `S_n=X∩Pre(S_{n-1})` 前若干层，判断 facet family 稳定、持续增长或集合变空，并定位首先成为阻塞的 hard state/input constraint。