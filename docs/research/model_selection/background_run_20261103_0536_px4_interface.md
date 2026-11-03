# 外环MPC模型选型：PX4 Offboard接口语义审计（2026-11-03）

## 唯一主问题
成熟PX4内环之上的位置/速度/加速度命令，究竟对应怎样的闭环被控对象？Santos–Lagoa位置指令模型和Andriën加速度参考模型能否不改合同直接迁移？

## 仓库基线与边界
本轮读取main上的 `docs/research/CURRENT_CHECKPOINT.md`、`docs/literature/PAPER_READING_LOG.md` 和 `docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md`。GitHub搜索提交返回的最近SHA为 `eb18e857090b0babe531c13c61aea944793af428`，但搜索结果不等于原子性branch HEAD验证；创建分支时使用远端main引用。矩阵旧条目仍将平面六状态 `[p_x,p_z,v_x,v_z,phi,omega]` + `(T,tau)` 标为条件性首选；**该输入是刚体wrench级，不是PX4位置/速度/加速度外环指令**。四状态冻结Euler Run246/260/261/278的安全证据不能迁移到新的闭环位置参考plant。

## 新增一级证据：PX4官方Offboard接口
核验官方当前文档 https://docs.px4.io/main/en/flight_modes/offboard （2026-11-03，文档HTML相关Multicopters、OffboardControlMode、TrajectorySetpoint段落；版本main会漂移，复现应锁定固件tag/commit）：
- ROS2 `TrajectorySetpoint.position` 非NaN：位置设定值生效；非NaN速度、加速度是前馈，不是并行独立优化输入。
- 仅速度非NaN、位置NaN：速度设定值生效；加速度非NaN是前馈。
- 仅加速度非NaN、位置/速度NaN：加速度设定值生效。
- 三类指令均由 `mc_pos_control` 管理；即使OffboardControlMode标记velocity，只要TrajectorySetpoint.position非NaN，仍会执行位置控制。必须联合审计flag和NaN mask。
- NED坐标，位置m、速度m/s、加速度m/s²；需审计仿真ENU/NED转换、重力及符号。
- OffboardControlMode要求位置模式具备有效位置估计，速度/加速度模式具备有效速度估计；这不等价于本研究SMF观测在GNSS失测时必有可靠真值包含。飞控EKF若已经融合IMU，不能再把同源原始IMU当独立测量。
- `VehicleAttitudeSetpoint`与`VehicleRatesSetpoint`为更低层接口；`VehicleThrustSetpoint`/`VehicleTorqueSetpoint`甚至直接绕过内部控制回路，不能与本任务外环相混淆。
- 官方文档指出部分MAVLink全局加速度接口映射到归一化推力，不能简单将所有加速度接口视为精确物理加速度伺服。

**文档仅证明命令语义，不证明PX4内环跟踪误差、延迟、带宽、饱和或确定性误差界。** 未运行SITL/HIL，未固定PX4固件SHA，也未读到闭环辨识数据。

## 跨论文复核（本轮原文新核验状态）
1. Santos, D. A.; Lagoa, C. M. (2022), *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, ISA Transactions 128, 123–135, DOI https://doi.org/10.1016/j.isatra.2021.12.002 。本轮DOI出版商跳转返回不可访问；**本轮仅既有仓库文献记录及书目信息复核，非全文**。历史记录给出的模型为 `x=[r,rdot]` 六状态，输入位置参考 `r_c`，预稳定位置/姿态内环，Tube RMPC。采样0.3s、N=30等参数须待可访问原文逐页确认。位置指令符合PX4 Offboard语义，但矩阵A/B中的内环增益不可当作PX4已知参数；应辨识离散闭环模型 `x_{k+1}=A_cl x_k+B_cl r_{c,k}+E w_k`，再证实残差界。
2. Andriën, A. R. P.; Lefeber, E.; Antunes, D. J.; Heemels, W. P. M. H. (2024), *Model Predictive Control for Quadcopters With Almost Global Trajectory Tracking Guarantees*, IEEE TAC 69(8):5216–5230, DOI https://doi.org/10.1109/TAC.2023.3349098 。本轮DOI访问受限；**沿用仓库既有正文证据，非本轮全文逐式核验**。外环为加速度参考/指令整形12状态（不是12状态刚体），内环为作者设计的非线性姿态跟踪器。PX4加速度模式在接口层存在，但作者的级联系统稳定性定理不可自动适用于PX4。
3. Xue, R.; Dai, L.; Wang, P.; Sun, Z.; Xia, Y. (2024), *Output feedback stochastic MPC for tracking control of quadrotors with disturbances*, IET Control Theory & Applications 18(5):566–580, DOI https://doi.org/10.1049/cth2.12588 。本轮重读仓库既有正文分节摘录（§2–5），**本轮未重新下载全文**。外环平移6状态+3维风增广，虚拟加速度输入，姿态内环ADRC/ESO；每拍带噪位置和速度观测，概率约束，不能证明本课题间歇位置测量的确定性硬安全。

**本轮实际外部原文新增核验：0篇全文、0篇论文正文分节、2篇DOI访问受限的书目复核、1篇既有正文摘录复核；另新增PX4官方接口文档正文核验1份。** 不把既有阅读冒充本轮阅读全文，也不向唯一论文总账新增“已读”。

## 迁移合同与模型选择
候选A（条件性首选）：PX4位置模式，`x=[p;v]∈R^6`、`u=p_ref∈R^3`；辨识并验证闭环 `A_cl,B_cl`，将延迟用扩展指令缓存状态或有界残差处理；约束包含参考位置、变化率及可验证的实际速度/加速度包络。若存在严重非线性/时变饱和，LTI+固定W不可靠，应采用LPV/LTV或分段可验证外包。
候选B：PX4加速度模式，`x=[p;v]`、`u=a_ref`，双积分器仅在 `a_actual-a_ref∈W_a` 经验证时成立。考虑倾角/总推力限制、姿态动态、延迟、限幅和指令变化率；如无法界定则增广加速度跟踪动态，或不选该接口。
候选C：速度模式，`u=v_ref`，不能将其直接代入加速度双积分器；需辨识速度参考到实际速度的一阶/更高阶闭环模型。
三者均需对PX4 Offboard setpoint有效性、状态估计有效性和失联failsafe建立安全合同；SITL不等于确定性证明。

## SMF/CZ连接
预测 `X_{k+1|k}=A_cl X_{k|k}⊕B_cl U_k⊕E W`；有位置量测时与有界条带相交，丢包时仅传播。若飞控EKF持续给出状态估计，需要证明其误差集合或使用独立原始观测，不可把EKF输出视为无误差真值。将后验集合用于Tube初始化，需要证明未来误差管束和终端可行性，而非仅将中心值交给MPC。

## 矩阵决策变化与下一轮唯一问题
**决策变化：** 将旧矩阵“平面六状态(T,tau)条件性首选”明确标注为**旧主任务刚体控制基线，不符合新外环接口首选**；本独立任务首选候选改为**三维六状态[p,v] + PX4位置参考**，加速度参考为备选，速度参考待辨识。当前仅接口文档证明可调用，不是正式模型锁定；无CI/闭环/递归安全证明。
**唯一下一步：** 获取Santos–Lagoa(2022)可核验的完整正文并逐式审计闭环位置控制器的状态方程、输入、扰动和终端假设；同时锁定一个PX4固件版本并核验位置模式闭环状态/限幅实现，以确定可复现的A_cl、B_cl和W辨识合同。
