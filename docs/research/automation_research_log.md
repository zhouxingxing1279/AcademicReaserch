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

### 2026-10-02 Run 144

精读 Houska 2023 的 invariant information ensemble 与 polytopic extreme-set control，重读
Hempel 2011 fiber 量词，并精读 Kumar--Kothyari 2026 zonotope-LP output-feedback RCI。
联合信息集及其多面体优化已有直接近邻，本轮只作当前 packet/shared-primitive 合同的一步
实例化。对正确候选 `S_j=E_eta_vertical^j x B_e`，精确证明 modes 4、9、14 的 predecessor
均包含 `|d_pz|<=1/5,|d_vz|<=1/4` 对应的四维正体积内集；统一 `deltaT=0` 同时服务
mode 4/9 两条未知后继，且 residual 半宽由同一 actual thrust 计算。该结果仅排除三个关键
模态“一步即空”，不是 RCI 或递归可行性。下一步执行全15模态的一次 joint descending
predecessor sweep。详见 `run144_research_log.md` 与第81章。

### 2026-10-02 Run 145

重读 Rungger--Tabuada 2017 的 descending predecessor/停止证书、Houska 2023 的
information ensemble 极端集合控制及 Hempel 2011 的 fiber 共享输入量词。一次下降层和
多面体信息投影均是已有方法，本轮不作创新声明。对15个 packet mode 构造零修正、完整
隐藏 fiber 的 exact observation 内投影；15/15 均为正面积，17/17 estimator edges 精确
包含，且都保留 Run144 公共 observation box。证据仅为 first-sweep 四维正体积内集，不是
最大投影、固定点或 RCI。下一步以本轮保留集合为 target 执行第二层，判断该受限 policy
class 是否自映射。详见 `run145_research_log.md` 与第82章。

### 2026-10-03 Run 147

先审计远端新增Run146并独立复现其second-sweep证书。排重发现Run146要求“压缩mode-14
`q|d`且保留初始化miss-chain”的下一问题已被Run143精确否定，故停止重复支线。精读
Houska 2023 information ensemble的控制不变性、极端集合与多面体tube，重读Hempel 2011
fiber量词。本轮把初始化14条miss后的完整`E_14`经强制success映成共享原语的四行
zonotope：106列、精确rank 3；完整`eta`和真实`e`投影满足当前竖直约束，虽然`d_v`支持
严格超过Run146 product target约0.641398。它是必要correlated return seed，不是RCI。
下一步统一核查5/10/15 tick三种return seed的mode-0相关模板。详见
`run147_research_log.md`与第84章。

### 2026-10-03 Run 148

重读Houska 2023 Sections 6.4--6.7的极端信息多面体/连续凸权重控制、Hempel 2011 OFCI
fiber量词和Dey--Bhasin 2026 adaptive tube收紧与递归可行性。对固定零修正初始化
5/10/15 tick三种success return构造共享原语exact联合像：三者rank均为3且满足竖直约束。最小凸容器
`conv(J4 union J9 union J14)`有exact perspective lift，仍rank 3，但mode-0 estimator
两坐标余量均为0；直接拼接生成元会错误形成Minkowski和并违反约束。后续语义复核确认
连续selector允许分数混合，且零中心return依赖全零correction；故本轮只认证fixed-policy
baseline，不是policy-independent必要target或RCI。下一步先做零策略自映射核查，再决定
是否准入带中心平移的causal predecessor。详见`run148_research_log.md`与第85章。

### 2026-10-03 Run 149

先修复Run148把零修正image称为一般必要target、把连续selector含混为路径排他的证据边界。
随后重读Houska 2023固定扰动集下的intrinsic separation、Hempel 2011 OFCI量词，以及
Wehbeh--Kerrigan--Scaccia 2026 decision-dependent uncertainty GSIP。精确有理数证书表明：
固定Run136 global residual envelope时，correction对miss/success联合动力学都只产生中心
平移；保留`r_z(barT+deltaT)`时，一步共享生成元在实际推力端点间严格增加
`79461/4000000`，同时改变联合形状。故后续先研究`C0+c`固定shape translation类；scheduled
分支必须作为decision-dependent robust containment单独认证。详见`run149_research_log.md`
与第86章。

### 2026-10-03 Run 150

刷新远端并独立复验Run149后，重新精读Houska 2023关于fixed-`W` intrinsic separation、
translation functions与extreme information controls的相关定理；复核Hempel fiber量词及
Wehbeh等2026 GSIP边界。把Run148的`C0=conv(J4 union J9 union J14)`沿固定Run136
envelope传播后，三条success return的`e_p`半宽均严格超过`C0`：mode 4/9/14超量分别为
`32650721/144000000`、`70450729/144000000`、`4725001/6000000`。集合中心和current
correction只平移，不能改变宽度；故最早在mode 4即否定translated fixed-shape family，
但不否定history-conditioned ensemble或scheduled GSIP。下一步构造最小return-age/history-
conditioned intrinsic shape family并检查有限周期fixed point。详见`run150_research_log.md`
与第87章。

