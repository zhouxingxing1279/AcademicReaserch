# 背景第27轮：Cao等(2017)四旋翼分层GPMPC的机会约束与PX4最终驱动接口审计

日期：2026-11-02 UTC。任务边界：只查原始四旋翼MPC论文、源码及模型选型证据；不开发主任务控制器、SMF验证脚本或飞行仿真。研究问题：**已在MPC内部约束的随机状态/虚拟输入，能否支持本项目确定性20ms、逐桨硬约束与失测SMF安全合同？**

## 1. 原始论文与实际阅读证据

Gang Cao; Edmund M.-K. Lai; Fakhrul Alam, *Gaussian Process Model Predictive Control of an Unmanned Quadrotor*, *Journal of Intelligent & Robotic Systems* **88**(1):147–162 (2017), DOI https://doi.org/10.1007/s10846-017-0549-y 。原始作者公开预印本 arXiv:1707.04515v1 https://arxiv.org/pdf/1707.04515 （22页）；机构最终稿目录 https://openrepository.aut.ac.nz/items/abfa201e-c3ce-4b48-927f-160b92af42d6 。2026-11-02 **分节阅读作者v1 pp.3–18（PDF页索引2–17）§2–6，重点§2状态/输入、§3机会约束式(19)–(20)、§4局部QP与Algorithm 1、§5实验设置/时间、§6结论；参考文献未逐条核验，未逐页对照期刊终版，未复现优化/GP训练**。期刊卷页和DOI交叉核验；该论文为**真实四旋翼MPC仿真研究，不是实飞**。

## 2. 模型、输入、量测、优化和结果

- 物理平台为6自由度四旋翼，广义坐标q=(x,y,z,phi,theta,psi)。**控制器分层为两个各6状态子系统**，不是6状态物理平面模型，也不是独立的12自由度：平移状态 x_xi=(x,xdot,y,ydot,z,zdot)，外环虚拟输入 u_xi=(U1,u_x,u_y)，其中 u_x=cos(phi)sin(theta)cos(psi)+sin(phi)sin(psi)，u_y=cos(phi)sin(theta)sin(psi)-sin(phi)cos(psi)；旋转状态 x_eta=(phi,phidot,theta,thetadot,psi,psidot)，内环输入 u_eta=(U2,U3,U4) 为三轴力矩。外环给期望姿态，内环给力矩；论文没有从 (U1,U2,U3,U4) 到四桨RPM/PWM/DSHOT的确定性分配及真实误差外包。
- GP用离散增量x[k+1]-x[k]和状态-输入训练，零均值高斯白噪声；训练/仿真状态来自数值模型，**未报告实际IMU、Vicon、GPS、视觉传感器或位置丢包**；不是状态SMF/CZ。作者§5使用已有NMPC在**数值系统**生成每条轨迹189条训练记录，不能将“empirical observations”误写为真实飞行日志。
- 分层GPMPC以GP预测均值/方差构造期望二次代价、单侧概率状态约束和输入盒；局部线性化成严格凸QP，active-set求解。论文§5比较时H=Np=Nc=1、采样**1Hz**；一般§3 H可为更大值，但数值对照只H=1。**未给出终端鲁棒不变集、逐桨推力速率/饱和、所有丢包路径的递归可行性定理、20ms最坏求解时间**。
- §5两条数值轨迹Elliptical/Lorenz、50次重复，Gaussian white noise（无确定性有界支持）；计算平台3.40GHz Core2 Duo/MATLAB 8.1。189步GPMPC总时间60s与56s，算术平均分别**0.317460s/步、0.296296s/步**；比较非线性GPMPC为220s、272s，约1.164s、1.439s/步。这里是**作者报告总时间除以步数的平均**，不是WCET，不能满足仓库20ms实时目标；“约20%计算时间”是相对同文非线性GPMPC，不是相对20ms预算。
- §5外环Elliptical虚拟输入约束U1∈[0,100]、u_x,u_y∈[-0.2,0.2]；Lorenz的U1∈[-45,0]、u_x,u_y∈[-2,2]。后者数值盒与式(2)由姿态三角函数定义的可实现范围不构成自动物理证书，U1符号也须结合坐标/推力约定核验，**不得把数值盒当逐桨物理推力盒**。文中未报告本仓库1kg机体的桨臂、推力系数、ESC速率或执行误差。

## 3. 新的独立数学审计：v1式(20)不能作为95%机会约束证书

预印本§2.1式(7)定义Sigma为高斯状态**协方差**，§3.2式(19d,e)要求单侧概率≥eta=0.95，但紧接的式(20a,b)写成 mu±2Sigma（不是mu±2sqrt(Sigma)）。PDF印刷页7已逐图核对，不是网页文本丢失根号。对于一维 X~N(mu,sigma²)，正确单侧95%充分条件是 mu+Phi^{-1}(0.95)*sigma≤xmax（及下侧对称），其中Phi^{-1}(0.95)≈1.644853627。

**严格反例（研究者独立构造，非论文实验）**：取mu=0，Sigma=sigma²=0.01，xmax=0.05。预印本式(20b)判定0+2*0.01=0.02≤0.05为可行，但真实 Pr(X≤0.05)=Phi(0.5)≈0.69146246<0.95。并且2Sigma与mu量纲不同。因此**按v1原样解释为协方差时式(20)不是所声称机会约束的充分条件**。此审计只针对作者arXiv v1可见公式，**尚未核对期刊最终版是否勘误**；不据此否定论文全部控制性能或QP求解方法。即便修正为概率约束，也不能替代本仓库对所有有界扰动和失测路径的确定性真值包含。

