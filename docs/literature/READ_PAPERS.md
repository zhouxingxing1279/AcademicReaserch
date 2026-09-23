# 已阅读/核对论文记录

> 本文件记录为当前 SMF + Tube MPC / constrained-zonotope 主线实际核对过的文献。“已阅读”指至少核对原文/正式摘要中的模型、方法与和本项目直接相关的定理或集合运算；不等同于作者已完成逐页人工精读。新增条目前先查重。

## Scott, Raimondo, Marseglia, Braatz — Constrained zonotopes: A new tool for set-based estimation and fault detection

- 年份/出处：2016, *Automatica*, 69:126–136
- DOI：https://doi.org/10.1016/j.automatica.2016.02.036
- 原文：https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf
- 研究问题：普通 zonotope 对交集不封闭、一般 polytope 又太昂贵时的集合表示。
- 方法概要：定义 constrained zonotope，给出线性映射、Minkowski 和、广义交及复杂度约减。
- 关键结论：不限制复杂度时可表示任意凸多面体；约减采用外包，保留包含性但引入保守性。
- 与本项目关系：CZ-SMF 表示与历史等式增长的基础。
- 可借鉴点：不能把“CZ 保留相关性”当创新。
- 局限：不提供 MPC 性能证书驱动查询调度。
- 本项目状态：已采用基础表示。

## Le, Stoica, Dumur, Alamo, Camacho — Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation

- 年份/出处：2011, CDC-ECC
- DOI：https://doi.org/10.1109/CDC.2011.6161131
- 原文：https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1657.pdf
- 研究问题：未知有界扰动和测量噪声下 guaranteed state estimation + robust output-feedback MPC。
- 方法概要：zonotopic SMF + tube-based output-feedback MPC，分离估计误差和 nominal-control error。
- 关键结论：通过离线 LMI 和稳定反馈获得约束/稳定性质。
- 与本项目关系：“zonotopic SMF + Tube MPC”已有直接先例。
- 可借鉴点：联合误差分解与 RPI tube。
- 局限：没有当前 anytime support/recenter certificate。
- 本项目状态：最近邻基础文献。

## Rego, Raffo, Scott, Raimondo — Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems

- 年份/出处：2020, *Automatica*, 111:108614
- DOI：https://doi.org/10.1016/j.automatica.2019.108614
- 预印本：https://arxiv.org/abs/1908.09950
- 研究问题：非线性未知有界系统 guaranteed prediction/update。
- 方法概要：CZ mean-value / first-order Taylor extension 与更准确的 measurement intersection。
- 关键结论：数值例中比普通 zonotope 更紧。
- 与本项目关系：四旋翼非线性阶段的重要传播基线。
- 可借鉴点：remainder enclosure 与 measurement intersection 分开认证。
- 局限：不处理 MPC 方向查询预算。
- 本项目状态：尚未接入闭环。

## Cong, Wang, Zhou — Stability of linear set-membership filters with respect to initial conditions: An observation-information perspective

- 年份/出处：2025, *Automatica*
- DOI：https://doi.org/10.1016/j.automatica.2024.111993
- 公开记录：https://openresearch-repository.anu.edu.au/items/6b286fd3-a31e-49c7-b1d3-ba98f943c73a
- 研究问题：线性 SMF 对初值的稳定性。
- 方法概要：Observation-Information Tower 与快速 constrained-zonotopic SMF。
- 关键结论：给出初值稳定性的必要充分条件和稳定性保证框架。
- 与本项目关系：SMF 稳定性不是空白；须与控制闭环稳定性区分。
- 局限：不直接给 Tube MPC 递归可行性。
- 本项目状态：稳定性边界文献。

## Qiu, Yang, Zhu, Mousavinejad — Output feedback model predictive control based on set-membership state estimation

- 年份/出处：2020, *IET Control Theory & Applications*, 14(4):558–567
- DOI：https://doi.org/10.1049/iet-cta.2019.0881
- 研究问题：ellipsoidal set-membership state estimate + output-feedback MPC。
- 方法概要：整个估计椭球进入 MPC 约束并用 LMI 近似。
- 关键结论：在其假设下递归求控制输入，状态收敛到原点邻域。
- 与本项目关系：ellipsoid-SMF + MPC 直接基线。
- 局限：LMI 保守近似与方向支持证书不同。
- 本项目状态：后续对比基线。

## Köhler, Kötting, Soloperto, Allgöwer, Müller — A robust adaptive model predictive control framework for nonlinear uncertain systems

- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*
- DOI：https://doi.org/10.1002/rnc.5147
- 预印本：https://arxiv.org/abs/1911.02899
- 研究问题：非线性参数不确定系统的 set-membership + RAMPC。
- 方法概要：parameter-estimator monotonicity/non-increasing 条件 + incremental Lyapunov tube。
- 关键结论：robust recursive feasibility、constraint satisfaction 与有限增益性质。
- 与本项目关系：集合缩小帮助递归可行不是新结论。
- 局限：参数集合而非 state posterior CZ。
- 本项目状态：递归可行性近邻基线。

