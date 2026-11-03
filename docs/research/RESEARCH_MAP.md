# 研究路线图：12 状态仿真 plant 上的成熟飞控外环 MPC + SMF/CZ

当前主线不是电机级/姿态内环控制。完整 12 状态六自由度刚体模型作为仿真物理对象，成熟飞控承担姿态/角速度稳定、控制分配和电机执行；研究其上的位置/速度/加速度外环 MPC，并将间歇/异步测量下的 SMF/CZ 与 Tube MPC 安全保证接入。

## 阶段 1：冻结仿真物理对象与飞控接口

1. 选定 12 状态六自由度刚体物理 plant、机体参数、坐标系、重力方向和工作包线。
2. 暂以 PX4-Autopilot v1.17.0（commit `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`）、Gazebo Harmonic X500、Ubuntu 22.04 / ROS 2 Humble、`px4_msgs release/1.17`（commit `86d8239e962f6939e05c3737784f60c02fa884db`）作为可复现 SITL 基线候选；这不是最终硬件选型，且尚未运行 SITL。
3. 核验 Offboard setpoint 的真实字段语义、NaN mask、NED/ENU 转换、更新率、状态估计有效性、超时和 failsafe。
4. 先使用 PX4 ROS 2 `TrajectorySetpoint` position-only 参考；首轮辨识变体设 `MPC_USE_HTE=0`、`MPC_THR_HOVER=0.60`，之后单独做 HTE-on 对照；速度和加速度参考后续独立测试。

## 阶段 2：确定外环预测模型，而不是改变物理仿真对象

1. 在 12 状态物理 plant + 成熟飞控闭环下记录 setpoint、实际位置/速度/姿态/角速度、饱和状态与时间戳。
2. 首先检验六状态平移预测 \\(x_{out}=[p;v]\\)；位置 setpoint 经 PX4 位置 P—速度 PID 级联，不是理想双积分器。
3. 在 HTE-off 固定悬停推力基线下，通过重复历史/不同积分器初值试验检验六状态是否 Markov；若残差依赖 `_vel_int`、速度导数滤波或饱和，增广最小必要闭环记忆状态。
4. 做 HTE-on 对照，检查 hover-thrust estimate 是否需要作为慢变增广状态；辨识位置参考到 \\([p,v]\\) 的闭环 \\(A_{cl},B_{cl}\\)，并检验输入延迟和零阶保持。
5. 对独立验证工况计算残差外包，覆盖姿态瞬态、飞控跟踪误差、延迟、饱和、风扰和模型失配。
6. 如果六状态模型不能给出约束相关瞬态的可靠外包，则增广预测状态；12 状态物理 plant 始终保留用于仿真验证。
7. 外环输入始终是已验证的高层参考；不把电机推力、wrench 或姿态稳定命令当作当前研究输入。

## 阶段 3：冻结测量与丢包合同

- 区分 Gazebo 真值、PX4 内环 EKF 的 `vehicle_local_position`、外环 SMF 测量通道；首轮保持 PX4 EKF 高频运行，单独对外环测量施加有界噪声/丢包。
- 记录坐标、时间戳、延迟、噪声界和信息相关性；不得重复融合 EKF 已经使用的同源 IMU/GNSS/VIO。
- 规定位置/速度测量到达时序及正式丢包自动机（初始相位、状态、转移、最大连续丢包）。
- 不把飞控 EKF 已融合的信息与同源原始 IMU 当作独立测量重复使用。

## 阶段 4：SMF/CZ 估计

- 先实现并验证有界噪声下的集合预测、到达测量条带更新和丢包传播。
- 比较 Box、Zonotope、Constrained Zonotope 的可靠包含、集合紧致性、降阶保守性和计算开销。
- 将 12 状态仿真真值用于离线 containment 验证；外环估计状态可先为 \([p;v]\)，必要时增广姿态/风等状态。
- 不能将 Run285–293 的合成悬停模型结果当作 PX4 外环 SMF 证明。

## 阶段 5：Tube MPC 与安全闭合

1. 区分 SMF/CZ 当前后验、估计误差集合与未来 Tube。
2. 证明真实初始状态被后验包含，并证明后验到 Tube 初始误差集合的包含关系。
3. 将飞控跟踪误差、风扰、延迟、限幅和模型残差纳入有依据的扰动集合。
4. 构造约束收紧、终端鲁棒不变集和递归可行性条件；不得用有限仿真或概率约束替代确定性硬安全证明。

## 阶段 6：SITL/HIL 验证与对照

- 在同一 12 状态物理 plant、同一飞控版本和同一测量自动机下比较点估计 MPC、固定最坏界 Tube MPC、SMF/CZ 条件化 Tube MPC。
- 报告跟踪误差、约束违例、集合包含、集合宽度、求解时间分布和最坏观测步耗时；明确仿真结果与形式化保证的边界。
- 先建立可复现基线，再逐步增加不确定性和测量丢包复杂度。

## 关键文档

- [当前研究检查点](CURRENT_CHECKPOINT.md)
- [临时模型与接口合同](MODEL_CONTRACT.md)
- [PX4 外环接口证据](model_selection/PX4_INTERFACE_EVIDENCE.md)
- [PX4 v1.17.0 源码审计与 SITL 辨识协议](model_selection/PX4_V1_17_SOURCE_AUDIT.md)
- [外环 MPC 与 SMF/CZ 文献证据](model_selection/OUTER_LOOP_MPC_LITERATURE.md)
- [模型选型证据矩阵](model_selection/MODEL_SELECTION_EVIDENCE.md)
- [开放 PR 分类与依赖图](PR_TRIAGE_20261103.md)

## 禁止捷径

不把 12 状态物理 plant 与 12 维外环优化器混为一谈；不把六状态外环预测与六自由度物理模型混为一谈；不把 setpoint 当成实际加速度/推力；不混淆 SMF 后验与未来 Tube；不把概率保证改写成确定性硬安全；不把 Run246/260/261/278 或 Run285–293 的旧/合成模型结论直接迁移到新 PX4 外环合同。
