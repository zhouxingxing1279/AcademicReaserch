# PX4 v1.17.0 源码审计与外环辨识方案（2026-11-03）

> **证据状态：** 已核对 PX4 v1.17.0 官方文档、消息定义、DDS topic 配置、位置控制器源码、X500 airframe 脚本及 hover-thrust estimator；尚未运行 SITL，未辨识任何数值闭环矩阵/延迟/残差界。本文给出可复现的候选环境与实验合同，不把源码审计冒充仿真结果。

## 1. 建议的可复现基线（暂定，不等于最终硬件选型）

| 项目 | 建议基线 | 证据与状态 |
|---|---|---|
| 飞控 | PX4-Autopilot **v1.17.0** | 官方 Stable release；签名 tag 解引用到 commit `d6f12ad1c4f70ad3230afd7d86e971421e02fef4`。这是本轮建议锁定的研究基线，不代表已验证所有外部依赖。 |
| 物理仿真 | Gazebo Sim 的 X500 四旋翼 | v1.17 文档给出 `make px4_sitl gz_x500`，`PX4_SYS_AUTOSTART=4001`。 |
| OS / ROS 2 | Ubuntu 22.04 / ROS 2 Humble | v1.17.0 自身 ROS 2 指南推荐该组合；不要把较新 main 文档的 Jazzy 指引与 v1.17.0 混成一个环境合同。 |
| Gazebo | Harmonic | v1.17.0 文档说明 Ubuntu 22.04 开发环境默认安装 Harmonic。 |
| ROS 2 消息 | `PX4/px4_msgs` 的 `release/1.17` | 本轮核对分支 commit `86d8239e962f6939e05c3737784f60c02fa884db`；应与 PX4 v1.17.0 的消息定义匹配。 |
| Middleware | uXRCE-DDS | v1.17.0 文档给出 Micro XRCE-DDS Agent v2.4.3 的安装示例；SITL 模拟器会自动启动固件内 client。 |

**为什么暂定 v1.17.0：** 它是可固定的正式稳定版本，Offboard、消息、Gazebo SITL 和 ROS 2 资料可按同一 tag 审计。若后续改用 v1.18/main，必须重新核对 Offboard 估计有效性要求、消息版本、参数及源码，不能沿用本文件的版本特定结论。

**复现入口：**

```bash
# PX4-Autopilot
git checkout v1.17.0
make px4_sitl gz_x500

# ROS 2 message package
git clone https://github.com/PX4/px4_msgs.git
cd px4_msgs
git checkout release/1.17
```

正式复现实验时还要记录实际检出的 commit、子模块 SHA、Gazebo Harmonic 补丁版本、ROS 2 包版本、Agent 版本和 PX4 参数导出文件；分支名本身不足以作为长期实验锁定。

## 2. 位置参考接口：应如何发送

### 2.1 消息与模式

v1.17.0 的 ROS 2 Offboard 输入使用：

- `/fmu/in/offboard_control_mode`：声明外部控制层级并持续提供 Offboard heartbeat。
- `/fmu/in/trajectory_setpoint`：发送实际位置/速度/加速度参考。
- 接口选择暂不冻结，首轮在相同 HTE-off 条件下比较两种独立模式：**位置-only**（`OffboardControlMode.position=true`；`TrajectorySetpoint.position` 三轴有效，velocity/acceleration 为 NaN）与**加速度-only**（`OffboardControlMode.acceleration=true`；position/velocity 为 NaN，acceleration 三轴有效）。两种模式均保持 yaw 固定或使用 NaN 让 PX4 保持当前 yaw；不能把两种控制模式混在同一条样本里。

`TrajectorySetpoint` 的消息注释明确：数据采用 NED；位置/速度/加速度单位分别为 m、m/s、m/s²；NaN 表示该状态不受控；setpoint 必须运动学一致且可实现，才能平滑飞行。位置模式下，position 有效；若同时给出非 NaN velocity/acceleration，它们会作为内环前馈，而不是另一个独立控制模式。加速度-only 则是独立路径：position/velocity 均为 NaN，仅 acceleration 有效。