## Lu, Cannon, Koksal-Rivet — Robust adaptive model predictive control: Performance and parameter estimation

- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*
- DOI：https://doi.org/10.1002/rnc.5175
- 研究问题：在线参数集合收缩、robust tube MPC、性能和参数收敛。
- 方法概要：固定复杂度多面体包络参数/预测状态集合。
- 关键结论：recursive feasibility 与 ISS。
- 与本项目关系：“固定复杂度集合 + 在线收缩 + Tube MPC + ISS”已有成熟结果。
- 局限：没有 state-CZ anytime support certificate。
- 本项目状态：fixed-complexity 基线。

## Peschke, Mönnigmann — Robust adaptive tube tracking model predictive control for piece-wise constant reference signals

- 年份/出处：2023, *International Journal of Robust and Nonlinear Control*
- DOI：https://doi.org/10.1002/rnc.6814
- 研究问题：nominal model/reference 在线变化时的 adaptive tracking MPC。
- 方法概要：set-membership 缩小 uncertainty set，point estimate 更新 nominal model，并适应 tube/terminal ingredients。
- 关键结论：明确指出 nominal model 改变使 nominal-centered tube 的 recursive-feasibility proof 困难。
- 与本项目关系：支持 center/model drift 动机，但说明该问题本身不新。
- 局限：参数/模型更新，不是 state posterior CZ support budget。
- 本项目状态：nominal-update 近邻。

## Köhler et al. — Robust adaptive MPC using control contraction metrics

- 年份/出处：2023, *Automatica*
- DOI：https://doi.org/10.1016/j.automatica.2023.111169
- 研究问题：较一般非线性系统的 robust adaptive tube MPC 与在线模型更新。
- 方法概要：control contraction metric + set-membership 参数更新 + nominal parameter 在线优化。
- 关键结论：recursive feasibility、constraint satisfaction，并含 planar quadrotor 数值例。
- 与本项目关系：四旋翼 + set-membership + adaptive tube MPC 的强近邻。
- 局限：CCM/参数不确定性，不是 state-CZ anytime support/recenter certificate。
- 本项目状态：四旋翼阶段必须对比。

## Andrade, Normey-Rico, Raffo — Tube-Based Model Predictive Control Based on Constrained Zonotopes

- 年份/出处：2024, *IEEE Access*, 12:50100–50113
- DOI：https://doi.org/10.1109/ACCESS.2024.3381622
- 研究问题：高阶 uncertain LPV 系统的 Tube MPC 如何用 zonotope/CZ 降低集合与在线优化复杂度。
- 方法概要：LMI 设计反馈增益；离线用 zonotope 计算 reachable set；admissible state/input 与 nominal sets 使用 constrained zonotope；MPC 按 CZ 结构重写。
- 关键结论：在 24-state tiltrotor UAV + suspended load 上通过 HIL/高保真模拟验证可行性与计算性能。
- 与本项目关系：直接否定“CZ + Tube MPC + UAV”作为创新组合；也是未来完整 CZ tube 重算的强基线。
- 可借鉴点：比较集合表示时必须同时比较计算成本和可行域，而不能只比较体积。
- 局限：其 reachable tube 主要离线构造，不是 rolling SMF state posterior 的 anytime support/recenter certificate。
- 本项目状态：新增为必须全文排重和实验比较的核心近邻。

## Dey, Bhasin — Output Feedback MPC with Adaptive Tubes

- 年份/出处：2026, CoRR/arXiv preprint
- 稳定链接：https://arxiv.org/abs/2605.23661
- 研究问题：LTI 系统存在参数和加性不确定性时，如何让 output-feedback observer 的 evolving estimates 驱动 adaptive tube MPC。
- 方法概要：adaptive observer 同时给 state/model/initial-condition point estimates 与对应集合；这些估计在线参数化 tightening、terminal ingredients 和 tube geometry。
- 关键结论：作者建立 recursive feasibility 与 robust exponential stability，并避免要求整个参数集合存在共同 quadratic-stabilizing feedback gain。
- 与本项目关系：这是第 22–23 章非常接近的新近邻，说明“observer estimate 更新 + adaptive tube + output feedback”本身也不是创新。
- 可借鉴点：下一轮必须逐式核对其 estimate/tube update 如何处理 point-estimate drift，特别是是否存在与本项目 directional support budget 等价的约束。
- 局限：从公开摘要可确认的是参数/初值/状态联合自适应框架；是否已有 constrained-zonotope state posterior 的 finite-direction anytime support certificate 尚需全文逐式排重。
- 本项目状态：高优先级全文排重文献；当前不作首创声明。
