# 背景第30轮：Laguerre分层四旋翼MPC与RPG体角速→SBus执行接口

核验日期：2026-11-03 UTC。任务仅进行原始论文阅读、固定版本源码审计与模型选型，不修改主控制器或验证脚本。开始时远端main `3a29c333a86b431e2f9ebc5311f92a69649f4809`；读取CURRENT_CHECKPOINT、唯一PAPER_READING_LOG、MODEL_SELECTION_EVIDENCE、第29轮背景日志、Run278研究日志、6状态配置及物理模型文件。主任务Run278已证明指定真实MMS观测纤维速度直径下界0.71304449m/s、66拍共享开环安全障碍；不排除观测条件化因果反馈；Gate A=blocked。六状态平面(T,τ)仍是条件性首选。

## 1. 新增真实四旋翼MPC论文：全文分节阅读

**Mapopa Chipofya, Deok Jin Lee, Kil To Chong (2015)**, *Trajectory Tracking and Stabilization of a Quadrotor Using Model Predictive Control of Laguerre Functions*, *Abstract and Applied Analysis* 2015, Article 916864, 11pp，DOI https://doi.org/10.1155/2015/916864 ，开放期刊正文 https://onlinelibrary.wiley.com/doi/10.1155/2015/916864 。实际阅读§1–7，重点§3–4.1、§5.1–5.2、§6及表1–3。阅读等级：**期刊开放全文正文分节已读**；当前HTML数学矩阵未完整渲染，不能声称逐式复核全部公式。

- **动力学/自由度/状态**：6物理自由度四旋翼原始12状态：惯性位置(x,y,z)、机体速度(u,v,w)、姿态Euler角(φ,θ,ψ)、机体角速率(p,q,r)。近悬停小角度线性化并Euler离散，三控制子模型：高度(z,v_z) 2状态；水平(x,y,v_x,v_y) 4状态；姿态(φ,θ,ψ及三角速) 6状态。原始机体速度与线性化后v_x/v_y的坐标关系未在当前HTML逐式确认；不能把状态维数当自由度。采样周期仅符号ΔT，**具体数值未从可读全文确认**。
- **控制任务/输入**：三层MPC分别高度、水平位置、姿态；水平位置控制输出期望(θ,φ)，姿态输出(τφ,τθ,τψ)，高度输出总推力F。论文§3列出旋翼推力/反扭矩与ω²关系，但没有可靠电机动态、逐桨饱和/速率或ESC硬误差界。小角度耦合与垂向推力投影不可直接证明本仓库6状态非零倾角高度安全。
- **量测/估计**：位置/姿态角作为子控制器输出；§5.1一般SS-MPC假设零均值高斯噪声、Kalman状态估计；§5.2 Laguerre方法称每拍状态可用，未明确其隐藏速度在数值仿真中的观测器实现。IMU/GPS/Vicon/视觉、丢包、噪声硬界、SMF/CZ均未报告。
- **MPC实现**：SS-MPC二次目标与一般线性约束QP；Laguerre正交函数对增量输入参数化并滚动施加首项。§6.2 N=5,a=0.8187 对照SS-MPC控制时域N_c=25；不是预测时域N_p的确认值。§6.1 α=1.2，用LQR极限和线性闭环特征值支持仿真稳定性，但§5.2.5措辞为“great chance”；没有给间歇观测/有界扰动硬约束递归可行或终端信息RCI定理。求解器、在线耗时、终端集合、实际逐桨约束：未报告/无法从可读全文确认。
- **证据与复现**：MATLAB仿真m=0.7kg、l=0.275m、Jx=Jy=0.1063、Jz=0.2122kg·m²；3D路径(0,0,0)→(5,5,10)，比较DLQR与SS-MPC，图表展示跟踪；没有实飞、SITL/HIL、20ms最坏计算、硬约束违约统计或公开可复现代码。可复用：分层控制和Laguerre参数压缩；不是可靠SMF+Tube MPC既有完整方案。

## 2. RPG源码固定版本及执行接口