### 2026-10-11 Run 155

重新精读 Hempel 2011 §III-A--C/Definition 2/Theorem 1，并复核 Houska §6.4--6.5 的
extreme information-set 凸权重控制。精确证明：固定 global residual、线性边、凸扰动/约束
及同一 source 标签的一张 affine-in-`d` 策略时，闭环边映射与同标签凸包严格交换，故新增
fibers 无需逐点枚举；但逐边 target inclusion 和 fixed point 仍未建立。语义纠正 Run148 三个
首次 return seeds 分属三个 `last_return` 标签，跨标签凸包只会退回更粗 mode-only 外包。
下一步传播九条第二周期路径并按共同 target 标签分组。详见 `run155_research_log.md` 与第91章。

### 2026-10-11 Run 156

重读 Houska §6.5/Theorem 3 完整证明与 Yang--Ozay 的缺测 product safety 量词。固定 global
residual 下精确传播九条第二周期零策略 histories；六条全程安全，但 `10->15` 在第14 miss、
`15->10` 和 `15->15` 在第9 miss 首次使真实 `e_v` 半宽达到 `99649307/36000000`，严格超过
`11/4` 达 `649307/36000000`。因此终止零/label-only 策略支线，不再计算其 target hull；该反例
不否定 affine-in-`d` feedback。详见 `run156_research_log.md` 与第92章。

### 2026-10-11 Run 157

精读Goulart--Kerrigan--Maciejowski 2006 affine-feedback参数化，重读Hempel fiber共享输入与
Houska information-set control。纠正Run156时序：失败miss的输入取于age13/8，两条当前边
均无未知分叉。对`J_9` age13、`J_14` age8 exact fibers构造`deltaT=K_v d_v`有理数见证，
robust input support恰饱和correction盒；下一`e_v`半宽约2.71470、2.70783，均严格低于
2.75。故零策略局部反例可由affine可见反馈一步修复，但尚无target inclusion、后续mode-9
共享分叉、RCI或递归可行性。详见`run157_research_log.md`与第93章。

### 2026-10-11 Run 158

精读Goulart--Kerrigan 2007 affine output-feedback robust constraints，重读Hempel/Houska量词。
纠正“先对单一constituent作共同外包”的平凡支线，转而检查Run157 rescued `(9,15)` 的真实
未知分叉。精确见证`K_v=-114428600/70527869`用同一输入同时覆盖`9->10 miss`和`9->0
success`；输入support恰饱和correction盒，两支共享`e_p≈0.973594,e_v≈2.719148`并满足硬
约束，estimator targets继承既有full-envelope facet包含。证据仍非target闭合/RCI。详见
`run158_research_log.md`与第94章。

### 2026-10-11 Run 159

重读Goulart--Kerrigan 2007、Yang--Ozay 2021与Houska相关正文。纠正Run158下一步：
`(0,15)` 的rescued constituents尚未完成return，不能直接凸化。对`J14` age-8 exact set给出
三条miss后的position支持下界：零输入support为`3714127151/3600000000`，两次bounded
centered affine correction至多削减`3h²U`，故mode-11仍至少为`369867929/360000000>1`。
这精确否定当前fixed-residual/seed/correction盒下的`15->15` affine constituent，阻断安全
`(0,15)` target hull，但不否定更早介入或一般output feedback。详见`run159_research_log.md`
与第95章。

### 2026-10-11 Run 160

重读Yang--Ozay 2021、Rungger--Tabuada 2017与Goulart--Kerrigan 2007相关正文；Rutledge等
2020仅核查摘要/引言。把“从mode0更早反馈”放宽为任意causal full-state bounded policy，利用
镜像轨迹证明`k` miss后位置半直径至少为`H_k^0-k(k-1)h²U/2`。第12 miss下界约0.995520，
第13 miss首次达到`934206607/900000000≈1.038007>1`。因此当前fixed residual、`J14` seed
与correction盒的15-tick constituent即使在乐观信息权限下也不可行；停止继续调gain，转向
seed/residual/input-authority trade-off审计。详见`run160_research_log.md`与第96章。

### 2026-10-11 Run 161

精读Lu--Cannon--Koksal-Rivet 2021的fixed-complexity set update、tube与recursive-feasibility
章节，重读Köhler 2021和Dey--Bhasin的online-bound compatibility；Robbins 2026仍仅有正式摘要。
把Run160的`k=14`下界精确分解为seed方向半直径`alpha`、future residual`beta`和correction
authority`gamma`：`alpha*S+(beta-gamma)D<=1`，其中
`S=3889781459/3600000000`、`D=52065013/400000000`。当前`g_r=hU`导致baseline residual
与乐观输入削减相消；单因素至少需seed半直径缩小7.4498%、residual缩小61.8418%或authority
增加61.8418%。一般后验须以正反两个support计算半直径；只有realized state width可由当前SMF
直接改变；其余两项分别需要未来
扰动保证或物理输入合同。详见`run161_research_log.md`与第97章。

