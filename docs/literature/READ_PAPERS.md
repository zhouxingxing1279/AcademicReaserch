# 已阅读/核对论文记录

> 本文件记录为当前 SMF + Tube MPC / constrained-zonotope 主线实际核对过的文献。“已阅读”指至少核对原文/正式摘要中的模型、方法与和本项目直接相关的定理或集合运算；不等同于作者已完成逐页人工精读。新增条目前先查重。

## Scott, Raimondo, Marseglia, Braatz — Constrained zonotopes: A new tool for set-based estimation and fault detection
- 年份/出处：2016, *Automatica*, 69:126–136；DOI：https://doi.org/10.1016/j.automatica.2016.02.036
- 方法/关系：CZ 定义、精确集合运算与复杂度约减；是本项目 CZ 基础，因此“CZ 保留相关性”不是创新。

## Le, Stoica, Dumur, Alamo, Camacho — Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation
- 年份/出处：2011, CDC-ECC；DOI：https://doi.org/10.1109/CDC.2011.6161131
- 方法/关系：zonotopic SMF + tube output-feedback MPC；直接说明该组合不是创新。

## Rego, Raffo, Scott, Raimondo — Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems
- 年份/出处：2020, *Automatica*, 111:108614；DOI：https://doi.org/10.1016/j.automatica.2019.108614
- 方法/关系：CZ mean-value/Taylor guaranteed nonlinear propagation/update；四旋翼非线性阶段的重要传播基线。

## Cong, Wang, Zhou — Stability of linear set-membership filters with respect to initial conditions: An observation-information perspective
- 年份/出处：2025, *Automatica*；DOI：https://doi.org/10.1016/j.automatica.2024.111993
- 方法/关系：Observation-Information Tower、CZ-SMF 初值稳定性；须与控制闭环稳定性区分。

## Qiu, Yang, Zhu, Mousavinejad — Output feedback model predictive control based on set-membership state estimation
- 年份/出处：2020, *IET Control Theory & Applications*；DOI：https://doi.org/10.1049/iet-cta.2019.0881
- 方法/关系：ellipsoidal SMF + output-feedback MPC；是 CZ 方法必须比较的几何基线。

## Köhler, Kötting, Soloperto, Allgöwer, Müller — A robust adaptive model predictive control framework for nonlinear uncertain systems
- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.5147
- 研究问题：递归模型/参数更新后，如何仍保证 robust recursive feasibility 与 constraint satisfaction。
- 方法/关键结论：set-membership estimation 提供逐步更准确的参数不确定集合；论文明确推导 estimation algorithm 与 tube/set-based RAMPC 所需的 monotonicity / non-increasing 条件，并在 incremental-Lyapunov tube 中给出可实现条件。
- 与本项目关系：第28章 exact CZ shift-nesting 属于同一“更新必须与旧预测兼容”的大理论边界；因此 nesting 本身不是创新。真正未闭合的是 fixed-complexity CZ reduction 是否保持这种兼容性。
- 局限：处理参数不确定性 RAMPC，不是当前 output-feedback CZ state posterior 的固定复杂度压缩接口。
- 本项目状态：作为 recursive-update monotonicity 的强基线。

## Lu, Cannon, Koksal-Rivet — Robust adaptive model predictive control: Performance and parameter estimation
- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.5175
- 方法/关系：固定复杂度参数/预测集合 + robust tube MPC；证明 recursive feasibility 与 ISS，是 fixed-complexity 强基线。

## Peschke, Mönnigmann — Robust adaptive tube tracking model predictive control for piece-wise constant reference signals
- 年份/出处：2023, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.6814
- 方法/关系：nominal model/reference 在线变化时的 adaptive tracking MPC；明确 nominal-model update 会使 nominal-centered tube 的 recursive-feasibility proof 更困难。

## Köhler et al. — Robust adaptive MPC using control contraction metrics
- 年份/出处：2023, *Automatica*；DOI：https://doi.org/10.1016/j.automatica.2023.111169
- 方法/关系：CCM + set-membership + adaptive tube，含 planar quadrotor；四旋翼阶段强近邻。

## Andrade, Normey-Rico, Raffo — Tube-Based Model Predictive Control Based on Constrained Zonotopes
- 年份/出处：2024, *IEEE Access*, 12:50100–50113；DOI：https://doi.org/10.1109/ACCESS.2024.3381622
- 方法/关系：CZ Tube MPC，24-state tiltrotor UAV + suspended load HIL；“CZ + Tube MPC + UAV”不是创新。

