# 背景第15轮：Crazyflie实飞NMPC的13坐标模型与执行器接口审计（2026-11-02 UTC）

## 1. 远端仓库与任务边界

本轮开始读取远端 main SHA 4971aa0de0a3b909793d90deec82ab008c4348a1；读取 CURRENT_CHECKPOINT、统一 PAPER_READING_LOG、MODEL_SELECTION_EVIDENCE、背景第14轮、Run262日志、planar_baseline.json、01_model_and_bounds.md，确认主任务 Gate A 仍 blocked。Run260仅固定历史15拍有限安全，Run261排除固定零力矩无限重复，Run262证明冻结四状态Euler模型的三拍力矩到横向速度响应必要下界；不把这些结论扩展为六状态/实飞安全。本背景轮不修改主任务控制器、测试、检查点或配置。

## 2. 本轮直接相关四旋翼MPC论文（公开原文§I–VI已读）

**Barbara Barros Carlos; Tommaso Sartor; Andrea Zanelli; Gianluca Frison; Wolfram Burgard; Moritz Diehl; Giuseppe Oriolo (2020)**, *An Efficient Real-Time NMPC for Quadrotor Position Control under Communication Time-Delay*, **16th International Conference on Control, Automation, Robotics and Vision (ICARCV 2020)**, IEEE, pp. 982–989. DOI: https://doi.org/10.1109/ICARCV50220.2020.9305513 ; 公开作者预印本 https://arxiv.org/abs/2010.11264 ; 会议书目 https://www.diag.uniroma1.it/en/publication/22132 。

**核验状态与范围**：2026-11-02，公开arXiv HTML全文§I、§II-A–E、§III-A–D、§IV-A–E、§V–VI，重点式(1)–(5)、Table I、Fig.6/7对应正文；不是对IEEE最终排版逐页核验，未复算实验曲线或原始数据。

- **真实控制任务/结构**：Crazyflie 2.1四旋翼三维位置/轨迹跟踪；offboard NMPC配合onboard姿态/角速度PID内环，不是同一NMPC直接闭合电机动力学。仿真比较LQR与NMPC，实飞有平滑阶跃和螺旋轨迹。
- **模型维数与自由度**：§II-A定义 ξ=(p,q,v_b,ω)，p∈R³惯性位置、q=(q_w,q_x,q_y,q_z)单位四元数4坐标、v_b∈R³机体系线速度、ω∈R³角速度，合计**13坐标但仅6个刚体自由度**（四元数单位范数约束）。§III-A的**12状态**是悬停线性化LQR为了去掉冗余四元数标量而投影的模型；**不能把LQR的12状态写成论文NMPC状态**。连续非线性牛顿–欧拉模型包含坐标旋转、重力、角速率耦合、惯量。
- **优化输入与物理执行器**：§II-A的优化输入为四个螺旋桨转速 Ω₁…Ω₄，假设转速可瞬时改变；§III-C每个优化输入0–22 krpm，推力/力矩经转速平方映射。§IV-C/D实机并不直接执行四转速最优输入：实际命令为期望滚转、俯仰、偏航角速度与公共PWM，且由onboard PID跟踪；论文明确指出此接口与NMPC内部模型不一致，PID会使反馈策略失真。没有可直接移植的四转速→实际执行器精确硬安全证明。
- **测量/估计**：§IV-A/B十台动捕相机提供100 Hz三维位置，机载IMU/日志重构Euler角及角速度，位置经二阶离散Butterworth滤波估计线速度；不是全状态直接测得。§II-B采用固定RTT预测补偿，实验估计RTT≈60 ms；**通信延迟不是测量包丢失**。没有有界噪声条带、成功/失测自动机、状态SMF/CZ后验或参数SMF。
- **MPC实现/约束**：§II-C式(2)为多重打靶、非线性模型、阶段及终端二次跟踪代价、显式四电机转速上下界；未在式(2)看到硬状态集合、终端受控不变集合或鲁棒tube。§II-D/E使用acados、SQP实时迭代RTI、Gauss–Newton、HPIPM、BLASFEO与partial condensing，ERK4离散。§III-B测试N=10/20/30/40/50，选N=50，采样τ_s=15 ms，故名义预测窗口50×0.015=0.75 s。文中没有针对有界失测的输出反馈递归可行性证明。
- **实验与计算证据**：§IV 真实Crazyflie 2.1、ROS/C++ offboard、动捕，66.67 Hz运行；§V在Intel Core i5-8250U Ubuntu测得平均优化耗时7.4 ms、**观察到最大22.1 ms**（起飞阶段），高于15 ms采样周期，也高于本仓库20 ms目标；这不是最坏执行时间WCET证书。§III比较LQR/NMPC、不同N及延迟，§IV-E实飞平滑阶跃和螺旋参考。实飞展示轨迹跟踪可用性，不是全扰动硬约束、终端不变性或SMF包含证明。
- **复现与局限**：§IV-B给出crazyflie_nmpc ROS代码 https://github.com/bb-carlos/crazyflie_nmpc （本轮未独立clone/运行，代码可用性待核）；原文使用的质量/惯量、旋翼系数见Table I。NMPC假设瞬时转速、实际经PWM/PID接口、固定RTT、没有系统性有界过程噪声和测量丢包安全分析。不要把其0–22 krpm直接等同仓库T∈[4.905,14.715]N、τ∈[-0.08,0.08]Nm。

