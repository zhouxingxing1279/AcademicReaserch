# 背景第21轮：Jacquet等(2020)逐桨NMPC实飞与未知上一拍推力的共同输入域（2026-11-02）

## 1. 远端基准、主任务接口和唯一问题

本轮先读取远端main、CURRENT_CHECKPOINT、PAPER_READING_LOG、MODEL_SELECTION_EVIDENCE、背景第20轮Xu(2023)日志、主任务Run268日志/结果概况。起始main=5465b31bdff08cda24c35c99255c83988011a4dd。主任务Run268仅为11种合法包模式提供测量条件化$(v,\phi,\omega)$可靠仿射条带；Run267的三拍必要守卫通过不等于存在终端反馈；Run246/261负面证据仍有效。Gate A=blocked。背景任务不改主任务控制器、验证源码、结果或检查点。

**唯一问题**：真实四旋翼NMPC如何将逐桨动态限制纳入优化；当上一拍逐桨推力不是点值而是可靠集合时，是否仍存在同一观测纤维可共享的$(T,\tau)$命令？

## 2. 原始论文及实际阅读范围

Martin Jacquet; Gianluca Corsini; Davide Bicego; Antonio Franchi (2020), *Perception-constrained and Motor-level Nonlinear MPC for both Underactuated and Tilted-propeller UAVs*, ICRA 2020 pp.4301–4306, DOI https://doi.org/10.1109/ICRA40945.2020.9197281 。机构开放PDF https://aerial-core.eu/wp-content/uploads/2021/01/Perception-constrained-and-Motor-level-Nonlinear-MPC-for-both-Underactuated-and-Tilted-propeller-UAVs.pdf ，机构书目 https://research.utwente.nl/en/publications/perception-constrained-and-motor-level-nonlinear-mpc-for-both-und/ 。2026-11-02实际阅读全文pp.4301–4306，重点§II式(1)–(9)、§III式(11)–(15)、§IV Fig.3–7及§V；未独立复现或检查其他期刊扩展版。

论文刚体状态$x_b=(p_3,v_3,\eta_3,\omega_3)$共12维，$\eta=(\phi,\theta,\psi)$；n桨力$\gamma$为执行器状态，$u=\dot\gamma$为等效电机力矩控制输入，P个视场余弦附加到优化状态，故标准四旋翼NMPC为$16+P$维，真实物理自由度仍为6。连续非线性动力学通过固定步长Runge–Kutta离散，$G\gamma$表示力/力矩；标准四旋翼$\mathrm{rank}(G)=4$，倾桨六旋翼可达5/6。模型并非平面六状态。作者未在所读正文报告可复现的质量/惯量/桨臂/采样步长/N具体数值。

MPC代价为状态/特征视场输出跟踪加权二次和；约束为逐桨$\underline\gamma\le\gamma\le\bar\gamma$、状态相关的逐桨速率界及$\cos\alpha\le c_{\beta}$，求解MATMPC/RTI/qpOASES。地面Intel i7-8850H笔记本经USB连接；实飞四旋翼求解/控制150–400Hz，但§IV-C明确**实飞使用模拟相机**，不是实飞真实视觉闭环；§IV-B 60Hz模拟相机及特征预测展示滞后信息，未提供可靠丢包状态SMF。实际状态传感器逐项型号、终端代价/集合、最坏求解时间、鲁棒递归可行定理、统计RMSE/违约率、完整复现代码**未报告或无法从所读全文确认**。仿真与实飞是经验性结果，非有界扰动下硬安全证明。

## 3. 研究者独立推导：有误差时共同执行器命令（不是论文定理）

沿用第20轮十字型四桨混控：$T=\sum_i f_i$，$\tau_x=l(f_2-f_4)$，$\tau_y=l(f_3-f_1)$，$\tau_z=c(-f_1+f_2-f_3+f_4)$。要求$\tau_x=\tau_z=0$，则名义命令$f^*=(T/4-\tau_y/(2l),T/4,T/4+\tau_y/(2l),T/4)$。