- `rpg_mpc` commit **33263db209105f716e204acc6481834fbd9bc778**：https://github.com/uzh-rpg/rpg_mpc/tree/33263db209105f716e204acc6481834fbd9bc778 。`model/quadrotor_model_thrustrates.cpp`定义10坐标(p3,q4,v3)、4输入(T,ωx,ωy,ωz)，`dot(v_z)=(1-2q_x²-2q_y²)T-g`；此T在模型里是**m/s²质量归一化推力**，尽管代码示例T上下限注释写[N]，不能混淆。模型未含角速动态或直接力矩。
- `src/mpc_controller.cpp` `updateControlCommand`对T和三轴ω分别限幅，发 `ControlMode::BODY_RATES`、`collective_thrust=T` 和 `bodyrates`。这只是外环虚拟命令，非真实逐桨控制。
- `rpg_quadrotor_control` commit **22b55b085546a3322c302a68c2b67108a092a298**：https://github.com/uzh-rpg/rpg_quadrotor_control/tree/22b55b085546a3322c302a68c2b67108a092a298 。`bridges/sbus_bridge/src/sbus_bridge.cpp` `generateSBusMessageFromControlCommand`对BODY_RATES模式把 `collective_thrust * mass_` 送进 `thrust_mapping_.inverseThrustMapping(...,battery_voltage_)`，并将ω/各轴最大速率转换SBus。随后 `limitAllChannelsFeasible`。静态逆二次映射见`thrust_mapping.cpp`，电压补偿可选；没有动态误差包含。
- 默认`bridges/sbus_bridge/parameters/default.yaml`质量**0.865kg**，二次标定系数和电压补偿；`sbus_msg.h`规定通道192–1792；`fc_settings/lumenier_f4_aio_betaflight_rpg.txt`是公开配置实例：`mixer QUADX`、`motor_pwm_protocol=DSHOT300`。只证明配置和SBus信号链，**不等于读取/验证Betaflight固件内部混控实现、ESC实际RPM、推力或速率误差**。
- **单位一致性可核算**：模型悬停T=9.8066m/s²，默认m=0.865kg，`F_N=mT=8.482709N`；把T直接当牛顿再乘质量会造成错误标定。桥接watchdog超时和发送门控不是确定性最坏延迟/推力证书。需要共同可执行域 `(T_N,τ)` 与上一拍实际执行器状态集合，不能直接以SBus限幅替代硬推力/力矩约束。

## 3. 证据矩阵与SMF/CZ迁移判断

2状态姿态仅内环保底；4状态固定推力保留有限数学安全基线；**6状态平面(p_x,p_z,v_x,v_z,φ,ω),(T_N,τ)条件性首选不变**，且必须统一 `T_N=m*c` 和真实施加力矩；10坐标PAMPC是虚拟体角速输入的实飞对照，非本仓库直接力矩权限；12状态/级联可作为工程对照但未提供当前丢包硬安全。Chipofya的KF/LMPC不等于状态SMF/CZ，RPG内环与Betaflight黑箱也不能视为有界执行器扰动合同。主任务Run278的66拍开环障碍不排除未来因果反馈；**Gate A仍blocked**。SMF创新性仍须对照已有集合估计与输出反馈MPC原始论文，不宣称首次。

**主任务接口建议**：在任何分层/虚拟输入方案中明确输出 `c_cmd`(m/s²)、`ω_cmd`(rad/s)、实际总推力 `T_act`(N)、实际力矩 `τ_act`(N·m)、执行残差与采样时序；SMF状态传播只能使用已施加且有可靠外包的物理输入。若需要证明执行误差，目标机体台架同步记录SBus/DSHOT、RPM、推力、供电电压、时间戳、测量误差、温度、输入跃迁及带宽先验；采样率本身不是误差硬界。

## 4. 检查、限制、唯一下一步

检查范围：独立Python数值单位算术`0.865*9.8066=8.482709`；文献DOI/作者/文章编号与开放正文交叉核验；固定版本GitHub源码逐文件静态审计；唯一总账DOI去重、Markdown引用/预期文件检查。**未编译ROS/Betaflight、未运行SITL/台架、未重跑主任务、未新增MPC/SMF算法、未证明终端信息RCI或20ms WCET。**

**下一轮唯一优先问题**：审计与上述配置匹配的Betaflight固件固定版本，检查BODY_RATES SBus→QUADX混控→DSHOT300是否公开足够的同步RPM/实际推力残差界；若没有，写出本机体台架辨识的最小可核验合同。仅做文献/模型论证，不开发主任务控制器。
