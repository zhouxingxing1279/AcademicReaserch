# 外环模型与飞控接口合同（临时版）

> 状态：**PROVISIONAL / NOT FROZEN**。建议的复现实验基线暂定为 PX4 v1.17.0 + Gazebo Harmonic X500 SITL + Ubuntu 22.04 / ROS 2 Humble / `px4_msgs release/1.17`；尚未运行 SITL，不是已验证的 PX4 闭环模型或控制器实现。版本与源码依据见 [PX4 v1.17.0 源码审计](model_selection/PX4_V1_17_SOURCE_AUDIT.md)。

## 被控对象边界与物理仿真对象
主仿真对象为完整 12 状态六自由度四旋翼刚体 plant：
\[
x_{phys}=[p^\mathsf T,v^\mathsf T,\eta^\mathsf T,\omega^\mathsf T]^\mathsf T\in\mathbb R^{12}
\]
其中位置、速度、姿态和角速度各为三维。它在成熟 PX4/ArduPilot 飞控闭环下仿真；姿态/角速度闭环、控制分配、执行器限幅和电机仍由飞控承担。

外环 MPC 只输出高层位置/速度/加速度参考，不直接输出四桨推力、总推力/力矩 wrench 或姿态稳定输入。12 状态物理 plant 不等于 12 个状态都必须由外环优化器直接控制，也不意味着优化器拥有四个电机输入。

## 外环预测状态候选
首个可检验的降阶预测状态为：
\[
x_{out}=[p^\mathsf T,v^\mathsf T]^\mathsf T
=[p_x,p_y,p_z,v_x,v_y,v_z]^\mathsf T\in\mathbb R^6
\]
它仅表示三维平移闭环状态，不是六自由度物理对象。只有在 12 状态 SITL plant 上证明姿态/角速度瞬态、飞控跟踪误差、延迟、饱和和模型失配可由统一有界残差外包时，才允许使用该降阶模型。若残差不能覆盖约束相关瞬态，应增广外环预测状态（包括姿态/角速度或必要的飞控滞后状态），而不是更改外环控制权限、转为电机级控制。

## 待比较的指令接口
### A. 位置参考
\[
\dot p=v,\qquad \dot v=-K_p(p-r_c)-K_vv+w_{fc}
\]
不得先验指定连续二阶模型为 PX4 真值。应辨识离散闭环模型 \\(x_{k+1}=A_{cl}x_k+B_{cl}r_{p,k}+E_{cl}w_k\\)，并测试输入延迟/零阶保持。PX4 v1.17.0 源码显示位置 P—速度 PID 级联，存在 `_vel_int` 积分记忆、速度/导数滤波、速度/倾角/推力限制与 anti-windup；若其历史影响不能被统一残差覆盖，必须增广可识别的控制器状态。Santos & Lagoa (2022) 提供类似位置指令型闭环模型的多旋翼 Tube RMPC 先例；论文增益和扰动界不可直接移植。

### B. 加速度参考
\[
\dot p=v,\qquad \dot v=a_c+w_a
\]
\(w_a\) 必须覆盖加速度跟踪误差、命令延迟、风扰和限幅影响。Andriën et al. (2024) 与 Izadi et al. (2026) 提供级联外环加速度参考依据；其自定义姿态内环不等于现成飞控黑盒。

### C. 速度参考
速度参考 \(v_c\) 的响应需依据飞控模式和实测辨识，不能预设为理想一阶/二阶系统。

## PX4 ROS 2 Offboard 字段语义（官方文档级证据）

对于多旋翼 `TrajectorySetpoint`，position 非 NaN 时运行位置控制链，velocity/acceleration 可作为前馈；position 为 NaN 且 velocity 有效时运行速度控制链，acceleration 可作为前馈；position 与 velocity 均为 NaN、acceleration 有效时进入加速度设定路径。数据为 NED，单位分别为 m、m/s、m/s²；NaN 表示对应状态不受控。v1.17.0 的 acceleration-only 模式在 OffboardControlMode 表中要求有效 velocity estimate。首轮采用 position-only：position 三轴有效，velocity/acceleration NaN。

必须联合检查 `OffboardControlMode` 与 `TrajectorySetpoint` 有效字段/NaN mask；不同 ROS 2 与 MAVLink 消息路径不能默认等价。该接口语义不提供实际跟踪误差、延迟、带宽或饱和界。完整证据和来源见 [PX4 外环接口证据](model_selection/PX4_INTERFACE_EVIDENCE.md)。

## 内环估计器与外环间歇测量的边界

PX4 内环使用自身高频 `vehicle_local_position` 状态维持位置/速度控制。研究中的间歇/异步位置量测应先定义为外环 SMF 可获得的独立通道；首轮 SITL 可由 Gazebo 真值生成独立有界噪声观测并施加丢包，PX4 EKF 保持正常运行。若对 `vehicle_local_position` 的 ROS 2 副本施加丢包，丢包只作用于外环副本，不能写成 PX4 内环估计器同时失测。EKF 输出与其已融合的同源 IMU/GNSS/VIO 不得重复作为独立量测融合。

## 测量与集合估计
\[
y^p_k=C_px_k+\nu^p_k,\quad C_p=[I_3\ \ 0]
\]
位置量测可间歇到达；速度可能来自飞控 EKF、VIO/GNSS 或差分估计。必须记录时间戳、延迟、噪声界、更新模式及相关性。若 EKF 输出已融合 IMU，不得把同一 IMU 数据作为独立观测重复融合。

集合预测/更新抽象接口：
\[
\mathcal X_{k+1|k}=A_d\mathcal X_{k|k}\oplus B_du_k\oplus E_d\mathcal W_k
\]
\[
\mathcal X_{k+1}=\mathcal X_{k+1|k}\cap\{x:y_{k+1}-Cx\in\mathcal V_{k+1}\}
\]
实际矩阵、噪声集合和异步模式必须在接口选定后确定。

## Tube MPC 接口
SMF/CZ 后验 \(\mathcal X_k\) 不是未来 Tube。需构造估计误差集合 \(\mathcal E_k\)，证明其可靠包含真实初始误差，再传播未来 Tube。名义约束收紧可写为：
\[
\bar{\mathcal X}_k\subseteq\mathcal X_{\mathrm{safe}}\ominus\mathcal E_k
\]
只有在 \(\mathcal E_k\) 是有效误差外包且控制接口/约束映射闭合时才有安全意义。

## 不确定性与约束
风扰与模型残差；飞控跟踪误差、延迟和通信抖动；速度/加速度/倾角/推力限幅及分配饱和的外环等效影响；测量噪声、时间戳误差和异步更新；安全位置区域、速度上限及可实现参考约束。

## 模型冻结准入条件
1. 暂定指定 PX4 v1.17.0 tag/commit、X500/Gazebo Harmonic、Ubuntu 22.04/ROS 2 Humble、匹配的 `px4_msgs release/1.17`、Offboard ROS 2 路径和 NED 坐标系；完整 pin 见 [源码审计](model_selection/PX4_V1_17_SOURCE_AUDIT.md)。
2. 核验外环指令字段物理语义、频率、时间戳、failsafe 与限幅。
3. SITL 记录参考输入与真实位置/速度响应，辨识延迟、带宽、饱和和误差界。
4. 在拟用工作域验证闭环模型残差的有界外包。
5. 冻结传感器量测方程、异步模式、噪声/相关性合同。
6. 检验 \\(x_{out}=[p;v]\\) 六状态模型对积分器/滤波器历史的残差覆盖；若失败先增广最小必要闭环记忆状态。
7. 再设计 SMF/CZ、Tube MPC 与终端安全条件。
