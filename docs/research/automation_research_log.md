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

---
## 2026-09-24 — LPV ancillary 候选获得严格 common-quadratic 证书

第31章的 K 不再只有 frozen/switching 数值证据。找到显式 `P>0`，其 `lambda_min(P)=0.002844724644`；两个 thrust 端点的 `lambda_min(P-M'PM)` 分别为 `6.188232256e-4` 与 `6.188357202e-4`。由于 `M(T)` 对标量 T 仿射，固定 x 时 `x'M(T)'PM(T)x` 关于 T 为凸二次函数，因此端点严格不等式推出整个 `T∈[4.905,14.715]` 上的 common-quadratic stability。统一 P-metric contraction factor 为 `0.9995634925266`。

新增 `verification/check_lpv_common_quadratic_certificate.py` 与 `results/lpv_common_quadratic_20260924/checks.json`，1001 点 dense grid 仅作为实现交叉检查。该结果严格闭合无扰动 LPV ancillary 稳定性，但**不**闭合 additive remainder RCI、`|tau|<=0.08`、terminal append 或 recursive feasibility，因此 config 的 K 仍保持 null。

文献边界：Hanema–Lazar–Tóth 2017 已覆盖 LPV tube terminal/periodic contraction；Sala 2019 覆盖离散 polytopic LPV decay-rate stability；Meijer–Dolk–Heemels 2024 研究 poly-quadratic certificate/nonexistence。common-P 本身只作为基础证书，不作为创新。

下一轮必须加入语义一致的 aero + `sin(phi)-phi` remainder，优先审计真实 torque RCI margin。若 coarse P-ball 因 contraction 太弱而失败，改用 direction-aware zonotope/CZ finite-sum + certified tail，不能把 P-ball 失败误判为控制器不可行。详见第32章。

---
## 2026-09-24 — 高推力有限 reachable support 严格否定第31/32章 ancillary K

本轮没有使用粗糙 common-P ball，而直接在语义一致 `A(T)` 模型上检查 finite disturbance reachable support。固定 `T=14.715` 是合法 scheduling path；任意包含原点的 RPI 必须包含该路径下所有有限 reachable sets，因此有限 N 的 `h_RN(K)>0.08` 已足以严格否定 torque tube，不需要无限尾项。

完整 residual `|r_x|<=2.1034840625` 下，第50项即得到 `h_R50(K)=0.08029718766>0.08`，1000项有限和为 `0.09228806639`。更强的诊断是：即使删除全部 `sin(phi)-phi` remainder、只保留 `|aero_x|<=1.880`，第69项仍有 `0.08003032078>0.08`，1000项为 `0.08248294717`。因此失败不是 P-ball 保守性，也不是 Taylor remainder 单独造成；当前 aero contract 已足以淘汰该 hover-DARE K。

新增 `verification/check_lpv_torque_rpi_obstruction.py`、`results/lpv_torque_rpi_obstruction_20260924/checks.json` 与第33章。第31章 rolling CZ 在该 K 法向上的 331/468 strict gaps 仍是几何事实，但因 K 无法通过 hard-input RPI 必要条件，不能再作为正式控制性能证据。`planar_baseline.json` 的 `K=null` 继续保持。

下一轮转向约束感知 ancillary synthesis：优先搜索同时满足整个 thrust vertex family nominal stability 与高推力 finite-reachable torque support `<0.08` 的 K；若广泛搜索仍失败，再尝试形成 actuator-authority obstruction，而不是为了让控制器通过而缩小 disturbance contract。详见第33章。
