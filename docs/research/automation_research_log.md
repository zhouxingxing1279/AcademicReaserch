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
## 2026-09-24 — Rolling control-normal ledger 现实检查
当前姿态 terminal normals `+/- (4,1)` 上 coordinate box 对 rolling CZ support-exact；诊断 `+/- (4,-1)` 有明显 gap。因此 support-ledger/reduction 主线降级，等待真实 ancillary feedback 自动产生输入法向。详见第30章。

---
## 2026-09-24 — 保留推力语义的 LPV ancillary 候选：真实输入法向出现 CZ gap

### 研究问题
第30章因 `K=null` 无法判断 CZ posterior correlation 是否会在真实输入约束中产生 tightening 收益。本轮不再人为挑 mixed normal，而在第12/25章语义一致的 `A(T)` 家族上用 hover DARE 生成一个 ancillary 候选，再检查由 `|tau|<=0.08` 自动产生的 `K` 法向。

### 理论/模型
使用 `e=[px,vx,phi,omega]` 与 `vx+=vx-h*T*phi`，保留已知/决策推力 T；不把 `(T-g)phi` 错误独立盒化。得到候选

`K=[0.1425749515, 0.2006738212, -1.1714620252, -0.2286054551]`。

冻结 `T={4.905,9.81,14.715}` 的谱半径分别为 `0.9915812083, 0.9778088237, 0.9781403290`。端点矩阵全部长度1–12 switching products 的最大归一化谱半径 `0.99158120835`。这只是 falsification search，不是任意 switching 稳定证明；config 的 `K` 保持 null。

### 代码验证
新增 `verification/check_candidate_lpv_input_normal.py`。将候选 K 嵌入六状态真实 torque input normal，在第30章相同 rolling CZ（26 ticks, horizon=8）上比较 exact CZ 与 minimal coordinate box。正负方向共 468 queries：331 次 strict gap，mean `3.1982541e-5`，max `1.8127720e-4`。

这首次表明由**真实反馈候选 + 真实 torque constraint**产生的 normal 会消费 CZ posterior correlation；但 gap 很小，且 K 尚无 common Lyapunov/RCI/terminal certificate，因此不能声称可行域已改善。

运行环境：Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0。结果归档 `results/candidate_lpv_input_normal_20260924/checks.json`。

### 文献更新
新增 Hanema–Lazar–Tóth, Automatica 2017：LPV tube MPC 的 periodically contractive terminal set/cost；新增 Ping–Yao–Ding–Li, IEEE TCYB 2022：LPV output-feedback tube RMPC、nested RPI/RCI sets 与 scaled terminal sets。由此确认“LPV terminal family”和“nested LPV output-feedback tube”都不是创新。

### 被否定/限制
- frozen vertices Schur 不推出 arbitrary switching stability；
- 有限 switching product 搜索通过不能替代 common Lyapunov/contractive-set proof；
- input-normal support gap 不能替代 additive-remainder RPI 与 `|tau|<=0.08` 硬约束证书；
- 不修改 `planar_baseline.json` 的 `K=null`。

### 保留候选
`CZ-SMF posterior correlation -> certified tightening on real ancillary input normals` 恢复为条件候选。要成为贡献，必须证明该 gap 在合法 ancillary/terminal controller 下持续存在并转化为 nominal input margin / feasible-set 的严格改善，而不是只展示几何差异。

### 下一轮关键证明义务
对 `A(T)+BK, T in [4.905,14.715]` 搜索严格 common quadratic 或 periodically contractive certificate；若成功，再加入语义一致的 `r_x(T)` remainder 做 robust control invariant tube 和 torque margin 审计。若硬输入约束仍失败，则当前 K 只能保留为诊断法向，不能进入控制器。