**XY 成对约束：** v1.17.0 `PositionControl::_inputValid()` 检查 x/y 的 position、velocity、acceleration 有效性必须成对；每个轴至少要有一种有效 setpoint。位置 setpoint 有效时，对应位置状态估计也必须有效。因此 position-only 工况应确保 x、y 同时有效，且 PX4 的 local position validity 正常；acceleration-only 工况也需 x/y 成对有效，并满足 Offboard 模式所要求的 velocity estimate。

### 2.2 Offboard heartbeat 与外环更新不是同一件事

- v1.17.0 官方 Offboard 文档要求 heartbeat/setpoint 流大于 2 Hz，并在切入 Offboard 前持续发送至少 1 秒；断流后由 `COM_OF_LOSS_T` 和 `COM_OBL_RC_ACT` 决定退出与 failsafe 行为。
- ROS 2 路径中，heartbeat 由 `OffboardControlMode` 提供；保持位置时 PX4 允许只收到一次 `TrajectorySetpoint`。这意味着 PX4 会继续保持最近的有效参考。
- **对 receding-horizon MPC 的要求不同：** 外环每次优化后仍必须发布新 `TrajectorySetpoint`，按选定 MPC 周期更新；heartbeat 应独立、持续发布。不能把“保持位置只需发一次”误读为 MPC 可以不更新控制输入。

v1.17.0 文档中的加速度-only 模式要求有效 velocity estimate。该要求具有版本语境；本研究必须锁定 v1.17.0 文档/源码，不把 rolling `main` 文档中的估计有效性表格直接套到该版本。

## 3. 源码揭示的真实级联控制链

### 3.1 位置参考并非直接的双积分器输入

v1.17.0 `PositionControl.cpp` 的实现顺序是：

1. `_positionControl()`：位置误差乘位置 P 增益，生成速度参考；再叠加有效的速度前馈，并按水平/垂直速度上限约束。
2. `_velocityControl(dt)`：速度误差进入 PID；积分状态 `_vel_int` 和速度导数反馈共同影响加速度参考；有效加速度字段还会作为前馈；存在 anti-windup。
3. `_accelerationControl()`：把期望加速度转换为机体 z 轴/姿态与推力；执行倾角限制、推力限制及垂直/水平优先级处理。
4. 控制器发布姿态 setpoint，由 PX4 后续姿态/角速度、控制分配与执行器链继续处理。

因此，外部位置参考 (r_p) 到真实 ([p,v]) 的映射是一个**已预稳定的闭环级联系统**，而不是 (\dot p=v,\;\dot v=a_c)，也不能把 `TrajectorySetpoint.position` 当成实际位置，更不能把 acceleration 字段直接当作实际加速度。

### 3.2 隐含动态状态与限幅

源码还确认了下列会影响闭环记忆/残差的因素：

- `PositionControl` 内部保存速度积分状态 `_vel_int`；它会影响后续加速度输出，即使当前 ([p,v]) 与当前参考相同，控制器历史状态不同也可能产生不同输出。
- `MulticopterPositionControl::set_vehicle_states()` 对速度使用 notch/low-pass 滤波，并对速度导数再低通；估计无效时会把相应状态设为 NaN，重新获得有效估计时会重置滤波器。
- 控制周期由 `vehicle_local_position.timestamp_sample` 差值驱动；源码将用于控制更新的 dt 限制在 **2–40 ms**。这不是外部 MPC 的采样周期，也不证明 ROS 2 setpoint 能以相同频率到达。
- 位置/速度控制链有速度上限、倾角上限、推力饱和及 anti-windup；垂直推力优先级会改变水平可用推力。
- 控制输入/状态无效时，控制器会尝试使用最近有效 setpoint（源码中的回退时间窗为 200 ms），仍失败则生成 failsafe setpoint。
- 起飞 ramp、hover-thrust 参数/估计、落地状态与 failsafe 也会改变局部闭环行为；辨识数据必须排除起飞/降落阶段，或将这些模式明确分层建模。

**直接后果：** ([p,v]\in\mathbb R^6) 仍是首个待检验的外环预测状态，但并未因 PX4 采用位置控制链而自动成为完整 Markov 状态。位置 PID 积分和滤波记忆可能需要作为增广状态，或在明确初始化/工作域内由统一有界残差集合覆盖。不能预先武断地把预测模型定为 6、9 或 12 维；模型阶次应由输入—输出辨识、历史依赖检验和残差覆盖决定。

### 3.3 Hover Thrust Estimator 是额外的慢变内部状态

