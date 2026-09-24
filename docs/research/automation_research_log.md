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
固定 seed=20260924 的启发式搜索找到 torque-only 候选，但 state supports 失败；另一个 joint-normalized 候选仍在低推力 vx/phi 边界失败。结论：真正问题是 joint state/input constrained synthesis；启发式搜索既不能证明存在，也不能证明不存在。详见第34章。

---
## 2026-09-24 — vertex-consistent residual 修正第34章低推力假阴性
改为 `d_x(T)=1.880+T*0.45^3/6` 后，第34章 balanced candidate 的低推力 phi support 降到 0.419154<0.45，但 vx 仍为 3.69609>3。30,000 点 static-K 搜索无样本同时通过 finite state+torque necessary checks；这是 falsification evidence，不是不存在证明。详见第35章。

---
## 2026-09-24 — controller-independent actuator authority audit 与 scheduling-conditioned residual 基线
移除固定反馈结构后，global residual 的首个数值 torque-feasible horizon 为 N=381；按已知 T 条件化同一解析 residual 后为 N=160，约降低58%。因此 static-K failure 不能升级为 actuator impossibility；但 horizon 最短性仅为 HiGHS 数值证据。详见第36章。

---
## 2026-09-24 — axis-aligned RCI box 结构性不可能
对 `p+=p+h v`，任何有限 P、V>0 的 origin-centered Cartesian box 都包含 `(P,V)` 并一步越界；V=0 又被非零 residual 一步破坏。因此当前模型不存在非空 origin-centered axis-aligned Cartesian RCI box。该结论只否定 box certificate class。详见第37章。

---
## 2026-09-24 — hard-box 一步 robust predecessor 给出精确 correlated normals
第37章提出至少加入 p-v braking facets；本轮证明这仍不够。对当前 hard box 做一步 robust controlled-predecessor，精确得到 `|p+h v|<=5`、`|v-hT phi|+h dbar(T)<=3`、`|phi+h omega|<=0.45` 以及角速度的 admissible-torque 条件，因此 template 必须至少包含 p-v、v-phi、phi-omega 三类 mixed normals。

对固定 `(v,phi)`，速度 robust-support `|v-hT phi|+h(1.880+T*0.45^3/6)` 关于 T 为凸函数，所以整个连续 thrust interval 的最大值精确落在 T_low/T_high 两端，不需要网格采样。exact-rational corner witnesses：`p=5,v=3` 位置越界 3/50；`phi=.45,omega=2` 姿态越界 1/25；`v=3,phi=-.45` 在低/高推力正最坏 residual 下分别速度越界约 0.0832349/0.174505。

文献核查 Gupta–Köroğlu–Falcone 2021（DOI 10.1002/rnc.5378）：论文正文确实处理 rationally parameter-dependent + additive disturbance、polytopic state/input constraints、predefined-complexity symmetric polytopic RCI，并不强制固定线性 feedback；因此 correlated fixed-complexity RCI 本身不是创新。本轮贡献只是为当前四旋翼降阶模型从 exact predecessor 推导非任意 shape prior。

新增第38章、`verification/check_hard_box_predecessor_facets.py` 与 exact-rational 归档结果。尚未证明该一次 predecessor 或固定 normals candidate 是 RCI。

下一轮唯一优先问题：使用第38章导出的 p-v/v-phi/phi-omega normals 建立第一个 fixed-complexity correlated polytope candidate，并做真正 robust controlled-invariance feasibility certificate；对允许 T、d in W(T) 与全部 state/input constraints，检查 candidate extreme points 是否存在 admissible scheduling-dependent torque。若失败，区分 facet complexity 不足与 actuator authority，不恢复随机 K/CZ geometry 搜索。
