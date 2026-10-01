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

---
## 2026-09-29 — 539-generator Scott CZ 的终端 mRPI 反例

证明冻结模型中终端包含与当前压缩集包含等价；以 exact-rational CZ witness 和 900 项+block-tail mRPI 上界得到严格支持差 `9.1323e-8`。因此 Run 126 的 539-generator CZ 虽通过 300 个阶段方向，仍不能进入 terminal/recursive-feasibility 证明链。详见 `run127_research_log.md`。

---
## 2026-09-29 — 通用 AH/CZ 终端证书的在线预算止损

重读 Sadraddini–Tedrake 的 AH/zonotope 包含充分证书并精读 Hellwig 等的可靠 witness 条件。正确处理 CZ equality 后，当前 539–605 对 `S_602` 的通用证书约需 162–182 万变量；忽略 equality 的保守 zonotope 证书仍需 65–73 万变量。605 后验已由 measurement-intersection 构造直接包含，通用 LP 不可行又不能否定 540–604，故不实现无解释力的大 LP 扫描。下一步改为随 Scott 消去维护稀疏包含 witness 的 certificate-carrying reduction。详见 `run128_research_log.md`。

---
## 2026-09-29 — 携证 Scott 消元首步失败

沿 605→604 的冻结 Scott 首次消元同步传播到 `S_602` 的系数映射，并利用 CZ 三条等式逐行优化行 `l1` 预算。4 个超限行均无法由等式修正；对偶 proposal 经三个零目标变量的精确有理数重解后，等式残差与盒超限严格为零，最小对偶间隔仍为 `1.2869e-8`。因此该携证充分规则首步即失败，但不推出 604-CZ 真实不包含。按停止规则关闭当前普通 Scott 扫描，下一步只审计 witness-constrained 非-Scott 单步替换。详见 `run129_research_log.md`。

---
## 2026-09-29 — 终端 witness 约束降阶的文献否决

精读 Sadraddini--Tedrake Section V-B/Proposition 6、Kopetzki Section III-D 和 Raghuraman--Koeln Section 5 后确认，containment-constrained zonotope/CZ reduction 已有直接近邻；当前 sandwich 只是既有模块组合。更关键的是 `R_red=S_602` 可形式上删除3列却丢弃全部 measurement 信息，现有300个控制查询全部变松，故“删至少一列”成功标准失效。直接604-generator map 参数化在完整CZ约束前已至少729,028条目。本轮不实现并关闭 post-hoc reduction；下一步转向 finite-horizon posterior tightening + backup/adaptive terminal tube 的完整架构审计。详见 `run130_research_log.md`。

---
## 2026-09-29 — 两层 output-feedback tube 架构排重

全文定向精读 Dey--Dhar--Bhasin 2022、Dey--Bhasin 2025/2026、Köhler 2021 与 Ping 2015。two-tube/two-tier 架构、在线 estimation bounds、terminal shift proof、adaptive terminal compatibility/backup，以及 zonotopic update feasibility gate/fallback 均已有直接近邻；广义“posterior finite-horizon tightening + backup terminal tube”创新/实现准入不通过。下一步只研究更窄的必要骨架：在15-mode bounded-dropout automaton和同一执行器/扰动合同下构造或反驳 mode-indexed backup terminal family，并逐边验证 robust invariance 与 input tightening。详见 `run131_research_log.md`。

---
## 2026-09-29 — 间歇数据 terminal baseline 纠偏

精读 Hassaan 等 IFAC 2021/HSCC 2021、Rutledge 等 2020、Wildhagen 等 2022。有限 missing-data language、path-dependent controller/estimator、时变 tube 和 packet-loss terminal/shift proof 已有直接近邻；尤其 Hassaan 2021 用一个对全部周期相位有效的 common `K_f,X_f` 即可证明递归可行，故 15-mode terminal family 不是默认必要骨架。当前六状态配置又缺少合法 `K` 和 terminal certificate，旧候选已被 residual/torque 合同否定。本轮不写代码；下一步先用 certificate-based joint synthesis 实例化或反驳 common-terminal baseline，只有它为空或实质过保守时才准入 mode-indexed family。详见 `run132_research_log.md`。

---
## 2026-09-29 — ancillary 与 nominal terminal 两层证书分离

