# Run 135 文献准入卡：15 模态估计误差不变多集

日期：2026-09-29。仓库起点为本地 Run 134 提交 `e666490`；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。本轮问题是：现有 rolling SMF 的 15 模态半径递推能否闭合为 time-uniform `E_eta^j`，以及该集合是否能实际进入硬约束收紧。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读层级 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Athanasopoulos, Smpoukis, Jungers, *Invariance in Constrained Switching Systems*, 2017, [arXiv:1702.00598](https://arxiv.org/abs/1702.00598) | **全文定向精读** pp. 2--6：Assumptions 1--4、Definitions 1--3、Proposition 1、Theorems 1--3 | 在图约束切换系统上定义 node-indexed invariant multi-set；逐边包含等价于不变性；由 forward reachable sets 构造 minimal invariant multi-set，并给有限外逼近和 maximal admissible multi-set。 | “按模式索引不变集”和 forward-reachability 外逼近均已有直接基线，不能作为创新。其最小集/外逼近定理假设 disturbance 为 C-set 且图强连通；本项目部分边扰动低维，不能无条件照搬。 |
| Hassaan, Pati, Shen, Yong, *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, 2021, DOI [10.1016/j.ifacol.2021.08.482](https://doi.org/10.1016/j.ifacol.2021.08.482), [作者全文](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf) | **全文定向重读** pp. 1--3：Definition 1、system/timing、Section 3.1.1 的 estimator 与 time-varying error tubes | 用 finite-length missing/delay language 和 equalized recovery 构造周期时变误差界；未来数据模式未知时，对全部未来模式取 worst case，并周期复用。 | time-uniform invariant `E_eta^j` 比其 finite/periodic equalized-recovery tube 更强，可能显著更保守；不能把“存在统一不变包”当成 MPC 所必需。 |
| Rutledge, Yong, Ozay, *Finite horizon constrained control and bounded-error estimation in the presence of missing data*, 2020, DOI [10.1016/j.nahs.2020.100854](https://doi.org/10.1016/j.nahs.2020.100854) | **仓库既有全文精读；本轮定向对照** equalized-recovery 定义与 missing-data language | 有限时域路径/前缀相关 bounded-error estimation 与 control 已有系统化框架。 | 本轮 time-uniform 集合只能作为 backup/尾端接口；有限时域在线 tightening 的强基线仍是路径/相位相关集合。 |

全文门槛由前两篇本轮正文阅读满足。检索未发现可支持“15 模态椭球 Bellman 固定点”为首次性的依据；本轮不作创新声明。

## 2. 严格差异、直接推论与强基线

本轮把第 07 章已证明的边递推

```math
r_b^+\ge c r_a+\sqrt{q_{ab}},\qquad c=\sqrt{19/20}<1
```

闭合为图上的 Bellman 固定点。这是 contraction mapping 与 invariant multi-set 逐边条件的直接应用，不是新算法。与 Athanasopoulos 等的通用基线相比，本轮只增加：仓库实际 15 模态/17 边、actual-input observer 时序、精确有理数根区间，以及对当前状态硬约束的严格否证。

最强同条件比较不是固定盒，而是：同一图、同一边 disturbance map 上的 geometry-preserving minimal invariant multi-set 或其带 certified tail 的外逼近；MPC 层还必须与 Hassaan 等的 finite/periodic equalized-recovery tube 比较。单一标量椭球只是保守基线。

## 3. 推进价值与推翻条件

该问题决定 Run 134 的联合 ancillary 图是否获得合法 `eta` 输入。通过条件是：全部 17 条边满足 time-uniform 包含，且集合在 residual 有效域和硬约束 tightening 上不自相矛盾。以下结果会推翻候选：

- Bellman 上界不能逐边闭合；
- 只能由浮点迭代“看似收敛”而没有 directed-rounding 包含；
- 完整椭球的某坐标半宽超过原状态区间半宽，使任何中心下的 tightening 都为空；
- 用冻结线性 inclusion 的集合跨越 residual 验证域后，仍声称得到物理真值的自洽全局不变集。

## 4. 准入判断

**作为必要基线复核与否证：通过。作为新算法/论文贡献：不通过。**

理由：闭合固定点能回答上轮唯一问题，并可严格排除一个错误的控制接口；但图不变多集与 finite/periodic missing-data tubes 都已有直接近邻。允许实现一个最小 verifier，禁止据此声称创新或闭环安全。

## 5. 本轮停止条件

若 scalar/common-metric 固定点逐边存在但其可靠下界已经使 state tightening 为空，立即停止继续调参或搜索椭球，转向 geometry-preserving invariant multi-set。只有后者在同一实际输入/物理域合同下闭合，才恢复 ancillary RCI。
