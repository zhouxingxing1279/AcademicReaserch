# 外环模型与飞控接口合同（临时版）

> 状态：**PROVISIONAL / NOT FROZEN**。本文用于约束研究边界，不是已验证的 PX4/ArduPilot 模型或控制器实现。

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
矩阵需由目标飞控闭环辨识。Santos & Lagoa (2022) 提供类似位置指令型闭环模型的多旋翼 Tube RMPC 先例；论文增益和扰动界不可直接移植。

### B. 加速度参考
\[
\dot p=v,\qquad \dot v=a_c+w_a
\]
\(w_a\) 必须覆盖加速度跟踪误差、命令延迟、风扰和限幅影响。Andriën et al. (2024) 与 Izadi et al. (2026) 提供级联外环加速度参考依据；其自定义姿态内环不等于现成飞控黑盒。

### C. 速度参考
速度参考 \(v_c\) 的响应需依据飞控模式和实测辨识，不能预设为理想一阶/二阶系统。

## PX4 ROS 2 Offboard 字段语义（官方文档级证据）

对于多旋翼 `TrajectorySetpoint`，position 非 NaN 时运行位置控制链，velocity/acceleration 可作为前馈；position 为 NaN 且 velocity 有效时运行速度控制链，acceleration 可作为前馈；position 与 velocity 均为 NaN、acceleration 有效时进入加速度设定路径。数据为 NED，单位分别为 m、m/s、m/s²。

必须联合检查 `OffboardControlMode` 与 `TrajectorySetpoint` 有效字段/NaN mask；不同 ROS 2 与 MAVLink 消息路径不能默认等价。该接口语义不提供实际跟踪误差、延迟、带宽或饱和界。完整证据和来源见 [PX4 外环接口证据](model_selection/PX4_INTERFACE_EVIDENCE.md)。

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
1. 指定飞控栈、版本、模式和坐标系。
2. 核验外环指令字段物理语义、频率、时间戳、failsafe 与限幅。
3. SITL 记录参考输入与真实位置/速度响应，辨识延迟、带宽、饱和和误差界。
4. 在拟用工作域验证闭环模型残差的有界外包。
5. 冻结传感器量测方程、异步模式、噪声/相关性合同。
6. 再设计 SMF/CZ、Tube MPC 与终端安全条件。
