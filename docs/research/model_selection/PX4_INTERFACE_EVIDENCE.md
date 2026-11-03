# PX4 Offboard 外环接口与闭环模型证据

> 状态：接口语义已由官方文档核验；具体固件版本、闭环动态、跟踪残差界均未冻结。本文整合 PR #188、#186、#190 的重复审计，不替代原始研究记录，也不宣称已完成 SITL/HIL 辨识。

## 1. 研究边界

当前仿真对象采用完整四旋翼六自由度刚体物理模型，包含位置、速度、姿态和角速度；成熟 PX4 飞控负责姿态/角速度稳定、控制分配、执行器限幅及电机控制。外环 MPC 只发出位置、速度或加速度等高层参考。

必须区分三种对象：

1. **物理仿真 plant（12 状态）**：\(x_{phys}=[p^T,v^T,\eta^T,\omega^T]^T\)，其中 \(p,v\in\mathbb R^3\)，\(\eta\) 为姿态参数化，\(\omega\) 为角速度。它是 SITL/高保真仿真中的真实动力学对象。
2. **外环预测状态**：首个候选为 \(x_{out}=[p^T,v^T]^T\in\mathbb R^6\)。只有当姿态/角速度内环效应、时延、饱和和模型误差可被有依据的残差集合外包时，才允许采用这个降阶闭环预测模型。
3. **外环优化输入**：位置参考 \(r_p\)、速度参考 \(r_v\) 或加速度参考 \(r_a\) 三选一（可按已验证接口包含前馈项）。它们不是电机推力、wrench 或实际加速度。若 6 状态预测模型无法覆盖约束相关的姿态瞬态，应增广预测状态或采用可验证的更高阶闭环模型，而不是让外环直接接管电机。

12 个物理状态不意味着外环 MPC 必须优化 4 个电机输入；反过来，6 状态外环预测也不意味着仿真只运行简化 6 状态 plant。

## 2. PX4 ROS 2 Offboard 接口语义

主要官方来源（滚动文档，检查日期 2026-11-03）：

- [PX4 Offboard mode](https://docs.px4.io/main/en/flight_modes/offboard)
- [PX4 TrajectorySetpoint message](https://docs.px4.io/main/en/msg_docs/TrajectorySetpoint)
- [PX4 上游 Offboard 文档](https://github.com/PX4/PX4-Autopilot/blob/main/docs/en/flight_modes/offboard.md)

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

**边界：** 官方文档只证明字段语义与接口能力，不证明位置/速度/加速度命令能被零延迟、无饱和、无偏差地跟踪；也不提供本研究所需的确定性闭环误差界。

## 3. 三类接口的正确预测模型

### A. 位置参考：首要辨识候选

外环状态候选 \(x_{out,k}=[p_k^T,v_k^T]^T\)，输入为位置参考 \(r_{p,k}\)。应通过锁定 PX4 固件、参数、机体、仿真步长和 Offboard 消息路径后的 SITL/HIL 数据辨识：

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
- 飞控 EKF 输出可能已经融合 IMU、GNSS、VIO 等信息。未建立信息相关性合同前，不得把 EKF 输出和同源原始 IMU 当作独立观测重复相交。
- SMF/CZ 当前后验集合与未来 Tube 误差集合不同；必须证明真实状态在后验内，并证明后验到 Tube 初始误差集的包含关系。
- Tube 扰动需覆盖风、闭环跟踪误差、通信/计算延迟、限幅/饱和、控制分配残差及模型失配。若无法得到确定性有界残差，相关硬安全结论必须降级，不得用概率指标替代。

## 5. 模型冻结 Gate

1. 锁定 PX4 版本/commit、参数集、机型、仿真器版本、ROS 2 或 MAVLink 消息路径、NED/ENU 约定。
2. 核验 `OffboardControlMode`、`TrajectorySetpoint` 有效字段、更新率、超时、failsafe、状态估计有效性及限幅。
3. 设计 position/velocity/acceleration 分别独立的阶跃与轨迹辨识工况；记录请求 setpoint、实际位置/速度/姿态/角速度、饱和标志、时间戳与延迟。
4. 在声明的工作域内拟合 \(A_{cl},B_{cl}\)，验证残差集合对全部采样点和独立验证工况的覆盖；不能仅报告均方误差。
5. 若 6 状态平移预测无法覆盖姿态瞬态和约束耦合，则增广预测状态；12 状态物理仿真 plant 保持不变。
6. 冻结传感器噪声、丢包自动机、相关性和输入可实现性后，才进入 SMF/CZ 与 Tube MPC 设计。

## 6. 来源与整合关系

- PR [#188](https://github.com/zhouxingxing1279/AcademicReaserch/pull/188)：Offboard setpoint 字段、NaN mask、NED 与控制层级。
- PR [#186](https://github.com/zhouxingxing1279/AcademicReaserch/pull/186)：同一接口的跨论文迁移边界与 SMF/Tube 影响；与 #188 重复部分已在本文合并，不再作为两个独立接口决策。
- PR [#190](https://github.com/zhouxingxing1279/AcademicReaserch/pull/190)：位置/速度/加速度闭环模型迁移合同、辨识与残差界要求。
- 本文是对上述审计的规范化摘要；原 PR 分支与其原始研究记录未被修改或关闭。相关 CI 尚未提供可验证的 check-run，本文也不声称完成 SITL/HIL。
