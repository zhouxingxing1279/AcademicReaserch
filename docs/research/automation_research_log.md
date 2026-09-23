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
## 2026-09-24 — Exact rolling CZ 的 shift-nesting 自动成立；缺口转向 fixed-complexity reduction
固定预测算子 `P(S)=F S (+) W`、合法 measurement update 下，`P^i(X_k+1) subset P^(i+1)(X_k)`；horizon=8、26 ticks 数值审计 200 个 shifted inclusions，0 violations。详见第28章。

---
## 2026-09-24 — Naive fixed-complexity reduction 的 shift-support reversal 反例
第29章构造 `A=alpha B` 且只改变 generator 表示的反例。10,000 nested pairs 中 326 对在 terminal mixed normal `(4,1)` 上发生 independent reduction support reversal；coordinate normals 0 reversal。证明 outer inclusion 本身不足以支撑 shifted-candidate proof。

---
## 2026-09-24 — Rolling control-normal ledger 现实检查：当前真实 terminal normal 无 tightening 收益

### 研究问题
第29章的一般二维反例是否真的发生在当前六状态 rolling CZ 的真实控制法向？若廉价 monotone coordinate box 在真实 normals 上已经 support-exact，则 support ledger 虽安全但没有降低保守性的价值。

### 代码验证
新增 `verification/check_rolling_control_normal_ledger.py`，复用六状态 affine outer model、truth-consistent measurement、26 ticks、horizon=8。对每个 tick/horizon 查询 exact CZ 与最小 coordinate box，共每方向 234 次。

当前有来源的姿态 terminal normals `+/- (4,1)`：两方向均 `0/234` strict box gap，最大差分别约 `3.47e-18`、`6.94e-18`，即数值精度内 support-exact；其 exact support ledger 的 shifted nesting violations 为 0。

作为负对照，非控制诊断方向 `+(4,-1)` 有 `233/234` strict gaps，mean `8.613e-3`、max `1.10e-2`；`-(4,-1)` 同样 `233/234`，mean `7.496e-3`、max `9.88e-3`。因此 rolling posterior 的确存在 phi-omega correlation，只是当前已认证 terminal normal 没有消费这部分相关性。

### 被否定/降级的结论
- “第29章 mixed-normal reversal 已经证明当前四旋翼 MPC 需要 support ledger”：否定。随机/构造法向不能代替真实 controller normals。
- “control-normal ledger 当前能降低 terminal tightening”：否定；当前 `+/- (4,1)` 上 coordinate box 已经 exact。
- support ledger 的 shift-safety 接口仍成立，但降级为基础组件，不再作为当前主创新。

### 文献更新
重新核对 2026 ACC Robbins–Siefert–Pangborn 的 exact CZ representation complexity reduction：其方法删除表示冗余但保持集合完全不变，因此天然保持 support/nesting，应先于任何 approximate reduction 使用；但不能保证长期固定预算。该边界已补充进 `READ_PAPERS.md`。

### 候选创新状态
`certificate-preserving fixed-complexity reduction` 仅条件保留。要恢复为主候选，必须先得到真实 ancillary feedback `K` 和 terminal family，再证明其 state/input/terminal normals 上 exact CZ 相比 monotone box/ellipsoid 有持续严格 support gap。

### 下一轮关键任务
停止制造任意 mixed normals。当前 config 仍明确 `K=null`、`terminal_certificate=null`。下一轮应回到语义一致的 ancillary/terminal synthesis：自动生成真实 `P_MPC={state normals, K^T q_u, terminal normals}`，随后才比较 exact CZ、coordinate box、ellipsoid 和 fixed-order CZ。若真实 normals 仍无 tightening gap，应主动放弃 reduction-ledger 主线。
