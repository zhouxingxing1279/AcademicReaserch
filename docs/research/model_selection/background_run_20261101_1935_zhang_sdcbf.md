# 背景第10轮：采样/量测/执行误差安全CBF论文的物理输入接口审计（2026-11-01 19:35 America/Los_Angeles）

## 基准与分工
读取远端main `ffec517748b8cee6a3d558c06cbce64a0c6f9012`、`docs/research/CURRENT_CHECKPOINT.md`（Run256）、唯一论文总账、`docs/research/run256_research_log.md`、背景第9轮日志、`docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md`和`docs/research/01_model_and_bounds.md`。主任务Run256严格排除了**独立盒SMF**无限期认证未测速度的模板：特定历史S30速度宽2.69364701m/s，任意非空success/miss分支盒速度宽每拍至少增长0.081159575m/s，W71≥6.021189585>6；不是实际后验不可生存证明。主任务唯一优先事项是p-v关联H-rep/CZ第35拍分支比较。本背景任务不重复开发控制器或修改主任务checkpoint。

## 实际论文阅读及出处
Yuhao Zhang, Sequoyah Walters, Xiangru Xu (2022), Control Barrier Function Meets Interval Analysis: Safety-Critical Control with Measurement and Actuation Uncertainties, American Control Conference (ACC 2022), DOI https://doi.org/10.23919/ACC53348.2022.9867681; 作者公开预印本 arXiv:2110.00915v1 https://arxiv.org/pdf/2110.00915 。本轮阅读arXiv公开PDF **pp.1–7**：§II-B/C、§III-A/C（Propositions 1–2，式(9)–(17)）、§IV（Assumptions 1–2、Proposition 3、式(18)–(19)）、§V Examples 1–3与式(20)；第8页参考文献未逐条复核。期刊会议最终稿未逐式对照；已读等级为**预印本正文分节已读**，不是全文终版复核。论文是ACC 2022会议论文，不是四旋翼SMF-MPC论文。

**论文研究问题与方法：** 连续控制仿射系统`xdot=f(x)+g(x)u`，数字采样零阶保持`u(t)=u_k`，在有界状态估计误差、执行器误差下用区间Taylor模型、采样间可达管外包和多项式下界，计算采样CBF裕量`varphi(xhat_k,Delta_k)`；再解有物理输入域`U`的USDCBF-QP。Proposition 1处理相对阶1；Proposition 2处理高相对阶且要求初始高阶屏障辅助量非负；Proposition 3还要求**每拍**`x_k∈B_epsx(xhat_k)`、实际输入`u_real∈u_des+B_epsu`、收紧输入`u_des∈U⊖B_epsu`、每拍安全输入集非空，才能保证前向安全。集合外包及多项式下界必须可靠；论文不是无条件保证QP有解。

**论文实际四旋翼实验模型，切勿混淆维数：** §V Example 3式(20)是`x=(x,y,z,xdot,ydot,zdot)∈R6`的**三维平移双积分器**，输入`u=(xddot,yddot,zddot)`为**三个虚拟加速度**，没有roll/pitch/yaw、角速度、总推力`T`或力矩`tau`的真实执行器动力学。6维状态不是平面6状态`(px,pz,vx,vz,phi,omega)`，更不是六自由度刚体。安全约束仅为`x∈[-0.5,0.5],y∈[-0.5,0.5],z∈[0,0.6]`的位置盒；高阶相对阶2。控制用LQR名义轨迹加USDCBF-QP。论文设状态估计误差2-范数界`eps_x=0.02`、虚拟输入执行误差界`eps_u=0.01`，控制频率50/100Hz，Crazyflie实飞约20s，报告该线性例平均单步0.005s。**没有写出实际T/tau饱和映射、位置丢包自动机、状态SMF/CZ递推、终端信息RCI、MPC求解或20ms最坏耗时证明**；实验轨迹不等于所有不确定性下的实飞验证。§V Example 1的18ms和Example 2的20ms平均耗时也不能冒充最坏耗时。

## 与仓库模型的方程接口（解析/符号核对，不是安全证明）
仓库六状态名义连续模型`xdot=(vx,vz,-T sin(phi)/m,T cos(phi)/m-g,omega,tau/J)`，实际输入`(T,tau)`。对位置上界屏障`h_x=px_max-px,h_z=pz_max-pz`，`L_f h_x=-vx,L_f h_z=-vz`，输入相对阶2处的系数分别为`L_g L_f h_x=(sin(phi)/m,0)`、`L_g L_f h_z=(-cos(phi)/m,0)`。在hover`phi=0`时，横向位置对**T通道的二阶系数为0**，而垂向对T为`-1/m`；力矩`tau`对横向位置在常T、无扰动的名义轨迹中首次出现在四阶导数：`p_x''''=T[ J omega^2 sin(phi)-tau cos(phi)]/(Jm)`。因此不能把论文虚拟三轴加速度的三个独立相对阶2输入直接替换成仓库物理`(T,tau)`并继承QP可行性；还必须考虑相对阶退化、耦合、推力相关`r_z(T)`、饱和、失测和高阶屏障初始条件。该解析式忽略外部残差的可微性/导数，**仅是名义输入通道审计**。

与Run246/背景第7轮：存在合法六状态隐藏`v_z=±3`的候选纤维无共享推力；与背景第8轮：真实hover初始盒固定T=9.81、tau=0有15拍有限安全证书；两者不矛盾。论文每拍固定半径估计误差假设不由本项目间歇位置自动保证，尤其Run256已说明独立盒无法持续给出有限速度证书。将论文的CBF条件作为**待研究的辅助可行性筛选/采样保持余量**是可复用接口，但不是替代主任务信息状态终端前驱的充分方案。

## 模型选型、风险和测试
首选仍为**条件性物理目标：平面6状态、实际双输入T/tau**；4状态Run249–256是当前有限安全SMF+MPC算法基线，2状态姿态是低风险递归保底；10/12状态和分层方案不升级。创新性应限定于有噪间歇位置的状态SMF/CZ相关后验、物理饱和共享因果输入与信息终端可移位安全；**“六状态四旋翼采样安全”“部分观测CBF”“50Hz实时安全”均已有先例，不是新颖性**。可行性：采样CBF给出了物理安全接口但不满足原合同；创新性：联合信息状态可行性仍待证；难度：高（关联后验、推力耦合、终端核、WCET）。

验证：使用SymPy在名义六状态方程上符号求Lie导数，核对横向/垂向位置的`LgLf`和横向位置四阶导数，解析结果与上述一致。没有新六状态仿真、未运行主任务完整CI、未声称硬安全或稳定性证明。此次仅更新专用模型矩阵、唯一阅读总账和独立日志；保留Run256负面结果。

**下一轮唯一优先问题：** 对照Run256的第35拍关联H-rep/CZ结果，判断六状态`(T,tau)`模型能否建立**带位置失测的统一有界状态误差/执行误差合同**，以便将采样间安全裕量用于终端信息前驱；若关联后验仍无法在预算内闭合，建议将六状态限于有限时域物理验证。