本轮继续检查 X500 airframe 和 v1.17.0 参数定义，发现一个会影响模型阶次的关键默认项：

- X500 airframe `4001_gz_x500` 显式设置 `MPC_THR_HOVER=0.60`；
- 通用参数定义中 `MPC_USE_HTE=1`，即默认启用 Hover Thrust Estimator（HTE）；
- `MPC_THR_HOVER` 在 HTE 开启时是估计器初始化值，不是整个飞行期间固定不变的悬停推力；
- HTE 在 armed/in-air 条件下，结合垂直加速度、姿态、推力 setpoint 与控制分配器未分配推力更新 hover-thrust EKF；有效估计随后通过 `updateHoverThrust()` 写入位置控制器。

因此，HTE 开启时位置—速度闭环除 `[p,v]`、速度积分和滤波记忆外，还包含自适应 hover-thrust estimate。更重要的是，`PositionControl::updateHoverThrust()` 在更新 hover thrust 时会同步修正垂直速度积分器 `_vel_int(2)`，以补偿推力映射变化；HTE 与 z 轴积分记忆是耦合状态，不应只把它当作独立静态参数。v1.17.0 默认 DDS topic 列表没有 `hover_thrust_estimate`，若保留 HTE，需通过 ULog 检查估计轨迹，或显式扩展 DDS 暴露；不能假设外环 ROS 2 节点默认能读取该状态。

**建议采用两阶段辨识，而不是直接把 HTE 混进首轮模型：**

1. **基线辨识配置：** 显式设 `MPC_USE_HTE=0`，并保留 X500 airframe 的 `MPC_THR_HOVER=0.60`，固定悬停推力参数。此配置是用于隔离控制器动态的研究基线变体，不是 X500 的 stock 默认运行配置；必须在实验配置文件和论文中明示。
2. **HTE-on 对照：** 恢复 `MPC_USE_HTE=1`，记录 hover-thrust estimate 与方差，比较相同位置参考轨迹下的响应差异；若其影响不能由统一残差外包，则将 hover thrust estimate 作为有界慢变增广状态，或明确把研究工作域限制在 HTE 未显著变化的阶段。

v1.17.0 相关参数定义还给出：`MPC_XY_P=0.95`、`MPC_Z_P=1.0`；水平速度 PID 为 P/I/D = 1.8/0.4/0.2，垂直为 4.0/2.0/0；水平速度上限 12 m/s，垂直上升/下降上限 3/1.5 m/s，空中最大倾角 45°，推力最小/最大 0.12/1.0。滤波参数默认 `MPC_VEL_LP=0`、`MPC_VEL_NF_FRQ=0`（关闭），`MPC_VELD_LP=5 Hz`（开启）。这些是参数源码默认值；X500 airframe 另有覆盖项，运行时还可能被参数文件覆盖，必须导出实际参数，不能直接把表中值当作实验值。

### 3.4 DDS 默认观测/命令 topic 的边界

v1.17.0 `dds_topics.yaml` 默认包含：

- 输入：`/fmu/in/offboard_control_mode`、`/fmu/in/trajectory_setpoint`。
- 输出：`/fmu/out/vehicle_local_position`（DDS rate limit 配置为 50 Hz）、`vehicle_attitude`、`vehicle_control_mode`、`vehicle_status`、`vehicle_odometry`。

该版本默认 DDS 列表**没有** `vehicle_local_position_setpoint` 输出。因此若要直接观测位置控制器内部修正后的速度/加速度 setpoint，首选检查 PX4 ULog 中是否记录相应 uORB topic；若需 ROS 2 实时订阅，则须明确修改 DDS topic 配置并重编固件，不能假设默认已经暴露。所有频率应实测，不应把 DDS rate limit 当成实际发布频率。

### 3.5 Acceleration-only setpoint 可绕过位置/速度 PID 的有效输出路径

v1.17.0 源码支持一个重要的接口对照：

- 当 `TrajectorySetpoint.position` 与 `velocity` 为 NaN、`acceleration` 有效时，`PositionControl::_inputValid()` 接受加速度 setpoint；Offboard 模式层仍要求有效 velocity estimate。
- `PositionControl::update()` 仍调用位置/速度处理函数，但在 velocity setpoint 为 NaN 的情况下，速度误差为 NaN；源码将 NaN 误差置零后再更新积分器，因此该模式不会用速度 PID 生成一个有限的加速度修正项。
- `ControlMath::addIfNotNanVector3f()` 不会用 NaN 的速度环输出覆盖有限的外部 acceleration setpoint；随后 `_accelerationControl()` 将该加速度请求转换为姿态/推力，并继续受 HTE、倾角/推力限制和姿态/角速度内环影响。