## Dey, Bhasin — Output Feedback MPC with Adaptive Tubes
- 年份/出处：2026, arXiv:2605.23661
- 方法/关系：adaptive observer 的 state/model/initial-condition estimates 联动 tightening、terminal ingredients 和 tube geometry；作者建立 recursive feasibility 与 robust exponential stability。与本项目 recenter/update gate 高度相邻，必须全文排重。

## Ping — Dynamic Output Feedback Robust Model Predictive Control via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems
- 年份/出处：2015, *Journal of Applied Mathematics*, Article 875850；DOI：https://doi.org/10.1155/2015/875850
- 方法/关系：zonotopic estimation-error set 刷新后用辅助 feasibility condition 决定是否采用更新；失败时继承旧 controller parameters。“更新前 feasibility gate”不是创新。

## Mayne, Seron, Raković — Robust model predictive control of constrained linear systems with bounded disturbances
- 年份/出处：2005, *Automatica*, 41(2):219–224；DOI：https://doi.org/10.1016/j.automatica.2004.08.019
- 方法/关系：经典 bounded-disturbance robust/tube MPC 基线；当前 LQR+RPI 不能作为创新。

## Raković, Kerrigan, Kouramas, Mayne — Invariant approximations of the minimal robust positively invariant set
- 年份/出处：2005, *IEEE Transactions on Automatic Control*, 50(3):406–410；DOI：https://doi.org/10.1109/TAC.2005.843854
- 方法/关系：mRPI 可控精度外逼近；有限 Minkowski 和必须补无限尾项才能作安全 tube。

## McCormick — Computability of global solutions to factorable nonconvex programs: Part I — Convex underestimating problems
- 年份/出处：1976, *Mathematical Programming*, 10:147–175；DOI：https://doi.org/10.1007/BF01580665
- 方法/关系：单 bilinear term 的经典 convexification 基础；box-domain 线性 support 下普通 CZ 不会比 exact convex hull 更紧。

## Müller, Serrano, Gleixner — Using Two-Dimensional Projections for Stronger Separation and Propagation of Bilinear Terms
- 年份/出处：2020, *SIAM Journal on Optimization*；DOI：https://doi.org/10.1137/19M1249825
- 方法/关系：非矩形二维可行域可产生比 box McCormick 更强的 separation；支持利用真实 posterior/scheduling 域，但不提供 Tube MPC 递归可行性。

## Kochdumper, Althoff — Constrained polynomial zonotopes
- 年份/出处：2023, *Acta Informatica*, 60:279–316；DOI：https://doi.org/10.1007/s00236-023-00437-5
- 方法/关系：支持 quadratic/higher-order maps；“用 polynomial zonotope 表示乘积”已有成熟理论，只能作为实现工具。

## Bujarbaruah, Nair, Borrelli — A Semi-Definite Programming Approach to Robust Adaptive MPC under State Dependent Uncertainty
- 年份/出处：2020, European Control Conference；预印本：arXiv:1910.04378
- 方法/关系：set-membership refinement + state-dependent uncertainty envelope + robust MPC；“SMF 信息进入 state-dependent robustification”已有先例。

## Hanema et al. — Stabilizing non-linear model predictive control using linear parameter-varying embeddings and tubes
- 年份/出处：2021, *IET Control Theory & Applications*；DOI：https://doi.org/10.1049/cth2.12131
- 研究问题：利用 nonlinear system 的 LPV embedding 构造可稳定 MPC，同时处理未来 scheduling parameter 未知。
- 方法/关键结论：限制 state evolution 于时变集合，并利用 scheduling-state 关系构造 future scheduling tube；相较静态 bounds 得到更紧未来 bounds，并以该结构建立 recursive feasibility/stability。
- 与本项目关系：第27–28章的未来 `phi` scheduling intervals 与 shift nesting 有直接近邻，因此“state set -> scheduling tube”不能作为创新。差异只能落在 CZ-SMF measurement posterior、certified finite-normal support 与 fixed-complexity reduction compatibility。
- 局限：不是 set-membership output-feedback CZ 压缩问题。
- 本项目状态：作为 scheduling-tube 强基线。

## Abbas — Linear parameter-varying model predictive control for nonlinear systems using general polytopic tubes
- 年份/出处：2024, *Automatica*, 160:111432；DOI：https://doi.org/10.1016/j.automatica.2023.111432
- 方法/关系：anticipated scheduling bounds + general polytopic tubes；“更紧未来 scheduling interval 降低保守性”不是新机制。

