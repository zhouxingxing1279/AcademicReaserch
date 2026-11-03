# PX4 Offboard 外环接口与闭环模型证据

> 状态：Offboard 字段语义与 v1.17.0 源码级控制链已核验；**尚未运行 SITL，也未冻结闭环矩阵、延迟或残差界**。本文整合 PR #188、#186、#190，并链接 [PX4 v1.17.0 源码审计与辨识协议](PX4_V1_17_SOURCE_AUDIT.md)。

## 1. 研究边界

当前仿真对象采用完整四旋翼六自由度刚体物理模型，包含位置、速度、姿态和角速度；成熟 PX4 飞控负责姿态/角速度稳定、控制分配、执行器限幅及电机控制。外环 MPC 只发出位置、速度或加速度等高层参考。

必须区分三种对象：

1. **物理仿真 plant（12 状态）**：\(x_{phys}=[p^T,v^T,\eta^T,\omega^T]^T\)，其中 \(p,v\in\mathbb R^3\)，\(\eta\) 为姿态参数化，\(\omega\) 为角速度。它是 SITL/高保真仿真中的真实动力学对象。
2. **外环预测状态**：首个候选为 \(x_{out}=[p^T,v^T]^T\in\mathbb R^6\)。只有当姿态/角速度内环效应、时延、饱和和模型误差可被有依据的残差集合外包时，才允许采用这个降阶闭环预测模型。
3. **外环优化输入**：位置参考 \(r_p\)、速度参考 \(r_v\) 或加速度参考 \(r_a\) 三选一（可按已验证接口包含前馈项）。它们不是电机推力、wrench 或实际加速度。若 6 状态预测模型无法覆盖约束相关的姿态瞬态，应增广预测状态或采用可验证的更高阶闭环模型，而不是让外环直接接管电机。

12 个物理状态不意味着外环 MPC 必须优化 4 个电机输入；反过来，6 状态外环预测也不意味着仿真只运行简化 6 状态 plant。

## 2. PX4 ROS 2 Offboard 接口语义

主要官方来源（滚动文档，检查日期 2026-11-03）：