## 3. 对仓库模型选型的新增证据

**本轮独特证据：** 同一篇四旋翼实飞论文的NMPC使用13个四元数坐标、LQR对照用12状态，实际执行器又通过姿态/速率PID间接实现优化命令。因此“12状态已实飞”或“优化输入硬界即物理执行器硬界”均不成立。四旋翼论文中的**优化状态、物理自由度、估计输出、固件实际控制接口**必须分别列出；对本课题的六状态平面(T,τ)也是如此。

- **6状态平面条件性首选不变**：其状态(p_x,p_z,v_x,v_z,φ,ω)、真实输入(T,τ)直接表达垂向耦合和姿态力矩，较13坐标NMPC更适合先做集合估计/终端可行性证明；但不能声称本仓库6状态比该文更有实验验证，且须审查T/τ到真实四电机及内环误差映射。
- **4状态固定T理论基线不变**：非零φ时a_z=g(cosφ−1)，不能作为整机高度/轨迹安全模型；Run262力矩→速度三拍延迟不可用虚拟即时横向加速度替代。
- **2状态姿态备选**：仅证明姿态闭环，不能外推位置安全。
- **10/12/13坐标**：维数不是优先级；13坐标含四元数冗余，12状态LQR只是投影，且该论文未解决丢包SMF/硬安全。暂不升级。
- **分层/级联**：论文实飞直接显示内环与优化模型不一致；任何以外环虚拟输入做SMF+MPC的选题，必须单独外包内环误差、饱和、通信延迟与实际执行器动态。

**SMF/CZ研究缺口定位**：这篇论文已有实飞NMPC、执行器限幅与固定RTT预测；本课题不能将这些视为创新。仍可探索**有噪间歇位置的状态集合估计与MPC可行/安全接口**，但须对比成熟名义NMPC与Hassaan等周期tube输出反馈基线，证明新信息后验在相同硬约束、可计算预算下带来收益。没有证明“首创”。

## 4. 静态核验与未验证事项

独立算术/逻辑核对：3+4+3+3=13；13坐标−1四元数范数约束=12局部独立状态坐标；50×0.015=0.75 s；60/15=4采样间隔；22.1>15且22.1>20。**这些是论文参数的一致性检查，不是代码回归、动力学证明或实飞复现。** 本轮没有新控制器、SMF递推、MPC仿真或CI算法测试；不修改主研究任务。

**可行性**：6状态输出反馈硬安全仍中低，因Run246/260/261/262终端阻塞未解除；**创新性**：仅“实飞NMPC+通信补偿”已非新颖，状态SMF与硬安全终端接口仍有条件空间；**难度**：6状态有界失测+物理约束中高，13坐标全NMPC+CZ+终端证明过高。Gate A blocked。

**下一轮唯一优先论文问题**：全文核验Kamel、Burri、Siegwart (2017) *Linear vs Nonlinear MPC for Trajectory Tracking Applied to Rotary Wing Micro Aerial Vehicles*（arXiv:1611.09240；DOI:10.1016/j.ifacol.2017.08.849）的**LMPC/NMPC各自状态向量、真实控制输入及实飞/仿真计算成本**，与本轮13坐标+PID执行器接口形成直接模型复杂度对照；不要并行开发新控制器。

## 5. GitHub提交状态

本文件与证据矩阵/统一论文总账为背景文档增量；PR/CI/main状态应在实际核验后单独报告，不能在文档中提前宣称合并成功。
