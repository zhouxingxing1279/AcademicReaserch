# 背景第24轮 — Nan(2022) NMPC后置INDI执行器约束审计（2026-11-02 UTC）

## 1. 基准与唯一研究问题

本轮通过GitHub连接读取远端main **c52e172ee4bfdfaf3da79ea221239484bfd79e1a**（compare与main一致）、docs/research/CURRENT_CHECKPOINT.md、docs/literature/PAPER_READING_LOG.md、docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md、第23轮背景日志、主任务Run271日志，并核对当前分支基准。主任务Run271只证实第60拍特定MMS后验双真值成员资格与速度直径下界0.568117025m/s；**没有15拍共享因果终端回返**。本背景任务不修改主任务源码/检查点，不开发并行MPC。

本轮唯一问题：**真实四旋翼MPC直接约束逐桨命令后，再经过INDI/控制分配后置修正，最终执行器约束是否仍然得到证明？** 与上轮Eschmann标称电机辨识/逐桨可靠域问题衔接。

## 2. 原始论文与阅读证据

Fang Nan, Sihao Sun, Philipp Foehn, Davide Scaramuzza (2022), *Nonlinear MPC for Quadrotor Fault-Tolerant Control*, *IEEE Robotics and Automation Letters* 7(2):5047–5054, DOI https://doi.org/10.1109/LRA.2022.3154033；作者接受稿 https://rpg.ifi.uzh.ch/docs/ICRA22_Nan.pdf；arXiv https://arxiv.org/abs/2109.12886 。2026-11-02完整阅读接受稿pp.1–9（§I–V及参考文献）；期刊终版未逐页核对。作者接受稿§III Table I给出200组仿真、最大迭代25.75ms；网络arXiv文本转录在约束/试验次数存在不同呈现，本文优先以接受稿为准。完整书目、模型、量测、求解器与局限记入唯一论文总账，按DOI去重。

## 3. 模型、执行链与严格区分

- 6DOF真实四旋翼；x=(p3,q4,v3,omega3,t1..t4)共17坐标，q为单位四元数，因此不能误称17物理自由度。连续Newton–Euler、四桨混控 [T;tau]=Gt、推力一阶动态 dot t_i=(u_i−t_i)/sigma；u_i是逐桨目标推力命令。故障时单桨命令固定0，偏航目标权重置0；没有小角度悬停线性化，气动失配仍存在。
- NMPC：SQP/RTI，ACADO＋qpOASES，1s预测时域、20节点（50ms预测网格），二次跟踪/输入/终端成本，逐桨u盒。后置INDI用RPM/角速度反馈得到目标力矩tau_d，最终 u_indi=Ghat^+ [Td;tau_d]；这是**改变MPC决策变量后的命令**。单靠0≤u_i≤Tmax并不证明0≤(u_indi)_i≤Tmax；接受稿未给该后处理的投影/鲁棒误差外包定理，不能反推一定违约。
- 量测：Vicon位置/姿态400Hz、IMU/ESC RPM 500Hz、EKF全状态估计；0.75kg、5英寸桨、单桨标称8.5N，Jetson TX2板载150Hz。没有位置success/miss自动机、状态SMF/CZ或逐桨最坏跟踪误差。
- §III Table I在TX2仿真报告平均6.431ms、最大25.75ms，后者故障切换重初始化导致；**大于20ms目标**，但不等于严格WCET。§III接受稿200次随机恢复NMPC200成功、对照85成功；§IV真实单桨失效后悬停/8字轨迹/翻滚恢复。这是实验/仿真证据，非任意扰动硬安全或递归可行证明。

## 4. 独立代数与模型选择增量

对本仓库健康四旋翼虚拟输入 w=(T,tau) 与标准混控 f=G^{-1}w（零滚转/偏航目标），即使 f在静态盒内，若实际执行命令经后置补偿变成 f_cmd=f+delta，必须额外验证对所有允许的补偿/上一拍执行器状态、参数与ESC误差，最终施加命令及实际推力仍满足各桨上下界和变化率限制。此为**本任务的必要接口审计逻辑**，不是Nan论文定理，也没有宣称该论文真实飞行违反约束。

维数核算3+4+3+3+4=17，单位四元数减1个独立自由坐标；预测网格1/20=0.05s；控制更新1/150≈0.00667s；样本最大迭代25.75ms比仓库20ms预算超5.75ms。以上是原文数据的独立算术检查，不是控制器回归。作者接受稿式(1)平移动力学与式(2)推力合成存在质量归一化记号需核验的量纲问题，本轮**不把它直接当成模型错误结论**。

**模型矩阵变化**：增加17坐标电机状态NMPC实飞对照、后置INDI执行命令约束和超时证据；六状态平面仍条件性首选，4状态理论基线和2状态备选不变。主任务Run271的后验下界不能解决执行器接口；本轮也没有改变Run246可生存性反例/Run260/261终端阻塞。Gate A仍blocked。

## 5. SMF/CZ研究空间与未验证事项

已有Bicego/Jacquet/Nan等电机级MPC实飞，Didier等四旋翼参数SMF＋RAMPC实飞；不能宣称“首次四旋翼MPC考虑执行器”或“首次SMF＋MPC”。潜在可迁移接口是：有噪/间歇状态SMF后验 + 电机状态/参数可靠集合 + 最终命令共同可实现集合 + MPC管束/终端约束。**这只是待证明研究问题**，没有实现CZ递推、闭环MPC、严格鲁棒安全或飞行实验。

上轮Eschmann代码/数据初查：读取 https://github.com/arplaboratory/data-driven-system-identification README.MD、download_cfusdlog.sh、load_ulg.py；公开仓库存在logs_crazyflie/logs_large及sysid.ipynb，README给出安装和运行流程，但未能在本轮逐样本读取日志或跑出确定性误差界，故不宣称辨识残差已认证。

## 6. 检查、提交边界与下轮唯一问题

本轮执行：作者接受稿全文和期刊书目核验；DOI/题名在唯一论文总账去重检查；17维/预测网格/超时算术检查；文档白名单、链接与三份Markdown内容检查。**不执行主任务控制算法回归**，因为本轮不修改源码、配置或验证脚本。PR、CI、main状态须以实际连接返回为准，不预填成功。

**唯一下一轮问题**：寻找并核验一篇标准健康单向四旋翼实飞MPC原始论文/作者公开实现，追踪“优化输出→后置控制分配/INDI→ESC实际命令”的饱和与误差处理，判断能否提供对本项目(T,tau)共同可实现集合有证明价值的硬件约束/残差证据。
