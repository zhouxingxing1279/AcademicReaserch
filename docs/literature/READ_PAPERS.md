# 已阅读/核对论文记录

> 本文件记录为当前 SMF + Tube MPC / constrained-zonotope 主线实际核对过的文献。“已阅读”指至少核对原文/正式摘要中的模型、方法与和本项目直接相关的定理或集合运算；不等同于作者已完成逐页人工精读。新增条目前先查重。

## Scott, Raimondo, Marseglia, Braatz — Constrained zonotopes: A new tool for set-based estimation and fault detection

- 年份/出处：2016, *Automatica*, 69:126–136
- DOI：https://doi.org/10.1016/j.automatica.2016.02.036
- 原文：https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf
- 研究问题：在 set-based estimation/control 中，普通 zonotope 对交集不封闭、一般 polytope 又太昂贵，如何获得更好的精度—复杂度折中。
- 方法概要：定义 constrained zonotope \(\mathcal Z=\{G\xi+c:A\xi=b,\|\xi\|_\infty\le1\}\)，给出线性映射、Minkowski 和、广义交等集合运算，以及约束/生成元约减。
- 关键结论：不限制复杂度时可表示任意凸多面体；多种估计所需运算可用简单恒等式精确实现；约减采用外包，因此保留包含性但会引入保守性。
- 与本项目关系：当前 CZ-SMF 表示与历史等式增长的核心基础；第 21 章通用多等式支持认证直接针对这种表示。
- 可借鉴点：不要把“CZ 保留相关性”当创新；复杂度控制必须明确外包方向与包含保证。
- 局限：主要解决集合表示/运算与估计，不提供本项目的 MPC 性能证书驱动查询调度。
- 本项目状态：已采用 CZ 表示与保守约减边界；不宣称相关基础为新贡献。

## Le, Stoica, Dumur, Alamo, Camacho — Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation

- 年份/出处：2011, CDC-ECC
- DOI：https://doi.org/10.1109/CDC.2011.6161131
- 原文：https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1657.pdf
- 研究问题：线性离散系统存在未知有界扰动和测量噪声时，如何把 guaranteed state estimation 与 robust output-feedback MPC 结合。
- 方法概要：用 zonotopic set-membership estimation 产生状态估计集合，并在 tube-based output-feedback MPC 中把估计误差和 nominal-control error 分开处理。
- 关键假设/结论：通过离线 LMI 设计让估计集合尺寸有界/收缩，并使用稳定反馈与 tube 结构保证约束满足和闭环稳定性质。
- 与本项目关系：直接证明“zonotopic SMF + Tube MPC”已有先例。
- 可借鉴点：联合估计误差/名义误差的分解和 RPI tube 思路与本项目 15–17 章相呼应。
- 局限：其 set representation、在线更新和性能证书结构与当前控制相关 CZ 查询问题不同；不能据此证明本项目调度/压缩接口已有或没有新颖性。
- 本项目状态：作为最近邻基础文献，明确用于压低创新声明边界。

## Rego, Raffo, Scott, Raimondo — Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems

- 年份/出处：2020, *Automatica*, 111:108614
- DOI：https://doi.org/10.1016/j.automatica.2019.108614
- 预印本：https://arxiv.org/abs/1908.09950
- 研究问题：非线性离散系统、未知有界不确定性下，如何进行 guaranteed prediction/update，同时减少普通 zonotope 在非线性传播和测量交中的保守性。
- 方法概要：基于 CZ 构造 mean-value extension 与 first-order Taylor extension 来包络非线性映射，并利用 CZ 更准确地表示 measurement intersection。
- 关键结论：文中数值例显示 CZ 方法能产生比 zonotopic 方法更紧的预测/更新包络，同时保留较好的计算可操作性。
- 与本项目关系：未来从当前线性基准转到四旋翼非线性时，这是比“直接线性化后加大盒”更相关的集合传播基线。
- 可借鉴点：非线性 remainder 必须有 guaranteed enclosure；测量交和传播的包含性要分开审计。
- 局限：没有解决当前 MPC 约束方向/目标证书驱动的在线查询预算分配。
- 本项目状态：尚未接入当前线性控制闭环；列为四旋翼阶段的重要对照。

## Cong, Wang, Zhou — Stability of linear set-membership filters with respect to initial conditions: An observation-information perspective

- 年份/出处：2025, *Automatica*
- DOI：https://doi.org/10.1016/j.automatica.2024.111993
- 公开记录：https://openresearch-repository.anu.edu.au/items/6b286fd3-a31e-49c7-b1d3-ba98f943c73a
- 研究问题：经典线性 SMF 对初值不可靠时的稳定性如何刻画。
- 方法概要：提出 Observation-Information Tower (OIT)，刻画不依赖初值的测量信息交结构，并据此给出 SMF 初值稳定性分析与稳定性保证框架；同时发展快速 constrained-zonotopic SMF。
- 关键结论：给出经典 SMF 关于初值稳定性的必要充分条件，并构造稳定性保证的过滤框架；CZ 实现用于降低 wrapping effect。
- 与本项目关系：提醒我们不能把“CZ-SMF 稳定性”本身视为空白；若后续宣称闭环稳定，需要明确控制稳定性与滤波对初值稳定性是不同命题。
- 可借鉴点：滚动后验不能只看单步集合变小，还要考虑历史信息、初值影响与长期稳定。
- 局限：不直接给 Tube MPC 的递归可行性/性能查询调度结论。
- 本项目状态：作为稳定性边界文献，尚未把 OIT 结构纳入当前算法。

## Qiu, Yang, Zhu, Mousavinejad — Output feedback model predictive control based on set-membership state estimation

- 年份/出处：2020, *IET Control Theory & Applications*, 14(4):558–567
- DOI：https://doi.org/10.1049/iet-cta.2019.0881
- 研究问题：有未知有界过程扰动时，如何直接利用 set-membership state estimate 构造 output-feedback MPC。
- 方法概要：使用 ellipsoidal set-membership estimation，把整个状态估计椭球引入 MPC 约束，通过 LMI 近似处理二次矩阵不等式。
- 关键结论：在其假设下递归求控制输入并分析预测时域内的约束，闭环状态收敛到包含原点的区域。
- 与本项目关系：提供 ellipsoid-SMF + MPC 的直接基线，说明“改成 CZ”必须用可量化的收紧/计算差异，而不是只凭集合形状宣称更优。
- 可借鉴点：未来比较应至少包含 ellipsoidal set-membership MPC，而不只比较普通 MPC 与 CZ 方法。
- 局限：LMI 保守近似和当前方向支持证书接口不同；不能直接回答控制相关 CZ 压缩是否值得。
- 本项目状态：列入后续方法对比基线。
