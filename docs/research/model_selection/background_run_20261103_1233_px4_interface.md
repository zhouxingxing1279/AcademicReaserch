# 2026-11-03 外环接口核验：PX4 Offboard setpoint 语义与级联论文迁移边界

## 本轮唯一问题
Santos–Lagoa 位置指令型外环与 Andriën 等加速度指令型外环，能否映射至成熟 PX4 Offboard 而不错误地将指令当作真实动力学输入？

基准 main SHA: eb18e857090b0babe531c13c61aea944793af428。前一轮 PR #184 尚未合并；本轮不重写其日志。核对 main 的 CURRENT_CHECKPOINT、唯一论文总账、模型证据矩阵与 PR #184。

## 原始论文交叉核验（本轮均为出版方/机构摘要与元数据核验，非全文逐式审计）
1. Santos, D. A.; Lagoa, C. M. (2022), *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, ISA Transactions 128:123–135, DOI https://doi.org/10.1016/j.isatra.2021.12.002 。机构摘要 https://flavioluiz.github.io/pgeam/en/publicacoes/85122342732/ ：明确 supervisory outer guidance + preexisting stabilizing attitude/position laws，使用降阶**闭环平移**离散线性模型，假设平移/旋转时间尺度分离，考虑有界随机扰动和测量噪声，声称递归可行、鲁棒稳定，数值验证。摘要不能独立核验 A/B 矩阵、Ts/N、位置指令与物理推力映射；保留前轮待审计。
2. Andriën, A. R. P.; Lefeber, E.; Antunes, D.; Heemels, W. P. M. H. (2024), *Model Predictive Control for Quadcopters With Almost Global Trajectory Tracking Guarantees*, IEEE TAC 69(8):5216–5230, DOI https://doi.org/10.1109/TAC.2023.3349098 ，机构页面 https://research.tue.nl/en/publications/model-predictive-control-for-quadcopters-with-almost-global-traje/ 。摘要明确外环生成二次可微加速度参考，内环非线性姿态/角速度控制；推力上下界与整体几乎全局渐近稳定性。非 PX4 黑盒，稳定性结论不可直接迁移。
3. Izadi, M.; Cobbenhagen, A. T. J. R.; Sommer, R.; Andriën, A. R. P.; Lefeber, E.; Heemels, W. P. M. H., *High-Performance Model Predictive Control for Quadcopters with Formal Stability Guarantees*, arXiv:2412.20277 (2024 preprint), https://arxiv.org/abs/2412.20277 。摘要明确外环加速度参考→姿态/角速参考→非线性内环，非直接电机优化。未核验正式 Automatica 终版与预印本差异，本轮仅将其计作预印本摘要核验，不冒充正式全文。
本轮实际论文3篇：全文0、正文部分0、摘要/元数据3；其中直接四旋翼外环原始研究3篇（含一篇预印本）。论文阅读总账已有条目不重复登记；本轮新增的是官方飞控接口证据，而不是新的已读全文。

## 新的直接接口证据（官方文档）
PX4 官方 Offboard 文档 https://docs.px4.io/main/en/flight_modes/offboard 和上游仓库 https://github.com/PX4/PX4-Autopilot/blob/main/docs/en/flight_modes/offboard.md ：
- 多旋翼 ROS2 `TrajectorySetpoint`：position 非 NaN 时运行位置控制，velocity/acceleration 非 NaN 作为前馈；position=NaN、velocity 非 NaN 时运行速度控制，acceleration 非 NaN 作为前馈；position=velocity=NaN、acceleration 非 NaN 时运行加速度设定路径。数据为 NED 坐标，单位 m/m/s/m/s²。
- `OffboardControlMode` 的意图标志不保证控制层级；**实际 setpoint 字段的 NaN/非 NaN 决定控制器是否运行**。错误混合字段会导致误以为运行速度/加速度模式，实际仍运行位置控制器。
- 姿态 setpoint 是四元数+归一化机体系推力；不等价于电机输入。当前研究无需深入此级。
- 文档确认接口接受某类指令，**不等于**飞控能够无延迟、无饱和、按理想双积分器跟踪指令；不同 PX4 版本、ROS2/MAVLink 路径必须冻结。

## 跨论文与 PX4 的关键区别
| 候选 | MPC 输出 | PX4 内部仍运行的环 | 合理 plant | 主要缺口 |
|---|---|---|---|---|
| Santos–Lagoa 型 | 位置参考 r_c | 位置+速度+姿态环 | 已闭环的 r_c→[p,v] 离散模型 | 位置环带宽/限速/饱和/延迟、参数辨识、原文公式 |
| 速度指令型（PX4接口证据，非本轮论文直接基线） | 速度参考 v_c | 速度+姿态环 | v_c→[p,v] 闭环模型 | 速度环动态、积分与限幅 |
| Andriën 型 | 加速度参考 a_c（其论文还含参考整形动态） | PX4 加速度→姿态/推力相关通路 | 有界加速度跟踪误差的平移模型或增强模型 | PX4 实际指令语义与论文自定义非线性内环不一致 |
| 仓库原平面6态 | (T,τ) | 直接控制刚体姿态/力矩 | [p_x,p_z,v_x,v_z,phi,omega] | 与成熟飞控外环研究权限不符，不能沿用安全证明 |

## 对 SMF/CZ 与 Tube MPC 的实质影响
若使用位置参考输入，SMF 的被估状态仍可为 x=[p,v]∈R6，但其预测模型应是闭环 x(k+1)=A_cl x(k)+B_cl r_c(k)+Ew(k)，不是把 r_c 直接当加速度。若使用加速度参考，理想双积分器仅在飞控跟踪残差 a_actual−a_c 被**统一有界**且延迟/饱和纳入扰动或增广状态时可用。丢包位置测量仅在真实新量测到达时更新 CZ；飞控 EKF 输出与其已融合 IMU 不能未经相关性证明重复作为独立信息源。管束需同时覆盖初始状态后验误差与未来闭环扰动，不可把两者等同。

## 模型矩阵变化和决策
- 将「六状态三维位置/速度 + 位置指令 + 已闭环 PX4 位置控制」提升为**优先待验证候选**，而非已证正式模型。
- 将「六状态三维位置/速度 + 加速度指令 + 有界跟踪残差」保留为**理论对照**；Andriën 的12维是平移加参考整形状态，不等于12态刚体。
- 旧四状态冻结 Euler、六状态平面 (T,τ) 和 Run246/260/261 只能作不同控制合同下的理论/反例基线；不得继承其递归可行或硬安全结论。
- 无新增数学证明、闭环代码、SITL/真实飞行数据或 WCET；Gate A 对旧合同仍 blocked。新外环合同需另立验证门槛。
- 本轮未实际检查 PX4 固定版本源代码、位置环具体增益和限幅，不能给出闭环 A/B 或数值扰动界。

## 下一轮唯一优先问题
**冻结一个具体 PX4 版本及 ROS2 TrajectorySetpoint 位置模式，读取 mc_pos_control 的位置→速度→加速度控制链和限幅源码；给出 r_c→[p,v] 可辨识闭环模型所需参数、测量日志和有界误差验证方案，并对照 Santos–Lagoa 正文逐式核验。** 如无法获得可证统一扰动界，位置指令型 Tube MPC 的严格安全证明必须降级为有条件保证。
