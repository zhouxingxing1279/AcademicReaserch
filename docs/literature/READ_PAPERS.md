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
- 方法/关系：set-membership 参数更新的 monotonic/non-increasing 条件与 tube update 联合保证 robust recursive feasibility/constraint satisfaction；“集合缩小帮助递归可行”不是新结论。

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
- 研究问题：离散线性系统受持续有界加性扰动且有状态/输入硬约束时的 robust MPC。
- 方法/关键结论：以 disturbance-invariant / tube 思想构造 robust constrained MPC，使闭环状态收敛到 disturbance-invariant neighborhood；是经典 bounded-disturbance tube/RMPC 基线。
- 与本项目关系：第25章 LQR + RPI 检查属于这一经典框架的基础实例，不能把“稳定 K + RPI tightening”作为创新。
- 局限：加性 LTI disturbance contract 不保留本项目 `T*phi` 输入—状态相关性；直接套用会要求把相关项独立盒化。
- 本项目状态：作为 ancillary-controller 与 terminal-set 合成的经典基线。

## Raković, Kerrigan, Kouramas, Mayne — Invariant approximations of the minimal robust positively invariant set
- 年份/出处：2005, *IEEE Transactions on Automatic Control*, 50(3):406–410；DOI：https://doi.org/10.1109/TAC.2005.843854
- 研究问题：稳定离散 LTI 系统受有界持续扰动时，如何计算 mRPI 的可控精度外逼近。
- 方法/关键结论：给出 robust positively invariant outer approximation 及可预先指定逼近精度的条件。
- 与本项目关系：第25章有限 Minkowski 和 + 尾项外包属于同一 mRPI 计算问题；后续合法 tube 需要以此类方法作为基线。
- 可借鉴点：有限和本身是 mRPI 的内侧截断，不能直接当安全 tube；必须处理无限尾项。
- 局限：仍是 additive LTI setting，不能解决 `deltaT*phi` 的 joint correlation。
- 本项目状态：已用于约束第25章的证书语义；下一步比较 correlation-preserving joint tube 时继续作为 independent-additive baseline。