## Fleming, Hawari — Robust Tube MPC Using Gain-Scheduled Policies for a Class of LPV Systems
- 年份/出处：2024, *IEEE Control Systems Letters*, 8:1589–1594；DOI：https://doi.org/10.1109/LCSYS.2024.3412652
- 方法/关系：gain-scheduled policy、parameter-rate bounds、online polyhedral tubes，证明 recursive feasibility/exponential stability；decision/scheduling-dependent tube 已有成熟理论。

## Girard — Reachability of Uncertain Linear Systems Using Zonotopes
- 年份/出处：2005, HSCC, LNCS 3414:291–305；DOI：https://doi.org/10.1007/978-3-540-31954-2_19
- 研究问题：用 zonotope 可扩展地计算不确定线性系统 reachable sets，并控制表示复杂度。
- 方法/关键结论：zonotope 传播配合 generator/order reduction；经典 generator-box 外包模式保证单次 outer enclosure，但其目标不是跨两个嵌套集合保持 reduction operator 的 monotonicity。
- 与本项目关系：第29章使用同类 generator-box reduction 构造 shift-support reversal；普通 order reduction 本身不能作为创新。
- 局限：不处理 SMF measurement posterior 与 MPC shifted-candidate support compatibility。
- 本项目状态：作为 naive fixed-order reduction 基线。

## Raghuraman, Koeln — Set operations and order reductions for constrained zonotopes
- 年份/出处：2022, *Automatica*, 139:110204；DOI：https://doi.org/10.1016/j.automatica.2022.110204；预印本：https://arxiv.org/abs/2009.06039
- 研究问题：提高 zonotope/CZ 在控制集合运算中的实用性，并提供复杂度约减方法。
- 方法概要：扩展 halfspace intersection、convex hull、RPI、Pontryagin difference 等 CZ 运算，并研究 zonotope/CZ order reduction。
- 与本项目关系：说明“CZ order reduction”已有系统理论；本项目若有贡献必须落在 reduction error 与 recursive-feasibility control normals 的联动证书，而不是提出一般 reduction。
- 局限：没有给出本项目所需的 rolling SMF shift-support ledger。
- 本项目状态：作为 fixed-complexity CZ 强基线。

## Robbins, Siefert, Pangborn — Exact Representation Complexity Reduction for Constrained Zonotopes with Applications to Dynamic Systems and Control
- 年份/出处：2026, *American Control Conference (ACC 2026)*；IEEE Xplore 收录日期 2026-08-13。
- 稳定链接：https://ieeexplore.ieee.org/document/11615961
- 研究问题：反复集合运算会使 zonotope/CZ representation complexity 增长；哪些 generators/constraints 是表示冗余，能否在保持集合完全不变时删除？
- 方法/关键结论：形式化 irredundant zonotopic representation 与多类 redundancy，给出检测/删除算法；数值例包含 robust controllable sets 和 ReLU domain partitioning。其 reduction 是 exact representation reduction，不是 approximate outer enclosure。
- 与本项目关系：该方法不改变集合，所以 exact-CZ 的 shift nesting 和所有 support 都自动保持；它应成为压缩流水线第一阶段，先 exact-prune，再讨论 approximate fixed-budget reduction。
- 可借鉴点：把“表示复杂度”与“集合几何近似误差”明确分离，避免把可精确删除的冗余误算成必须牺牲 tightness 的 fixed-order 问题。
- 局限：exact pruning 不能保证长期 propagation/update 后一定达到预设固定 generator/equality budget；也没有解决 independent approximate reductions 导致的 control-normal support reversal。
- 本项目状态：已采用为设计原则；不把 exact redundancy removal 声称为本项目创新。

## Hanema, Lazar, Tóth — Stabilizing tube-based model predictive control: terminal set and cost construction for LPV systems
- 年份/出处：2017, *Automatica*, 85:137–144；DOI：https://doi.org/10.1016/j.automatica.2017.07.046；扩展版：https://arxiv.org/abs/1702.05393
- 研究问题：LPV tube MPC 如何构造 terminal set/cost 并建立 recursive feasibility 与 stability。
- 方法/关键结论：采用 controlled periodically contractive terminal sets 与适合集合的 Lyapunov-like terminal cost；给出满足参数化假设时的递归可行性与渐近稳定性，并构造 periodic homothetic tube 参数化。
- 与本项目关系：第31章保留推力 T 的横向—姿态模型天然是 LPV family；因此“LPV terminal family/periodic contractive set”不能作为创新，只能作为 ancillary/terminal 证明工具。
- 可借鉴点：若 common quadratic certificate 过强，可转向 periodic/finite-step contractive terminal construction，而不是回到语义错误的 fixed-hover LTI。
- 局限：不使用 CZ-SMF measurement posterior，也不研究 posterior correlation 在真实 input normals 上的 tightening value。
- 本项目状态：下一阶段 ancillary/terminal synthesis 的主要理论基线。

