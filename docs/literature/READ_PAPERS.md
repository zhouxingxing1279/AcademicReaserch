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
- 年份/出处：2015, *Journal of Applied Mathematics*, Article 875850
- 稳定链接：https://doi.org/10.1155/2015/875850
- 研究问题：quasi-LPV 受约束系统中，zonotopic set-membership estimation 刷新后如何维持 dynamic output-feedback robust MPC。
- 方法概要：在线刷新 zonotopic estimation-error set，并专门设置下一采样时刻的辅助可行性判据；若该判据不通过，则继承上一时刻 controller parameters，而不是无条件采用新估计集合对应的控制更新。
- 关键结论：论文明确指出，直接使用 true-state bounds 处理不确定性时主优化问题的 recursive feasibility 可能丢失，并给出辅助优化/继承机制来维持下一时刻可行性。
- 与本项目关系：这是“估计集合更新必须经过 recursive-feasibility gate”非常直接的旧近邻，进一步否定把 gate 本身当作创新。
- 可借鉴点：更新失败时 fallback 到旧控制器/旧证书，与本项目 anytime certificate 不足时拒绝 recenter 的语义接近。
- 局限：其几何、controller parameterization 与当前 constrained-zonotope finite-support certificate 不同；尚未证明两者计算结构等价。
- 本项目状态：新增为高优先级递归可行性近邻；后续创新只能落在更窄的 finite-control-normal certified computation / cost advantage 上。