设上一拍真实桨力未知但属于非空紧集合$F_{k-1}$，坐标投影为$[a_i,b_i]$；本拍真实力$f_{k,i}=f^*_{i}+e_i$，$e_i\in[e_i^-,e_i^+]$，并对上一拍推力和本拍误差采取独立笛卡尔量词。定义离散真实速率合同$-hr_i^-\le f_{k,i}-f_{k-1,i}\le hr_i^+$和真实幅值$f_i^{min}\le f_{k,i}\le f_i^{max}$。对**所有**上一拍推力及误差同一命令有效的充要逐桨条件是
$L_i=\max(f_i^{min}-e_i^-,b_i-hr_i^--e_i^-)$，
$U_i=\min(f_i^{max}-e_i^+,a_i+hr_i^+-e_i^+)$，
$L_i\le f^*_i(T,\tau_y)\le U_i$（i=1,...,4）。
这里同一命令的共同可实现域为4个仿射条带交集；若$L_i>U_i$任意一个，域为空。若实际误差非零，实际wrench=$G(f^*+e)$，因此实际与名义wrench的差为$Ge$；**不能声称名义$(T,\tau)$在所有误差下精确执行**。若误差与上一拍状态相关、旋翼变化率为状态依赖或实际混控含交叉耦合，需重新构造可靠集合，以上区间是当前明示独立模型的精确结论而非普适动力学定理。

**反例**（假设参数，仅说明量词）：h=1/50s，$r^+=r^-=2$N/s，上一拍某桨$f\in[2.4,2.5]$N，当前误差$e\in[-0.01,0.01]$N，幅值[0,4]N。要求$2.47\le f^*\le2.43$N，故不存在同一共同命令；逐个已知$f$却可以分别选择可行命令。此反例并不对应仓库已辨识的ESC参数。

**独立验证**：Linux Python 3、Fraction精确端点全枚举与SymPy符号混控逆解均通过（4桨公式逐项恒等，示例严格分数$L=247/100,U=243/100$）。仅是静态代数/量词检查，不是控制器回归、闭环测试、硬件测量或主任务Run268复现。

## 4. 模型矩阵、SMF/CZ、可行性与创新性

新增论文与Bicego(2020)逐桨变化率NMPC、Xu(2023)后置QP分配对照：逐桨动态约束在优化内已有实飞先例，不能将其作为创新。SMF/CZ可将上一拍桨力可靠集合投影为$[a_i,b_i]$并生成共享命令域，再把$Ge$纳入Tube扰动；但这尚未实现，更未证明Run268位置失测后验与执行器不确定性的联合因果终端闭合。平面六状态仍为**条件性首选**；四状态固定T=mg仅理论基线，二维姿态是低风险备选；完整16+P维NMPC高计算/辨识工作量，不推荐作为首个硕士安全证明对象。

可行性：区间/线性约束接口计算低成本，但未知桨臂、$f_i^{min/max}$、$r_i^\pm$、ESC误差、上一拍桨力可靠集合。创新性：组合词已被多个先例覆盖，待证明的差异是间歇位置SMF/CZ与**共同物理可执行输入**和终端信息集合的因果闭合。研究难度：若加入逐桨动态状态和完整6DOF实时NMPC将明显超出当前可证明范围。Run246/260/261/268既有证据不改变；Gate A=blocked。

**向主任务建议的明确接口（仅建议，不开发控制器）**：输入$G,h,F_{k-1},[f^{min},f^{max}],r^\pm,E_{ESC}$；输出同一观测纤维共享的$\mathcal U_k^{common}=\{(T,\tau_y):L_i\le f_i^*(T,\tau_y)\le U_i\ \forall i\}$及实际wrench误差集合$GE_{ESC}$。主任务须对每个合法第60拍后验与所有未来观测分支验证此域非空、输入选择因果可实现并能返回终端信息集合；不能以本轮静态检查替代递归可行证明。

## 5. 文档检查和下一轮唯一问题

本轮仅更改唯一论文总账、唯一模型矩阵、独立背景日志。检查DOI去重、研究范围、文献URL、公式量词、文件白名单、分支ahead/behind和CI状态；未修改主任务源码/测试/配置/结果/检查点，未运行闭环。**下一轮唯一问题**：取得有实测依据的逐桨推力幅值、变化率及ESC误差界，检验本仓库六状态候选的共同$(T,\tau_y)$域在Run268观测纤维条件下是否非空；缺少参数时不提供数值安全认证。
