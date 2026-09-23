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

### 研究问题
第28章留下的问题是：`A subset B` 时，独立执行 fixed-order outer reduction 是否会破坏 MPC control normals 上的 support ordering。本轮直接构造反例，而不是继续停留在“可能”。

### 反例构造
取二维 zonotope `B=Z(0,G)`，令 `A=alpha B`，`alpha in [0.65,0.98]`。A 的表示把第一根 generator 精确拆成 s=2..6 根 `alpha*g/s`；这个 split 不改变集合，因此集合层面严格有 `A subset B`。对 A/B 独立执行 generator-box outer reduction：按 `||g||_1-||g||_inf` 选择保留 generator，其余 boxify。

### 代码验证
新增 `verification/check_reduction_shift_monotonicity.py`。固定 seed `20260924`，10,000 个 nested pairs。检查 coordinate normals 与仓库姿态 terminal mixed normal `p=(4,1)`。

结果：326/10,000 pairs 在 `+/- (4,1)` 上发生 reduction support reversal；coordinate normals 0 reversal，符合 boxification 保留坐标 support 的预期。最坏样例 exact support 从 `10.249386` 收缩到 `9.802623`，但 reduction 后反而从 `10.249386` 增至 `14.634527`，reversal gap `4.385141`。结果归档 `results/reduction_shift_monotonicity_20260924/checks.json`。

### 理论结论
单次 outer inclusion `X subset R(X)` 不足以支持 recursive-feasibility shift proof。必须额外证明至少对有限 MPC normals `p_j`：`h_R(A)(p_j) <= h_R(B)(p_j)`。

### 修复候选
1. **control-normal cap intersection**：先 outer-reduce，再与旧 horizon 已认证 halfspace caps 相交。因为 exact A 已包含于旧 caps，该交仍外包 A，同时强制 finite-normal support non-expansion。缺点是 constraint count 增长，后续若再 naive reduce 会重新破坏证书。
2. **shared H-template / certified support ledger**：固定真实 state/input/terminal normals，只维护其 certified supports。`A subset B` 自动给 componentwise support monotonicity，facet complexity 固定。它不能单独替代用于 propagation/measurement intersection 的 CZ，因此更合理的是 CZ-SMF + reduced propagation set + 独立 control-normal ledger 的双层接口。

### 新增文献边界
核对 Girard 2005 zonotope reachability/order reduction、Raghuraman & Koeln 2022 Automatica CZ set operations/order reductions，以及 2026 ACC 最新 *Exact Representation Complexity Reduction for Constrained Zonotopes with Applications to Dynamic Systems and Control*。后者做不改变集合的 redundancy removal，天然不破坏 nesting，但不能保证长期传播始终满足固定复杂度预算。因此普通 reduction 与 exact redundancy pruning 均不能直接构成本项目创新。

### 候选创新状态
主候选更新为 **certificate-preserving fixed-complexity reduction + control-normal support ledger**。创新必须同时证明 outer inclusion、有界复杂度、真实 MPC normals 上 shift compatibility，并在 worst-case tube 基线上产生严格 tightening 改善。首次性仍未确认。

### 下一轮关键任务
把 naive reduction 和 cap/ledger 修复真正接入第28章六状态 rolling CZ。若真实 rolling posterior 上 mixed control normals 从不触发 reversal，或 repair 的 constraint growth/LP 成本抵消 tightening 收益，则降级该方向；否则开始构造 shifted-candidate recursive-feasibility lemma，并补 terminal append。