因此，**acceleration-only 在有效控制输出路径上绕过位置 P 和速度 PID 积分/导数反馈**，可能比 position-only 更容易建立低阶平移预测模型；但它不是“实际加速度被精确施加”，跟踪残差仍包含姿态/角速度瞬态、推力映射、重力补偿、风扰和饱和。v1.17.0 Offboard 文档仍要求 acceleration-only 有效 velocity estimate，不能误写成不需要速度估计。

该路径没有替外环自动解决加速度平滑、jerk 限制和推力/倾角约束映射。Andriën 等的加速度参考级联控制使用动态扩展使期望加速度两次可微；PX4 的 setpoint 语义与该论文内环并不相同，但提示本课题应在外环显式约束加速度变化率/平滑性，并在 SITL 检查加速度到姿态/推力的跟踪误差。

**当前接口选择应做同条件 A/B，而不是先验冻结：**

| 对照 | 优点 | 主要代价/风险 |
|---|---|---|
| position-only | 与 Santos & Lagoa (2022) 的位置命令型 6 状态 Tube RMPC 更接近；航点/位置约束自然 | PX4 位置 P—速度 PID 含积分和滤波记忆，隐藏闭环状态较多 |
| acceleration-only | 绕过位置/速度 PID 的有效输出路径；在 HTE-off 时更接近平移加速度输入 | 需要 velocity estimate；姿态/推力映射与饱和仍在；外环需保证加速度平滑并处理推力/倾角约束 |
| velocity-only | 直接给速度参考 | 仍使用速度 PID 积分/滤波，未消除主要内部记忆；暂作低优先级对照 |

## 4. 外环 SMF 的量测通道必须与 PX4 内环估计器分开定义

PX4 位置控制器使用自己的 `vehicle_local_position` 状态估计维持内环。研究中的“间歇/异步位置测量”首先应定义为**外环 SMF/MPC 可获得的测量通道**，不能默认意味着 PX4 内部 EKF 也同时失去位置状态。

建议第一阶段采用清晰的双通道合同：

- **内环通道：** PX4 EKF 继续以其正常高频传感器/状态估计运行，维持姿态和位置控制器。
- **外环测量通道：** SMF 只接收独立定义的带噪位置观测，并由研究中的丢包/异步自动机决定何时到达。SITL 初期可从 Gazebo 真值生成独立合成位置观测 (y_k^p=p_k^{true}+v_k)，再施加有界噪声和丢包；这只是可控仿真测量模型，不得称为真实传感器实测。
- 若改用 PX4 `vehicle_local_position` 作为外环观测并在 ROS 2 链路中丢包，丢包只作用于外环副本，PX4 内部控制器仍使用其本地高频估计；此时观测误差是 EKF 输出误差，不是原始 GNSS/VIO 噪声。
- 不得把 PX4 EKF 输出与其已经融合的同源 IMU/GNSS/VIO 数据作为独立观测重复相交。若要融合，必须建立交叉相关/信息来源合同。
- Gazebo 真值、PX4 `vehicle_local_position`、外环传感器观测和外环 SMF 后验必须分别记录，不得互相冒充。

这样才能把研究问题严格限定为：**内环稳定运行时，外环只能间歇获得位置测量，SMF/CZ 能否可靠约束位置—速度状态并为 Tube MPC 提供安全初始集？** 若未来研究 PX4 内部估计器也失效，那是另一种更高风险的故障场景，必须另建合同。

## 5. SITL 辨识实验协议（尚未执行）

### 5.1 冻结项

每次实验至少保存：PX4 tag/commit、Gazebo 版本、`px4_msgs` commit、ROS 2/Agent 版本、X500 airframe/autostart、完整参数导出、仿真步长/实时因子、风场设置、Offboard 消息路径、坐标变换、setpoint 发布频率、MPC 外环采样周期及初始 hover/积分器状态。