## Ping, Yao, Ding, Li — Tube-Based Output Feedback Robust MPC for LPV Systems With Scaled Terminal Constraint Sets
- 年份/出处：2022, *IEEE Transactions on Cybernetics*, 52(8):7563–7576；DOI：https://doi.org/10.1109/TCYB.2020.3041334
- 研究问题：有 bounded disturbance/noise 的离散 LPV 系统如何做低在线复杂度 output-feedback tube RMPC。
- 方法/关键结论：离线优化并存储 nested RPI estimation-error sets 与 RCI control-error sets；在线依据时变 estimation-error bounds 搜索控制参数，并使用 scaled terminal constraint sets；论文给出 recursive feasibility 与 robust stability 保证。
- 与本项目关系：LPV + output feedback + nested error sets + scaled terminal 已有强近邻，因此第31章不能把这些结构本身作为创新。差异若存在，只能落在 CZ-SMF posterior correlation 如何被真实 state/input/terminal support normals 消费并形成可认证的 tightening 改善。
- 可借鉴点：其 nested RPI/RCI lookup 与 scaled terminal 是当前语义一致 ancillary synthesis 的直接比较基线。
- 局限：不是 constrained-zonotope posterior 的 control-normal support certification问题。
- 本项目状态：列为后续 LPV output-feedback 基线。


## Tahir, Jaimoukha — Robust Positively Invariant Sets for Linear Systems subject to model-uncertainty and disturbances
- 年份/出处：2012, IFAC Proceedings Volumes 45(17):213–217；DOI：https://doi.org/10.3182/20120823-5-NL-3013.00032
- 研究问题：在线性离散系统存在 model uncertainty、additive disturbance 以及 state/input constraints 时，如何联合计算 controller 与 robust positively invariant set。
- 方法/关键结论：将 RPI set 与反馈律一起放入 LMI 优化；论文强调不要求先给定 controller 或初始 invariant set，并在固定 K、无模型不确定性的特例下给出更简单的优化。
- 与本项目关系：第34–35章的“约束感知 ancillary synthesis”已有直接方法学基础，因此 controller/invariant co-design 只能作为 baseline 工具，不能作为创新。
- 局限：其 uncertainty class 与当前 thrust-scheduled、state-dependent nonlinear remainder 不完全相同；不能直接替代本项目的 vertex-consistent residual contract。
- 本项目状态：列为下一阶段 joint state/input synthesis 的 baseline。

## Ben Sassi, Girard — Controller synthesis for robust invariance of polynomial dynamical systems using linear programming
- 年份/出处：2012, *Systems & Control Letters*, 61(4):506–512；DOI：https://doi.org/10.1016/j.sysconle.2012.01.004；预印本：https://arxiv.org/abs/1107.1580
- 研究问题：bounded disturbances 和 input constraints 下，如何联合求 controller 与 invariant set。
- 方法/关键结论：给定候选 polyhedral invariant 后，把 controller synthesis 写成多项式优化并用 LP relaxation；随后迭代更新 controller 与 invariant polytope。
- 与本项目关系：再次说明“同时搜索反馈和不变集”已有成熟工作。若本项目采用类似 co-design，只能作为认证工具。
- 局限：不是 constrained-zonotope SMF posterior 与 Tube MPC 的接口问题，也不处理当前特定 LPV scheduling 语义。
- 本项目状态：作为 polyhedral joint synthesis 的方法基线。

## Wehbeh, Kerrigan — State-Dependent Uncertainty Modeling in Robust Optimal Control Problems through Generalized Semi-Infinite Programming
- 年份/出处：2025, arXiv:2503.10389；稳定链接：https://arxiv.org/abs/2503.10389
- 研究问题：当 uncertainty set 本身依赖 state/control decision 时，如何避免用全局 uniform uncertainty set 造成额外保守性。
- 方法/关键结论：用 generalized semi-infinite programming 表示 decision/state-dependent uncertainty，并通过 local reduction 求解；文中包含 planar quadrotor 案例，展示相对 uniform uncertainty bounds 的保守性改善。
- 与本项目关系：第35章的 vertex-consistent residual 修正属于同一建模原则：已知 scheduling parameter T 时，应保留 d_x(T) 的依赖关系，而不是无条件替换为 d_x(T_max)。
- 局限：该工作不是 SMF/CZ output-feedback Tube MPC，也没有解决本项目的 recursive-feasibility shift certificate。
- 本项目状态：作为“不得丢失 uncertainty dependence”的强建模基线。