全文精读 Tahir 2010、Tahir--Jaimoukha 2012，并重读 Hassaan 2021 的 tracking tube、terminal assumptions 与 shift proof。确认 Tahir 类 joint feedback/RPI synthesis 对应 disturbance-tracking ancillary 层；Hassaan common `K_f,X_f` 则作用于由该 tube 收紧后的 nominal system。当前证明义务次序据此修正。Tahir 的轴对齐 box 类已被第37章精确排除；固定形状椭球及 norm-bounded uncertainty 公式又未直接保持同一推力决定的 `(A(T),W(T))` 配对，完整六状态 estimator/recenter disturbance 合同也未冻结。因此本轮不实现语义错误的 SDP。下一步先闭合六状态 ancillary error contract 与非轴对齐 correlated-LPV RPI/RCI certificate，再恢复 common nominal terminal synthesis。详见 `run133_research_log.md`。

---
## 2026-09-29 — 实际推力使 ancillary 合同成为控制相关调度

全文精读 qLPV polytopic RCI 与 2025/2026 decision-dependent uncertainty GSIP 近邻，并重读外生 LPV tube baseline。推导六状态 tracking error 后确认：推力修正 `delta T` 同时进入横/竖误差、`delta T*z_phi` 和 `d_x(T),d_z(T)`，实际 `T` 不能再当外生 scheduling。若禁止 `delta T`，垂向非零 residual 使任何非空紧致全状态 RPI 在最大 `e_vz` 点一步越界；该结论与集合形状和反馈增益无关。因此不实现旧 paired-endpoint RPI。下一步先从 rolling SMF 得到/否定 15-mode time-uniform estimator-error family `E_eta^j`，再实例化联合图 RCI。详见 `run134_research_log.md` 与第71章。

---
## 2026-09-29 — time-uniform 模式椭球存在但控制接口严格失败

精读 graph invariant multi-set 与 intermittent-data equalized-recovery tube 近邻。对冻结六维 actual-input 误差 inclusion，15 模态 Bellman 映射为 contraction，唯一固定点给出 scalar/common-metric 类最小不变椭球多集；有向有理数证书通过17条边。但全部模式的速度支持下界均超过3 m/s、角度支持均超过0.45 rad，任何中心下的硬状态 tightening 都为空，且不能自洽闭合 residual 物理域。停止共同椭球支线；下一步仅构造 geometry-preserving reachable-sum 外不变多集及 certified tail。详见 `run135_research_log.md` 与第72章。

---
## 2026-10-01 — 联合 ancillary RCI 前的名义推力预留门槛

精读 coupled output-feedback RPI，重读 online estimation-bound MPC、qLPV RCI 与 decision-dependent GSIP。联合误差 RCI 方法学已有强近邻，不作创新声明。当前配置无独立 nominal input bounds；精确证明 nominal thrust 若允许完整 actual interval，则持续端点计划使垂向速度误差严格单调漂移，任何有限 mode-indexed compact ancillary family 都不存在。必要 nominal thrust 区间为 `[7.48763125,11.13910625] N`，hover 通过但 RCI 存在性仍未证明。新增 exact verifier；下一步先冻结 nominal thrust/torque allocation，再做 augmented `(eta,d)` RCI。详见 `run137_research_log.md` 与第74章。

### 2026-10-02 Run 138

重读 Lorenzetti--Pavone coupled RPI 的 input projection 与 Köhler nonlinear joint tightening/terminal proof。冻结一个显式、最有利的 ancillary-RCI existence probe：nominal thrust `[8.48089375,11.13910625]`、correction `+-3.57589375`，nominal torque `{0}`、correction torque `[-0.08,0.08]`。精确验证 Minkowski 输入合同，但推力上边界余量为0且 nominal torque 无内点，因此不升级为最终 MPC allocation。本轮不启动高维 solver；下一步在共享噪声与 actual-thrust residual graph 下构造或严格否定 augmented RCI。详见 `run138_research_log.md` 与第75章。

### 2026-10-02 Run 139

重读 Lorenzetti--Pavone fixed-policy augmented RPI，精读 Mejari--Mulagaleti--Bemporad RCI 量词与 Wehbeh--Kerrigan decision-dependent uncertainty。确认当前 augmented `(eta,d)` 问题缺少 partial-information quantifier、causal policy、nominal state domain、17-edge input timing、actual-thrust shared primitive graph 和 nonempty initialization slice；普通 full-state RCI 会允许控制读取隐藏 `eta`。新增 contract gate 与6项测试，当前配置返回 `blocked`；该结论只证明问题未实例化，不证明 RCI 不存在。并修复 Run138 配置变更造成的两个旧 envelope 陈旧 hash，重建确认几何未变；全仓170/170通过。下一步先冻结17条 edge 的 exact joint update 与 causal policy class，再启动 synthesis。详见 `run139_research_log.md` 与第76章。