独立执行环境：Linux Python3，math.erf/sqrt，断言paper_margin=0.02≤0.05、actual_probability<0.95、60/189>0.02、56/189>0.02，全部通过；没有运行论文代码。复核命令：
```bash
python - <<'PY'
from math import erf,sqrt
v=0.01; upper=0.05
p=0.5*(1+erf(upper/sqrt(2*v)))
assert 2*v <= upper and p < .95
assert 60/189 > .02 and 56/189 > .02
print(p, 60/189, 56/189)
PY
```

## 4. 固定PX4源码独立交叉审查（非Cao论文的配套飞控）

固定PX4-Autopilot commit `216039a12bab5a86769128f7be3e5f63dc7b4952`，读取：
- `src/lib/mixer_module/functions/FunctionMotors.hpp` blob `76e2b274f01eb194c3706d75e87b094f6fc6bda4`，函数updateValues：从actuator_motors归一化推力r反解静态模型 r=a*s²+(1-a)*s，之后对不可逆电机映射s∈[0,1]到[-1,1]；负推力请求变NaN。此反解只对**配置的标称静态模型**成立，默认参数并不证明真实ESC/桨的映射误差界。
- `src/lib/mixer_module/motor_params.yaml` blob `aabf8e6cb0407717738ebf339e92541c22f0410f`，`THR_MDL_FAC`默认**0.0**；其定义仅是静态归一化推力—控制信号模型，非硬件辨识证书。
- `src/lib/mixer_module/mixer_module.cpp` blob `086cded5fa2a8d827dba7fb80232a4a76002edf2`，`output_limit_calc_single`把[-1,1]插值至配置的输出最小/最大，`output_limit_calc`处理arming/failsafe/ramp及非有限值；不是牛顿推力实测闭环。
- `src/drivers/dshot/DShot.cpp` blob `33e4b93f4b6f5a2413a558e268d0941e6b11d105`，DShot驱动配置`DSHOT_MIN_THROTTLE/MAX_THROTTLE`，updateOutputs将输出舍入成uint16并送硬件；可选ESC遥测eRPM不等于已验证的f=Kf*RPM²，遥测可用性依硬件与设置。此审查**没有构建PX4、运行SITL、读取真实ESC日志或测量推力**。

因此完整链为：上层wrench→分配器归一化actuator_motors→THR_MDL_FAC静态反解→通道限幅与PWM/DSHOT数字指令→ESC/电机RPM→桨实际推力→G混控。源码能证实**命令处理路径**，不能认证`F(a_k,f_{k-1},theta,ESC)`确定性外包。若要给主任务交付共同可实现`(T,tau)`，必须由**本机体**固定硬件/固件版本、逐桨台架或可靠遥测标定、供电/温度/电池范围、最坏残差和速率界；否则保持“未知”，不能从PX4默认值编造物理硬界。

## 5. 模型矩阵、SMF/CZ创新边界、主任务接口与决策

2状态姿态/高度：仍为低风险内环/高度备选，不能证明整机轨迹安全；4状态固定T：已有有限安全/失测反例，但非零倾角导致垂向漂移；**6状态平面(p_x,p_z,v_x,v_z,phi,omega)+(T,tau)仍为条件性物理首选**，必须同时验证推力-倾角耦合、隐藏速度SMF后验、四桨共同可实现域及终端信息RCI；10/12状态/分层GPMPC：此文支持分层的模型/优化拆分，却没有真实逐桨可实现性、20ms或确定性安全证书；完整6DOF/电机增广继续作外部对照。Run246可生存性反例与Run260/261/274/275终端证据缺口均不被概率GP仿真消除。**Gate A=blocked**。

已有状态集合估计+MPC与四旋翼MPC先例；不能声称首次SMF+MPC。Cao的GP方差/概率约束不是SMF真值包含；可迁移的是双环任务分工、均值/方差与集合语义对照、物理接口审计；不迁移其v1机会约束公式作为硬安全定理。主任务接口建议：冻结真实`THR_MDL_FAC`及其误差、DShot/PWM通道设置、逐桨`f_{k-1}`后验、`f_k`有界响应映射与`G`，输出针对全部同一观测纤维的共同可执行wrench集合和`E_alloc`，由主任务验证，不在背景任务实现。

可行性：分层结构和PX4接口均可复现静态审计；**确定性执行器证书和20ms实时性尚未可行性闭合**。创新性：不能基于概率GPMPC或关键词空白声称首次；核心仍是间歇有噪位置状态SMF/CZ→真实执行器共同域→共享因果Tube MPC→终端信息状态。硕士难度中高，优先避免同时实现GP-MPC与SMF-MPC。

**下一轮唯一优先问题**：找到固定标准单向四旋翼硬件的ESC命令—eRPM—推力原始逐样本数据及采样/校准协议，判断能否在明确操作域内构造可复核的确定性残差与速率外包；若无则把本机体台架辨识列为必要实验，不以文献标称时间常数代替。