位置环/速度环关键参数至少包括：`MPC_XY_P`、`MPC_Z_P`、`MPC_XY_VEL_P/I/D_ACC`、`MPC_Z_VEL_P/I/D_ACC`、`MPC_XY_VEL_MAX`、上下行速度限制、`MPC_TILTMAX_AIR`、`MPC_THR_MIN/MAX/HOVER`、`MPC_USE_HTE`、`MPC_VEL_LP`、`MPC_VEL_NF_FRQ/BW`、`MPC_VELD_LP`、hover-thrust estimator 噪声/门限参数，以及 Offboard loss 参数。首轮受控基线建议 `MPC_USE_HTE=0`、`MPC_THR_HOVER=0.60`；随后必须做 HTE-on 对照；此时需检查 `hover_thrust_estimate` 与 `_vel_int(2)` 的耦合，必要时把两者作为联合增广状态或给出联合残差外包。实际值必须从运行实例导出，不能只写“PX4 默认参数”。

### 5.2 分阶段输入激励

1. 稳定悬停与零参考变化：估计基线噪声、漂移、时间同步误差。
2. **position-only arm：** 位置参考逐轴小阶跃与斜坡/三角波/低幅多频激励；N/E/D 三轴分别正负方向测试，先选不会触发限速/限倾角/推力饱和的小幅值；position 有效，velocity/acceleration NaN。
3. **acceleration-only arm：** position/velocity NaN，发送有界、连续平滑的加速度斜坡/多频激励；同时约束加速度幅值和变化率，避免用不连续加速度阶跃把姿态瞬态误判为正常工作域响应。
4. 对两种 arm 使用相同外环更新率（例如 5、10、20 Hz）和相同运行 envelope，记录实际应用/保持行为；Offboard heartbeat 单独持续发布。
5. 重复相同轨迹，但改变此前的运动/参考历史与悬停时间，检查 position-only 的积分/滤波记忆是否造成相同 `[p,v,r_p]` 下不同的后续响应；对 acceleration-only 检查姿态/推力动态及加速度输入历史是否造成同类残差。
6. 分别测试远离饱和的线性工作域与接近速度/倾角/推力限制的边界工况；不可把饱和数据与未饱和 LTI 模型混为一个未经分层的残差集。
7. 再加入受控风扰与外环测量丢包；先确认闭环辨识，再研究估计器与 Tube。

### 5.3 记录信号

ROS 2 外部日志：实际发送的 `OffboardControlMode`、`TrajectorySetpoint`（含时间戳、NED 值、NaN mask）、`vehicle_local_position`、`vehicle_attitude`、`vehicle_control_mode`、`vehicle_status`、`vehicle_odometry`，以及独立外环测量/丢包事件/SMF 输出。

PX4 ULog：检查并保存 `vehicle_local_position`、`vehicle_local_position_setpoint`、`vehicle_attitude_setpoint`、角速度/执行器输出、failsafe、land/takeoff 状态等内部 topic（以实际日志 topic 清单为准）。用 PX4 时间戳和 `timestamp_sample` 对齐外部 ROS 2 命令；不能仅按两台电脑的墙钟时间相减得到控制延迟。

### 5.4 模型辨识与准入判据

- 分别拟合 position-only 的位置参考模型与 acceleration-only 的加速度参考模型；两者均以平移输出为目标，输入延迟、零阶保持、采样时间和坐标系必须写入合同。
  [
  x_{k+1}=A_{cl}x_k+B_{cl}r_{p,k}+E_{cl}w_k,quad x_k=[p_k^T,v_k^T]^T
  ]
  position-only 可用 `x_{k+1}=A_p x_k+B_p r_{p,k}+E_p w_k`；acceleration-only 可用 `x_{k+1}=A_a x_k+B_a a_{c,k}+E_a w_k`。两式均为待辨识结构，不是已知 PX4 方程。若对加速度命令增加外部平滑滤波器，其已知滤波状态应显式增广进预测模型。
- 训练与验证轨迹必须分开；至少做一步预测、多步自由运行预测、跨初始历史预测和跨激励幅值验证。
- 报告最大/分位残差、延迟、上升时间、超调、稳态误差、轴间耦合、饱和占比和计算周期；不能只报告 RMSE。
- 如果残差明显依赖先前参考、积分器历史、饱和或飞行模式，6 状态模型不准入：优先增广可识别的闭环滞后/积分状态，或收窄并明确工作域；必要时才把姿态/角速度加入外环预测。
- 有限 SITL 样本的最大残差只是经验观察，不是全工作域的数学上界。确定性 Tube 扰动集还需有物理/参数依据的外包与独立验证；未做到前不得宣称硬安全。