- [PX4 v1.17.0 Offboard mode](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/docs/en/flight_modes/offboard.md)
- [PX4 v1.17.0 TrajectorySetpoint message](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/msg/versioned/TrajectorySetpoint.msg)
- [PX4 v1.17.0 PositionControl.cpp](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_pos_control/PositionControl/PositionControl.cpp)
- [PX4 v1.17.0 Gazebo SITL / ROS 2 指南](https://github.com/PX4/PX4-Autopilot/tree/v1.17.0/docs/en)

对于多旋翼 ROS 2 `TrajectorySetpoint`，有效字段与 NaN mask 决定位置/速度/加速度控制层级：

| 有效 setpoint 字段 | 控制含义 | 其他有效字段 |
|---|---|---|
| position 非 NaN | 位置设定值；位置控制链生效 | velocity、acceleration 可作为前馈 |
| position 为 NaN，velocity 非 NaN | 速度设定值；速度控制链生效 | acceleration 可作为前馈 |
| position、velocity 为 NaN，acceleration 非 NaN | 加速度设定路径 | 不能假定为无滞后的理想加速度伺服 |

- 数据采用 NED 坐标；position 为 m，velocity 为 m/s，acceleration 为 m/s²。仿真和估计器若使用 ENU，必须显式转换并统一重力符号。
- `OffboardControlMode` 的模式标志与 `TrajectorySetpoint` 的字段有效性必须联合检查。不能只看模式标志，就推断实际生效的是速度或加速度控制器。
- PX4 Offboard 还依赖有效状态估计与持续 setpoint/心跳；失联 failsafe、状态估计有效性、更新率和超时属于接口安全合同的一部分。
- ROS 2 `TrajectorySetpoint`、MAVLink `SET_POSITION_TARGET_LOCAL_NED`、全局加速度命令及姿态/推力 setpoint 不是可以互换的同一种接口。某些 MAVLink 加速度路径可能被映射为归一化推力，不能把所有标注为“acceleration”的消息视为物理加速度闭环。

**边界：** 官方文档只证明字段语义与接口能力，不证明位置/速度/加速度命令能被零延迟、无饱和、无偏差地跟踪；也不提供本研究所需的确定性闭环误差界。v1.17.0 的 acceleration-only 模式要求有效 velocity estimate；此处只把 position-only 作为首轮接口，不跨版本混用 rolling main 的估计要求。

## 2.1 v1.17.0 源码级位置控制链（已核验，未做 SITL）

固定版本 [PX4-Autopilot v1.17.0](https://github.com/PX4/PX4-Autopilot/releases/tag/v1.17.0) 的源码显示，position setpoint 依次经过位置 P → 速度 PID（含积分与导数反馈）→ 加速度到姿态/推力转换；速度上限、倾角/推力饱和、anti-windup 和起飞/failsafe 状态均会改变闭环响应。速度导数默认经过 5 Hz 低通滤波（速度低通和 notch 默认关闭），内部控制周期由 local-position sample 驱动，dt 被限制在 2–40 ms。X500 还默认启用 HTE（`MPC_USE_HTE=1`），在线更新 hover-thrust estimate，并通过 `updateHoverThrust()` 修正垂直速度积分器 `_vel_int(2)`；HTE 与 z 轴积分记忆耦合。X500 airframe 将初始化参数 `MPC_THR_HOVER` 设为 0.60。

因此，`[p;v]` 是候选预测状态而非自动成立的完整 Markov 状态。若相同 `[p,v,r_p]` 在不同参考历史/积分器状态下产生不同输出，必须增广可识别的控制器记忆/滞后状态，或在明确工作域内证明统一残差外包；不能直接假设理想双积分器。HTE 开启时还存在慢变 hover-thrust estimate，且它会联动修正 `_vel_int(2)`；首轮建议 HTE-off 固定 `MPC_THR_HOVER=0.60` 隔离位置环，再做 HTE-on 对照并检查两者的联合记忆效应。

**建议的可复现基线（暂定）：** PX4 v1.17.0 + Gazebo Harmonic X500 SITL（`make px4_sitl gz_x500`）+ Ubuntu 22.04 / ROS 2 Humble / uXRCE-DDS + `px4_msgs release/1.17`。首轮位置环辨识使用明确标注的 HTE-off 变体（`MPC_USE_HTE=0`、`MPC_THR_HOVER=0.60`），随后 HTE-on 对照。完整版本、commit、消息兼容、topic 可用性和阶跃/轨迹辨识合同见 [PX4 v1.17.0 源码审计](PX4_V1_17_SOURCE_AUDIT.md)。

首轮 position-only 发送：`OffboardControlMode.position=true`；`TrajectorySetpoint.position` 三轴有效，velocity/acceleration 为 NaN；持续发送 heartbeat，并在每个外环 MPC 周期更新 setpoint。Offboard heartbeat 与 MPC setpoint 更新是两个独立速率。

## 3. 三类接口的正确预测模型

### A. 位置参考：首要辨识候选

外环状态候选 \(x_{out,k}=[p_k^T,v_k^T]^T\)，输入为位置参考 \(r_{p,k}\)。v1.17.0 的实际输入输出链包含位置 P、速度 PID 积分/导数反馈及限幅；应通过锁定固件、参数、机体、仿真步长和 Offboard 消息路径后的 SITL/HIL 数据辨识：

\[
x_{out,k+1}=A_{p,cl}x_{out,k}+B_{p,cl}r_{p,k}+E_{p,cl}w_{p,k}.
\]

\(w_{p,k}\) 必须覆盖闭环模型残差、风扰、跟踪误差、命令延迟、限速/饱和、坐标变换误差及仿真数值误差。不能将位置参考直接代入双积分器作为加速度输入。

### B. 加速度参考：理论备选

理想零阶保持双积分器为：

\[
p_{k+1}=p_k+h v_k+\tfrac12h^2 a_{r,k},\qquad
v_{k+1}=v_k+h a_{r,k}.
\]

只有在实际加速度跟踪残差 \(e_{a,k}=a_{actual,k}-a_{r,k}\) 的有界集合经过验证，且延迟、倾角/推力限幅与姿态动态已被纳入扰动或增广状态时，才能把该模型用于鲁棒 Tube 设计。PX4 接受加速度 setpoint 本身不证明上述假设。

### C. 速度参考：对照候选

需要辨识 \(r_v\to[p,v]\) 的闭环响应；不得假设 \(v_{k+1}=r_{v,k}\)，也不得直接沿用加速度双积分器。若存在速度环积分、限幅、延迟或明显动态，应显式建模或外包残差。

## 4. 对 SMF/CZ 与 Tube MPC 的影响

- SMF/CZ 预测应使用已经辨识的闭环模型及实际已应用的高层参考；不能使用未经确认的请求命令代替真实已应用输入。
- 位置量测到达时才应用有界测量条带更新；丢包时按已验证的闭环模型传播集合。
- 必须区分 PX4 内环 EKF 的高频状态估计与外环 SMF 的间歇测量通道。首轮建议让 PX4 内环 EKF 正常工作，外环 SMF 使用独立合成位置测量/丢包通道；若对 `vehicle_local_position` 的 ROS 2 副本施加丢包，不能误认为 PX4 内部 EKF 也丢失该数据。
- 飞控 EKF 输出可能已经融合 IMU、GNSS、VIO 等信息。未建立信息相关性合同前，不得把 EKF 输出和同源原始 IMU 当作独立观测重复相交。
- SMF/CZ 当前后验集合与未来 Tube 误差集合不同；必须证明真实状态在后验内，并证明后验到 Tube 初始误差集的包含关系。
- Tube 扰动需覆盖风、闭环跟踪误差、通信/计算延迟、限幅/饱和、控制分配残差及模型失配。若无法得到确定性有界残差，相关硬安全结论必须降级，不得用概率指标替代。

## 5. 模型冻结 Gate

1. 暂定锁定 PX4 v1.17.0 tag/commit、X500/Gazebo Harmonic、Ubuntu 22.04/ROS 2 Humble、`px4_msgs release/1.17` commit、uXRCE-DDS 和 NED/ENU 约定；完整候选见 [源码审计](PX4_V1_17_SOURCE_AUDIT.md)。
2. 核验 `OffboardControlMode`、`TrajectorySetpoint` 有效字段、更新率、超时、failsafe、状态估计有效性及限幅。
3. 设计 position/velocity/acceleration 分别独立的阶跃与轨迹辨识工况；记录请求 setpoint、实际位置/速度/姿态/角速度、饱和标志、时间戳与延迟。
4. 在声明的工作域内拟合 \(A_{cl},B_{cl}\)，验证残差集合对全部采样点和独立验证工况的覆盖；不能仅报告均方误差。
5. 若 6 状态平移预测的残差依赖 PX4 速度积分器/滤波器历史、HTE 慢变状态、姿态瞬态或约束耦合，则增广必要闭环记忆状态；不能预先指定增广维数，12 状态物理仿真 plant 保持不变。
6. 冻结传感器噪声、丢包自动机、相关性和输入可实现性后，才进入 SMF/CZ 与 Tube MPC 设计。

## 6. 来源与整合关系

- PR [#188](https://github.com/zhouxingxing1279/AcademicReaserch/pull/188)：Offboard setpoint 字段、NaN mask、NED 与控制层级。
- PR [#186](https://github.com/zhouxingxing1279/AcademicReaserch/pull/186)：同一接口的跨论文迁移边界与 SMF/Tube 影响；与 #188 重复部分已在本文合并，不再作为两个独立接口决策。
- PR [#190](https://github.com/zhouxingxing1279/AcademicReaserch/pull/190)：位置/速度/加速度闭环模型迁移合同、辨识与残差界要求。
- [PX4 v1.17.0 源码审计与 SITL 辨识协议](PX4_V1_17_SOURCE_AUDIT.md)：固定 tag/commit、位置 P—速度 PID 级联、积分/滤波/饱和、DDS topic 与外环测量通道边界。
- 本文是对上述审计的规范化摘要；原 PR 分支与其原始研究记录未被修改或关闭。本轮仅做文档/源码核验，不声称完成 SITL/HIL。
