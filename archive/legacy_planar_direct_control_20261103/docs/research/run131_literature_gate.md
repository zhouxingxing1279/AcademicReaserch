# Run 131 文献准入卡：两层 output-feedback tube 与 backup terminal 架构

日期：2026-09-29。仓库起点为本地 Run 130 提交 `ee12daf`；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。本轮只判断下述架构是否仍有方法级空白：在线 SMF posterior 用于有限时域 tightening，独立 backup/adaptive terminal tube 负责缺测、重定心与旧计划移位下的递归可行性。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读层级 | 已解决内容 | 与本轮关系 |
|---|---|---|---|
| Dey, Dhar, Bhasin, *Adaptive Output Feedback Model Predictive Control*, arXiv:2209.08908, 2022 | **全文定向精读** IV-A、IV-D--IV-F、Algorithm 1、recursive-feasibility proof | 用不变估计误差集包围状态估计误差，以 homothetic tube 包围估计轨迹；二者相加得到 true-state outer tube。终端集与移位候选封闭递归可行性。 | 论文明确称为 `homothetic and invariant` two-tube。故“两层 tube”本身已有直接先例。 |
| Dey, Bhasin, *Adaptive Output Feedback MPC With Guaranteed Stability and Robustness*, IEEE TAC 70(12):8345--8352, 2025, DOI [10.1109/TAC.2025.3584302](https://doi.org/10.1109/TAC.2025.3584302) | **全文定向精读** IV-A--IV-D、Assumption 4、Theorem 1--2 | 时间相关估计误差集与 homothetic state-estimate tube 构成 two-tier tube；固定 terminal set 在估计状态空间中封闭 shift，证明 recursive feasibility 与 robust exponential stability。 | 直接覆盖“在线/时变估计信息 + 独立终端骨架”的宽泛主张。 |
| Dey, Bhasin, *Output Feedback MPC with Adaptive Tubes*, arXiv:2605.23661, 2026 | **全文定向精读** IV-C--IV-F、Criterion 1、Algorithm 1、Theorem 2、Appendix IV | 随 state/model/initial-set 更新 tube、tightening 和 terminal set；Criterion 1 检查相邻 terminal 兼容性，失败时保留旧点估计/回退集合并重构可行 COCP；Appendix IV 用旧解移位和 terminal 追加证明 recursive feasibility。 | 已覆盖比本轮候选更强的 adaptive terminal、acceptance criterion 与 backup/revert 逻辑。 |
| Köhler, Müller, Allgöwer, *Robust output feedback model predictive control using online estimation bounds*, arXiv:2105.03427, 2021 | **全文定向精读** III-C、IV-B，Assumption 7、Theorem 4 及证明 | 在线有效 estimation-error bounds 驱动阶段 tube；augmented terminal ingredients 同时约束 nominal、observer mismatch 和 error-bound scalars，旧解移位证明 recursive feasibility；含 10-state quadrotor 数值例。 | 已覆盖“在线估计信息服务有限时域 tightening，固定 augmented terminal envelope 负责尾端”的核心分工。 |
| Ping, *Dynamic Output Feedback Robust MPC via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems*, 2015, DOI [10.1155/2015/875850](https://doi.org/10.1155/2015/875850) | **全文定向精读** 4.2--4.4、Algorithm 8、Theorem 9 | zonotopic estimation-error set 在线刷新并限制阶数；辅助一步 feasibility problem 决定是否采用新 controller parameters，失败时继承旧参数；给出约束满足/收敛结论。 | “zonotopic SMF 更新 + feasibility gate + fallback controller”已经存在。 |

补充边界：Ping--Yao--Ding--Li 2022 *Tube-Based Output Feedback Robust MPC for LPV Systems With Scaled Terminal Constraint Sets* 本轮只取得正式摘要，摘要已说明 nested RPI/RCI lookup、在线 tightening 与 scaled terminal set，但本轮不据摘要引用定理细节。Robbins 等 ACC 2026 正文仍未取得，首次性继续标为未知。

## 2. 严格差异、直接推论与最强基线

候选相对近邻的严格差异不再是“两层”“online bound”“terminal backup”或“更新失败回退”，而只可能是这些条件的交集：

1. estimator 是带间歇测量的可靠 CZ-SMF posterior，而不是 adaptive observer 的标量/多面体 bounds；
2. 在线控制器只查询固定数量的真实 state/input/terminal normals，不把完整高维 posterior 压成一个 post-hoc tube；
3. backup 是按 15-mode bounded-dropout automaton 索引的固定 terminal/RCI family；
4. acceptance/handoff 必须在 posterior 重定心、查询集变化和旧计划移位下仍成立；
5. 与 Dey 2026 adaptive tube、Köhler online-bound tube、Ping 2015 zonotopic gate 及固定 tube 在相同模型、传感信息、硬约束和完整计算预算下比较。

前四篇已经给出一般 recursive-feasibility 骨架，因此单纯把 SMF posterior 接到阶段 tightening，再附加 fixed/adaptive terminal set，是已有方法的直接组合，不是新贡献。最强同条件基线至少包括 Dey 2026 的 compatibility criterion/backup、Köhler 2021 的 online-bound augmented terminal、Ping 2015 的 zonotopic update gate，以及不消费 posterior 的固定 robust tube。

## 3. 论文链条价值与推翻条件

真正可能推进课题的不是再命名一个 two-layer architecture，而是闭合以下尚未证明的接口：

- **真值包含：** dropout 模式下 SMF posterior 与固定预算 support oracle 始终给出可靠外界；
- **backup 不变性：**每条允许模式边 `sigma -> sigma'` 满足 terminal family 的 robust controlled-invariance/input-tightening 条件；
- **handoff：**在线 stage-tightening 计划在接受时可移位，在拒绝/丢包时必能进入已认证 backup domain；
- **时序一致性：**重定心、未来控制序列变化和查询 normals 更新不能破坏旧计划的量词；
- **严格收益：**相同预算下相对 fixed/scalar/box tube 至少扩大认证可行域或改善闭环指标，而非只改进一个 support；
- **物理接口：**四旋翼外环余项、推力调度和执行器硬约束与 terminal family 使用同一 disturbance contract。

若 15-mode terminal family 为空，或 acceptance 只能退化为固定 tube，或相同预算下不能优于 Dey/Köhler/Ping 基线，则候选方法被推翻。即使上述条件成立，在取得 Robbins 2026 正文并完成更广检索前，首次性仍不能确认。

## 4. 准入结论

**广义架构的创新/实现准入：不通过。方向纠正准入：通过。**

- 不实现新的“两层 controller”或将已有模块拼接成代码；本轮没有新增优化器、控制器或数值实验。
- 宽泛命题被 Dey 2022/2025 的 two-tube、Dey 2026 的 adaptive terminal/backup、Köhler 2021 的 online-bound terminal proof 和 Ping 2015 的 zonotopic feasibility gate 共同覆盖。
- 下一步只允许研究一个更窄且直接阻塞闭环的命题：在当前 bounded-dropout automaton 与已核查物理/执行器合同下，构造或反驳 mode-indexed backup terminal family。它是后续 support-query tightening 能否安全 handoff 的必要骨架，而不是另一个局部压缩技巧。