### 2026-10-12 Run 162

重读Dey--Bhasin adaptive update兼容条件、Lu等旧解移位及Lorenzen recursive model update。
纠正Run161下一步：dropout string由环境选择，控制器不能在方向半直径gate失败后自行把15-tick
合同降为5/10-tick。短计划只有在终端进入覆盖剩余miss语言的robust invariant backup时才安全；
当前仓库无该证书，故不实现伪fallback。下一步只核查可认证通信调度，或在改变合同后构造仍覆盖
15-tick语言的backup family。详见`run162_research_log.md`与第98章。

### 2026-10-12 Run 163

精读Wildhagen等2022的自触发通信、bounded-loss Assumption 1、min-max预测和terminal设计，重读
Hassaan等2021的有限缺测语言。仓库审计确认`PacketSchedule`只消费并检查外生`drop`，不存在
measurement request、重传、ACK、预约或冗余链路控制接口；既有scheduler只是support-query计算
预算调度。因此把`max_missing=2`改成1只是换假设，不能由控制器证明最长return从15降到10 tick。
通信支线停止；下一步保留15-tick语言，反推并审计满足Run161必要阈值的可初始化seed合同。详见
`run163_research_log.md`与第99章。

### 2026-10-12 Run 164

全文定向重读Scott等2016的CZ等式切片/线性像，复核Goulart--Kerrigan信息集反馈；Alamo等2005
只核查摘要与可访问正文片段。发现Run161把测量后可区分的不同`d=e-eta`合并进整体`J14`宽度。
精确证明最坏可见fiber在`e_p+14h e_v`方向半宽为`16315003/75000000≈0.21753337<1`，
原始/对偶证书相等；整体半宽`≈1.08049485`只适用于所有观测共用一张计划。故撤回“条件化策略
必须缩小seed 7.4498%”的必要性外推，下一步改为参数化fiber的完整15-tick安全/终端包含。
详见`run164_research_log.md`与第100章。

### 2026-10-12 Run 165

全文重读Yang--Ozay缺测安全串并复核Hempel/Houska近邻。Run164的fiber宽度门槛虽通过，绝对中心
仍构成反例：可达极端观测`d_p=24272147/48000000`的fiber在`e_p+14he_v`方向整体偏正。
即使允许全状态因果反馈，14次miss的正端residual与最大负输入因`g_r=hU`精确相消，最终位置仍
至少为`3889781459/3600000000>1`。故停止当前15-tick合同下的gain/terminal综合；下一步转向
极端可见偏差、future residual与物理输入权限的中心范围三因素最小修约。详见第101章。

### 2026-10-12 Run 166

精读Lu--Cannon--Koksal-Rivet 2021的固定复杂度集合更新、鲁棒tube与recursive-feasibility证明。
把Run165中心反例化为精确三因素界面：在覆盖安全阈值的支持LP仿射支上，
`H(r)=16315003/75000000+(29/15)r`，且必要条件为`H(r)+beta D-gamma C<=1`。
单项修约至少需要可见范围降至`0.404724`、future residual缩小61.84%，或correction authority
增加61.84%。下一步只核查可见范围阈值是否能由合法measurement intersection可靠保证；不把
状态后验收缩外推为未来扰动收缩。详见第102章。

### 2026-10-12 Run 167

精读Scott等2016的generalized intersection、Proposition 1及bounded-error估计递推，复核Alamo
2005和Lu等的真值包含边界。当前14-miss强制return满足`d_p^+=q+n_p`；即使取合法零测量噪声，
`q`支持`≈0.485670`仍严格超过Run166要求的`≈0.404724`。因此精确CZ相交也不能对所有允许真值
保证该全局cap，measurement-only支线终止；当前噪声下源支持必须缩至现值的79.2152%。下一步
转向future residual的物理分解，不再继续局部fiber或传感器调参。详见第103章。

### 2026-10-12 Run 168

精读Do--Prodan 2024的固定扰动tube和Hu等2018的tube-dependent非线性余项界。当前竖直
future residual精确分为气动核心`2.086`与姿态--推力项`1.48989375`；定义离散真值没有隐藏
积分余项，external process为零。Run166绝对门槛仅`≈1.364497`，故即使完全删除姿态项，
剩余气动核心仍过大，姿态单项救援支线终止。下一步只构造覆盖15-tick全信息一致轨迹的局部
风相对速度域，检查气动核心能否可靠缩至当前的65.4121%。详见第104章。

### 2026-10-12 Run 169

重读Hu等2018的RFIT全tube量词，并保留J14 cycle-lifted生成元相关性构造首步反例。横、竖速度
极值由互不相交生成元支撑，可同时实现；配合合法nominal state、实际状态、风端点和零俯仰，
真实竖直气动余项严格大于`1.484305`，已超过Run168门槛`1.364497`。因此无需继续15步传播，
当前J14合同的local-aerodynamic缩放支线终止。下一步只审计能否可靠改变联合初始化合同；否则
停止冻结benchmark主线并重构课题方向。详见第105章。