## 6. 与论文证据的关系

Santos & Lagoa (2022), *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, ISA Transactions 128:123–135, DOI [10.1016/j.isatra.2021.12.002](https://doi.org/10.1016/j.isatra.2021.12.002)，明确采用 supervisory outer guidance loop，并假设下层稳定姿态/位置控制已存在；外环使用考虑下层闭环与平移/旋转时间尺度分离的降阶离散平移动力学，加入有界扰动和测量噪声，再设计 dual-mode Tube RMPC。该论文为本课题“成熟内环之上的外环 Tube MPC”提供直接同行评审先例。

迁移限制：论文中的内环控制律和时间尺度分离假设不是 PX4 v1.17.0 的黑盒闭环模型；论文证明不能直接覆盖 PX4 的 PID 积分/滤波/饱和、ROS 2 延迟、异步位置丢包或本课题的传感器相关性。必须先完成本文件的源码合同与 SITL 辨识。

## 7. 本轮结论与下一唯一问题

**暂定仿真基线：** PX4-Autopilot v1.17.0 + Gazebo Harmonic X500 SITL + ROS 2 Humble/uXRCE-DDS + `px4_msgs release/1.17`；接口选择不预先冻结。先在 HTE-off、`MPC_THR_HOVER=0.60` 的同一受控配置下比较 position-only 与 acceleration-only，再做 HTE-on 对照，并检验其对垂直速度积分器的联动修正。

**下一唯一研究问题：** 在同一 PX4 v1.17.0、X500、HTE-off 和物理 envelope 下，position-only 与 acceleration-only 哪一种接口能用更低/更可观测的外环预测阶次，对 `[p,v]` 闭环响应给出更紧且可复现的残差外包？position-only 要检验速度 PID 积分/滤波记忆；acceleration-only 要检验加速度到姿态/推力的跟踪、平滑性和饱和。选定接口后，再做 HTE-on 对照，决定是否需联合增广 hover-thrust estimate 与垂直积分状态。

在回答该问题之前，不启动 Tube MPC 终端集合综合，不声称控制闭环已实现，也不把历史平面直接控制结果迁移为当前安全保证。

## 8. 可复核的官方源码与文档

以下均固定到 PX4-Autopilot v1.17.0 tag（解引用 commit：`d6f12ad1c4f70ad3230afd7d86e971421e02fef4`），避免滚动 main 的语义漂移：

- [v1.17.0 Stable release](https://github.com/PX4/PX4-Autopilot/releases/tag/v1.17.0)
- [Offboard mode 文档](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/docs/en/flight_modes/offboard.md)
- [TrajectorySetpoint 消息定义](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/msg/versioned/TrajectorySetpoint.msg)
- [OffboardControlMode 消息定义](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/msg/OffboardControlMode.msg)
- [PositionControl.cpp](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_pos_control/PositionControl/PositionControl.cpp)
- [PositionControl.hpp](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_pos_control/PositionControl/PositionControl.hpp)
- [ControlMath.cpp：NaN 前馈合并语义](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_pos_control/PositionControl/ControlMath.cpp)
- [MulticopterPositionControl.cpp](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_pos_control/MulticopterPositionControl.cpp)
- [X500 airframe defaults](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/ROMFS/px4fmu_common/init.d-posix/airframes/4001_gz_x500)
- [Position controller gain defaults](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_pos_control/multicopter_position_control_gain_params.c)
- [Position controller limits/defaults](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_pos_control/multicopter_position_control_limits_params.c)
- [Hover-thrust estimator](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/mc_hover_thrust_estimator/MulticopterHoverThrustEstimator.cpp)
- [uXRCE-DDS topic 配置](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/src/modules/uxrce_dds_client/dds_topics.yaml)
- [v1.17.0 Gazebo SITL 指南](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/docs/en/sim_gazebo_gz/index.md)
- [v1.17.0 ROS 2 用户指南](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/docs/en/ros2/user_guide.md)
- [px4_msgs release/1.17 分支](https://github.com/PX4/px4_msgs/tree/release/1.17)
