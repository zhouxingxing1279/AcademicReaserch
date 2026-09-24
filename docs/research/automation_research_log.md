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
## 2026-09-24 — 约束感知 ancillary synthesis：否定“执行器不可能”过度解释
固定 seed=20260924 的启发式搜索找到 torque-only 候选 `K=[0.00153696,0.00744545,-0.09093386,-0.09567285]`，三个 frozen-thrust 顶点均 Schur，1000项 torque support 最大仅 0.01216，说明第33章不能升级为 actuator-authority impossibility。但该 K 在低推力下 `vx`/`phi` finite supports 达 9.7573/0.8058，严重违反 3/0.45 硬界。另一个 joint-normalized 搜索候选 torque support 仍低于0.08，但低推力 `vx=3.9778`, `phi=0.451106` 仍失败。结论：真正问题是 joint state/input constrained synthesis；启发式搜索既不能证明存在，也不能证明不存在。新增 `verification/check_constraint_aware_ancillary_search.py` 与可复现结果；详见第34章。下一轮优先采用成熟 LMI/polyhedral RCI synthesis 得到可认证 baseline，再恢复 CZ-SMF tightening 比较。


---
## 2026-09-24 — vertex-consistent residual 修正第34章低推力假阴性

本轮只解决一个阻塞点：第34章把高推力顶点的统一 residual `DX=2.1034840625` 用于所有 thrust 顶点。该做法安全，但在已知 scheduling 参数 T 的 LPV 语义下额外保守。改为
`d_x(T)=1.880+T*0.45^3/6` 后，第34章 balanced candidate 在低推力的 finite phi support 从约 0.451106 降到 0.419154，实际低于 0.45；因此原“低推力 phi 失败”属于统一 worst-case residual 造成的假阴性，必须撤回。但同一候选低推力 `vx` finite support 仍为 3.69609>3，故候选总体仍被否定。

新增一个 controller-independent 必要条件：固定 T 和持续常值最坏 residual 下，任何稳定闭环的 origin-containing RPI 都必须包含平衡点 `|phi_*|=d_x(T)/T`。低推力 T=4.905 时得到 0.3984699 rad，占 `|phi|<=0.45` 权限的 88.55%，只剩约 0.05153 rad；这是独立于 K 与集合外包算法的结构性瓶颈，但尚未达到不可能性。

新增 `verification/check_vertex_consistent_ancillary_search.py`，seed=20260924、30,000 点 Latin-hypercube、220 项 finite reachable supports。12,666 个样本三个 frozen vertices 均 Schur；1,196 个通过 torque finite 必要界；320 个通过 state finite 必要界；**0 个同时通过 state+torque**。最接近样本延长到 2000 项后仍在 px/vx/phi/tau 多个方向失败。该结果是可复现实验 falsification evidence，不是 static K 不存在证明。

文献新增 Tahir–Jaimoukha 2012、Ben Sassi–Girard 2012 和 Wehbeh–Kerrigan 2025。前两者说明 controller/invariant co-design 已是成熟 baseline；后者强化“state/decision-dependent uncertainty 不应无条件替换为 uniform global set”的建模边界。

下一轮唯一优先问题：停止扩大随机 K 搜索，建立 certificate-based joint state/input synthesis baseline。必须保留 vertex-consistent W(T)，将 px/vx/phi/omega/tau 硬约束直接纳入 common-quadratic 或 polyhedral invariant certificate；若不可行，只能声称该 certificate/controller class 不可行，不能升级为物理 actuator impossibility。
