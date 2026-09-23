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
