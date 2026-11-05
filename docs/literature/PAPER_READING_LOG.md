# 唯一论文阅读总账

## 2026-11-05 · 阶段 2 系统性文献调研

本轮录入 37 项，沿用阶段 1 的 21 个文献身份，扩展 16 项。这里统计主库条目，新增条目中含仓库早已读过的工作。各篇的十一字段、作者、书目版本、原文链接、阅读定位及证据缺口见[逐篇阅读卡](stage2/reading_cards.md)。筛选与引用均可从[综述](stage2/literature_review.md)、[关键对比](stage2/key_comparison.md)、[BibTeX](stage2/references.bib)追溯。

- Meslem（M7）的历史创新校正、区间交与块末 ER 是不同命题。Hassaan（M8/M9/M1）分别提供估计恢复、共同前缀策略、时变管与移位的对照。Brunner（M2）的期刊正文仍待核，窗口设计按机构摘要记录。
- 补入 Bemporad–Garulli（N3）、Le 等（N1）、Köhler 等（N2）。分别定位相容状态的全称约束、zonotope 估计中心反馈和在线误差预算的移位归纳。N2 按 arXiv 作者稿登记。Kögel 的主动通信调度（N13）可作为有额外信息权限的对照。
- 李育东、董久祥、丛一睿（N16）的正式 PDF 印刷页 32 经版面核读。式 (42) 的分块 Kronecker 矩阵与式 (43) 的逐轴交错向量需要置换后使用。图 7 是六维无人机轨迹重构数值比较；未复现作者仿真。[原版](sources/cong_mpc_20261104/线性离散系统的自适应集员滤波方法.pdf)
- M6 署名及会议届次按正式会议程序复核。保留 Crossref 注册原件与导出说明。来源受限或定理未取得者按实际阅读层级记录，统计与数学判据见[验收表](stage2/literature_review.md)。

## 2026-11-05 · 阶段 1 背景与技术路线

项目版本仅取自本地仓库，论文使用本地原文与在线学术来源。[21 项文献的题录、定位与逐项阅读层级](../research/research_background.md)是本阶段的证据索引。该数目统计本轮对照的不同论文，其中包含既有记录。

- **Meslem, Hably, Wang, Raïssi (2024)**，*Set-Valued State Estimator With Sparse and Delayed Measurements for Uncertain Discrete-Time Linear Systems*，IEEE Control Systems Letters 8，904–909。式 (8)–(11) 描述固定稀疏指数及过去时刻的输出，Assumption 1 针对该采样律的可检测性，式 (14)–(15) 区分有校正与仅预测时的误差传播。其区间观测器可作为周期延迟对照。任意乱序、永久丢失与 MPC 移位均需另外给出条件。定向核对会议展示稿及作者期刊记录，按一篇登记。[展示稿](https://css.paperplaza.net/images/temp/CDC/files/2323.pdf#page=1) · [期刊 DOI](https://doi.org/10.1109/LCSYS.2024.3405376)
- **Hassaan, Shen, Yong** 的 IEEE Control Systems Letters 估计器论文在线核对 §II-B、可见事件 Def. 2 与前缀 Def. 6。**同作者 HSCC 2021** 的 Thm. 3.2 式 (26) 明确要求所有允许事件词、噪声与初始误差满足中间及末端界，并施加共同前缀约束。**Hassaan, Pati, Shen, Yong (IFAC 2021)** 的 Assumptions 1–3 与 Thm. 6 则将上述类型的误差管接入 MPC。分别登记三种结果的适用范围。[估计器](https://arxiv.org/pdf/2101.03389) · [HSCC](https://doi.org/10.1145/3447928.3456655) · [IFAC 作者稿](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf)
- **几何与应用核对**涵盖 Scott Prop. 1、Rego §2、Ji §V-B，以及本地 Cong 的最优集员滤波 Thms. 1–2、OIT Thm. 1、Qin 的有限窗 CZ Thm. 1、Li 的平滑 Thm. 1 式 (8)。Brunner 与 Santos–Lagoa 两项的可访问材料支持摘要层判断，具体窗口移位和终端条件分别列入待查项。[论文版本及定位](../research/research_background.md) · [技术路线中的时间戳对照](../research/research_technology_map.md)

## 2026-11-05 — 阶段 0 既有关键引用抽核

见[阶段 0 审查报告 §4](../research/STAGE_0_AUDIT_20261105.md)：Scott Prop. 1、Hassaan Assumptions 1–3 / Thm. 6、Ji 十二状态算例定向复核；Rego、Cong、Brunner 核对摘要、版本或机构题录。保留 DOI 网页不可访问与 PMC 验证页等限制。此条仅记录核验范围，不新增论文计数、不认定全文复现或创新。

## 2026-11-04 — 六维CZ启动共同输入专题定向复核（既有DOI，不新增计数）

本轮围绕[一步共同输入证明](../research/cz_startup_predecessor.md)复读以下原始正文；阅读等级为相关章节精读，未声称本轮三篇全文精读。定理核验卡、量词、输入/状态/噪声、终端条件及迁移限制集中在专题第6节。

- Scott等2016，DOI [10.1016/j.automatica.2016.02.036](https://doi.org/10.1016/j.automatica.2016.02.036)，[作者正式稿](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) pp.128–129：Definition3、Eq.(10)、Propositions1–2、Theorem1。T1；R1支持LP独立重推，R2限定为CZ表示/支持原语。Eq.(10)三角形顶点精确复算通过；原文未给顶点数值表，因此无“原表数值误差”可报。不计为滤波实验R3。
- Rego等2020，DOI [10.1016/j.automatica.2019.108614](https://doi.org/10.1016/j.automatica.2019.108614)，[arXiv1908.09950v3](https://arxiv.org/pdf/1908.09950) PDF pp.3–4、8–9：Property1、Proposition1、§4.4–4.5。复核LP支持/可行代表点与外包方向；所用方法属T1，既有四旋翼估计背景属D2。本轮不复现非线性滤波实验，不提升R3。
- Hassaan等2021，DOI [10.1016/j.ifacol.2021.08.482](https://doi.org/10.1016/j.ifacol.2021.08.482)，[作者稿](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf) PDF pp.4–5：Assumptions1–3、Theorems5–7及移位证明。T1；确认初始整段MPC可行/共同终端等前提独立于首步门，本轮无论文数值复现。

本轮原创算例与论文复现分开：64个有理数实例和8,976个联合顶点验证属于项目独立实验，不冒充上述论文图表。标准支持函数鲁棒对应式不作新颖性声明；延迟CZ、全路径恢复和共同终端仍未闭合。

> 本文件是当前唯一持续追加的论文登记总账，按研究轮次保留书目、阅读范围、模型/输入/观测假设、定理条件和迁移限制。论文证据记录不自动构成当前模型决策或控制器设计指令。
>
> 当前研究架构、模型分层和下一优先问题以 [当前研究检查点](../research/CURRENT_CHECKPOINT.md) 与 [模型选型证据矩阵顶部摘要](../research/model_selection/MODEL_SELECTION_EVIDENCE.md) 为准。历史 Run 日志已移入 [历史归档](../../archive/legacy_planar_direct_control_20261103/ARCHIVE_INDEX.md)，本总账中的链接已指向归档原件；不得将旧 Run 的证明/仿真结果直接迁移为新 PX4 外环合同的保证。

## 背景第30轮新增论文 — Chipofya/Lee/Chong (2015) 三层Laguerre MPC（2026-11-03 UTC；正文分节已读）

- **书目及原始全文**：Mapopa Chipofya, Deok Jin Lee, Kil To Chong, *Trajectory Tracking and Stabilization of a Quadrotor Using Model Predictive Control of Laguerre Functions*, *Abstract and Applied Analysis* **2015**, Article ID **916864**, **11 pages** (2015-02-19), DOI https://doi.org/10.1155/2015/916864 ，出版社开放全文 https://onlinelibrary.wiley.com/doi/10.1155/2015/916864 。**实际阅读**：2026-11-03，开放HTML正文§1–7，重点§3–4.1动力学、§5.1–5.2 MPC/观测器、§6参数和结果、表1–3。**核验状态：全文正文分节已读，但网页数学公式部分未被文本接口完整渲染；矩阵系数/数值采样周期/终端证明未逐式确认，不声称所有公式全读或复现。**
- **控制任务/实际模型**：标准四旋翼6物理自由度，原始刚体12状态为惯性位置(x,y,z)、机体速度(u,v,w)、Euler角(φ,θ,ψ)、机体角速度(p,q,r)；小角度/近悬停线性化后采用三个分层离散Euler子模型：高度2状态(z,v_z)、水平位置4状态(x,y,v_x,v_y)、姿态6状态(φ,θ,ψ及对应角速率)。论文§3原始机体速度与§4线性子模型v_x/v_y记号转换需谨慎，不能不经坐标变换视为同一状态。**状态维数不等于物理自由度。** §4.1只给采样符号ΔT，当前可读正文**未报告可核实的数值采样周期**。
- **输入/执行器**：物理控制抽象为总推力F和三轴力矩(τφ,τθ,τψ)；水平位置MPC输出期望(θ,φ)作为姿态MPC参考，高度MPC输出F，姿态MPC输出三轴力矩。§3有旋翼力/反扭矩与转速平方关系，但优化与验证未显式给出电机RPM状态、ESC动态、逐桨真实饱和/速率、共同可执行混控误差或实际测力。
- **量测/估计**：§4.1各子系统选择位置/姿态角为输出；§5.1 SS-MPC一般模型假设零均值高斯过程/测量噪声并描述Kalman滤波；§5.2 Laguerre推导称采样时状态可获得，**未证明LMPC实际数值仿真如何处理不可测速度**。没有报告IMU/GPS/Vicon/视觉等真实传感器、间歇测量/丢包、带界状态SMF/CZ或真实后验包含。
- **MPC结构/约束/求解**：小角度线性MPC；SS-MPC以二次成本及一般线性约束组成QP，LMPC以Laguerre正交基参数化增量控制轨迹，降低决策变量。§6.2取a=0.8187,N=5，对照SS-MPC控制时域N_c=25（表2）；**N_c=25不是已确认的预测时域N_p**。§6.1稳定性演示取α=1.2，展示闭环特征值，§5.2.5讨论加权LQR极限；作者亦称“great chance”，**不是有噪失测下硬约束/递归可行定理**。在线QP求解器、终端硬集合、最坏计算时间、明确逐桨输入约束：**未报告/无法从可读全文确认**。
- **结果证据**：MATLAB仿真，m=0.7kg,l=0.275m,Jx=Jy=0.1063,Jz=0.2122 kg·m²；3D路径(0,0,0)→(5,5,10)，与SS-MPC及DLQR比较；5 Laguerre参数对照25控制步参数。**无实飞、SITL/HIL、确定性安全保证、真实测力或20ms WCET**；未提供可复现代码/随机种子和硬约束违约率。
- **局限/关联/可复用技术**：低维分层MPC及Laguerre控制参数压缩可作为硕士实时性基线；但虚拟姿态/推力到实际电机的约束传递、间歇位置SMF和终端信息不变性均缺失，不能直接替代本仓库的6状态(T,τ)物理闭合验证。后续应核验是否能在相同硬约束/因果信息条件下保留Laguerre压缩的可行性，不预设新颖性。**待查**：PDF中具体A/B/C矩阵、数值ΔT、预测N_p、实际QP/代码、逐桨控制分配与完整闭环保证。

---
## Run278 — Yan/Cannon/Goulart（2022）间歇观测随机输出反馈MPC复读（2026-11-03；既有DOI去重不增加）

- **书目/版本**：Shuhao Yan, Mark Cannon, Paul J. Goulart, *Stochastic output feedback MPC with intermittent observations*, *Automatica* 141 (2022), 110282；DOI https://doi.org/10.1016/j.automatica.2022.110282；作者arXiv:2009.11071v3 https://arxiv.org/pdf/2009.11071 （2022-03-01），牛津存档 https://ora.ox.ac.uk/objects/uuid%3A65493a65-7eb6-4897-9f30-bc51e091266c 。**此前背景第13轮已登记，按DOI去重，非新增论文。**
- **本轮实际阅读/状态**：2026-11-03重新阅读公开13页PDF pp.2–4 §2–3式(1)–(10)、Assumptions 1–3及pp.11–12 §9的四状态双倒立摆算例；**分节复读**，没有逐式重现全文证明或复现仿真。
- **研究问题/状态/输入**：一般离散线性系统`x+=Ax+Bu+Dw,y=Cx+v,z=gamma*y`，数值案例为**4状态双倒立摆、2输入**，不是四旋翼四状态；真实电机/推力、推力分配和无人机物理约束不适用。
- **量测/估计/不确定性**：全输出按已知成功率的i.i.d. Bernoulli随机丢包，噪声零均值、有限二阶矩，观测器使用点估计/协方差；不是有界噪声真值包含SMF/CZ，且不能保证仓库最多连续2miss的确定性自动机。
- **MPC结构/约束/理论**：§3式(6)将未来控制表示为已接收输出创新的仿射**因果反馈**，固定K/M、在线优化偏置和创新增益；优化为凸随机MPC，约束为折扣期望二阶矩预算，不是每拍状态/输入硬盒。Theorem 7的优化递归可行、Theorem 9的长期平均代价条件，不能改写为本课题所有合法观测路径下的硬安全与终端信息不变性。§9双倒立摆数值仿真`h=0.01s,N=5,lambda=0.6`，与LQG对照，非四旋翼实飞；未报告本课题20ms WCET。
- **关联、可复用技术与限制**：可复用未来量测条件化控制策略的因果参数化与候选策略移位思想；但Run278的`0.713044490909...m/s`速度直径和66拍开环障碍是本仓库**冻结四状态有界扰动数学证书**，不是本文结论。**待查**：能否在所有合法success/miss分支下构造可靠SMF外包和共同因果安全前驱；不能将随机期望约束当作确定性安全证书。详见`docs/research/run278_research_log.md`。

---

## 背景第29轮 — Falanga等(2018)机载视觉感知MPC与软可见性限制（2026-11-02；新增去重）

- **书目/全文/阅读状态**：Davide Falanga; Philipp Foehn; Peng Lu; Davide Scaramuzza, *PAMPC: Perception-Aware Model Predictive Control for Quadrotors*, *2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, pp.5200–5207, DOI https://doi.org/10.1109/IROS.2018.8593739；作者公开接受稿 https://rpg.ifi.uzh.ch/docs/IROS18_Falanga.pdf ，arXiv v2 https://arxiv.org/pdf/1804.04811v2 ，开源 https://github.com/uzh-rpg/rpg_mpc 。2026-11-02阅读8页公开稿正文§I–VII、式(1)–(13)、实验与计算章节；**正文分节全篇已读**，未对照IEEE终版、未逐式审计全部四元数投影导数、未构建源码。
- **问题/状态/物理模型/控制权限**：6物理DOF健康四旋翼的机载视觉定位、圆周、点到点与暗光导航；10个状态坐标`x=(p3,v3,q4)`（单位四元数约束，9独立运动学状态），`dot p=v,dot v=g+R(q)(0,0,c),dot q=0.5 Lambda(omega_B)q`，优化4虚拟输入`u=(c,omega_x,omega_y,omega_z)`，其中`c=sum(f_i)/m`，**不是逐桨推力、三轴力矩或含角速度状态的完整12维刚体模型**；无显式电机RPM、推力分配、动态、实际速率硬界。
- **量测/估计/不确定性**：420g、对角220mm、推重比约2的真实四旋翼；Snapdragon Flight、IMU、下倾45°前视全局快门相机、机载VIO输出状态点估计，兴趣点质心及图像投影速度作为感知目标。**无可靠SMF/CZ状态后验、位置机会丢包自动机、确定性有界视觉误差或延迟证明**；视觉居中/减模糊是**软代价而非硬可见性保证**。
- **MPC结构/约束/实时性**：非线性多重打靶、RK积分、ACADO/qpOASES、SQP每100Hz控制循环一迭代warm-start；预测网格`dt=0.1s`、`th=2s`即20间隔，10ms实际更新周期。二次状态/输入/图像位置及速度成本（含终端**代价**）；`cmin<=c<=cmax,|omega_B|<=omega_max,|v|<=vmax`；**未见终端鲁棒不变集合、所有有噪失测路径硬安全定理或逐桨真实推力约束**。作者报告单迭代平均3.53ms、样本最大<5ms，非WCET。
- **结果/局限/可复用/待查**：实飞圆周1–3m/s、hover-to-hover主动升高、低光环境保持视觉特征；非统计硬违约证明。可复用机载VIO与NMPC并行计算、虚拟输入与实际电机权限分离、视觉软成本和硬安全分离；不直接迁移为本课题间歇位置SMF/CZ/Tube终端RCI。Elokda数据 DOI https://doi.org/10.3929/ethz-b-000490768 本轮ETH页面403/域名不可达，**未下载、未审计字段，不得声称无逐桨数据**。主任务Run277仅排除共享开环模板，Gate A=blocked；6状态平面`(T,tau)`条件性首选不变。详见`docs/research/model_selection/background_run_20261102_2337_falanga_vio_data_access.md`。**待查**：`rpg_mpc`最终混控与ESC执行误差、目标机体同步台架数据、因果终端信息可行性。

---

## 背景第28轮 — Elokda等(2021)真实四旋翼DeePC及8状态输出反馈MPC实飞（2026-11-02；新增去重）

- **书目、作者、全文与阅读状态**：Ezzat Elokda; Jeremy Coulson; Paul N. Beuchat; John Lygeros; Florian Dörfler, *Data-enabled predictive control for quadcopters*, *International Journal of Robust and Nonlinear Control* **31**(18):8916–8936 (2021), DOI https://doi.org/10.1002/rnc.5686；出版社开放全文 https://onlinelibrary.wiley.com/doi/full/10.1002/rnc.5686 ，PMC数学公式全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC9291934/ ，原始数据集 https://doi.org/10.3929/ethz-b-000490768 。**2026-11-02实际阅读公开期刊正文§1–4及Appendix A–C，重点§2.1–2.3式(1)–(8)、§3.1–3.4式(9)–(10)、Fig.6–11、Table 1和附录参数；状态：全文正文与附录分节已读**；未重放作者数据、未实飞、未逐条核验参考文献。
- **控制任务、物理状态与模型**：28g Crazyflie 2.0位置阶跃、8字轨迹；**分层**外层滚动预测优化、厂家IMU角速内环与固定偏航。§2.1连续非线性6DOF**仿真模型12状态** `(p_x,p_y,p_z,v_x,v_y,v_z,γ,β,α,ω_x,ω_y,ω_z)`，输入4个逐桨推力`f_i`；未显式包含电机动态。真实DeePC把电机电流/内环状态视为**未知黑箱状态**，不能误称实飞优化了12状态；§3.4对照模型式输出反馈MPC为悬停线性化**8状态**`(p_3,v_3,γ,β)`，忽略内环角速跟踪延迟。
- **输入与执行器**：真实外环3个**虚拟输入**`(f_tot,ω_ref,x,ω_ref,y)`，不是逐桨推力或平面`(T,τ)`；厂家内环→Crazyflie混控/ESC的最终指令、速率、饱和及最坏误差**未报告/无法从全文确认**。Appendix A虚拟输入盒`f_tot∈[0.1597,0.4791]`N、角速参考`[-π/2,π/2]`rad/s；不能据此证明四桨硬约束。
- **量测、估计与不确定性**：外部运动捕捉25Hz位置`p_3`和横滚/俯仰；DeePC选输出`p=3`或`p=5`，用历史I/O Hankel隐式初始状态识别（不显式Kalman/SMF/CZ）；对照MPC用位置差分估速度。仿真高斯量测噪声，实飞有噪但**没有有界噪声集合、间歇位置丢包、延迟自动机或确定性真值包含**。p=3不表示真实内环不使用IMU。
- **优化、约束、定理与计算**：正则化DeePC`T_d=331,T_ini=6,T_f=25,h=0.04s`，1秒预测；二次跟踪/输入成本、软初值、`λ_g||g-g_r||_2`，OSQP；位置盒`p_x,p_y∈[-4,4]`m、`p_z∈[0.1,4]`m，p=5时姿态角盒`[-π/6,π/6]`。§2.3 Theorem 1是**确定性最小LTI**的轨迹Hankel表征，不证明有噪非线性四旋翼鲁棒递归可行、终端信息不变或硬安全。终端鲁棒集合、逐桨速率、20ms最坏求解时间**未报告/无法从全文确认**。
- **真实实验/证据级别**：p=3与p=5分别28次真实飞行（各14满电+14部分电量），地面Intel i7-8550U/OSQP；Table 1积分平方跟踪误差mean/median/SD分别`75/69/21`与`93/86/23`（不是RMSE）；求解时间mean/median/SD分别`4.14/3.92/1.49ms`与`6.66/5.70/4.78ms`，**不是WCET**；25Hz=40ms周期，不能证明仓库20ms全链路预算。§3.4模型式8状态MPC真实对照，p=3性能较好是实验观察，不是失测状态可观测性定理。无硬约束零违约证书、HIL/SITL或无限安全证明。
- **局限、可复用技术、创新边界**：可复用真实低维虚拟输入输出反馈预测控制架构、位置-only经验基线、OSQP/求解量级与原始数据链接；但无SMF/CZ可靠状态后验、共同执行器可实现域、Tube收紧、终端信息RCI。不能声称首次四旋翼输出反馈预测控制或仅位置量测必然安全。**六状态平面(T,τ)仍条件性首选**；主任务Run246/260/261/276负面证据与Gate A=blocked不变。独立审计QuadQuestions公开单向桨台架CSV前199行典型约10Hz、含PWM/电转速/推力，但不能认证20ms瞬时速率或本仓库机体硬界；见背景第28轮日志。
- **下一轮唯一待查**：核验本论文开放数据包是否实际包含同步逐桨ESC/RPM/推力，若仅外环I/O则明确需要目标机体台架辨识。

---

## 背景第27轮 — Cao/Lai/Alam（2017）四旋翼分层GP-MPC：机会约束与真实执行器边界（2026-11-02；新增去重）

- **书目/链接/版本**：Gang Cao; Edmund M.-K. Lai; Fakhrul Alam, *Gaussian Process Model Predictive Control of an Unmanned Quadrotor*, *Journal of Intelligent & Robotic Systems* **88**(1):147–162 (2017), DOI https://doi.org/10.1007/s10846-017-0549-y；作者预印本 arXiv:1707.04515v1 https://arxiv.org/pdf/1707.04515 ，22页；机构稿 https://openrepository.aut.ac.nz/items/abfa201e-c3ce-4b48-927f-160b92af42d6 。**2026-11-02作者预印本§2–6 pp.3–18分节阅读**（重点§2模型、§3式(19)–(20)、§4 QP、§5仿真/计算），参考文献未逐条核验，**未对照期刊终版、未复现代码**；状态：**部分全文阅读，非仅摘要**。
- **研究问题/物理模型/控制输入**：6DOF四旋翼分层轨迹跟踪；外环6状态`(x,xdot,y,ydot,z,zdot)`、虚拟输入`(U1,ux,uy)`，`ux=cos(phi)sin(theta)cos(psi)+sin(phi)sin(psi)`、`uy=cos(phi)sin(theta)sin(psi)-sin(phi)cos(psi)`；内环6状态`(phi,phidot,theta,thetadot,psi,psidot)`、三轴力矩`(U2,U3,U4)`。两个6状态不是两个物理刚体，也不是本仓库平面6状态。GP从离散状态增量训练；数值系统产生189条训练数据/轨迹，**非真实实飞采样**。未给最终四桨RPM/PWM/DSHOT分配、饱和、速率、ESC动态/误差界。
- **量测/不确定性/SMF**：§5高斯白噪声、仿真状态/输入训练；实际IMU、视觉、Vicon、GPS、气压计、状态观测器、延迟/丢包均**未报告/无法从该预印本确认**。GP均值/协方差是概率预测，不是有界真值包含的状态SMF/CZ；模型和量测不满足仓库位置每5拍机会、最多连续2miss的硬自动机。
- **MPC与约束/求解**：外环、内环各自GP随机MPC，期望二次成本，概率状态约束eta=0.95和虚拟输入盒，局部线性化QP、active-set；比较仿真H=Np=Nc=1、fs=1Hz；无可复核终端代价/集合、全路径递归可行定理、逐桨速率或20ms WCET。**重要原稿公式审计**：v1式(7)Sigma定义为协方差，但式(20)写`mu±2Sigma`声称等价95%机会约束；独立一维反例`X~N(0,0.01), xmax=0.05`使`2Sigma=0.02<=0.05`却`P(X<=0.05)=0.691462<0.95`，因此**该v1公式按字面并非概率保证充分条件**；期刊终版是否已修订**待查**，不得将其移植为本课题硬安全。
- **结果/证据级别/计算**：仅MATLAB 8.1、Core2 Duo 3.40GHz数值仿真，Elliptical/Lorenz轨迹50次；189步GPMPC累计60s/56s，即0.31746s/0.29630s每步算术平均，非最坏耗时；比较非线性GPMPC 220s/272s。作者报告跟踪接近无约束NMPC但更容易加输入约束，**不等于真实逐桨可执行、20ms预算或无限时域安全**。没有实飞、HIL/SITL、SMF/CZ或确定性硬约束违约统计。
- **局限/复用/下一步**：可复用分层模型与虚拟输入权限审计；概率GP与可靠SMF必须分离；PX4独立源码`FunctionMotors.hpp`/`motor_params.yaml`/`mixer_module.cpp`/`DShot.cpp`固定commit `216039a12bab5a86769128f7be3e5f63dc7b4952`显示归一化推力→标称静态反解→PWM/DSHOT数字指令，**不含真实推力硬误差证书**。六状态平面(T,tau)条件性首选不变；4状态有限数学基线，2状态内环保底。**Gate A blocked**；下一步核验标准单向四旋翼逐样本ESC命令/RPM/推力数据。详见`docs/research/model_selection/background_run_20261102_2135_cao_gp_px4_chance.md`。

---

## Run275 — Reis de Souza、Efimov、Raïssi（2022）时滞系统区间观测器＋输出反馈MPC（2026-11-02；新增去重）

- **书目与来源**：Alex Reis de Souza; Denis Efimov; Tarek Raïssi, *Robust output feedback model predictive control of time-delayed systems using interval observers*, *International Journal of Robust and Nonlinear Control* 32(3):1180–1193 (2022), DOI https://doi.org/10.1002/rnc.5874 。作者公开全文 https://www.researchgate.net/publication/355700252_Robust_output_feedback_MPC_of_time-delayed_systems_using_interval_observers ；出版社 https://onlinelibrary.wiley.com/doi/10.1002/rnc.5874 。2021-11-08在线发表、2022卷期。核验/阅读日期2026-11-02。**状态：作者全文分节阅读§2–6（印刷pp.1182–1192），部分数学符号网页提取乱码，未逐式核验全部LMI、未复现仿真；不标记为全公式核验。**
- **研究问题、模型与输入**：离散已知固定时滞线性系统 x[k+1]=A0*x[k]+A1*x[k-h]+B*u[k]+w[k]，y[k]=C*x[k]+v[k]；通用n状态、m输入、p输出。§6数值案例为2状态、1输入、1输出、10拍时滞，状态盒[-9,3]×[-7,4]、输入[-1,1]。不是四旋翼，未包含电机、推力或姿态动力学。
- **量测、估计、不确定性**：Assumption 1要求初始时滞历史及过程/量测噪声已知区间；每拍输出可用。区间观测器IO每拍更新状态上下界，区间预测器IP对未来无输出预测；属于状态集合估计，不是参数辨识。合作性/非负条件与适当坐标变换是重要限制；不含位置成功/丢包混合自动机。
- **MPC结构与约束**：Theorems 1–3离线LMI设计IO/IP及局部反馈；§4式(23)–(24)对区间中心作二次QP，预测上下界满足状态硬约束、输入位于U、终端中心在Xf；Algorithm 1按每拍观测更新→IP重置→QP→执行首控制。Theorem 4在Assumptions 1–3、初始可行、扰动包络嵌套、终端局部控制满足输入约束等条件下给出递归可行、ISS及约束满足；不可直接用于本项目间歇测量非线性模型。
- **结果、局限与复用**：§6 MATLAB 2017a/YALMIP/quadprog，N=20、100次2状态线性时滞仿真；作者报告平均0.0042±0.0021秒/步、最大观察0.1358秒；未复现、无实飞、非20ms WCET。可复用“集合包含→预测硬约束→终端可移位”分工；Run275只新增有噪位置双成功包对隐藏速度的条件化充分界，尚非完整SMF/CZ后验或终端信息RCI。**待查**：全部成功/丢包读数纤维、终端反馈可行性、LMI完整逐式核验、可复现代码。关联docs/research/run275_research_log.md。

---

## 背景第26轮 — Mendez/Whidborne/Chen（2023）LiDAR风预报LMPC与四旋翼逐桨分配链（2026-11-02；新增去重）

- **书目/原始来源**：Arthur P. Mendez; James F. Whidborne; Lejun Chen, *Wind Preview-Based Model Predictive Control of Multi-Rotor UAVs Using LiDAR*, *Sensors* **23**(7):3711 (2023-04-03), DOI https://doi.org/10.3390/s23073711；出版社开放全文镜像 https://pmc.ncbi.nlm.nih.gov/articles/PMC10098597/ ，原文 https://www.mdpi.com/1424-8220/23/7/3711 。2026-11-02**公开期刊HTML全文§1–4及Tables 1–5已读**，重点§2.1–2.4、§3.3–3.5；HTML无稳定纸页码，未逐页核对PDF排版、未复现实验。状态：**全文HTML已读；数学/工程结论未独立复现**。
- **任务/架构/真实模型**：Draganflyer X-Pro标准四旋翼的抗阵风定点/降落位置保持；真实6物理自由度。非线性Newton–Euler＋逐桨气动模型用于仿真，质量2.36kg、惯量diag(0.1676,0.1686,0.2974)kg m²、臂长0.45m（Table 1）；悬停零风数值线性化形成**12状态** `x=(x,y,z,u_b,v_b,w_b,φ,θ,ψ,p,q,r)`，注意前三个速度在**机体系**，不是惯性系。离散LTI `x+=Ad x+Bd u+Bw wind`，采样0.1s。无间歇测量合同、未报告可认证的逐桨电机动态/ESC最坏误差界。
- **MPC输入与执行链**：外环**四虚拟输入** `u=(altitude demand,pitch-angle demand,roll-angle demand,yaw-angle demand)`，不是四个实际电机推力；内环四通道PID输出 `(U1 collective,U2 pitch,U3 roll,U4 yaw)`，§2.2式中的逐桨转速命令 `Ω=(U1+U2+U3+U4,U1+U2−U3−U4,U1−U2−U3+U4,U1−U2+U3−U4)`（论文标注X型）。该代数混控是论文**仿真架构**，不能据此断言有逐桨物理推力、非负RPM、饱和、速率或ESC跟踪的硬保证；未给足以移植到仓库1kg机体的实际混控辨识。
- **量测/估计**：MPC定义输出 `y=(x,y,z,u_b,v_b,w_b,p,q,r)`（9维，§2.2）；**KF实际测量** `z=(x,y,z,u_b,v_b,w_b,φ,θ,ψ)`（9维，§2.4），由KF估计不可直接测得的三轴角速率。该文的LiDAR是**地面风速预报传感器**，不是有噪间歇位置传感器；用历史LiDAR风数据作为非线性仿真的预报输入，不能把“实测风数据”误写成四旋翼实飞。KF协方差不是有界状态SMF/CZ真值包含。
- **MPC类型/约束/求解**：悬停线性化**增量LTI MPC**＋未来风扰预报；决策 `ΔU`，位置/输出跟踪二次项＋控制增量二次项，§2.3式(9)、线性不等式 `MΔU≤γ`，Hildreth QP算法；采样0.1s，默认预测/控制时域均1s，即10步（§3）；未报告可核验的数值逐桨RPM/推力/变化率硬界、终端鲁棒不变集合、最坏求解耗时或20ms WCET。
- **理论/结果/局限**：§3仅**线性及非线性仿真**，用既往真实LiDAR风数据驱动；与无风预报MPC对照，非线性阵风案例位置保持偏差约±0.2m vs ±0.6m，作者报告约66%改善；论文摘要另概述约80%改善，属不同汇总/场景，不混用。风预报时差1.75s/强度120%的“鲁棒裕量”是性能退化阈值的**仿真敏感性**，不是所有有界扰动的硬安全证明。没有真实四旋翼MPC飞行、没有SMF、失测、Tube终端递归可行性定理。
- **可复用与待查**：可复用“外环虚拟输入→PID→逐桨混控”的**接口审计清单**、状态/输出/测量严格区分、风预报与未知有界扰动的对照；与PX4开源分配代码（独立来源，**不是论文配套实现**）交叉对照。主任务须验证实际 `(T,τ)→分配器→限幅/限速→ESC→真实推力` 与后验相关的共同可实现域；不在背景任务开发控制器。待查本机体ESC/RPM/推力标定、分配残差上界、成功/丢包后的可重复终端信息集合及20ms预算。相关日志：`docs/research/model_selection/background_run_20261102_2034_mendez_px4_chain.md`。

---

## Run274 — de Souza等(2020)区间观测器＋MPC终端条件再核验（2026-11-02；既有DOI，不增加去重）

- **书目与链接**：Alex Reis de Souza, Denis Efimov, Tarek Raïssi, Xubin Ping, *Robust Output Feedback MPC: An Interval-Observer Approach*, *59th IEEE Conference on Decision and Control* (CDC 2020), pp.2529–2534, DOI https://doi.org/10.1109/CDC42340.2020.9304070；作者公开全文 https://www.researchgate.net/publication/343994166_Robust_Output_Feedback_MPC_An_Interval-Observer_Approach 。原书目已见背景第12轮，按DOI去重。
- **实际阅读范围/状态/日期**：2026-11-02重读公开可解析作者正文§II–V（原版面pp.2–6），重点式(5)–(16)、Theorems 1–3、Propositions 1–2、Assumptions 1–5、§V CSTR数值例；**作者全文分节重读**，未比对IEEE排版终版，论文Theorem 3证明原文省略，未独立复现LMI或仿真。
- **研究问题/模型/控制输入**：一般离散LTI系统 `x+=Ax+Bu+w,y=Cx+v`，有界状态/量测扰动，§V为2状态CSTR浓度与温度、冷却流温度单输入、温度单输出；无四旋翼T/τ、执行器分配或间歇位置量测。
- **状态SMF、MPC与约束**：式(5)逐拍量测区间观测器（状态而非参数估计），式(7)不依赖未来读数的区间预测器；中心二次MPC、预测域N=10、状态和输入硬盒、终端集合与局部反馈双模式切换。Theorem 1需`A-LC`非负且Schur，Proposition 1区间嵌套另需式(11)，Theorem 3在Assumptions 1–5和终端正不变、常值扰动界等条件下声称递归可行、终端中心ISS、硬约束满足。
- **主要结论/局限/可复用技术**：CSTR数值仿真比较IO-MPC与Tube-MPC，不能证明本仓库20ms WCET或四旋翼实飞。每拍完整输出、LTI/非负观测器和终端假设均与本项目5拍位置机会及两次丢包不同；其状态区间可用于说明“后验包含→预测硬约束→终端可移位”是三个独立合同，不得用Run274的30拍共享安全代替Theorem 3。**待查**：第90拍全部合法观测纤维的隐藏速度是否进入Run274的15拍充分门槛；不满足时能否用条件化力矩反馈恢复。
- **另核验但未阅读**：Alex dos Reis de Souza, Denis Efimov, Tarek Raïssi (2022), *Robust Output Feedback MPC for LPV Systems Using Interval Observers*, *IEEE TAC* 67(6):3188–3195, DOI https://doi.org/10.1109/TAC.2021.3099449；本轮仅出版社摘要/书目核验，**未读全文，不计入已读文献**。

---

## Run273 — Qiu等(2020)状态SMF＋输出反馈MPC终端RPI条件再核验（2026-11-02；历史已读，不新增去重）

- **书目**：Quanwei Qiu, Fuwen Yang, Yong Zhu, Eman Mousavinejad, *Output feedback model predictive control based on set-membership state estimation*, *IET Control Theory & Applications* 14(4):558–567 (2020), DOI https://doi.org/10.1049/iet-cta.2019.0881；出版社开放全文 https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-cta.2019.0881 。
- **本轮阅读范围/核验状态**：2026-11-02，重新阅读HTML §2 Assumptions 1–2、§3.1 Theorem 1、§3.2–3.4 minimax MPC/约束/Algorithm 1、§4终端RPI；**分节重读**，网页数学图片未逐式复核全部LMI，未运行数值仿真；与既有Run249/254条目按DOI去重，不另计篇数。
- **研究问题/模型与输入**：有界过程及量测噪声的离散线性时变系统，通用状态 `x`、控制 `u`、输出 `y`；非四旋翼物理模型，无逐桨执行器或位置包自动机。
- **估计/控制/约束**：椭球**状态**集员估计，先预测后当前输出更新；Theorem 1给递归真值包含的LMI充分条件。以估计椭球驱动有限时域minimax MPC，约束经S-procedure/LMI处理；§4依赖额外终端鲁棒正不变集及局部反馈假设，不能由一次15拍安全前缀推出。
- **结论、局限、复用**：论文提供在其线性时变、多面体不确定及终端假设下的状态集合—MPC约束与稳定性结构；不含本仓库正弦Euler、位置每5拍机会、最多连续两次丢包、真实速度隐藏的因果终端合同。可复用**必须分别证明估计包含、预测硬约束、终端回返**的证明分工；Run273只证明完整外包15拍安全，另证明零力矩不能无限重复。
- **待查问题**：如何为所有合法成功读数及丢包分支构造信息状态终端RPI；如何从四状态理论基线过渡到六状态物理输入可实现域。
- **Run276复核（2026-11-02；同一DOI不重复计数）**：重新阅读出版社开放HTML §2 Assumptions 1–2、§3.1 Theorem 1、§3.2–3.4 Algorithm 1、§4终端鲁棒正不变集条件、§5数值案例；特别核实§4局部终端反馈在终端集内**假设状态已知**，与本项目仅有间歇有噪位置读数的共享因果反馈不同。论文没有四旋翼、丢包自动机、可执行逐桨约束或20ms最坏求解时间。Run276构造Run260真实SMM观测历史使第90拍v=2.3942074625m/s超过此前充分准入G=2.3459809875m/s；这是本仓库冻结Euler模型的数学反例，**不是该论文的结果**。论文Theorem 1及终端条件不能直接移植。未复现论文LMI/仿真。下一步检验完整后验及信息状态终端可行性。

---

## Run272 — She与Wu(2023)：随机丢包输出反馈MPC，不等于路径级硬安全（2026-11-02；新增去重论文）

- **书目**：Minghong She, Wenbin Wu, *Efficient Output Feedback MPC for NCS With Data Dropout and Bounded Disturbance via Adaptive Event-Triggered Control*, *IEEE Access* **11** (2023):118161–118169, DOI https://doi.org/10.1109/ACCESS.2023.3324923；作者公开接受稿 https://www.researchgate.net/publication/374963972_Efficient_Output_Feedback_MPC_for_NCS_with_Data_Dropout_and_Bounded_Disturbance_via_Adaptive_Event-triggered_Control 。接受稿正文页脚印有正确DOI；首页未编辑占位DOI不作为书目。2026-11-02核验。
- **实际阅读范围/状态**：2026-11-02，**作者接受稿分节阅读**pp.1–7，§II–V（模型式(1)–(8)、Lemma 1–4、OP1–OP4、CSTR与三状态数值案例、结论）；参考文献未逐条核验、未逐式复核全部LMI、未复现实验；非期刊终版全文逐页核验。
- **研究问题/模型**：通信网络中的有界扰动、多面体不确定离散线性系统 `x+=A_t x+B_t u_applied+D_t w, y=C_t x+E_t w`，`||w||_2<=1`；状态维数一般记为`n_x`，论文数值案例分别为**2状态CSTR**与**3状态通用系统**，不是四旋翼或无人机，故没有旋翼执行器、四旋翼状态/输入分配模型。
- **量测与不确定性**：传感器输出按**Bernoulli**随机变量 `beta_t` 成功/丢包；丢包时缓存上一成功输出。Luenberger型状态估计器与椭球误差界 `e^T P_e e<=eta_t`；注意Lemma中的关键Lyapunov不等式使用**期望算子**，与对所有有界扰动和所有合法丢包路径的确定性真值包含证书不同。
- **MPC与约束**：离线LMI求观测器增益、反馈增益和椭球不变候选，在线优化有限维自由补偿 `u=F xhat+c`（OP4）；自适应事件触发后实际输入可能保持上一命令，须区分优化输入和施加输入。论文没有本项目四旋翼的逐桨幅值/速率、间歇位置测量自动机、15拍信息终端RCI或20ms WCET证据。
- **理论/实验结论及证据等级**：在论文给定多面体、随机丢包、LMI可行等假设下给出二次均值/期望意义的估计误差与控制性能分析，仿真展示CSTR与一般三状态系统的状态收敛趋势、触发节省通信及初始可行椭球扩大；**非四旋翼实飞、非全路径硬约束递归安全证明**。正文未给可直接迁移到本仓库的确定性SMF/CZ后验或丢包模式最坏情况保证。
- **局限/可复用技术/本课题关联**：可借鉴估计器—MPC接口、离线/在线优化分工、明确丢包模型和最终执行输入的区别；不能直接继承其Bernoulli期望稳定性作为最多连续两次位置丢包下的硬安全结论。与Run272的确定性两轨迹后验混叠形成对照。
- **待查**：期刊终版是否更改Lemma/OP公式；随机丢包稳定条件是否存在可验证的路径级强化版本；若用于六状态平面模型，如何加入真实姿态测量噪声和逐桨执行器误差。

---

## 背景第24轮 — Nan等(2022)四旋翼电机状态NMPC＋INDI实飞（2026-11-02；新增去重论文）

- **书目**：Fang Nan, Sihao Sun, Philipp Foehn, Davide Scaramuzza, *Nonlinear MPC for Quadrotor Fault-Tolerant Control*, *IEEE Robotics and Automation Letters* **7**(2):5047–5054 (2022), DOI https://doi.org/10.1109/LRA.2022.3154033；作者接受稿 https://rpg.ifi.uzh.ch/docs/ICRA22_Nan.pdf；arXiv:2109.12886 https://arxiv.org/abs/2109.12886 。2026-11-02核对作者接受稿与dblp/期刊书目。
- **实际阅读范围/状态**：2026-11-02，**作者接受稿9页正文完整阅读**（pp.1–8 §I–V、p.9参考文献；重点§II-A/B/C式(1)–(12)、§III Table I/II、§IV真实飞行）。未逐页对照IEEE排版终版，未运行作者控制代码。注意arXiv网页转录与作者接受稿在式(5)约束和仿真次数的表述存在差异，本条以作者接受稿为准。
- **任务/模型/维数**：单旋翼完全故障后的悬停恢复、8字轨迹跟踪和翻滚/高速飞行恢复；单个非级联全耦合NMPC、后接INDI修正。真实平台是**6物理自由度**四旋翼；状态 x=[p(3),q(4),v(3),omega(3),t(4)]，合计**17坐标**，其中q为单位四元数（有1个单位范数约束），不能称17自由度；额外4状态为各桨实际推力。连续Newton–Euler刚体模型、四元数姿态、G混控、逐桨一阶推力动态 d t_i/dt=(u_i−t_i)/sigma；离散模型由连续模型离散化，具体积分器和参数辨识数据表未从正文确认。无小角度悬停线性化，但未显式包含完整气动力；高旋转时气动失配靠INDI部分补偿。
- **控制输入/执行器**：NMPC直接优化四个旋翼的**期望推力命令** u=(u1,u2,u3,u4)，不是总推力/力矩虚拟输入、不是推力变化率。正常时命令盒0≤u_i≤Tmax，单桨故障时该通道上限强制为0；作者接受稿§II-B式(5)显式约束u，未发现对INDI最终输出u_indi再次进行同一盒内投影的证明。§II-C式(10)–(12)用测得角速度/RPM估计角加速度与力矩，经降秩混控伪逆生成u_indi；**NMPC命令盒内可行不蕴含INDI后处理命令也盒内可行**，需要单独检验最终施加命令及饱和残差。sigma称由数据辨识，但接受稿未报告可直接复用的sigma确定性区间、逐桨变化率硬界或ESC最坏跟踪误差。
- **量测/估计**：真实0.75kg四旋翼、5英寸桨，每桨标称最大8.5N；Vicon位置/姿态400Hz、机载IMU和ESC RPM约500Hz，EKF融合为状态估计；Jetson TX2板载NMPC与状态估计150Hz。不是每5拍有机会/最多连续丢两包的有噪位置SMF/CZ；故障索引由人工触发的mock detector提供，未验证自动故障检测、参数SMF或状态集合包含。
- **MPC实现/约束/理论**：非线性SQP实时迭代RTI、ACADO+qpOASES；预测域1s、N=20（预测网格50ms，**不等于**150Hz控制更新约6.67ms），位置/速度/姿态/角速/推力/命令跟踪二次阶段代价及二次终端代价；故障时偏航权重置零。作者接受稿没有可核验的终端鲁棒不变集合、测量丢包自动机、集合收紧或无限时域递归可行性/稳定性证明；逐桨命令盒与INDI后处理不是自动闭合的硬安全合同。
- **证据/计算**：§III在Jetson TX2上仿真测得NMPC平均单次迭代**6.431ms**、最大**25.75ms**（故障后求解器重初始化），**超过仓库20ms目标**；是观察到的样本最大值，不是形式化WCET。作者接受稿报告200组随机初始姿态仿真NMPC成功200/200，对照85/200；§IV真实飞行在单桨故障下完成悬停恢复、2/5m/s参考8字轨迹、倒飞翻滚恢复及高速轨迹故障恢复。真实飞行说明可执行性，不是任意有界风/丢包的硬安全证明；作者指出高速下气动力仍未被INDI完全补偿。
- **可复用/创新边界**：逐桨推力状态、故障时输入权限降秩、后处理命令可行性审计、控制更新与预测网格分离、求解超时样本是重要工程对照；但不能移植8.5N、sigma或故障后的失控偏航假设到仓库1kg标准健康四旋翼。对本项目首选平面6状态的建议是让主任务显式验证“SMF状态/电机不确定集合→MPC虚拟(T,tau)→四桨混控/执行器/后处理→真实输入”的**全链路共同可实现域**，背景任务不重复开发控制器。
- **未报告/待查**：接受稿未报告可认证的sigma区间、ESC误差外包、最终u_indi逐样本硬约束违规统计、严格终端集合/递归可行定理及20ms最坏保证；需核验作者开源实现是否有后置clip、分配残差记录和超时处理。相关背景日志 docs/research/model_selection/background_run_20261102_1833_nan2022_indi_actuator.md 。

---

## Run271 — Yang/Ozay（2021）既有论文补充复核（2026-11-02；去重数不变）

- **书目**：Liren Yang; Necmiye Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, ADHS 2021 / *IFAC-PapersOnLine*, pp.97–102, DOI https://doi.org/10.1016/j.ifacol.2021.08.481；作者6页PDF https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。
- **实际重读范围/日期/状态**：2026-11-02；PDF pp.2–5，§3式(3)–(7)/Assumption 1、§4.4 Propositions 4–5、§4.5式(17)；**部分正文重读**，不是本轮新增论文，亦未独立复现产品系统求解。
- **问题/模型/输入**：一般离散系统 `x+=f(x,u,w)`、有界扰动、控制输入集合U和状态安全集合；不是四旋翼MPC。成功包时完整无噪状态`y=x`，失测时`y=∅`；没有本仓库位置有噪且速度隐藏的状态SMF。
- **方法/定理/假设**：用受限丢包自动机、因果共享开环序列与产品系统不变核代替全信息幂集游戏；Proposition 5在Assumption 1及产品系统前提下给安全获胜集合等价。§4.5部分量测直接简化要求持续可测子状态的动力学不受隐藏状态影响且无扰动，不能移植为本项目的输出反馈递归可行性证明。
- **结论/局限/复用**：可借鉴合法丢包模式、共享控制量词与信息状态前驱；原论文不是有噪四旋翼状态后验、Tube MPC或20ms实现。Run271独立证明Run270第60拍双真值确实属于Run260 **MMS**真实观测历史，且SMM接续50/55双miss非法；这**不是原论文结论**。
- **待查问题**：能否在带噪位置条带与隐藏速度下，构造可计算的15拍信息状态安全前驱并得到真正可移位终端族？

---

## Run270 — Niazi等（2023）传感器攻击/间歇传输下的zonotope集合估计（2026-11-02；新增去重论文）

- **书目**：Muhammad Umar B. Niazi, Amr Alanwar, Michelle S. Chong, Karl H. Johansson, *Resilient set-based state estimation for linear time-invariant systems using zonotopes*, *European Journal of Control* **74** (2023), Article 100837, DOI https://doi.org/10.1016/j.ejcon.2023.100837 。开放全文：https://www.sciencedirect.com/science/article/pii/S0947358023000663 。
- **阅读日期/范围/状态**：2026-11-02；**出版社开放全文HTML §2–7分节已读**（§3 Assumption 1、§4 Theorems 2/4和Algorithm 1、§5.3间歇传输/复杂度、§6数值案例、§7结论）；未逐页核验PDF/未独立复现实验，不称全文PDF已读。
- **研究问题**：LTI系统遭受时间变化传感器攻击时，如何保持有界噪声下的可靠状态集合包含，避免误将被攻击读数用于收缩真实后验。
- **模型/控制输入**：离散LTI `x+=Ax+Bu+w`、多传感器`y_i=C_i x+v_i+a_i`，已知有界输入；不是四旋翼动力学，也不设计MPC控制输入。
- **量测与不确定性**：有界过程/测量噪声、最多`q<p`个攻击传感器；Assumption 1要求每个单独传感器`(A,C_i)`可观测、系统BIBS稳定及已知初始zonotope。§5.3讨论DoS/间歇传输属于易处理情形，但不是本项目每5拍一次位置机会的定理。
- **方法/重要定理**：zonotope预测、各传感器一致性集合、按未攻击传感器候选子集构造CZ交集并保留集合族；Theorem 4在Assumption 1下保证真值包含；§4.5剪枝、合并/外包降低复杂度。没有MPC终端约束或递归可行性定理。
- **主要结论/证据**：§6二维旋转目标数值仿真，报告平均每步约0.273s；属于仿真而非四旋翼实飞/20ms WCET；§5.3指出隐蔽攻击下候选集合数最坏可指数增长。
- **局限/课题关联/可复用技术**：本项目持续角度/角速测量并不单独可观测横向位置速度，不能直接套用论文全部保证。可借鉴成功包交集、丢包只预测、集合分支剪枝与复杂度预算；Run270证明即使第60拍成功位置包仍可有`0.568117025m/s`特定后验速度直径必要下界，此结论是本仓库独立推导，非论文结果。
- **待查问题**：在本项目固定位置机会/最多2次丢包自动机下，能否放宽逐传感器可观测假设，建立有界且可计算的观测纤维集合并与MPC终端安全接口相连？

---

## Run268 — de Paula等（2024）非线性CZ＋DC规划SMF（2026-11-02；新增去重论文）

- **书目**：Alesi A. de Paula, Davide M. Raimondo, Guilherme V. Raffo, Bruno O. S. Teixeira, *Set-based state estimation for discrete-time constrained nonlinear systems: An approach based on constrained zonotopes and DC programming*, *Automatica* **159** (2024), Article 111401, DOI https://doi.org/10.1016/j.automatica.2023.111401；公开作者预印本 arXiv:2211.05912v1 https://arxiv.org/pdf/2211.05912 。出版信息由DBLP和作者公开稿交叉核验，期刊终版未逐页比对。
- **阅读日期/范围/状态**：2026-11-02；实际阅读预印本PDF pp.1–7 §2–5（问题定义、CZ表示、Lemma 1、Theorems 1–2、Corollary 1、Algorithm 1、复杂度Table 1、§5两数值案例）和p.8 §6结论；**正文分节已读**，不是仅摘要，也未独立重现作者优化或期刊最终证明。
- **研究问题/模型与输入**：带未知但有界过程/量测噪声、状态线性不等式和非线性等式约束的离散非线性状态估计，`x_k=f(x_{k-1},u_{k-1},w_{k-1}), y_k=h(x_k,v_k)`，确定性已知输入。§5.1两状态非线性过程，§5.2四元数四状态飞行机器人**姿态估计**，陀螺仪角速输入含有界误差，输出为非线性姿态观测；并非四旋翼MPC/真实飞行、没有位置丢包或逐桨约束。
- **方法/重要定理/假设**：CZDC按预测、量测交集、状态可行域、非线性等式一致性、复杂度约减五步递推。Assumption 1要求线性不等式约束对应紧可行集；初始状态、过程和量测噪声为有界凸多胞体。Lemma 1用DC凸/凹界给线性化余项可靠区间；Theorem 1/2分别建立CZ预测与量测更新的**外包包含**，Corollary 1处理非线性状态等式；不是闭环MPC稳定性或递归可行性定理。
- **结果与证据**：§5报告MATLAB数值对照CZDC/CZFO/CZMV；姿态仿真Table 3中CZDC平均处理时间3.58s、CZFO 39.8s、CZMV 1.76s（作者特定旧CPU/MATLAB平台），作者同时报告更紧的区间盒面积；不能外推20ms实时性、实飞或硬安全。
- **局限/可复用技术/课题关系**：可复用非线性余项外包、CZ广义交集、状态可行域及降阶的结构；Run268解析 `(v60,phi60,omega60)` 条带是额外的测量一致性约束候选，**不是作者算法的已实现迁移**。论文未处理有噪位置每5拍机会/连续丢2包、真实推力/力矩响应或共享观测纤维的终端信息RCI。CZ＋SMF和非线性外包已是既有技术，不能据此声称首次提出。
- **待查**：如何在非零力矩反馈时保持条带与历史控制的依赖；如何将多时刻观测关联与CZDC合并而不丢弃扰动相关性；如何使计算预算低于20ms并证明终端回返。详见`docs/research/run268_research_log.md`。

---

## Run267 — Ping & Sun (2015) quasi-LPV zonotope SMF＋动态输出反馈MPC正文复核（2026-11-02；既有论文，去重数不增加）

**Run277 2026-11-02复读补记（不增加去重篇数）：** 复读出版社HTML§2 zonotope定义/降阶、§3 A1–A3、§4.2式(27)–(32)、§4.3式(33)–(35)、§4.4 Algorithm 8/Theorem 9、§5 CSTR和§6；强调动态输出反馈`u=C_c x_c+D_c y`和下一步可行性门控属于已有研究，**不能把继承旧控制器参数直接当作有噪位置丢包下的共同因果安全证明**。本轮冻结四状态真实MMS后验双真值证明任意测量无关开环力矩不能保证67拍硬安全，但不排除观测条件化反馈。原网页部分LMI公式缺失，未逐式重算；详见`docs/research/run277_research_log.md`。


- **书目/链接**：Xubin Ping, Ning Sun, *Dynamic Output Feedback Robust Model Predictive Control via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems*, *Journal of Applied Mathematics* 2015, Article 875850, DOI https://doi.org/10.1155/2015/875850；出版社开放全文 https://onlinelibrary.wiley.com/doi/full/10.1155/2015/875850 。
- **阅读日期/范围/核验状态**：2026-11-02，出版社HTML正文§3假设A1–A3、§4.1式(15)–(26)、§4.2式(27)–(32)、§4.3式(33)–(35)、§4.4 Algorithm 8/Theorem 9、§5 CSTR例及§6；**正文分节已读，HTML部分公式显示不完整，未逐式核验全部LMI，也未独立复现证明**。本条补充已有Run131条目，不另计新论文。
- **研究问题/模型/输入**：离散quasi-LPV不确定系统，当前调度矩阵已知、未来在已知多胞体内，有界扰动；动态输出反馈`u=C_c x_c+D_c y`，不假设真实状态直接可测。§5实际为两状态CSTR单输入数值仿真，**不是四旋翼、无物理总推力/力矩或执行器时滞**。
- **量测与集合/控制结构**：当前输出反馈与动态控制器状态；zonotope表示估计误差、按式(27)–(32)传播并限制生成元阶数`N_z`，将外包顶点纳入LMI主优化；辅助式(35)预判下一步主优化可行性，Algorithm 8失败时继承上一控制器参数。该文并未建立仓库每5拍位置机会、最多连丢2包的观测自动机，且并非精确CZ后验。
- **约束/理论/实验**：Theorem 9在初始主优化可行及文中quasi-LPV、扰动、输入/输出约束等假设下证明相应输入输出约束满足与增广状态趋于邻域；§5报告CSTR MATLAB数值比较（`N_z=2,4`），未报告四旋翼飞行或20ms WCET。定理不适用于本仓库未验证的非线性Euler、间歇位置量测与共享观测纤维终端回返。
- **可复用技术/局限/待查**：可复用有界生成元降阶、预测下一步可行性门控和继承旧控制器的架构思想；**SMF＋MPC＋门控/回退并非创新空白**。需验证任何门控是否对所有合法success/miss读数、同一隐藏状态纤维及真实力矩饱和保持可行。Run267严格筛选Run260/264可靠外包：四盒均通过三拍**必要**速度守卫，但没有15拍共享因果终端信息RCI。详细见`docs/research/run267_research_log.md`。

---

## 背景第19轮 — Bicego等(2020)四旋翼逐桨推力/导数约束NMPC实飞（2026-11-02；新论文）

- **题名/作者/年份/出版**：Davide Bicego, Jacopo Mazzetto, Ruggero Carli, Marcello Farina, Antonio Franchi, *Nonlinear Model Predictive Control with Enhanced Actuator Model for Multi-Rotor Aerial Vehicles with Generic Designs*, *Journal of Intelligent & Robotic Systems* 100:1213–1247 (2020; online 2020-09-26), DOI https://doi.org/10.1007/s10846-020-01250-9 。作者公开全文 arXiv:1911.08183 https://arxiv.org/abs/1911.08183 。2019初稿题名 *Nonlinear Model Predictive Control with Actuator Constraints for Multi-Rotor Aerial Vehicles* 是同一arXiv编号/同一论文，按DOI/题名合并去重；**不能误写为arXiv:1911.08175**。
- **阅读状态/范围/日期**：2026-11-02，[作者公开正文分节已读；出版社书目已核验；未与期刊终版逐页比对]。实际核验§2.1–2.3式(1)–(13)、§3/3.1式(22)–(34)、§4.1–4.2式(35)–(40)及真实四旋翼实验、§6结论与附录G辨识；§5其他机型仿真定向浏览。非论文代码复现或飞行复现。
- **研究问题/物理模型**：真实欠驱动四旋翼全耦合6自由度刚体控制，优化状态 `x=[p3,v3,η3,ω3,γ4]∈R16`，其中`γ=(f1,f2,f3,f4)`为逐桨推力状态，16维不等于16自由度；Euler 3-2-1姿态，固定步长RK4离散，避开俯仰奇异。式(2) Newton–Euler，式(5) `f_i=c_f w_i²`，式(6) `[F_body;τ_body]=Gγ`，UDT四旋翼`rank(G)=4`，机体系仅z方向推力；忽略陀螺、叶片挥舞及桨叶诱导阻力等气动效应。
- **控制输入/执行器/可复用方法**：`u=dotγ`（四桨推力变化率）为直接NMPC输入；逐桨非负推力上下界与**状态相关的推力变化率**由单电机/ESC斜坡辨识、力跟踪误差阈值和插值获得；优化后`dotγ`积分成`γ`、反算`w=sqrt(f/c_f)`、经串口传机载ESC。式(26)–(27)确实将推力和推力导数限制写入OCP，优于仅在级联外环后饱和虚拟姿态；但式(33)–(34)、(40)将未来导数界按当前桨力`f_{i,k}`冻结以保持QP线性，且约束可使用slack软化。**这些是物理来源的名义约束，不构成严格鲁棒硬约束保证**。
- **量测/不确定性**：MoCap位置与姿态、机载陀螺角速度、ESC转速；速度由MoCap位置多样本最小二乘拟合，推力由转速模型换算；加速度计因偏置未融合。控制器按全状态可测设计，无SMF/CZ、间歇位置测量、丢包自动机、速度可靠后验或明确有界误差集合；辨识阈值是经验跟踪准则，不是确定性最坏误差界。
- **MPC结构/求解器/约束/终端**：全耦合NMPC；tracking cost含位置/速度/加速度/姿态/角速度/角加速度及终端二次惩罚，multiple-shooting、RTI单次SQP、partial sensitivity update、MATMPC/CasADi、qpOASES；预测时域1s、N=10、网格0.1s；实际控制>200Hz；四旋翼平均求解3.5ms（**地面站**i7-6700HQ，不是板载WCET）。超时取上一轮预测输入下一项作为工程备份。无可核验终端信息RCI；作者明确不提供正式闭环稳定性证明，slack工程策略不能推出严格递归硬约束可行性。
- **实验结论/负面结果**：真实四旋翼chirp与位置阶跃实验，chirp峰值横向加速度5.85m/s²；人为放大推力导数限制系数至1.75时约84s失稳并中止，桨力值仍未饱和而导数接近界。实飞支持速率限制重要性，但不是数学上最坏扰动安全定理；另有六旋翼/可倾桨/故障仿真，不能把六旋翼状态或输入权限当四旋翼。
- **局限/与课题关系/待查**：已证明**直接逐桨约束NMPC实飞并非创新空白**，却没有本课题有噪位置丢包SMF/CZ、共享因果输入、状态硬盒收紧或无限终端安全。平面6状态`(p_x,p_z,v_x,v_z,φ,ω)`与`(T,τ)`仍条件性首选；未来须审计`(T,τ)→γ`的非负/饱和/变化率联合可实现域和跟踪误差有界合同。待查：是否有原始四旋翼论文给出可证明的**联合分配可实现集合**及其在间歇位置量测下的鲁棒收紧/递归可行性？详细证据见 `docs/research/model_selection/background_run_20261102_1335_bicego_actuator_nmpc.md`。

## Run266 — Le et al. (2011) zonotopic SMF + Tube MPC 分节重读（2026-11-02；既有论文，不增加去重数）

**文献**：Vu Tuan Hieu Le, Cristina Stoica, Didier Dumur, Teodoro Alamo, Eduardo F. Camacho (2011), *Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation*, 50th IEEE CDC-ECC, pp.4580–4585, DOI https://doi.org/10.1109/CDC.2011.6161131 ；作者上传全文 https://www.researchgate.net/publication/254054580_Robust_Tube-Based_Constrained_Predictive_Control_via_Zonotopic_Set-Membership_Estimation 。**核验状态**：[作者上传公开正文分节已读，非IEEE终版逐页比对]。实际核验pp.4580–4585：§III式(1)，§IV Algorithm 1/2、Property 4、式(2)–(22)，§V式(23)–(32)与Assumptions 1–3，§VI Table I；阅读日期2026-11-02。

**问题与方法**：离散LTI、标量每拍输出 y=cᵀx+σv、未知但有界过程扰动和测量噪声，使用zonotope预测/测量条带外包SMF；离线LMI计算估计收缩增益，在线以估计中心和双层误差管做名义Tube MPC。**重要假设与保证**：可控可观；初始估计/跟踪误差集合包含、收紧输入/状态可行、名义正不变终端集合与终端Lyapunov条件成立时，论文给出条件性约束与稳定性论证。**实验**：§VI仅2状态1输入数值系统，N=13；Table I是50个采样时刻的算法累计耗时，不是四旋翼单步WCET。

**局限/关联/可复用技术**：没有四旋翼、位置丢包、非线性sin/推力相关残差或真实tau→v三拍时滞；不可把论文保证直接用于本仓库。可复用Property 4的zonotope-条带外包、S^e⊕S^co双层管束、X⊖S与U⊖KS^co收紧、终端合同。**创新性边界**：zonotope SMF+Tube MPC已存在。**待查**：在仓库15模式失测、隐藏速度、物理力矩时滞下，是否能找到共同非空终端信息RCI及20ms预算内实现。对应新数学证据见 docs/research/run266_research_log.md。原总账Le条目保留，本文只是追加实读范围和假设，不新增去重篇数。

---

## Run263 — Li与Savla的状态/参数SMF＋MPC集合嵌入终端证明（2026-11-02；新增去重第111篇）

- **题名/作者/出版与链接**：Zhexian Li, Ketan Savla, *Output-feedback adaptive model predictive control for ramp metering: a set-membership approach*；arXiv:2308.05265（2023初稿、2025修订）https://arxiv.org/abs/2308.05265；作者出版页 https://zhexianli-usc.github.io/publications/ 将其列为2026年 *Automatica*，DOI https://doi.org/10.1016/j.automatica.2026.113290；期刊终版未逐页核验，期刊卷期页码待核实。
- **阅读日期/范围/状态**：2026-11-02；**arXiv开放HTML正文分节已读**§3.1、§3.3、§4.1–4.4、§5.1–5.3、§6部分实验、附录部分证明；不是期刊终版全文逐页复核，也未复现MILP。
- **研究问题/实际模型**：交通匝道流量控制而非四旋翼。Cell Transmission Model：I个主线单元车辆数和I个匝道队列车辆数共2I维状态，I维匝道流量控制，外生交通需求及未知交通参数。使用混合单调嵌入传播状态、需求、参数区间。
- **量测/SMF性质**：输出为部分主线单元和全部匝道队列状态的无噪直接量测；**状态SMF与参数SMF均有**，没有本仓库的有界噪声位置条带、间歇包自动机或四旋翼IMU。Lemma 1在初始化和估计更新假设下给真实状态、需求、参数的区间包含。
- **MPC、约束与定理**：优化为混合整数线性规划MILP；有匝道流量约束、主线拥堵约束和嵌入终端盒。Propositions 2–3给初始可行与递归可行的充分条件，尤其需要嵌入终端集合正不变性。Theorem 1在恒定需求、足够预测时域、特定终端结构与无限匝道存储等条件下给队列有界/进入终端；不能转述为四旋翼无限硬安全。§6为交通仿真，无飞行实验，报告T=300时约209.6秒的平均MPC求解时间，不是无人机实时可用方案。
- **主要结论/局限/可复用技术**：SMF+MPC和集合终端嵌入并非新的概念；可借鉴“集合预测、测量收缩、终端移位分别证明”的结构。但交通混合单调性、无噪量测和无限匝道存储的可行性机制不能直接迁移到有噪失测四旋翼及有限力矩/推力硬约束。Run263只证明测量时刻速度投影**宽度**统一有界，不是本文的递归可行性复现。
- **待查问题**：如何把Run263的宽度界和Run262物理力矩响应时滞结合成第60拍全部非空后验的绝对状态安全前驱？对应 docs/research/run263_research_log.md。

---

## 背景第15轮 — Carlos等（2020）Crazyflie实飞13坐标NMPC与执行器接口（2026-11-02；新增去重第110篇）

- **真实题名/完整作者/出版/DOI**：Barbara Barros Carlos, Tommaso Sartor, Andrea Zanelli, Gianluca Frison, Wolfram Burgard, Moritz Diehl, Giuseppe Oriolo, *An Efficient Real-Time NMPC for Quadrotor Position Control under Communication Time-Delay*, **2020 16th International Conference on Control, Automation, Robotics and Vision (ICARCV)**, IEEE, pp.982–989；DOI https://doi.org/10.1109/ICARCV50220.2020.9305513 ；作者公开预印本 https://arxiv.org/abs/2010.11264 ；大学出版记录 https://www.diag.uniroma1.it/en/publication/22132 。
- **实际阅读日期/版本/范围**：2026-11-02；**公开arXiv HTML原文§I–VI分节已读**，重点§II-A–E式(1)–(3)、§III-A–D式(4)–(5)、Table I、§IV-A–E、§V实飞耗时；未独立核验IEEE终版逐页排版，不声称重算原始数据。
- **研究问题/控制任务**：在固定无线通信RTT下以低计算成本实现四旋翼位置与轨迹跟踪；Crazyflie 2.1，offboard NMPC+onboard PID级联；对比LQR、不同预测时域和延迟。
- **真实模型/状态与输入**：§II-A非线性牛顿–欧拉，NMPC状态 ξ=(p,q,v_b,ω)∈R¹³：p为惯性系三维位置、q为4分量单位四元数、v_b为机体系三维速度、ω为三维角速率；物理刚体6自由度，四元数单位范数约束使13坐标有1冗余。**§III-A悬停LQR**才将q_w消去得到12状态。NMPC优化输入是四个电机转速Ω_i，假设转速瞬时变化；§III-C输入0–22 krpm，转速平方映射推力/力矩。§IV-C/D实机固件执行的是roll/pitch期望、yaw rate期望及公共PWM，经机载PID，而非直接执行四个最优电机转速；论文承认模型/执行接口不一致。连续模型以ERK4离散，采样15ms，选N=50（0.75s）。
- **实际量测/不确定性/估计**：§IV-A/B动捕相机100Hz三维位置；IMU日志重构Euler角与角速率；位置经二阶离散Butterworth滤波估计速度。固定RTT≈60ms，§II-B以RK4预测补偿；**没有位置丢包、确定性有界噪声条带、SMF/CZ状态后验或参数SMF**，不应把RTT误读为丢包。
- **MPC类型、约束、理论**：名义NMPC、direct multiple shooting、二次阶段/终端跟踪代价，式(2)显式输入盒，未提供鲁棒状态/输入Tube、终端RCI或有噪间歇观测下的递归可行/硬安全定理。acados SQP-RTI、Gauss–Newton、HPIPM、BLASFEO、partial condensing；对RTI一般稳定性条件有文献讨论，但不能视作本四旋翼SMF闭环已证。
- **主要结论/实验平台/性能**：§III仿真对比LQR、N=10/20/30/40/50及RTT影响；§IV真实Crazyflie 2.1，ROS/C++ offboard、平滑阶跃及螺旋轨迹；§V Intel Core i5-8250U Ubuntu平均优化7.4ms、观测最大22.1ms（起飞），超过论文15ms采样，也超过仓库20ms目标；**不是WCET上界**，无全扰动硬约束证书。实验跟踪表现不是数学鲁棒安全证明。
- **模型简化/局限**：瞬时电机转速假设；实际固件输入映射和内环PID未建模；固定RTT；无丢包与有界扰动集合；没有本仓库T/τ物理合同、推力依赖残差、终端信息RCI。该文13坐标不能直接替代本仓库6状态平面模型。
- **本课题关联/可复用技术**：直接提供四旋翼实飞NMPC模型、输入限幅、acados实时实现及传感器/固件接口证据；可作为名义MPC性能和计算预算对照。SMF/CZ应接入有噪间歇位置状态后验、考虑共享因果输入及实际执行器映射；创新性不在“使用NMPC/RTT预测”。**未运行其开源代码、未复现飞行实验**。
- **待查问题/下一轮唯一优先**：全文核验Kamel/Burri/Siegwart (2017) LMPC与NMPC对照的精确状态、输入、内环和计算成本；再评估降阶或分层MPC接入状态SMF的可行性。与本轮背景日志 docs/research/model_selection/background_run_20261102_0937_carlos_nmpc.md 对应。

---

## Run262 — Diaconescu等（2024）弹性zonotope Tube MPC全文分节核验（2026-11-02；新增去重第109篇）

- **题名、作者、出版及DOI：** Sabin Diaconescu, Florin Stoican, Bogdan D. Ciubotaru, Sorin Olaru, *Elastic Tube Model Predictive Control With Scaled Zonotopic Sets*, *IEEE Control Systems Letters* **8** (2024), 1343–1348；DOI https://doi.org/10.1109/LCSYS.2024.3408047 ；作者开放版全文可解析 https://www.researchgate.net/publication/381050260_Elastic_Tube_Model_Predictive_Control_With_Scaled_Zonotopic_Sets ；书目 https://dblp.org/rec/journals/csysl/DiaconescuSCO24 。
- **阅读日期、状态、范围：** 2026-11-02；**作者开放版§II–V分节已读**，核对式(8)–(15)、Lemma 2、Propositions 2–4、§V-A/B；未逐式核验IEEE终版PDF，不声称期刊终版全文已读。
- **研究问题、模型/输入、量测：** 已知A、B的离散LTI`x+=Ax+Bu+w`，有界加性扰动；`u=ubar+K(x-xbar)`，全状态误差反馈而非有噪位置输出反馈。双积分器示例2状态/1输入，耦合弹簧链示例2ℓ状态/2端部力输入；**没有四旋翼状态、推力力矩、真实传感器、间歇测量或丢包**。zonotope用于**MPC误差管束**，不是SMF状态估计或参数估计；没有CZ后验。
- **方法、约束与定理：** 硬状态/输入集合X/U、终端集合；固定K下`(A+BK)Omega_k⊕W⊆Omega_{k+1}`，生成元独立缩放的弹性zonotope；Proposition 3给出保证包含的**充分**线性条件，Proposition 4以LP构造一个RPI集合。§V双积分器N=12、弹簧链N=25，MATLAB/YALMIP/MOSEK/CORA/MPT3数值实验。不能把LP可行/仿真结果当作有噪间歇四旋翼的递归安全证明。
- **主要结论与局限：** 生成元缩放使管束形状可随预测时域变化，数值展示计算扩展性；没有物理四旋翼、真实飞行、丢包自动机、SMF/CZ后验、20ms最坏执行时间或本仓库终端信息RCI。与2025/26 Diaconescu等后续论文按题名与DOI区分，不重复计数。
- **本课题关联/可复用技术：** 可复用线性集合包含与RPI构造作对照；“zonotope弹性Tube MPC”本身已有文献，创新须落在有噪间歇量测、关联状态SMF/CZ、共享因果控制和物理力矩约束。Run262另外给出四状态原点三拍最坏速度`|v3|>=0.1214254425`的可达必要界，证明窄终端速度带`|v|<=0.12`不可鲁棒不变；这是仓库独立推导，不是该论文定理。
- **待查问题：** 第60拍所有非空有噪success观测纤维，能否在物理力矩三拍时滞下形成共享因果可移位终端安全前驱？详见`docs/research/run262_research_log.md`。

---

## Run261 — Lorenzetti、Pavone（2020）固定截面输出反馈Tube MPC终端条件重读（2026-11-02；既有108篇，不新增去重）

- **题名/作者/年份/出版**：Joseph Lorenzetti, Marco Pavone, *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, ECC 2020，DOI https://doi.org/10.23919/ECC51009.2020.9143979；arXiv:1911.07360v2 https://arxiv.org/pdf/1911.07360 。
- **本轮阅读范围/状态/日期**：2026-11-02，公开预印本PDF印刷pp.2–5，§II、§III-A、§IV-B–F、§V-C–D，Assumptions 1–2、Propositions 1–2、Theorems 1–2及式(8)–(13)；**分节已读**，未重新精读全部8页或逐式核验会议终版。此文早已在统一总账登记，本轮只补充终端假设审计。
- **研究问题/实际模型/输入/量测**：一般`n`维LTI离散系统`x+=Ax+Bu+w`、`y=Cx+v`，`m`维输入，逐拍带噪输出；Luenberger点估计`xhat`，不是状态/参数SMF或CZ；无丢包、无四旋翼物理`(T,tau)`模型。状态/输入及噪声以紧凸多面体约束，仿真为合成线性系统和风能系统。
- **关键定理/假设/结论**：`(A,B)`可控、`(A,C)`可观，`A-LC`和`A+BK` Schur稳定，联合估计/跟踪误差RPI存在且初始误差属于RPI；终端集满足式(10)不变与收紧输入/状态、式(11)下降。Proposition 1在初始MPC可行等条件下给出所有有界扰动下的约束满足；Proposition 2为趋向误差集合而非精确零点。Theorems 1–2的RPI构造还依赖Assumptions 3–5。
- **局限/与本项目关联/可复用技术**：不能直接覆盖本项目有噪间歇位置、15模式失测、非线性残差或共享因果信息状态；可复用**终端控制不变、耦合误差RPI与收紧非空**的证明义务清单。Run261证明固定零力矩桥无限重复会在第119拍真实速度越界，不能将有限安全桥冒充该论文的终端不变性；这项反例是仓库独立证明而非论文结果。
- **待查问题**：第60拍全部非空位置success测量纤维是否存在同一因果反馈与可移位15拍终端信息族？详见`docs/research/run261_research_log.md`。

---

## Run260 — Vinod、Weiss、Di Cairano（2025）CZ鲁棒可控集前驱全文分节阅读（2026-11-02；新增去重第108篇）

- **真实题名/作者/年份/出版**：Abraham P. Vinod, Avishai Weiss, Stefano Di Cairano, *Projection-free computation of robust controllable sets with constrained zonotopes*, *Automatica* **175** (2025), article 112211；DOI https://doi.org/10.1016/j.automatica.2025.112211；原始作者全文PDF https://www.merl.com/publications/docs/TR2025-023.pdf ；arXiv https://arxiv.org/abs/2403.13730 。
- **阅读日期/状态/范围**：2026-11-02，**作者公开全文分节已读**，PDF pp.3–5（§1–2.3、Def.2、式(13)–(14)），pp.9–11（§4.4–5、计算复杂度），pp.12–14（§6案例）；未声称全部19页逐式审校。
- **研究问题/实际模型**：一般线性时变离散系统`x_{t+1}=A_t x_t+B_t u_t+F_t w_t`，状态向量为任意`n`维全状态`x`，输入`u`为任意`m`维约束控制；扰动集合对称、紧、凸；目标集合、状态约束、输入约束以多面体/CZ描述。案例包括双积分器、稳定2状态LTI、100维线性系统与简化航天器安全撤离；**不是四旋翼2/4/6/10/12状态模型**。
- **实际量测/失测/噪声**：计算全状态空间中的鲁棒可控集，不设部分状态量测、SMF后验、测量噪声或丢包自动机；CZ在本文用于**可控/可达集合计算**，不是状态SMF也不是参数SMF。无四旋翼实际推力、力矩、执行器延迟/饱和物理映射。
- **方法/MPC类型/保证**：基于CZ的Pontryagin差内外近似、线性最小二乘、后向鲁棒可控集递推（式14），为有限步安全目标可达性提供**内近似**。是MPC终端集/安全前驱的可用离线构件，但本文不实现仓库的输出反馈Tube MPC或闭环估计器；§5要求特定满维、集合与线性系统条件，复杂度随时域增长。
- **主要结论/实验与局限**：§6给双积分器与高维线性数值对比；报告100维20步内近似低于15秒，不等于无人机20ms单步WCET；§7航天器应用不是四旋翼实飞。其全状态反馈鲁棒可控集合不直接解决“同一有噪测量纤维共享因果控制”的信息状态前驱。
- **与本课题关联/可复用技术**：将其安全**内近似**作为未来终端信息状态集合计算的候选几何工具；必须先定义SMF后验/失测模式的提升状态与统一量词，不能将全状态RC集合直接宣布为终端信息RCI。Run260的15拍共享开环安全桥是固定历史的有限证书，不是本文算法复现。
- **待查问题**：能否在固定15拍历史锚点下对所有合法非空测量分支构造可移位的终端信息状态族，并在有限输入与计算预算下获得非空安全前驱？参见`docs/research/run260_research_log.md`。

---

## 背景第13轮：Yan、Cannon、Goulart（2022）随机间歇观测输出反馈MPC（2026-11-02；新增去重第107篇）

- **题名/作者/出版**：Shuhao Yan, Mark Cannon, Paul J. Goulart, *Stochastic output feedback MPC with intermittent observations*, *Automatica* **141** (2022), article 110282；DOI https://doi.org/10.1016/j.automatica.2022.110282；作者预印本 arXiv:2009.11071v3 (2022-03-01), https://arxiv.org/pdf/2009.11071 ；牛津机构记录 https://ora.ox.ac.uk/objects/uuid%3A65493a65-7eb6-4897-9f30-bc51e091266c 。
- **阅读日期/状态/范围**：2026-11-02；**公开PDF正文分节已读**，pp.1–4 §1–3/Assumptions 1–3、pp.5–8 §4–6/Theorem 7、pp.8–9 Theorem 9、pp.12–13 §9–10；未逐页核对期刊终版，未独立重现完整证明。
- **研究问题与实际模型/输入**：线性离散`x+=Ax+Bu+Dw, y=Cx+v, z=gamma*y`下的随机丢包输出反馈MPC。§9数值例是**四状态双倒立摆线性化**、**两个输入**，`C=[[1,0,0,0],[0,0,1,0]]`，0.01s采样；不是四旋翼四状态、六状态或真实推力/力矩输入。
- **量测/丢包/扰动/执行器**：每拍整个输出`y`以已知成功率`lambda`独立Bernoulli到达（例中0.6），零均值独立噪声具有有限协方差，理论允许无界分布，仿真为Gaussian；无“最多连续2次miss”硬自动机、每5拍位置机会或每拍姿态通道；无无人机执行器、T/τ饱和/执行器动态合同。
- **估计与MPC**：固定观测器增益M的点状态估计与协方差/二阶矩递推，**不是状态SMF/CZ，也不是参数SMF**；未来控制为已接收创新量的仿射因果反馈，固定K/M、在线优化偏置与反馈增益；§5式(23)为凸随机MPC/LMI。
- **状态/输入硬约束**：实际限制是`sum_k beta^k E(||H x_k||^2)<=epsilon`的**折扣期望二阶矩预算**，不是逐拍`x∈X,u∈U`硬约束。数值例`N=5,beta=0.8,epsilon=2`；没有本课题位置/速度/倾角/推力力矩硬盒保证。
- **关键假设/定理**：Assumption 1要求(A,B)可稳定、(A,C)可检测；Assumption 2要求已知固定到达率；Assumption 3要求`A+BK`渐近稳定、随机误差均方稳定。Theorem 7在初始可行及预算更新下给**优化递归可行和折扣期望约束**；Theorem 9在额外有界矩及折扣条件下给长期平均期望代价有限上界。不能改写成所有丢包历史下鲁棒安全不变性或渐近稳定性。
- **结论、实验与局限**：§9为双倒立摆Monte Carlo/LQG对照，非无人机实飞；不提供CZ状态后验、硬输入安全、确定性失测自动机或20ms WCET。论文证明“间歇观测＋输出反馈MPC”已有先例，缩小本课题的创新主张。
- **与本课题关联/可复用技术**：可借鉴因果观测创新反馈、候选策略移位论证；**不能**把期望矩约束当成Run259的确定性硬安全证书。本轮独立精确Fraction审计：lambda=3/5时三次连续miss概率8/125>0；100组互不重叠三次机会中至少一次MMM概率约0.998658517925，故随机Bernoulli不能保证硬最多2次miss。与仓库Run259的15拍自动机/锚点估计是不同合同。
- **待查问题**：Li/Shi (2013) DOI https://doi.org/10.1016/j.sysconle.2013.01.003 的周期丢包输出反馈MPC，是否在明确硬状态/输入和最大连续失测下建立真正的递归可行性？见 `docs/research/model_selection/background_run_20261102_0634_yan_stochastic_contract.md`。

---

## Run259 — Yang、Ozay（2021）有界丢包安全自动机与因果前缀重读（2026-11-02；历史已读，去重数仍106）

- **真实题名、作者、出版与DOI：** Liren Yang, Necmiye Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, *IFAC-PapersOnLine*（ADHS 2021），DOI https://doi.org/10.1016/j.ifacol.2021.08.481；作者公开PDF https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。
- **本轮实际阅读状态/范围：** 2026-11-02，作者PDF pp.2–5（PDF页索引1–4）§3式(3)–(7)、Assumption 1、§4.2因果开环共享前缀、§4.3产品系统、§4.4 Propositions 4–5及§4.5式(17)；为已登记论文的**正文分节重读**，不新增去重篇数，不声称完整逐页精读。
- **实际问题/模型/输入/量测：** 一般离散系统`x+=f(x,u,w)`，有界扰动及受约束控制输入，成功时`y=x`为**完整无噪真值**、失测时`y=∅`；丢包受有限自动机约束。§4.5部分状态可测扩展要求该部分**完美观测且动力学无扰动、不受隐藏状态影响**。论文无特定四旋翼状态、物理T/τ、SMF状态或参数估计、CZ、Tube MPC或实飞。
- **定理、实验和限制：** Propositions 4–5在紧安全/输入集、连续动力学和自动机等条件下建立产品系统不变核/安全winning set；§5为汽车行人有限状态及线性二维算例，非无人机。无法直接迁移到仓库的有噪间歇位置、隐藏速度、真实推力/力矩饱和和20ms时限。
- **与Run259关联/可复用技术：** Assumption 1的最多连续2包miss给出成功位置间隔至多15个控制采样步；可以为滚动位置锚点限制缓存长度，但本文**没有证明**该锚点滤波器或共享因果终端不变性。Run259仅认证一个既定历史的7个有限观测分支。阅读日志/源码见`docs/research/run259_research_log.md`。
- **待查：** 固定15拍可靠锚点在任意有噪success/miss历史下是否足以构造非空、可移位且满足物理输入饱和的共享因果安全前驱？

---

## 背景第12轮：de Souza等（2020）区间观测器输出反馈MPC（2026-11-02；新增去重第106篇）

- **题名/作者/出版**：Alex Reis de Souza, Denis Efimov, Tarek Raïssi, Xubin Ping, *Robust Output Feedback MPC: An Interval-Observer Approach*, 59th IEEE Conference on Decision and Control (CDC 2020), pp.2529–2534；DOI https://doi.org/10.1109/CDC42340.2020.9304070 ；原始作者上传公开全文 https://www.researchgate.net/publication/343994166_Robust_Output_Feedback_MPC_An_Interval-Observer_Approach ；DBLP https://dblp.org/rec/conf/cdc/SouzaERP20.html 。不同于2022 IEEE TAC的LPV文章。
- **实际阅读日期/范围/状态**：2026-11-02；公开可解析作者全文§II–V，Assumptions 1–5、Theorems 1–3、Propositions 1–2、式(1)–(16)与§V数值例，约原版面pp.2–6；**作者全文分节已读，未逐页核对IEEE终版PDF**。Theorem 3证明原文省略，不能称独立验证其完整证明。
- **研究问题/真实模型/输入/量测**：离散LTI有界过程/输出噪声的鲁棒输出反馈MPC，`x+=Ax+Bu+w,y=Cx+v`，固定已知C且每拍观测。§V实际为CSTR两状态`(C_s,T)`、单输入冷却流温度`T_C`、单输出温度`T`（C=[0,1]），采样0.25min、预测N=10。无四旋翼动力学、实际推力/力矩、无人机传感器、位置丢包或实飞。
- **状态/输入硬约束与不确定性**：§V示例`X=[-0.4,0.4]×[-25,25]`、`U=[-15,15]`、`W=[-0.02,0.02]×[-0.4,0.4]`、`V=[-0.1,0.1]`。没有执行器动态或物理T/τ饱和；过程/量测噪声按区间有界而非概率置信区间。
- **方法/SMF性质/MPC**：式(5)区间观测器IO用于**状态**SMF（不是参数SMF）；式(7)区间预测器IP用于未来约束外包；式(13)–(16)中心轨迹二次代价MPC＋终端局部反馈。不是CZ、非线性四旋翼或间歇测量Tube MPC。
- **重要定理/假设**：Theorem 1需`A-LC`非负且Schur；Theorem 2以LMI设计有界IP；Proposition 1的IO/IP嵌套需式(11)额外条件；Assumption 5要求终端不变及输入可行；Theorem 3在Assumptions 1–5、式(11)、常值扰动界等条件下给递归可行、终端中心ISS与硬约束满足。不可只取中心终端条件而忽略全区间包含和不变性。
- **结论/局限/与本课题关联**：CSTR数值比较支持低复杂度与较低保守性，但无20ms WCET或无人机结果。仓库位置miss时观测矩阵仅保留姿态/角速；名义Euler线性化对任意L仍有四状态至少2个、六状态至少4个单位特征值，故论文**逐拍**Schur充分条件不能直接移植。跨5/10/15拍success的线性观测秩为4/6，不等于带扰动精确恢复。可复用IO→IP→硬约束→终端不变性合同审计。
- **待查问题**：主任务能否用第45拍强制success的全分支可靠H-rep/CZ后验构造15拍失测自动机条件化误差管束及共享物理T/τ终端前驱？详情见`docs/research/model_selection/background_run_20261102_0536_desouza_interval_miss.md`。

---

## Run258定向重读（2026-11-02；Scott等2016，既有条目不新增去重）

**真实题名/作者/发表：** Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, *Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036 ，作者公开PDF https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。**实际阅读：** 2026-11-02，PDF印刷pp.126–130，§2 Definitions 1–2、§3 Definition 3/Propositions 1–3/Theorem 1、§4开头；分节重读，未宣称全篇重读。

**研究问题/模型/方法：** 线性离散系统未知但有界过程/测量噪声下的**状态**集员估计与故障检测，不是参数估计；线性状态转移、已知输入、线性观测，CZ约束生成元表示保留状态相关性。无四旋翼状态向量、无T/τ物理输入、无专用传感器/位置丢包机制；不是MPC/Tube MPC，亦无四旋翼硬约束、终端RCI、稳定性或无人机实飞。**重要结论/假设：** Proposition 1式(11)–(13)对线性映射、Minkowski和广义测量交集给出CZ精确运算；Proposition 2的非空/成员检查需要LP；Theorem 1给出不限复杂度时CZ与凸多胞体的表示等价；§4降阶必须保持外包包含。无20ms WCET证据。**关联/复用：** 关联状态及success读数广义交集；不能把该论文线性SMF定理冒充非线性Euler或MPC终端安全证明。**本轮独立结果：** Run258利用第30拍历史位置锚点，使第35拍miss后第40拍success零读数速度宽度可靠上界0.857482532595m/s，MM仍3.5256474675m/s；详见docs/research/run258_research_log.md。**局限/待查：** 固定复杂度CZ能否跨强制第45拍success保持全部合法测量树可靠包含、满足共享因果安全前驱和20ms预算？**去重论文总数仍105。**

---

## 背景第11轮 — Niknejad等（2025）CZ误差观测器＋Tube MPC与间歇测量假设审计（2026-11-02；新增去重第105篇）

- **题名/作者/年份/来源**：Nariman Niknejad, Gokul S. Sankar, Bahare Kiumarsi, Hamidreza Modares, *Robust Model Predictive Control Design for Autonomous Vehicles with Perception-based Observers*, 2025, arXiv:2509.05201, https://arxiv.org/abs/2509.05201 （2025-09-05）；**未核验正式发表场所和DOI**，仅按预印本登记。
- **实际阅读范围/状态**：2026-11-02阅读arXiv HTML正文§II-B/C、§III（Eq.6–15/Assumptions 1–9）、§IV（Lemmas 3–4/Theorems 1–2/Eq.16–19）、§V（Theorems 3–4/Algorithm 1）、§VI-A/B（仿真、真实实验）。**HTML正文分节已读；PDF页码/最终发表版本未核验**。
- **研究问题、方法与模型**：有界非高斯感知误差下的离散LTI输出反馈tube MPC；一般x+=Ax+Bu+w，y=Cx+v；固定增益Luenberger点估计及CZ**估计误差外包**，非逐次量测条带交集的精确SMF后验，也不是参数SMF。收紧S_xbar=S_x⊖(S_e⊕S_xtilde)、S_ubar=S_u⊖KS_xtilde；Minkowski-Lyapunov终端代价、终端椭球及LP形式MPC。
- **真实实验状态/输入/量测**：§VI-B Husarion ROSbot XL三状态(x,y,theta)，四轮输入、A=I3、0.35s离散采样、N=12；位置x/y由CNN相机30Hz感知，theta由SLAM提供且假设每拍精确；**没有位置丢包自动机**。§VI-A另有2状态线性仿真。**不是四旋翼T/tau物理模型**。
- **扰动/硬约束/简化假设**：实验归一化状态盒[-1,1]^3、输入盒[-1,1]^4；初始估计误差diag(0.1,0.1,0)，状态偏差diag(0.2,0.2,0)；§VI-B设w=0，theta测量精确。假设(A,B)可控、(A,C)可观，感知误差只在局部B_rho(x_d)内有界；无推力/力矩、连续动力学或执行器饱和映射。
- **重要定理/结论**：Theorems 1–2在有界CZ噪声及可行增益下给误差/偏差管束包含；Theorems 3–4给终端代价下降、名义终端集合不变及状态/输入收紧的条件性保证。实机展示CNN感知驱动LP-MPC，不能自动转移为本仓库有噪失测四旋翼递归安全。
- **局限与证据级别**：§VI-B Eq.(34)的感知误差CZ由**95%数据点**拟合，无法证明确定性全样本包含；§VI-A用未截断Laplace模拟噪声，数学支持无界，与紧有界假设不同。论文每拍使用y(k)，未给失测分支；0.35s采样不支持本项目20ms WCET。以上是对正文假设与实验的独立逻辑审计，不等于论文定理被证伪。
- **与课题关系/可复用技术**：已存在CZ误差界+Tube MPC+终端集先例，创新点需落在有噪**间歇位置**、状态关联SMF/CZ后验、物理T/tau饱和、共享因果信息状态终端安全；可复用误差/偏差分离、Pontryagin收紧与终端代价证明结构，但不能直接移植固定L。
- **阅读日期/待查问题**：2026-11-02；在success/miss自动机下，是否存在非空的**多拍条件化**误差/终端信息集合，而非逐拍固定严格收缩？关联证据见 docs/research/model_selection/background_run_20261102_0433_niknejad_dropout_contract.md 。

---

## Run256 — Rego等（2020）非线性CZ状态估计定向正文重读（2026-11-02；历史已读，不新增去重数）

- **题名、作者、年份、出版：** Brenner S. Rego, Guilherme V. Raffo, Joseph K. Scott, Davide M. Raimondo, *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, *Automatica* 111:108614 (2020)；DOI https://doi.org/10.1016/j.automatica.2019.108614；公开预印本 arXiv:1908.09950v3 https://arxiv.org/pdf/1908.09950 。
- **核验状态及实际范围：** 2026-11-02重新阅读作者公开PDF pp.2–3 §2–3.1、pp.4–6 §4.1–4.2 Theorems 1–3、pp.8–10 §4.4–5（式(22)、Remark 10、Table 1）；未核对期刊终版逐式一致。Run179已有分节已读，Run214仅摘要复核，**本轮重读不新增文献**。
- **研究问题/模型/输入/测量：** 一般非线性离散系统 `x_k=f(x_(k-1),u_(k-1),w_(k-1))`，`u`是已知施加输入；`y=Cx+D_u u+D_v v` 为线性有界噪声量测。论文没有特定四旋翼状态向量、推力/力矩物理输入、无人机失测自动机或执行器硬盒；研究**状态集合估计**，不是参数估计或MPC。
- **假设、定理、结论：** 初始可靠包含、紧有界扰动/量测集合，非线性映射可微且Jacobian/Taylor余项有可靠包络；Theorems 2–3给出CZ均值/一阶Taylor预测外包，§4.4式(22)给出有界线性量测广义交集；Remark 10说明复杂度增长，必须保包含降阶。示例比较估计保守性与复杂度，**不证明**鲁棒输出反馈MPC递归可行性、无人机稳定性或20ms WCET。
- **与本课题关系/可复用技术：** Run256严格证明Run249/255独立区间SMF的未测速度宽度在所有非空success/miss分支每拍至少增加`2hR=0.081159575m/s`，从特定Run254历史`S30`起第71拍宽度下界`6.021189585>6m/s`。该命题仅否定现有独立盒的无限时域安全**认证能力**，不是实际后验/真实物理不可生存；CZ可保留`p-v`关联，但尚未在本项目实现和比较。
- **阅读日期/待查：** 2026-11-02；第35拍全部非空success/miss观测分支，关联H-rep/CZ后验能否严格缩小速度投影，且在同等在线预算下仍可用于终端前驱？证据与代码见 `docs/research/run256_research_log.md`。

---

## 背景第9轮 — Agrawal、Panagou（2023）有界误差观测器＋鲁棒CBF（2026-11-01；新增去重第103篇）

- **题名、作者、出版：** Devansh R. Agrawal; Dimitra Panagou, *Safe and Robust Observer-Controller Synthesis Using Control Barrier Functions*, *IEEE Control Systems Letters* **7**:127–132 (2023卷；2022-06-22在线发表)，DOI https://doi.org/10.1109/LCSYS.2022.3185142；作者公开期刊PDF https://dev10110.github.io/pdfs/2022-observer-controller.pdf；预印本 https://arxiv.org/abs/2211.14364 。**阅读日期/状态：** 2026-11-01；实际阅读作者公开期刊PDF pp.127–132，§I–IV，特别是(1)–(2)、Definition 5、Theorems 1–3、(16)–(18)、§IV-B/C；**正文分节已读**，未复现实验。
- **问题/方法：** 在有界动力学和有界量测扰动、部分状态可测时，用ISS观测器或bounded-error (BE) observer的可靠真值包含集与robust control barrier function联立求安全输入。Theorem 2要求一个共享输入落在全部可能真实状态的安全控制集合交集 `u∈∩_{x∈P(t,xhat)}K_trcbf(x)`；Theorem 3在额外下界、同号/相对阶1条件及**无界输入域 U=R^m**下将其写成QP并证明解的正则性/安全。BE集合允许interval/zonotope等，但论文并未实现本仓库离散CZ-SMF。
- **实际平面四旋翼模型：** §IV-B为**平面3物理自由度/6状态** `x=(p1,p2,phi,v1,v2,omega)`，位置与速度在惯性系，控制 `u=(T,tau)`；`m=1 kg,J=0.25 kg·m²,g=9.81`。输出是**连续有噪的二维位置＋俯仰角**（5cm和5°界），速度与角速度隐藏；外扰加速度范数≤2m/s²。DEKF构造椭球真值包含集，基于Theorem 2/3做障碍物避碰CBF-QP、LQR期望输入。没有仓库的每5拍位置机会/最多连丢2包自动机，也没有输出反馈Tube MPC、SMF/CZ后验的递归终端集合。
- **约束/保证/实验：** §IV-B安全集为**圆形障碍物避碰**，不是仓库的完整位置/速度/倾角/角速度与执行器硬盒；所读案例未给出与仓库相同的 `T∈[4.905,14.715], |tau|≤0.08` 认证。Theorem 2的连续时间前向安全依赖可靠BE集合、TRCBF和**每时刻非空的共享安全输入**，并不自动保证离散采样、输入饱和或MPC递归可行。§IV-C Crazyflie 2.0 实飞使用IMU、气压计和Vicon，EKF的**99.8%置信区间**是概率假设，不能等同于确定性全扰动真值包含；低层内置控制映射PWM，未核验真实输入硬约束或20ms最坏耗时。
- **结论/局限/本项目关联：** 论文已证明“六状态平面四旋翼＋有界误差状态估计＋安全控制”并非本课题独有创新；可复用的**结构性接口**是可靠集合 `P_k` → 所有状态的共享可行输入 → 安全后继。仓库第7轮的隐藏垂向速度 `±3m/s` 无共同推力反例说明必须先筛信息纤维；Run255仅特定历史39拍安全，不能以Theorem 2直接宣称终端RCI。**重要区分：** CBF交集空不等于所有可能非CBF控制策略不可行；论文的CBF充分条件不是可生存性的必要条件。
- **可复用技术：** BE集合（可为CZ/zonotope）与共享鲁棒安全输入交集的量词；作为主任务SMF→backup接口的文献比较基线，不另建CBF算法分支。
- **待查问题：** 在仓库**有界物理推力/力矩**和位置success/miss后验下，是否存在非空且可移位的共享输入信息集合族？如何处理连续CBF相对阶/采样保持与硬盒差异？**专用日志：** `docs/research/model_selection/background_run_20261101_1836_agrawal_be_observer.md`。

---

## Run255 — Yang、Ozay（2021）部分观测安全游戏的迁移边界重读（2026-11-02；去重102篇不变）

**真实题名/作者/出版：** *Safety Control Synthesis for Systems with Missing Measurements*；Liren Yang、Necmiye Ozay；ADHS 2021，*IFAC-PapersOnLine*，pp.97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ；作者公开PDF https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**实际阅读：** 2026-11-02重新核对PDF pp.2–5 §3、§4.2–4.5、Propositions 4–5及式(8)–(17)；**历史已读论文分节重读，不新增去重条目**。

**研究问题、方法、模型与输入：** 离散时间一般系统`x+=f(x,u,w)`，`u`为受约束控制输入，`w`为扰动；并非特定四旋翼模型、无专用姿态/推力输入。通过有限自动机约束连续失测次数、string automaton编码未知未来丢包、共享因果开环控制前缀、产品系统鲁棒安全博弈与不变核。**量测：** §3式(4)成功时**完整无噪状态**`y=x`，失测时空读数；§4.5式(17)允许一部分状态始终**完美**可测，且要直接应用约化结构需该部分动力学无扰动且不受隐藏状态影响。没有有噪位置-only SMF/CZ（既非状态SMF也非参数SMF），没有四旋翼MPC/Tube MPC。

**重要定理/假设、结论与限制：** Assumption 1要求自动机、可能success及有限最大连续miss；Proposition 4在安全集和输入集紧、动力学连续等条件下给出产品系统不变核极限；Proposition 5给出其假设下安全winning set与产品系统不变核的对应。该结论**不能**直接转用于本仓库有噪角/角速、有噪间歇位置、隐藏速度的Run249模型。实验是论文两个计算示例，不是无人机实飞，未认证本项目执行器硬约束或20ms WCET。

**与本课题关联/可复用技术：** 借鉴丢包自动机、共享前缀与先验证所有扰动/读数分支的量词结构；必须另建SMF后验信息状态及可移位安全前驱。Run255独立用Fraction对Run254特定`SSSMMS`零读数历史的**完整可靠区间后验**证明非零共享力矩+零尾在第30–69拍的有限硬约束安全，非论文原定理。**待查：** 第35拍所有非空success/miss后验能否映射进统一可重复闭合的信息状态族？**日志：** `docs/research/run255_research_log.md`。

---

## 背景第8轮 — Rodriguez-Guevara等（2023）12状态qLPV-MPC（2026-11-01；新增去重第102篇）

**题名：** *A qLPV-MPC Control Strategy for Trajectory Tracking of Quadrotors*。**作者：** Daniel Rodriguez-Guevara、Antonio Favela-Contreras、Oscar Julian Gonzalez-Villarreal。**发表：** *Machines* 11(7):755 (2023-07-19)。**DOI/原文：** https://doi.org/10.3390/machines11070755 ，https://www.mdpi.com/2075-1702/11/7/755 ，https://staging.core.mdpi.com/2075-1702/11/7/755 。

**阅读日期/状态：** 2026-11-01；核对出版社公开HTML索引§2.1–2.2式(1)–(3)、§3式(6)–(8)、§4 MPC策略、§5仿真和计算时间、§6结论。原站直接打开返回429/403，**分节已读（索引文本）**，未取得PDF逐页核验，非全文精读。

**研究问题/方法/模型：** 以12状态`(x,y,z,vx,vy,vz,roll,pitch,yaw,p,q,r)`描述三维位置、速度、欧拉角与机体角速；输入为四桨平方转速混控后的`U1`总推力与`U2,U3,U4`三轴力矩。§3用6个调度量`(roll,pitch,yaw,p,q,Omega_p)`构造qLPV模型，使用上次优化轨迹预测调度，滚动名义MPC采用`N_p=5`和MATLAB fmincon SQP。§3垂向动力学含`U1 cos(roll)cos(pitch)/m-g`；人为加入小`epsilon≈0.001`以改善矩阵可控性，不能视作无误差物理真值。

**量测、丢包/噪声、SMF类型：** 已核验章节没有定义实际传感器测量矩阵、测量噪声界或丢包；仿真使用状态/调度量，未核验独立传感器。没有状态SMF，也没有参数SMF；调度参数轨迹预测不是集员滤波。

**约束/理论/实验：** 文中MPC讨论状态/输入约束与四桨转速映射，但本轮未核验四电机饱和在任意不确定性下严格保持；未核验终端RCI、鲁棒输出反馈递归可行或硬约束全时域定理。MATLAB/Simulink R2019b、MacBook Air双核1.8GHz i5/8GB，10ms采样、直线/螺旋轨迹数值仿真；优化平均6.14ms、样本最坏8.76ms，不是形式化WCET；§6把风扰鲁棒性和实飞列为未来工作。

**主要结论/局限/课题关联：** 12状态名义qLPV-MPC在作者仿真平台能快速轨迹跟踪，但不是有噪间歇位置SMF+鲁棒Tube MPC的现成证明。可复用四输入物理混控、推力方向耦合、调度预测与计算基线；不能将其6.14ms移植到本仓库20ms WCET，也不应因为12维更高而淘汰六状态平面。**待查问题：** 如果引入qLPV调度，如何认证`epsilon`建模误差、未测调度变量和有噪失测下的全部未来调度分支，且保留终端信息集合可移位闭合？**本轮独立研究证据：** `docs/research/model_selection/background_run_20261101_1735_qlpv_hover.md`。

---

## Run254 — Qiu等（2020）终端RPI与有噪后验复核（2026-11-01；历史已读，不新增去重篇数）

**题名：** *Output feedback model predictive control based on set-membership state estimation*；**作者：** Quanwei Qiu、Fuwen Yang、Yong Zhu、Eman Mousavinejad；**出版：** *IET Control Theory & Applications* 14(4):558–567 (2020)；**DOI：** https://doi.org/10.1049/iet-cta.2019.0881；**开放正文：** https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-cta.2019.0881。**阅读日期/核验层级：** 2026-11-01再次核验出版社开放正文§2 Assumptions 1–2、§3.1 Theorem 1、§3.2式(19) minimax、§4终端RPI与稳定性条件；分节重读，非新读/非终版逐式复核。**问题/模型/方法：** 有界过程和量测噪声下的线性时变、部分状态测量、椭球状态SMF（不是参数SMF）及LMI/半定规划输出反馈MPC。**关键假设与结论：** 初始椭球和有界扰动/噪声、SMF递归包含条件；鲁棒终端正不变集合与局部反馈是稳定/可行性结论所需的额外结构，不能由一次成功量测推出。**局限：** 不含本仓库非线性正弦Euler、间歇位置包自动机及真实关联后验。**关联/可复用：** 估计集合包含、MPC预测硬约束、终端可移位条件分开检查。**本轮新独立结果：** Run254在强制成功位置包后仍构造同测量历史、不同隐藏速度的两条合法路径；参见`docs/research/run254_research_log.md`和`results/forced_success_velocity_alias_20261101/checks.json`。**待查：** 真实关联后验在所有成功读数和后续miss分支下能否形成共享因果安全前驱？**去重已读仍101篇。**

---

## 背景模型选型第7轮 — Lee、Leok、McClamroch（2013）SE(3)四旋翼鲁棒跟踪（2026-11-01；新增分节已读1篇，去重100→101篇）

**题名/作者/正式出版：** *Nonlinear Robust Tracking Control of a Quadrotor UAV on SE(3)*；Taeyoung Lee、Melvin Leok、N. Harris McClamroch；*Asian Journal of Control* 15(2):391–408 (2013；2012-07-05在线)，DOI https://doi.org/10.1002/asjc.567 。**公开原文：** arXiv:1109.4457v1 (2011-09-21)，https://arxiv.org/pdf/1109.4457 。**实际阅读日期/范围/状态：** 2026-11-01，核对公开预印本PDF pp.1–6 §II式(1)–(6)、§III Propositions 1–2、§IV式(20)–(39)/Propositions 3–4、§V数值例子；**分节已读**，未将2013期刊终版或附录全文冒充逐式核验。出版信息经期刊 https://onlinelibrary.wiley.com/doi/abs/10.1002/asjc.567 交叉核对。

**研究问题/方法/真实模型与输入：** 四旋翼在平移/转动有界不确定性下的姿态和位置鲁棒跟踪；`(x3,v3,R∈SO(3),Ω3)`是12维**局部独立坐标**、6个物理自由度的刚体模型（旋转矩阵不是9个独立角度状态）；输入为总推力`f`与三轴力矩`M`，由四桨推力经式(1)混控。姿态模式使用`(R,Ω)`，位置模式保留`fRe3`的耦合动力学。连续时间几何非线性反馈与模式切换，**不是MPC/Tube MPC**。

**测量、SMF、噪声/丢包：** 反馈直接使用`x,v,R,Ω`，论文未建立部分观测测量矩阵、速度隐藏、位置丢包/延迟、测量噪声或SMF/CZ（既非状态SMF也非参数SMF）；“output tracking”不等于output-feedback estimation。扰动假设`||Δx||≤δx,||ΔR||≤δR`，不是仓库控制相关残差界。

**约束/重要定理/结论：** Propositions 2–4在姿态初始域、参考光滑性、增益及扰动界等前提下给出姿态/位置跟踪误差一致最终有界；没有证明本仓库状态/执行器硬盒的逐拍安全、饱和后递归可行、SMF可靠集合包含或MPC终端不变性。论文给四桨混控公式，但没有将仓库的`T,τ`硬饱和和控制依赖残差纳入定理。**实验：** §V数值仿真（椭圆螺旋跟踪、倒置姿态恢复），未核验实飞或20ms最坏时延。

**与本课题关联/可复用与局限：** 推力方向耦合`fRe3`支持六状态平面`Tcosφ`物理闭合；姿态/位置模式支持分层方案的背景，但需独立认证内环误差与硬约束。已有鲁棒四旋翼几何跟踪不构成本课题新颖性；潜在创新在有噪间歇位置SMF/CZ与共享因果MPC安全信息状态。**待查问题：** 在原六状态hover初始盒和success/miss后验下，是否存在非空共享推力一拍前驱，并能进一步形成可移位终端信息核？**研究日志：** [背景第7轮](../research/model_selection/background_run_20261101_1634_lee_vertical_fiber.md)。

---

## Run253 — Yang与Ozay（2021）强制恢复测量与共享因果前缀重读（2026-11-01；去重100篇不变）

**题名/作者/出版：** *Safety Control Synthesis for Systems with Missing Measurements*；Liren Yang、Necmiye Ozay；ADHS 2021，*IFAC-PapersOnLine*，pp.97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，公开原文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**本轮实际阅读：** 2026-11-01再次核对§3式(3)–(7)、§4.2–4.4（含Proposition 4/5），此前Run248/251已分节阅读，**不新增论文去重数**。

**研究问题/方法/假设/结论：** 在自动机约束的完整状态测量丢失下，利用string automaton、因果共享开环前缀及产品系统安全游戏求不变核；成功测量为完整无噪状态`y=x`，失败为无读数；其Proposition 4/5有紧集、连续性及Assumption 1等条件。**局限：** 非四旋翼、非有噪位置-only SMF/CZ、无本仓库固定推力四状态控制器、无20ms时限认证；不能直接迁移其无限时域不变核结论。

**与课题关联/可复用技术：** 丢包自动机和控制前于未知success/miss的量词顺序。Run253在Run251/252特定真实双轨迹上，精确证明第25–30拍非零共享力矩有限安全及第30拍强制成功位置读数必然区分两路径（位置差至少0.29623244875m，噪声读数差至少0.25623244875m）；这是**本仓库独立数学证书，不是该论文结论**。**待查问题：** 第30拍各成功分支能否对全部SMF一致状态建立非空后继闭合终端信息集合？**日志：** [Run253](../../archive/legacy_planar_direct_control_20261103/docs/research/run253_research_log.md)。

---

## Run252 — Cosner等（2021）测量鲁棒CBF与安全备份（2026-11-01；新增分节已读1篇，去重99→100篇）

**真实题名/作者：** *Measurement-Robust Control Barrier Functions: Certainty in Safety with Uncertainty in State*；Ryan K. Cosner、Andrew W. Singletary、Andrew J. Taylor、Tamás G. Molnár、Katherine L. Bouman、Aaron D. Ames。**发表：** 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2021)，DOI https://doi.org/10.1109/IROS51168.2021.9636584 ，arXiv:2104.14030，作者公开正文 https://arxiv.org/pdf/2104.14030 （v1，2021-04-28）。**阅读日期/层级：** 2026-11-01，实际核对六页预印本§II-A/B、§III-A/B（Theorems 2–3、式(13)–(17)）及§IV实验；**分节已读**，未对IEEE终版逐式比对。

**研究问题/方法/模型：** 在状态估计有已知误差集合时，如何将measurement-robust control barrier functions (MR-CBF)与已知control-invariant backup set结合？一般理论为连续时间control-affine `xdot=f(x)+g(x)u`，非MPC；实验为四状态Segway `(position,forward velocity,pitch,pitch rate)`，输入车轮力矩（硬件饱和±20 Nm），不是四旋翼，也不是参数SMF或状态SMF/CZ滤波器。视觉VIO位置估计、编码器/IMU辅助估计；没有离散位置包丢失自动机、推力调度或本项目的隐藏速度-only位置测量合同。硬件Jetson TX2+ECOS SOCP，250Hz运行；报告仿真及真实Segway实验。

**重要定理/假设：** §II-B式(7)的隐式安全集要求存在**预先已知的控制不变备份集和备份控制律**，且备份轨迹在T时间内进入该集合。§III-A Theorem 2要求测量误差 `e(x)∈E(y)` 的已知界、CBF及Lie导数Lipschitz常数和满足测量鲁棒CBF不等式的Lipschitz控制器；§III-B Definition 4/Theorem 3在MRISS与全部式(16)条件满足时给出前向不变性。§IV实验误差界采用0.4m，备份预测T=1s、积分步5ms。论文不证明本仓库离散有噪SMF＋MPC无限时域递归可行；其数值求得Lipschitz界部分来自采样，不可直接视为我们模型的全域严格界。

**主要结论与局限：** 给出基于误差界收紧的测量鲁棒安全备份SOCP，Segway实验对比无鲁棒性的BS-QP；其安全结论有明确的备份不变集、正则性及优化可行性前提，不含有界独立外扰下的四旋翼终端信息状态后继闭合证明。

**本课题关联/可复用：** 可借鉴“先认证非空不变备份集、再扩张安全域”的论证顺序与误差界收紧；不能用有限55拍零尾充当论文的无限不变备份集。Run252针对特定Run251零力矩前缀及合法 `SSSMM` 观测串，精确得到第25拍速度投影必要直径1.3391329875m/s；这是仓库独立证书，**不是Cosner等论文结果**。**待查问题：** 能否在该真实双速度纤维上构造共享因果非零备份、并认证下一次必成功位置测量之前及其后继的安全集合闭合？**研究日志：** [Run252](../../archive/legacy_planar_direct_control_20261103/docs/research/run252_research_log.md)。

---

## 背景模型选型第5轮 — Song、Nuske、Scherer（2017）多传感器MAV估计（2026-11-01；新增分节已读1篇，去重98→99篇）

**题名/作者**：*A Multi-Sensor Fusion MAV State Estimation from Long-Range Stereo, IMU, GPS and Barometric Sensors*；Yu Song, Stephen Nuske, Sebastian Scherer。**出版**：*Sensors* 17(1):11 (2017期；2016-12-22在线)，DOI https://doi.org/10.3390/s17010011 ；**作者公开全文** https://publications.ri.cmu.edu/storage/publications/2016/12/sensors-17-00011.pdf 。**阅读日期/状态**：2026-11-01，实际分节阅读§4.1–4.4（PDF pp.11–15，式15–40）、§5.3–5.5（pp.20–24）、§6；未复现，不冒充全文逐式审计。

**研究问题与方法/模型**：为MAV在间歇GPS、强运动和高空视觉条件下提供状态估计；IMU积分和含陀螺/加计偏置的**随机**误差状态EKF，式(19)为`S=(p3,delta_theta3,v_body3,delta_b_g3,delta_b_a3)∈R15`，式(26)增广上一视觉位姿6维成21维stochastic cloning EKF，使用VO相对6维位姿、气压计高度及GPS绝对测量。**关键量测纠偏**：§4.4 GPS最终直接测水平**位置和速度**`(p_n,p_e,v_n,v_e)`，非仅位置；IMU提供加速度/角速率。本文没有MPC控制律或推力/力矩输入约束。§5.4以记录数据关闭GPS更新60秒及约120秒评估估计漂移；§5.5报告EKF链约2–3ms、VO约28–144ms（硬件依赖）。

**定理/假设/结论/局限**：式(15)–(17)假设高斯IMU噪声和缓慢变化偏置，式(29),(38)协方差传播/更新；相对VO帮助减缓GPS失测时漂移。论文**没有SMF/CZ状态集合包含定理、MPC/Tube MPC、终端RCI、硬状态/输入约束或无限递归可行性证明**；其3σ带是随机统计量，不能冒充所有有界扰动下的硬保证。实证为公开数据/真实飞行记录分析，不是本文证明飞行安全。

**本课题关联与可复用技术**：借鉴保留历史位姿关联/相对观测更新的思想，但现有仓库只每5拍有噪位置和每拍姿态/角速，无GPS速度/IMU/VO/气压计、无测量延迟；若引入这些传感器需新合同、偏置/延迟队列及可靠SMF集合传播。当前优先完成Run249–251的共享因果终端可行性；不能用15/21维滤波状态替换6维物理模型。**待查问题**：是否能在原位置-only合同下证明非空终端信息状态？如加入IMU/VO，其有界误差和时间关联如何认证？**背景日志**：[第5轮](../research/model_selection/background_run_20261101_1437_song_gamagedara.md)。

---

## Run251 — Yang与Ozay（2021）丢包因果安全控制定向重读（2026-11-01；去重98篇不变）

**题名/作者：** *Safety Control Synthesis for Systems with Missing Measurements*；Liren Yang、Necmiye Ozay。**正式发表：** ADHS 2021，*IFAC-PapersOnLine*，pp.97–102；DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ；作者公开正文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**阅读状态：** 2026-11-01重新阅读§3式(3)–(7)、§4.2–4.4及Proposition 4/5；历史Run248已分节阅读，故不新增去重数，未宣称逐式复核全文。

**研究问题/方法：** 具有自动机约束的完整状态测量丢失时，如何利用string automaton和因果控制承诺将部分信息安全问题转换为产品系统安全游戏。成功时观测`y=x`、失测时`y=∅`；无本仓库的成功位置有界噪声、隐藏速度和每拍姿态有噪SMF。**主要理论条件与结论：** 在论文Assumption 1的测量模式、产品系统紧性和连续性条件下，Proposition 4/5建立不变核与winning set联系；不能直接替代有噪位置SMF的终端递归可行性证明。**局限/课题关联：** 控制不能预知下一次测量何时成功，真实共享观测历史下必须施加相同因果动作。Run251独立推导15拍两条不可区分真实扰动路径的速度投影直径必要下界0.5275372375m/s，**不是Yang/Ozay原文结果**。可复用：丢包自动机、因果量词、信息状态安全游戏。待查：如何将共享观测速度纤维与四状态非零备份的后继闭合检验结合？详见[Run251日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run251_research_log.md)。

---

## 背景模型选型第4轮 — Panda与Guo（2026）GNSS/IMU延迟融合（2026-11-01；新增分节已读1篇，去重97→98篇）

**题名：** *Belief-Adaptive Online Autonomy for Quadrotor UAV Navigation under GNSS Degradation in Urban Environments*。**作者：** Deepak Kumar Panda; Weisi Guo。**年份/出版状态：** 2026-09-13 arXiv预印本，arXiv:2609.14806；https://arxiv.org/abs/2609.14806 ，公开正文 https://arxiv.org/html/2609.14806 。**未核验同行评审发表或DOI，不能写作期刊论文。**

**阅读日期/状态：** 2026-11-01；公开正文§I、§II-A–C式(1)–(11)、§III-A/B式(12)–(21)、§IV式(22)–(27)与Algorithm 1、§V-A/B、§VI **分节已读**；未逐式证明审计或代码复现。

**研究问题：** 四旋翼城市飞行中，GNSS多径、位置偏置和测量延迟使传统GNSS/IMU融合误差增大，如何在线自适应测量可信度？**方法/模型：** 真值为12状态刚体`s=(p3,v3,roll,pitch,yaw,p,q,r)`，输入总推力和3轴力矩；估计器为9状态`(p3,v3,bias3)` EKF，IMU加速度高频预测、GNSS`z=p+b+nu`位置更新，延迟到达时回溯更新历史状态并重传播；信任变量`beta`经NIS驱动的二阶在线更新调节协方差。**SMF类型：** 既非有界状态SMF，也非参数SMF；是随机EKF和自适应协方差。**控制：** 外环PID加速度、内环姿态PD，非MPC。

**重要假设/理论保证：** 采用随机过程/量测噪声、多径偏置与有上限的模拟延迟；没有本项目“每5拍位置机会、最多miss两次”的确定性丢包模型、全样本有界集合包含、输入/状态硬约束终端、输出反馈MPC递归可行性定理。**实验/结论：** Python模拟12状态飞行，IMU200Hz、GNSS/控制20Hz、最大延迟1.2s、10条城市任务；论文报告估计误差和跟踪误差分别改善约80%/30%（仅其仿真与基线），没有实飞验证或WCET。**局限：** 预印本未经核验同行评审，概率协方差不等于确定性安全集合；加入IMU将改变仓库现有观测权限。

**与本课题关联/可复用：** 有依据地解释GNSS低频/延迟与高频IMU多速率背景；可参考历史回溯观测更新，但必须重新定义有界偏置、延迟信息状态及集合包含证明。仓库Run249仅55拍安全、Run250零备份67拍上限不因EKF结果而改变。六状态平面模型仍为条件性物理首选，四状态仍为实际已验证的闭环/反例基线。**待查：** IMU辅助实验是否需要增广加速度偏置与延迟队列？在原量测权限下能否先完成非空终端信息状态？**研究日志：** [背景第4轮](../research/model_selection/background_run_20261101_1335_gnss_belief.md)。

**旁证不计已读：** Gamagedara、Lee、Snyder (2021), *Quadrotor State Estimation With IMU and Delayed Real-Time Kinematic GPS*, IEEE TAES 57(5):2661–2673, DOI https://doi.org/10.1109/TAES.2021.3061795 ，仅IEEE摘要核验，未核对正文模型/定理。

---

## Run250 — Wabersich与Zeilinger（2023）预测控制障碍函数（2026-11-01；新增分节已读1篇，去重96→97篇）

**题名：** *Predictive Control Barrier Functions: Enhanced Safety Mechanisms for Learning-Based Control*。**作者：** Kim P. Wabersich; Melanie N. Zeilinger。**年份/正式出版：** 2023，*IEEE Transactions on Automatic Control* 68(5):2638–2651。**DOI：** https://doi.org/10.1109/TAC.2022.3175628 。**公开正文：** https://arxiv.org/abs/2105.10241 （2021初稿、2022更新；与2023期刊终版逐式一致性尚未核验）。

**阅读日期/核验状态：** 2026-11-01；实际分节阅读公开正文§1、§2.1、§3.1–3.3、§4，特别是式(5f)、Definition 3.1式(13)、Assumption 1、Theorem 3.4/3.6及终端CBF设计思路；**分节已读，不冒充期刊终版逐式精读**。IEEE期刊DOI、卷期、页码由作者公开书目及DBLP独立核验。

**研究问题：** 当预测安全过滤器因初态不可行或未建模扰动而失效时，如何引入可恢复的软约束机制，同时对原安全过滤可行域给出稳定性分析？

**方法/模型：** 离散时间非线性系统，性能控制器外置，预测安全过滤(PSF)要求预测终点进入安全终端集合；通过沿预测时域逐级收紧的软约束、终端控制障碍函数和预测障碍值函数构造恢复机制。论文给出线性2D与非线性车辆数值案例；不是有噪间歇测量四旋翼状态SMF。**状态估计/参数估计：** 本文不是状态SMF或参数SMF论文；使用全状态名义控制模型，不能与Didier等2021的参数SMF混淆。

**重要定理/假设：** 式(5f)要求终端安全集；Definition 3.1给出离散CBF在安全集内后继闭合、集外下降的条件；Assumption 1要求终端CBF存在；Theorem 3.4在不变域等条件下给出安全集不变与渐近稳定；Theorem 3.6还需终端与软约束、连续性等条件，不能跳过。**主要结论：** 在完整假设成立时，软约束预测障碍函数可使原PSF可行域获得恢复机制，区别于单纯将优化问题改成总能求解。

**局限：** 软约束优化可行不等于所有物理硬约束在不可行初态下仍满足；本文没有直接处理有界有噪位置丢包SMF、共享因果控制、四状态对抗横向残差。不得直接迁移其全时域安全定理。

**与课题关联：** Run249的55拍零尾只是固定截止时间合同；Run250精确证明固定零备份对全初始盒最多67拍，68拍有真实角点越界。文献强调终端安全集必须存在后继闭合控制，Run249尚无这一条件。**可复用技术：** 终端控制律与安全集合证明清单、PSF旧计划移位、将不可行恢复与硬安全保证分开评价。**待查问题：** 在真实5拍success/miss和SMF后验信息状态上，能否构造非空共享因果终端控制集合？软约束恢复应如何作为非安全诊断通道而非硬安全证明？

**本轮独立数学证据：** [Run250研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run250_research_log.md)；精确Fraction真实角点第68拍反例。去重计数从96增加至97；历史Wabersich与Zeilinger（2021）*A predictive safety filter...*仍为不同论文的仅摘要核验记录，不在本轮升级已读。

---

## 背景模型选型第3轮 — Miladi等（2020）位置＋角度量测的四旋翼观测器ENMPC（2026-11-01；首次公开正文分节已读，去重95→96篇）

**题名：** *Explicit nonlinear model predictive control tracking control based on a sliding mode observer for a quadrotor subject to disturbances*。**作者：** Nadia Miladi; Habib Dimassi; Salim Hadj Said; Faouzi M’Sahli。**出版：** *Transactions of the Institute of Measurement and Control* 42(2):214–227 (2020)，2019-08-07在线首发。**DOI：** https://doi.org/10.1177/0142331219865816；**期刊页面：** https://journals.sagepub.com/doi/10.1177/0142331219865816；**公开正文：** https://www.researchgate.net/publication/335024865_Explicit_nonlinear_model_predictive_control_tracking_control_based_on_a_sliding_mode_observer_for_a_quadrotor_subject_to_disturbances。

**阅读日期与核验状态：** 2026-11-01；实际核对公开正文§2式(1)模型与量测、§3 ENMPC展开、§4式(19)–(32)与A1/A2、§5 Proposition 1/2和输入QP式(35)、§6仿真及附录Lyapunov思路；标为**公开正文分节已读**，不是期刊终版逐式核验，公开转录公式存在排版损失。此前唯一日志按DOI/标题核对未登记此文。

**研究问题：** 四旋翼只测位置和姿态角、线/角速度与气动扰动未知时，如何利用观测器辅助预测控制完成轨迹跟踪？**方法/模型：** Newton–Euler 12状态，`X=(φ,φdot,θ,θdot,ψ,ψdot,z,zdot,x,xdot,y,ydot)`；四输入 `(U1,U2,U3,U4)` 为总推力及姿态力矩通道；测量 `Y=(φ,θ,ψ,z,x,y)`（无速度直接量测），跟踪输出 `(x,y,z,ψ)`。级联高增益近似微分器＋滑模未知输入点观测器，ENMPC在输入盒约束下改为在线凸QP。**无SMF/CZ集合状态估计、无明确位置丢包自动机**。

**重要假设/定理：** Assumptions A1角速度有界、A2扰动有界且相对观测器变化缓慢；§4匹配条件 `rank(CD)=rank(D)` 不成立，借辅助输出处理。Proposition 1在条件下证明跟踪误差最终进入可调小紧集；Proposition 2给出四输入盒约束QP，并非全部状态硬约束或信息状态终端递归可行性定理。**主要结论：** 论文以位置＋角度量测构建点状态/扰动估计辅助的四旋翼ENMPC，数值仿真展示跟踪。**局限：** 连续可用量测、没有success/miss和SMF可靠后验，未提供本仓库全部对抗扰动下硬状态安全、20ms WCET或实飞证明。

**与课题关联：** 反证“未测速度＋四旋翼输出反馈MPC”是新组合的说法；本项目真正待验证缺口为有噪间歇位置、状态SMF/CZ、共享因果控制与硬约束安全终端。**可复用技术：** 12状态到位置/角度量测的观测权限建模、辅助输出与点估计基线、输入QP构造；不可将点估计收敛视为集合包含或递归安全。**待查问题：** GPS/位置包丢失时高增益/滑模观测器如何退化？能否在六状态平面模型上构造信息状态安全前驱并与Run249有限安全过滤形成对照？**本轮工件：** [模型矩阵](../research/model_selection/MODEL_SELECTION_EVIDENCE.md)、[研究日志](../research/model_selection/background_run_20261101_1233_miladi.md)。

---

## Run249 — Qiu等（2020）椭球状态SMF＋输出反馈MPC终端条件复核（2026-11-01；历史已读去重95篇不变）

**题名/作者/出版：** *Output feedback model predictive control based on set-membership state estimation*；Quanwei Qiu、Fuwen Yang、Yong Zhu、Eman Mousavinejad；*IET Control Theory & Applications* 14(4):558–567 (2020)。**DOI与原文：** https://doi.org/10.1049/iet-cta.2019.0881 ；https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-cta.2019.0881 。**阅读日期/核验状态：** 2026-11-01，重新分节阅读开放正文§2、§3.1–3.2（Theorem 1、式(19)）、§4（终端RPI条件）与§6；历史已读，**不是新读一篇，也不是逐式全文核验**。

**研究问题：** 有界过程/量测噪声下不可测状态的约束预测控制。**方法/模型：** 线性时变/多面体不确定系统，椭球集员状态估计（先预测后量测更新）、基于后验椭球的有限时域minimax/LMI MPC。**关键定理与假设：** Theorem 1给出在适当LMI条件下的估计椭球包含；§4的稳定/可行性论证需要鲁棒正不变终端集合、终端反馈及相应附加约束，不是有限安全管自动成立。**结论：** 论文在相应假设下给出估计—控制—约束一体化框架及数值/DC-DC变换器案例。**局限：** 没有本仓库四旋翼有噪位置-only丢包自动机、非线性正弦和独立极端残差；LMI框架也不能直接赋予Run249的55拍回退无限安全。**关联/可复用：** 状态SMF后验驱动优化、估计集合包含与终端RPI条件分离。**待查问题：** 如何把Run249固定截止时域的零尾安全合同转化为一个非空、对所有success/miss边闭合的共享因果信息状态终端合同？参考 [Run249日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run249_research_log.md)。

---

## 背景模型选型第2轮 — Xue等（2024）有噪全运动学输出的分层随机MPC（2026-11-01；首次分节已读，去重94→95篇）

**题名：** *Output feedback stochastic MPC for tracking control of quadrotors with disturbances*。**作者：** Ruochen Xue; Li Dai; Peizhan Wang; Zhongqi Sun; Yuanqing Xia。**出版：** *IET Control Theory & Applications* 18(5):566–580 (2024)，线上首发2023-10-18，正式卷期2024-03-11。**DOI/原文：** https://doi.org/10.1049/cth2.12588 ; https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/cth2.12588 。**阅读日期/状态：** 2026-11-01；期刊开放正文§2.1–2.3式(2.1)–(2.15)/Assumption 1–2、§3.1–3.4（Theorems 1–2、Problem 1、Algorithm 1）、§4（Theorems 3–4/ESO）、§5–6仿真/局限**分节已读**；未复现推导与仿真，不标全文逐式核验。

**研究问题：** 四旋翼在有噪测量、随机阵风、姿态跟踪误差和机会约束下的轨迹跟踪。**实际模型/控制输入：** 平移6状态 `xi_s=(xp,xv,yp,yv,zp,zv)` 加Dryden风滤波3状态 `xi_w`，外环MPC增广9状态 `x=(xi_s,xi_w)`，输入 `u=(ux,uy,uz)` 是三轴虚拟惯性加速度，由总推力和姿态角映射（式2.4、3.42）；内环3个二阶姿态通道用ADRC和三阶ESO，并非9状态统一MPC。**实际量测：** 式(2.3) `C_xi=I6`、式(2.11) `C=[I6,0]`，故每拍可得到带噪的三轴**位置和速度**，仅风状态隐藏；**没有位置-only/有界丢包**。状态估计为Luenberger observer，**不是SMF状态后验或参数SMF**。

**关键假设/定理：** Assumption 1噪声已知、独立、紧支撑分布；`A-LCA` 与 `A+BK` Schur。Theorem 1用概率分位数及最坏支持构造机会约束充分收紧，Problem 1引入近似最大允许终端集以支持shift递归可行；Theorem 2给出期望时间平均二次成本上界，不是逐路径硬安全/零误差渐近稳定。内环Theorems 3–4需扰动及导数有界、观测器和控制带宽满足条件。原文Assumption 1“Gaussian且紧支撑”文字与普通高斯性质冲突，§5实际使用截断高斯，应按截断分布理解而不能无条件搬用。

**主要结论/实验：** §5 MATLAB/YALMIP/SeDuMi仿真、外环 `Ts=0.05s`、内环 `Tsr=0.01s`、MPC `Tp=7`、100组噪声；机会约束概率阈值0.8，数值违约率低于20%。**局限：** 非本项目对抗扰动硬约束、位置每5拍success/miss、隐藏速度关联SMF；虚拟加速度约束不等于真实旋翼 `(T,tau)` 可行域；没有20ms WCET、实飞或完整物理输入硬安全证书。

**与本课题关联/可复用技术：** 已有“四旋翼+输出反馈+MPC”直接近邻，不能以术语组合主张创新。可复用：分层外环/内环接口、observer-error与控制误差耦合、shift-compatible终端及扰动收紧的证明结构；必须重新构造位置-only间歇观测的SMF/CZ和共享因果控制，明确内环误差集合与执行器约束。**待查问题：** 是否有论文在真实位置-only/丢包量测下给出四旋翼输出反馈鲁棒MPC硬约束递归安全；六状态平面系统是否能构造非空信息状态可生存核？

**本轮工件：** [模型证据矩阵](../research/model_selection/MODEL_SELECTION_EVIDENCE.md)、[独立背景日志](../research/model_selection/background_run_20261101_1136_xue_output.md)。只做正文证据与静态模型对照，未增加控制验证脚本。

---

## Run248 — Yang/Ozay (2021) 间歇量测安全综合分节重读（2026-11-01；已读去重94篇不变）

**题名：** *Safety Control Synthesis for Systems with Missing Measurements*。**作者：** Liren Yang; Necmiye Ozay。**出版：** 2021，*IFAC-PapersOnLine* 54(5):97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ；**公开全文：** https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**阅读日期/状态：** 2026-11-01，重新阅读§3 Assumption 1/Problem 1、§4.1–4.4 string automaton、因果承诺、Proposition 4–5；历史已读，本轮**重读而非新增**，统一去重总数仍94篇（含背景任务Sasfi 2023）。

**研究问题/模型：** 离散系统在有界扰动、自动机约束的间歇**完整状态**观测下，如何综合无限时域硬安全控制；成功包提供无噪完整状态，丢包时无状态测量。**方法：** string automaton和product safety game，控制必须在不知道下一次成功包何时出现时因果承诺控制序列。**假设与重要结论：** Assumption 1约束丢包语言、存在成功包及有限连续丢包；Proposition 4–5在紧性/连续性及自动机假设下建立product不变集与原问题安全控制的关系。**局限：** 不能直接处理本仓库有噪位置、每拍有噪姿态、隐藏速度的关联CZ后验。**与本课题关联/可复用：** 在第10拍或更早设计共享因果前缀，覆盖success/miss全部边；Run248的第14拍全状态不可恢复角点说明不能把第15/25拍成功位置包当成已失效前缀的补救。**待查：** 在每拍有噪姿态和位置间歇测量的集合值信息状态上如何构造非空安全前驱？**研究工件：** docs/research/run248_research_log.md。未将此文的理论结论冒充本仓库的递归可行证明。

---

## 背景模型选型任务：Sasfi/Zeilinger/Köhler (2023) 六状态平面四旋翼与参数SMF（2026-11-01；首次核验正文分节阅读，去重93→94篇）

**题名：** *Robust adaptive MPC using control contraction metrics*。**作者：** András Sasfi; Melanie N. Zeilinger; Johannes Köhler。**年份/出版：** 2023，*Automatica* 155:111169。**DOI：** https://doi.org/10.1016/j.automatica.2023.111169 。**arXiv：** https://arxiv.org/abs/2209.11713 （v2，2023-07-11）；**公开全文：** https://arxiv.org/html/2209.11713v2 。

**阅读日期与核验状态：** 2026-11-01；实际核对公开作者稿§2.1、§3.1（Assumption 1）、§3.2（Theorem 6）、§3.3（Proposition 7）、§3.4（Assumption 10）、§3.5（Theorem 12）、§4数值案例及动力学/约束/实现。标记**分节已读**，不是附录或期刊终版全文逐式核验。历史`READ_PAPERS.md`及本日志旧节仅有该论文的简短书目/方法关联，未有可核验的实际分节阅读记录；本轮按DOI去重后新增1篇阅读证据，既有书目不另计。

**研究问题：** 连续时间非线性系统有界加性扰动与未知固定参数下，如何在鲁棒状态/输入约束下使用在线参数更新降低Tube MPC保守性？**实际模型：** §4平面四旋翼六状态 `x=(p1,p2,phi,v1_body,v2_body,omega)`；p为惯性系位置、v为**机体系速度**；控制输入为两旋翼推力`u=(u1,u2)`，合推力与力矩由`u1+u2`、`l(u1-u2)`得到。**量测/失测：** §2.1与§3.3假设完整状态与输入精确可测、状态导数有界噪声；没有位置包丢失模型。**SMF类型：** 仅用有界导数噪声和模型方程对未知常参数`theta=1/m`构造非否证集合并交集更新`Theta_t`（式14）；**不是**对隐藏速度的状态后验SMF。

**不确定性与硬约束：** §4`theta=1/m`初始相对不确定性±1%、`d∈[-0.1,0.1]`；`|phi|≤pi/3`、`|omega|≤pi`、`|v1|≤2`、`|v2|≤1`、`u_i∈[-1,3.5]`及避障；负推力数学下限不可未经执行器解释直接用于真实旋翼。**方法：** CCM合成增量反馈与homothetic tube（Theorem 6），多面体参数SMF（Proposition 7），联合优化名义参数、名义轨迹及tube尺度的RAMPC（式18）。**关键定理/假设：** Assumption 1要求约束域上存在CCM；Assumption 10要求终端正不变、约束与下降及对参数/管束收缩单调性；Theorem 12在上述条件及初始MPC可行时证明递归可行、连续模型硬约束满足和**名义轨迹**趋近参考邻域/参考（具体以定理为准），不保证本项目的有噪输出反馈递归安全。

**主要结论与实验：** §4六状态平面四旋翼仿真展示参数SMF更新可减少tube保守性、改变避障路径；RK4、Ts=150ms、N=25（3.75s）、MATLAB/CasADi/IPOPT、笔记本仿真；文中采样点数值施加约束，不是实飞或20ms WCET。**局限：** 需要全状态反馈、CCM存在、终端集合及较小扰动；其风扰±0.1与本仓库在T=9.81N处水平约±2.029、垂向约±3.079的残差界相差很大，不能直接移植可行性结论；其机体系速度不同于仓库惯性系速度。

**与课题关联：** 文献证明六状态平面四旋翼是严肃的鲁棒MPC模型候选，也提醒“SMF+Tube MPC+平面四旋翼”不是可单独主张的新颖组合。可复用：CCM/tube随状态与参数变化的设计思路、参数集合嵌套与终端单调性条件；若本课题保留有噪位置/失测，则需**另外**构造状态SMF及同观测纤维共享控制。**待查问题：** 现有六状态配置的双向扰动下是否有非空信息状态可生存核？是否能用简单固定截面Tube代替复杂CCM？位置缺测时怎样把Theorem 12的真实状态初始化条件替换为集合条件？

**本轮独立证据：** [模型选型矩阵](../research/model_selection/MODEL_SELECTION_EVIDENCE.md)；[背景研究日志](../research/model_selection/background_run_20261101_1036_sasfi.md)。未修改主任务控制算法或宣称已认证六状态闭环。

---

## Run247 间歇量测安全过滤与定时CBF新论文（2026-11-01；新增分节已读1篇，去重92→93篇）

**题名：** *Robust Safety-Critical Control for Systems with Sporadic Measurements and Dwell Time Constraints*。**作者：** Joseph Breeden; Luca Zaccarian; Dimitra Panagou。**年份/出版：** 2024，arXiv预印本v3（2024-06-04），arXiv:2403.03663；公开正文 https://arxiv.org/html/2403.03663v3 ；摘要与版本 https://arxiv.org/abs/2403.03663 ；arXiv DOI https://doi.org/10.48550/arXiv.2403.03663 。未独立核验正式期刊版本，暂不填写期刊DOI。**阅读日期/状态：** 2026-11-01，实际分节阅读§II-C Rule 4、Lemma 1与Assumption 2、§III Theorem 1、§IV Lemma 3/Definition 2/Theorem 2、§V案例；**分节已读，非全文逐式精读**。**研究问题：** 在扰动、稀疏量测及执行器/量测间隔约束下，如何使真实系统始终满足安全集合。**方法/模型：** 连续时间/混合动力学，open-loop observer及误差半径上界，impulsive/continuous actuator两类robust timed control barrier functions（RIT-CBF/RT-CBF）；非四旋翼，算例为卫星交会和轨道保持。**重要假设/定理：** Rule 4每次量测提供带已知误差界的状态估计及下次量测时间界；Assumption 2要求新估计球包含于预测球；Lemma 1/3给出误差包含，Theorem 1/2在CBF可行及相关正则/时序条件下证明安全集合正向不变；不是本项目的离散有噪位置success/miss假设。**主要结论：** 通过控制时机和估计误差预测界联合构造安全过滤条件，满足相应CBF条件可得到严格安全保证。**局限：** 需要可验证的CBF存在性、误差增长界及量测时序；未解决本项目四状态非线性Euler、位置SMF后验与随机/对抗丢包的共享控制前驱。**与本课题关联：** Run247的双向速度可生存必要guard说明仅检查当前状态硬约束不足，且在第25拍位置包可能缺失时需要预测未来安全；与该文的timed uncertainty tube思想相容但不等价。**可复用技术：** 量测之间的误差半径预测、定时安全过滤器结构、CBF存在性与在线可行性条件的分离。**待查问题：** 能否把当前Fraction必要guard提升为带精确关联SMF后验的充分控制前驱，并在5拍success/miss自动机上闭合；是否存在满足该文CBF正则条件的非空安全域？

**本轮独立数学证据：** [Run247研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run247_research_log.md)、精确两侧必要速度guard及第26拍不可恢复反例。论文与Run246新增Kaynama等2015不同，不重复计数。去重已读总数从92增至93；此前只核对摘要/书目的论文不计入已读。

---

## Run246 鲁棒可生存核与四旋翼安全控制文献（2026-11-01；新增分节已读1篇，去重91→92篇）

**题名：** *Scalable Safety-Preserving Robust Control Synthesis for Continuous-Time Linear Systems*。**作者：** Shahab Kaynama; Ian M. Mitchell; Meeko M. K. Oishi; Guy A. Dumont。**年份/出版：** 2013预印本，2015 *IEEE Transactions on Automatic Control* 60(11):3065–3070。**DOI：** https://doi.org/10.1109/TAC.2015.2411872 ；**公开预印本：** https://arxiv.org/abs/1312.3399 。**阅读日期/核验状态：** 2026-11-01，实际阅读arXiv公开正文§1、§2（Definition 1–2与对抗扰动量词）、§5.3及§6（12维四旋翼飞行包线）；2015期刊终版具体公式未逐式对照，标记为**分节已读而非全文逐式核验**。书目与期刊DOI已独立核对。**研究问题：** 有界扰动和饱和执行器下，哪些状态允许无限时域保持硬安全，如何计算可用的安全控制策略？**方法/模型：** 连续时间LTI、discriminating kernel的保守内近似、robust maximal reachable sets、分段椭球及安全/性能混合控制器。**重要假设/定理：** 控制/扰动紧凸、有界动力学、连续时间全状态反馈及对抗扰动的非预见性；Definition 1–2区分有限安全与核内可生存性，§5.3讨论由有限时域构造无限安全的额外条件。**主要结论：** 在相应假设和核内近似条件下，可合成安全保护控制器；§6给出含饱和与风扰动的12状态四旋翼算例。**局限：** 不是离散Euler非线性、有噪部分观测/丢包自动机，不能直接将其安全定理移植至本仓库；论文已有此类安全核思想，本轮不将其称为创新。**与本课题关联：** Run246证明Run245的30拍有限安全管包含真实不可生存终点，必须增加终端viability guard而非只检查状态硬约束。**可复用技术：** 有限安全集合与鲁棒可生存核的量词区分、鲁棒内近似和安全后备策略筛选。**待查问题：** 如何把全状态discriminating kernel的内近似转成含SMF后验与5拍success/miss模式的可计算信息状态前驱，并确保控制器对同一观测纤维共享输入？

**既有书目未升级：** Franco Blanchini (1999), *Set invariance in control*, *Automatica* 35(11):1747–1767，DOI https://doi.org/10.1016/S0005-1098(99)00113-2 ，本轮再次核验DBLP元数据，但未阅读正文，仍**不计入已读**。

**本轮独立数学证据：** [Run246研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run246_research_log.md)、精确有理数非可生存终点证书。新增论文分节阅读计入去重已读总数92篇；未将Blanchini书目核验或数值sanity计为全文阅读。

---

## Run245 保留非零倾角与真实丢包因果控制文献复核（2026-11-01；历史已读去重91篇不变）

**Liren Yang; Necmiye Ozay (2021)**，*Safety Control Synthesis for Systems with Missing Measurements*，*IFAC-PapersOnLine* 54(5):97–102；DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ；作者全文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**阅读日期/核验状态：** 2026-11-01重新阅读原文§3 Assumption 1、§4.1–4.2 string automaton和因果控制承诺、§4.4 Proposition 4–5；既有已读，非本轮全文逐式精读。**研究问题：** 在由自动机描述的间歇全状态缺测下无限时域硬安全。**方法/模型：** string automaton、product system、控制器在不知道下一包是否成功时的开放环承诺及安全游戏不变集。**关键假设/定理：** 成功测量是无噪全状态；Assumption 1限制缺测语言；Proposition 4–5在其条件下联系product不变集与原系统安全控制。**主要结论：** 特定缺测自动机下可将部分信息综合转换为product安全游戏。**局限：** 不直接覆盖有噪位置+持续角传感器、非线性不确定集后验；不能将本文结论直接用于本项目。**本课题关联/可复用：** Run245使用每5拍机会、最多连续2次缺包的全部44个有限字串并提前承诺共享输入；需进一步实现可见SMF集合值product前驱。**待查问题：** 非空关联后验族的全部success/miss后继如何与共享反馈共同满足终端闭合？

**Johannes Köhler; Matthias A. Müller; Frank Allgöwer (2021)**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427 ；作者PDF https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf 。**阅读日期/核验状态：** 2026-11-01复核引言、§II-A Assumption 1及§III/IV框架；历史已读，非新增全文阅读。**研究问题：** 非线性有界扰动与有噪输出下的鲁棒MPC。**方法/模型：** 在线估计误差界、δ-IOSS/SMF/MHE、homothetic Tube MPC。**重要假设/定理：** 有界噪声与扰动、检测性/增量可稳定性及可靠当前/未来估计误差和估计器偏差界，结合MPC终端/移位条件。**主要结论：** 在完整假设下保证递归可行及约束，10状态四旋翼算例展示保守性改善。**局限：** Run245仅有30拍开放环可靠外包和粗区间SMF，没有在线优化与终端证书；论文保证不可直接移植。**关联/可复用：** 将双向控制权限、SMF后验可靠界与Tube收紧接口分开验证。**待查问题：** 在真实5/10/15拍失测序列和未知角度下如何构造共同终端移位证书？

**本轮独立证据：** [Run245研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run245_research_log.md)、精确Fraction外包和零力矩基线的负面权衡。两文历史已登记，不增加91篇去重计数。

---

## Run244 固定脉冲鲁棒权限反例与文献核验（2026-11-01；去重已读91篇不变）

**Johannes Köhler; Matthias A. Müller; Frank Allgöwer (2021)**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427，公开HTML https://arxiv.org/html/2105.03427v1 。**阅读日期/核验状态：** 2026-11-01实际核对原文§II-A Assumption 1、§III开头三项估计器误差合同和§IV相关接口；既有已读，非新增全文精读。**研究问题：** 非线性系统有噪输出与扰动下的鲁棒约束MPC。**方法/模型：** δ-IOSS/SMF/MHE在线估计误差界、homothetic Tube MPC。**关键假设/定理：** 有界扰动、可检测与增量可稳定性，需当前估计误差、未来估计误差及估计器偏差可靠界以支持递归可行。**主要结论：** 在其假设下可获得鲁棒约束与递归可行，展示10状态四旋翼算例。**局限：** 本项目Run243仅有无扰局部Schur，Run244证明固定角度复位脉冲在合法持续极端残差下必失效，不能套用论文保证。**关联/可复用：** 未来设计需先闭合控制权限，再构造完整SMF预测界与Tube接口。**待查：** 保留稳态倾角后如何为5拍success/miss自动机给出可计算估计误差与递归控制约束？

**Liren Yang; Necmiye Ozay (2021)**，*Safety Control Synthesis for Systems with Missing Measurements*，*IFAC-PapersOnLine* 54(5):97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 。**阅读日期/核验状态：** 2026-11-01对照历史Run240–242原文分节笔记，本轮未重新阅读全文。**研究问题：** 受约束丢包语言下的因果安全控制。**方法/假设：** 丢包自动机、product安全游戏，成功包提供无噪完整状态。**主要结论：** 在相应假设下可进行无限时域安全策略综合。**局限：** 不直接覆盖有噪部分位置测量。**关联/可复用：** Run244使用合法all-success路径反证Run243固定脉冲族的全模式安全；不能将选中使用的20/25/30拍误写为连续实际成功包间隔。**待查：** 带CZ后验的可实现product信息状态如何建立逐边闭合？

**本轮独立证据：** [Run244研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run244_research_log.md)，严格Fraction反例及单独标记的浮点sanity。两文历史已登记，唯一论文阅读记录去重91篇不变。

---

## Run243 两包速度区间与阻尼输出反馈（2026-11-01；历史已读去重91篇不变）

**Johannes Köhler; Matthias A. Müller; Frank Allgöwer (2021)**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427，全文 https://arxiv.org/pdf/2105.03427 。**阅读日期/状态：** 2026-11-01实际核对原文§II-A Assumption 1、§III开头、§IV-A/B和§V数值四旋翼实验；历史已读，非新增全文逐式阅读。**研究问题：** 非线性系统有噪输出、受扰与硬约束下的鲁棒MPC。**方法/模型：** δ-IOSS/在线估计误差界、SMF/MHE、homothetic Tube MPC。**重要假设/定理接口：** 有界扰动、可检测/增量可稳定性；递归可行需当前估计误差、未来误差及估计器与名义动力学偏差的可靠界。**主要结论：** 适当条件下约束满足与递归可行；10状态四旋翼示例展示在线误差界减保守性。**局限：** SMF全局优化成本高，不能直接处理本仓库15拍缺测及未知初始姿态；不能把本轮Schur结果当论文安全定理。**课题关联/可复用：** Run243提供特殊已知角轨迹的两包速度SMF包含界，但尚缺预测误差与终端移位合同。**待查：** Run240 CZ关联后验与预测误差合同能否支持5/10/15任意模式下统一输入裕度？

**D.Q. Mayne; S.V. Raković; R. Findeisen; F. Allgöwer (2006)**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222，DOI https://doi.org/10.1016/j.automatica.2006.03.005 。**阅读日期/核验：** 2026-11-01核对书目与公开摘要，未阅读全文；历史已登记不重复计数。**研究问题：** 有界过程与输出扰动下的线性约束MPC。**方法/模型：** 稳定观测器、估计误差RPI、Tube MPC和名义约束收紧。**关键假设/主要结论：** 误差与控制管束在相应不变性假设下保证硬约束。**局限：** 线性且要求误差集合不变；不覆盖本项目非线性角度、丢包模式。**关联/可复用：** 估计误差与控制误差分离的终端收紧合同。**待查：** 如何为带有噪角观测的冻结四状态系统构造共享因果估计误差RPI？

**独立验证：** [Run243研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run243_research_log.md)；精确Fraction Jury和两包速度区间证书、单条无扰数值闭环。固定模式局部Schur不等于任意切换鲁棒安全。已读去重仍91篇。

---

## Run242 重复脉冲局部不稳定性与文献定向阅读（2026-11-01；去重已读仍91篇）

**Liren Yang; Necmiye Ozay (2021)**，*Safety Control Synthesis for Systems with Missing Measurements*，*IFAC-PapersOnLine* 54(5):97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，作者全文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**核验状态/日期：** 2026-11-01本轮实际重读§3、Assumption 1、§4.1–4.2，历史已读不重复计数。**研究问题：** 丢包自动机下的无限时域硬约束。**方法：** 字符串自动机与控制因果性、product safety game。**关键假设/结论：** 成功包提供无噪完整状态，有限丢包串按自动机约束，策略在缺包期间必须提前承诺控制。**局限：** 与本仓库有噪位置、持续姿态量测不同。**关联/复用：** Run242的固定重复脉冲只是允许因果策略的受限特例，不能以其失败否定一般product信息状态策略。**待查：** 可否把有噪SMF后验作为product安全游戏状态并构造非空闭合域？

**Johannes Köhler; Matthias A. Müller; Frank Allgöwer (2021)**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427 。**核验状态/日期：** 2026-11-01实际阅读公开正文Introduction、§III-C集合估计、§IV输出反馈MPC概述；已有历史登记，去重已读仍91篇，不声称全文逐式验证。**研究问题：** 非线性受扰系统有噪输出下鲁棒约束满足。**方法：** 在线估计误差界、可预测估计偏差、homothetic tube MPC与MHE。**重要假设/结论：** 依赖检测性/估计误差有效性及适当递归可行条件；报告10状态四旋翼算例和减少保守性。**局限：** 未直接覆盖本项目5/10/15成功/丢包模式及控制相关扰动；无法直接借用其结论当本项目证明。**关联/复用：** 下一轮将SMF后验中心与半宽引入可实现阻尼控制，分别验证估计误差界与终端移位条件。**待查：** 固定复杂度集合降阶能否保持递归可行和20ms预算？

**项目独立证据：** [Run242日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run242_research_log.md)；精确Fraction Jacobian和判别式证明原样重复Run241脉冲的悬停平衡点局部不稳定，但不否定一般RCI或输出反馈控制。

---
## Run241 观测条件化非零力矩备份与文献复核（2026-11-01；去重已读仍91篇）

**Yang, Liren; Ozay, Necmiye (2021)**，*Safety Control Synthesis for Systems with Missing Measurements*，*IFAC-PapersOnLine* 54(5):97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，全文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**阅读日期/核验：** 2026-11-01，核对公开摘要并对照Run240已有§3–4、Proposition 2分节笔记；本轮未重读全文，既有已读不重复计数。**研究问题：** 丢包模式下因果安全控制。**模型/方法：** 字符串自动机、product game、提前承诺的输入策略。**重要假设/结论：** 成功包提供无噪完整状态、丢包语言由自动机约束；在适当假设下将部分信息安全综合化为product全信息博弈。**局限：** 本项目只有有噪位置成功包及持续姿态测量。**关联/可复用：** Run241的一次成功包后承诺15拍非零力矩是因果策略见证，不是递归product game。**待查：** 如何在5/10/15多模式下严格证明信息状态循环闭合？

**Scott, Joseph K.; Raimondo, Davide M.; Marseglia, Giuseppe Roberto; Braatz, Richard D. (2016)**，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036 ，全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。**阅读日期/核验：** 2026-11-01复核公开摘要及Run239既有Definition 3/Proposition 1–2笔记，未重读全文。**研究问题：** 有界误差下关联集合估计。**方法/假设：** 线性映射、CZ精确交集与已知有界噪声。**主要结论：** CZ可保留位置—速度相关性，代价是表示复杂度增长。**局限：** 不直接给出非线性输出反馈递归MPC。**关联/可复用：** Run241利用Run240关联生成元直接计算可见位置脉冲对速度/位置的可靠支持，而不是将隐藏状态当成可测。**待查：** 将该支持证书嵌入可降阶、可重复的SMF信息状态。两文均为既有文献，去重91篇不变。

**本轮独立结果：** [Run241研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run241_research_log.md)。10/15拍全部成功观测下，一次性15拍共享非零力矩脉冲的严格终端上界优于零力矩精确基线；5拍的同一上界方法不能认证收益。没有一般SMF-MPC递归可行性。

---

## Run240 全观测包络与丢包因果性复核（2026-11-01；去重已读仍91篇）

**Yang, Liren; Ozay, Necmiye (2021)**，*Safety Control Synthesis for Systems with Missing Measurements*，*IFAC-PapersOnLine* 54(5):97–102；DOI https://doi.org/10.1016/j.ifacol.2021.08.481；作者公开全文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。**阅读日期/状态：** 2026-11-01定向重读§3、Assumption 1、§4.1–4.2、Proposition 2；历史已读文献，不重复计数。**研究问题：** 丢包自动机约束下无限时域硬安全综合。**方法/模型：** 成功包提供无噪完整状态，缺包时用字符串自动机编码最长缺测串，按控制因果性预先承诺输入并在product game中求安全策略。**关键假设/结论：** 初始成功包、丢包连续长度有界、自动机语言满足Assumption 1；Proposition 2验证字符串自动机保留允许语言。**局限：** 不处理本仓库成功包仅含有噪位置、姿态单独持续观测的连续信息状态。**关联/可复用：** 5/10/15成功返回的分支必须由同一个提前可执行控制策略覆盖，不能事后知道返回时刻。**待查：** 如何在有噪SMF集合和非线性动力学下建立product信息状态的递归闭合证书？

**Scott, Joseph K.; Raimondo, Davide M.; Marseglia, Giuseppe Roberto; Braatz, Richard D. (2016)**，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。**阅读日期/状态：** 2026-11-01复核摘要、Proposition 1和Run239历史精读笔记，未重新阅读全文；已登记，不重复计数。**研究问题：** 如何以有限集合表示精确实现有界噪声下的线性预测、交集与支持计算。**方法/假设：** 线性映射、CZ的约束生成元表示及精确交运算，需有界过程/测量误差。**结论/局限：** 保留位置—速度相关性，但在线复杂度会增长；不直接给出有丢包非线性SMF＋MPC递归安全。**关联/可复用：** Run240的各初始分支是带测量条带的CZ，先计算一维支持再对两支取并，不能把非凸并集当成一个CZ。**待查：** 有界复杂度降阶能否保持共享恢复控制的可行性证书？

**本轮自有结果：** [Run240日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run240_research_log.md)。对所有成功观测值的5/10/15拍速度区间最大半宽分别0.2464585125、0.3188500014、0.3681367927m/s；仅限Run236两点纤维，不能推广为一般后验或MPC闭环。**去重已读仍91篇。**

---

## Run239 精确有噪位置后验与CZ交运算复核（2026-11-01；去重已读仍91篇）

**Scott, Joseph K.; Raimondo, Davide M.; Marseglia, Giuseppe Roberto; Braatz, Richard D. (2016)**，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。**阅读日期/核验：** 2026-11-01，实际重新核对§2 Definition 1/2、§3 Definition 3、Proposition 1(11)–(13)、Proposition 2(19)–(20)、§5(31)–(33)；其余章节本轮未精读。此文已有Run215等历史阅读记录，**不重复计数**。

**研究问题：** 有界过程和量测误差下如何保留状态集合的关联、交集和映射。**方法/模型：** 线性离散动力学，CZ表示{Gξ+c:||ξ||∞≤1,Aξ=b}；用线性等式与新增噪声变量实现量测条带交集。**关键定理/假设：** Proposition 1给出精确广义交及线性映射；§5(31)–(33)假设初始状态、过程扰动和量测噪声有已知紧致集合；Proposition 2给出CZ非空/成员资格LP判据。**结论：** 保留约束可以避免过早盒外包的相关性损失。**局限：** 生成元和等式随时间增长，在线降阶需另行保证外包；原论文未证明本仓库非线性、丢包、控制相关残差下的递归可行性。**与课题关联/可复用：** Run239对两初始符号分支分别引入15个扰动系数和一个位置测量噪声松弛，使用精确原始—对偶分数证书计算y=0时速度支持；单个CZ不能精确表示非凸两分支并集。**待查：** 全观测值及5/10/15拍模式下的有界复杂度后验、因果备份律与递归终端是否存在？

**本轮自有证据：** [Run239研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run239_research_log.md)。给定y=0的速度半宽0.3681367927m/s是限定子系统的精确Fraction结果，不是原论文直接提供的数值；不能推广为所有y均收缩。**去重已读仍91篇。**

---

## Run238 文献核验与15拍共享控制有限安全管（2026-11-01；去重已读仍91篇）

**Bemporad, Alberto; Garulli, Andrea (2000)**，*Output-feedback predictive control of constrained linear systems via set-membership state estimation*，*International Journal of Control* 73(8):655–665，DOI https://doi.org/10.1080/002071700403420 。**核验层级：** 2026-11-01，出版社摘要及作者研究机构书目 https://old.control.ee.ethz.ch/publications/2000/407.html ，未取得全文，不标记本轮全文已读。**研究问题：** 约束线性系统的部分观测与有界扰动下，如何对所有信息相容状态施加鲁棒MPC约束。**方法/模型：** 摘要确认MPC+SMF联合框架，线性、硬约束、有界扰动；具体优化及定理条件未逐式核验。**结论：** 摘要报告对所有信息相容状态与扰动的约束保证；不将其推断为适用于本项目非线性丢包模型。**局限：** 非线性sin、控制相关残差和15模式丢包合同尚无可直接套用的结论。**关联/可复用：** 把后验纤维上共同控制作为约束量词。**待查：** 取得原文并核对完整递归可行性条件。

**Qiu, Quanwei; Yang, Fuwen; Zhu, Yong; Mousavinejad, Eman (2020)**，*Output feedback model predictive control based on set-membership state estimation*，*IET Control Theory & Applications* 14(4):558–567，DOI https://doi.org/10.1049/iet-cta.2019.0881 。**阅读日期与核验：** 2026-11-01，重新阅读出版社开放正文§3.1–3.2、§4，未重建图片形式的全部LMI。**研究问题/方法：** 椭球SMF预测与量测更新、LMI/SDP鲁棒MPC、终端约束。**关键条件与结论：** 初始估计包含与初始优化可行、终端不变约束对可行性/稳定性分析重要；不能仅凭有限时域无违约推断无限递归可行。**局限：** 本项目冻结非线性、观测丢包与控制依赖残差未覆盖。**关联/可复用：** 估计集合必须进入未来控制决策。**待查：** Z15的后验测量收缩是否可与可执行终端备份形成闭合。此文此前已登记，不重复计数。

**本轮自有证据：** [Run238研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run238_research_log.md)。指定两状态纤维在共同零力矩下15拍安全的精确Fraction归纳，不是以上论文定理的直接应用。**统一已读计数仍91篇。**

---

## Run237 原文分节复核与共享后继判定（2026-11-01；去重已读仍91篇）

**题名：** *Output feedback model predictive control based on set-membership state estimation*。**作者/年份/出版：** Quanwei Qiu, Fuwen Yang, Yong Zhu, Eman Mousavinejad (2020), *IET Control Theory & Applications* 14(4):558–567, DOI https://doi.org/10.1049/iet-cta.2019.0881 。**核验状态与阅读日期：** 2026-11-01，出版社公开正文§2、§3.1–3.4、§4及结论的分节阅读；网页公式大量为图片，**没有逐式重建或核对全部LMI**。已在历史文献索引登记，本轮不重复增加去重篇数。

**研究问题：** 有界过程/观测扰动、状态不可直接测量时如何同时保证MPC约束与状态估计包含。**模型/方法：** 线性离散系统，椭球SMF预测+测量更新，估计集合参与minimax MPC，以S-procedure/Schur补和LMI/SDP处理约束，终端鲁棒正不变椭球。**重要定理/假设：** §2 Assumptions 1–2要求噪声与初始状态由已知椭球包围；§3 Theorem 1为递推估计包含的充分LMI条件；§4终端约束及初始可行是稳定/可行分析的重要条件（公式图片未逐式核实）。**主要结论：** 提出SMF+MPC统一设计及数值/电源变换器例子。**局限：** 椭球外包可能保守，SDP计算开销未达到本项目20ms认证，且不直接适用非线性sin、连续位置丢包和控制依赖扰动。**与本课题关联/可复用：** 信息状态集合而非单点估计必须进入终端控制；Run237严格证明原4000生成元F不适用于一个合法共享观测纤维。**待查：** 能否构造含估计误差/观测历史的非空输出反馈终端RPI与递归可行性证书？

**本轮项目自有证据：** [Run237研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run237_research_log.md)。严格支持超平面反例独立推导，不冒充Qiu等文献定理。

---

## Run236 文献核验与共享控制信息权限（2026-11-01；去重已读仍91篇）

**Mayne, Raković, Findeisen, Allgöwer (2006)**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222，DOI https://doi.org/10.1016/j.automatica.2006.03.005 。**本轮阅读/核验层级：** 2026-11-01，重新核对DBLP书目及公开摘要，并对照Run221已经阅读的§2–4、Propositions 1–3、Theorems 1–2笔记；本轮没有重新取得全文，不能声称重新逐条核对定理。**研究问题：** 有界过程与输出扰动下约束线性系统的输出反馈鲁棒MPC。**模型/方法：** Luenberger估计器、估计误差RPI、固定截面tube、名义MPC约束收紧。**重要假设/结论：** 需要估计误差包含、稳定误差系统、终端不变/下降与初始可行条件，方可保证约束与稳定性；不能从状态反馈RPI直接推导输出反馈。**局限：** 不覆盖本仓库连续丢包至15拍、非线性sin余项与控制依赖气动残差。**本课题关联/可复用：** Run236用同一后验观测纤维的两个真值证明Run235全状态律不可直接执行；下一步应研究联合估计/跟踪误差RPI或共享因果终端律。**待查：** 15模式观测图下能否得到可证明的模式条件化误差管并实现终端移位？书目 https://dblp.org/rec/journals/automatica/MayneRFA06.html 。

**Lucia, Ernesto, Castelan (2023)**，*Set-theoretic output feedback control: A bilinear programming approach*，*Automatica* **153:111004**，DOI https://doi.org/10.1016/j.automatica.2023.111004 。**本轮阅读/核验层级：** DBLP书目及公开资料复核，纠正本日志历史错误卷号/DOI，未重新精读原文；历史Run141已读状态保留。**研究问题/方法：** 输出反馈控制器及受控不变多面体的双线性联合综合。**假设/结论/局限：** 历史Run141的分节笔记讨论静态输出反馈与嵌套集合；该线性方法不能直接证明本项目非线性、失测及推力相关扰动下的安全性。**可复用：** 把观测等价类上统一控制作为合成约束。**待查：** 能否以更小维的模式依赖多面体替代4000生成元F？书目 https://dblp.org/rec/journals/automatica/LuciaEC23.html 。

**本轮自有证据：** [Run236研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run236_research_log.md)。去重已读仍91篇；不将仅核对书目的文献重复计入已读。

---

## Run235 文献核验与有限RPI表示（2026-11-01；去重已读仍91篇）

**题名：** *Invariant approximations of the minimal robust positively invariant set*。
**作者/年份/出处：** Saša V. Raković、Eric C. Kerrigan、Konstantinos I. Kouramas、David Q. Mayne（2005），*IEEE Transactions on Automatic Control* 50(3):406–410。DOI：https://doi.org/10.1109/TAC.2005.843854 。
**阅读日期与核验状态：** 2026-11-01；本轮复核DBLP/公开书目与摘要、已有Run234阅读笔记，未取得可核验全文，未重新核查定理编号或证明；**不是新增全文阅读，去重篇数保持91**。
**研究问题：** 对Schur稳定、持续有界加性扰动的离散线性系统构造最小RPI的有限外近似。
**方法/模型：** 有限Minkowski可达和、有限尾项外包、RPI集合闭合判据。
**重要假设/定理：** 稳定线性动力学、紧致扰动集合；具体定理编号和原文完整条件本轮未核实，不将其直接套用非线性无人机。
**主要结论：** 有限外近似可用于可靠约束验证；本轮项目自行以W=eps[-1,1]^4、rho=||A^800||∞构造有限4000生成元RPI，严格证明后继闭合。
**局限：** 原论文不解决间歇量测共享控制、控制依赖气动扰动、输出反馈Tube MPC及在线计算预算。
**与本课题关联及可复用技术：** 可将无限zonotope替换为有限生成元矩阵G和LP成员资格接口，但必须另证观测纤维上的单一因果控制；本轮的非线性正弦余项嵌入及有理数证明见 [Run235研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run235_research_log.md)。
**待查问题：** 如何降阶4000生成元而保持RCI，及在SMF后验纤维上建立共享控制和终端移位条件？

## Run234 定向复核：mRPI无限和与可证尾项（2026-10-31；去重仍91篇）

**题名：** *Invariant approximations of the minimal robust positively invariant set*。
**作者/年份/出版信息：** Saša V. Raković、Eric C. Kerrigan、Konstantinos I. Kouramas、David Q. Mayne，2005，*IEEE Transactions on Automatic Control* 50(3):406–410，DOI https://doi.org/10.1109/TAC.2005.843854 。
**阅读日期/核验状态：** 2026-10-31；本轮核对DBLP书目、公开摘要与仓库既有阅读笔记，**未重新阅读全文/逐条核查定理证明**；已在本日志历史条目登记，去重已读篇数保持91，不新增“已读”。
**研究问题：** 如何对稳定线性受扰系统的最小鲁棒正不变集构造可控制精度的外近似。
**方法/模型：** Schur线性离散系统、有界加性扰动、Minkowski可达和及尾项近似。
**重要定理/假设：** 线性稳定性、扰动紧致性、有限和外逼近；本轮未重新核对论文定理编号或全部假设。
**主要结论：** 经典mRPI可用有限可达和及可验证的尾项界近似；Run234使用精确有理数自行构造相应证书。
**局限：** 原论文线性条件不直接推出本项目非线性推力调度、间歇量测或输出反馈安全；本轮仅对固定推力、完整状态反馈、冻结四状态Euler模型独立证明。
**与本课题关联/可复用技术：** Run234定义无限zonotope S、用800步精确有理数矩阵幂和几何尾项证明S包含于物理硬约束、力矩不饱和，并以sin Taylor余项将真实非线性闭环嵌入稳定线性扰动包络。
**待查问题：** 如何得到可在线判定成员资格的有限RCI表示，并在SMF后验状态纤维上实现共享因果控制？参见 [Run234研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run234_research_log.md)。

## Run233 新增分节原文阅读：非线性鲁棒不变集的图方法（2026-10-31；去重90→91篇）

**题名：** *Computing robust control invariant sets of constrained nonlinear systems: A graph algorithm approach*。
**作者/年份/出版信息：** Benjamin Decardi-Nelson、Jinfeng Liu，2020 arXiv预印本，arXiv:2009.13581，https://arxiv.org/abs/2009.13581；本轮未独立核验正式期刊出版或DOI，故不虚构。
**阅读日期/核验状态：** 2026-10-31；直接阅读arXiv可公开访问的正文§2.1、§3.1–3.4，重点Definitions 1–2、Theorems 2–3、Algorithm 1与inner approximation说明；分节阅读，不声称全文逐页精读。查验既有PAPER_READING_LOG和READ_PAPERS未找到同名/同编号条目。
**研究问题：** 在状态、输入、扰动受限的非线性离散系统中，计算最大鲁棒受控不变集的内外近似。
**方法/模型：** 将状态空间细分为单元，用带扰动的有向图、强连通/无限路径选择与迭代细分形成外近似，再讨论控制器可用的内近似。
**重要假设/定理：** Assumptions 1–2要求紧约束、足够光滑且唯一的状态转移；Theorem 2给出图外近似包含关系，Theorem 3讨论细分极限的收敛；这些结论并不直接提供有限网格上的严格RCI证书。
**主要结论：** 细分图可系统地缩小可能的RCI区域；外近似不能直接作为安全终端集合，必须取得可认证的内近似与因果反馈。
**局限：** 本项目扰动界R(T)取决于当拍控制，且要求先选控制后允许扰动；论文的一般固定W建模与部分图论外近似不能未经重证直接套用。四维网格复杂度高，尚未解决间歇量测下同一观测纤维共享控制的问题。
**与本课题关联：** Run233先给出全状态饱和反馈的可复现数值候选，再计划将数值轨迹附近的关联四维单元送入严格的“每单元存在一个控制、覆盖所有后继”的内近似认证；不能将轨迹或图中有环等同于不变性。
**可复用技术：** 分层图细分、必要外剪枝、有限控制标签的充分后继包含测试、严格区分内外近似。
**待查问题：** 如何在R(T)控制依赖残差和不完整量测下构造可认证的非空闭合内核；是否必须缩小扰动合同或安全保证范围？

## Run232 定向原文复核：中央桥多拍阻塞（2026-10-31；去重仍90篇）

**Yinan Li; Jun Liu (2018)**, *Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*, *IEEE Transactions on Automatic Control* 63(7):2206–2211。DOI https://doi.org/10.1109/TAC.2017.2760106；作者原文 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf 。**阅读日期/层级：** 2026-10-31，重读§II–III Definition 1、Propositions 2–3、Definition 3、Theorem 1及其前提；历史Run227–231已计入，非新增全文精读。**研究问题：** 有限模式非线性离散系统的不变控制合成。**方法/模型：** 区间前驱、分支定界、有限模式标记与内近似。**重要定理/假设：** Proposition 2给出自身前驱包含判据；Theorem 1的有限终止/鲁棒内近似依赖有限模式、Lipschitz与正鲁棒裕度。**主要结论：** 满足前提可生成分区不变控制内近似。**局限：** 不覆盖本项目连续推力、控制后可选的推力相关对抗残差及SMF间歇测量。**与本课题关联：** Run232独立证明单一小倾角桥候选在速度半宽b<0.4060367...时非RCI；不能直接套用该文定理。**可复用技术：** 严格区分必要反证、未认证后继与充分闭合条件。**待查问题：** 多个小倾角位置—速度相关单元能否形成真正闭合循环并提升到部分观测信息状态。**研究工件：** [Run232研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run232_research_log.md)。

## Run231 文献定向复核：严格剪枝与闭合终端集合（2026-10-31；去重仍90篇）

**Yinan Li; Jun Liu (2018)**, *Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*, *IEEE Transactions on Automatic Control* 63(7):2206–2211，DOI https://doi.org/10.1109/TAC.2017.2760106，原文 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf 。**核验日期与层级：** 2026-10-31，重新阅读正式版§II–III、Definition 1、Proposition 2及Theorem 1的假设与结论；已于Run227/228计入，**不新增去重已读篇数**。**研究问题：** 有限模式离散非线性系统的受控不变内近似和分区控制合成。**方法：** 区间包含、分支定界、前驱固定点与控制模式标记。**重要假设：** 模式集合有限、各映射连续；Theorem 1的有限终止/内近似结论需要正鲁棒裕度与相应精度条件。**结论：** 符合条件时可构造分区不变控制内近似。**局限：** 文中鲁棒裕度与本项目不可见的逐拍控制依赖对抗残差不是同一个假设；不能直接套用论文定理。**与本课题关联：** Run231以独立的有理数对抗轨迹证明正体积四状态盒不属于无限时域安全核，作为候选终端图的严格剪枝，尚未找到闭合循环。**可复用技术：** 区间单元分类、正确区分必要排除与充分后继闭合、控制标签。**待查：** 中央区域能否构造非空闭合终端图；能否将其提升至SMF信息状态。**研究工件：** [Run231研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run231_research_log.md)。

## Run230 新增分节原文阅读：输入延迟RCI与有限前驱排除（2026-10-31；去重90篇）

**Zexiang Liu; Liren Yang; Necmiye Ozay (2020)**，*Scalable Computation of Controlled Invariant Sets for Discrete-Time Linear Systems with Input Delays*，American Control Conference (ACC 2020), pp. 4722–4728，DOI https://doi.org/10.23919/ACC45564.2020.9147731；arXiv:2003.04953 https://arxiv.org/abs/2003.04953；作者公开原文 https://web.eecs.umich.edu/~necmiye/pubs/LiuYO_acc20.pdf 。**阅读日期/核验级别：** 2026-10-31，直接阅读arXiv原文§I、§II-A/B、§III至Theorem 1及其证明关键段；分节阅读，非全文逐页精读。核对旧日志及READ_PAPERS中题名/arXiv编号未重复，去重已读89→90。**研究问题：** 输入纯延迟、不可测有界扰动下如何可扩展计算最大鲁棒受控不变集。**方法/模型：** 离散线性系统 x+=Ax+Bu(t-τ)+Fd，预测辅助状态与扰动集合的Pontryagin差，低维RCI重建。**重要假设/定理：** §II式(2)的量词为先选u后对所有d；式(4)给出有限前驱外近似；Theorem 1在其线性、纯输入延迟、固定多面体扰动等假设下证明辅助系统重建的C_ext是增广系统最大RCI。**主要结论：** 利用结构化状态预测，避免直接在n+mτ维增广空间求最大RCI；还可扩展扰动预见信息。**局限：** 非线性sin姿态动力学、控制依赖R(T)及SMF间歇观测均不满足其定理的直接适用条件；本轮Run230的姿态积分链也不是论文意义上的纯输入延迟。**与本课题关联：** Run230利用控制影响姿态的有限传播速度，得到25拍位置边界必要排除证书；该论文的有限前驱逻辑可作为安全语义参照，但Run230数学证书由本仓库模型独立推导。**可复用技术：** 正确的因果控制—扰动量词、有限步安全外近似、预测状态与可达误差分解。**待查：** 能否将状态相关控制权限与输入依赖扰动纳入可计算非空四状态RCI；如何提升至SMF信息状态并保持递归可行？

**本轮证据：** [Run230研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run230_research_log.md)；`verification/check_four_state_position_guard.py`。未声称论文证明本项目终端不变性。

## Run229 定向原文复核：有限后继图与无限时域不变性边界（2026-10-31；去重仍89篇）

**Yinan Li; Jun Liu (2018)**，*Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*，*IEEE Transactions on Automatic Control* 63(7):2206–2211，DOI https://doi.org/10.1109/TAC.2017.2760106；正式版 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf 。**阅读日期与核验层级：** 2026-10-31，本轮定向复核正式版Definition 1、Proposition 2、Assumption 1、Theorem 1；非全文重新精读，沿用Run227/228同一工作，**不增加篇数**。**研究问题：** 非线性切换系统如何合成不变集合及分区控制器。**方法/模型：** 有限模式切换、区间包含函数、分支定界、前驱不动点。**关键定理/假设：** Proposition 2要求 `Omega⊆Pre(Omega)` 才能称为受控不变；Assumption 1为局部Lipschitz；Theorem 1的有限终止/近似保证依赖鲁棒裕度及精度条件。**主要结论：** 在规定假设下可合成区间内近似与分区控制策略。**局限：** 不能直接套用到连续推力、控制依赖逐拍不可见残差、间歇量测。**本课题关联：** Run229虽严格认证三条两拍有向边，但无闭合循环，不能借用论文的无限时域不变性结论。**可复用技术：** 有理数区间外包、覆盖验证、细分及控制标签。**待查：** 有无可认证的非空闭合循环单元集合；如何提升至SMF观测纤维并保持控制先于扰动的量词？

## Run228 正式期刊版复核与版本去重（2026-10-31；去重已读仍89篇）

**Yinan Li; Jun Liu（2018）**，*Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*，*IEEE Transactions on Automatic Control* 63(7):2206–2211，DOI https://doi.org/10.1109/TAC.2017.2760106，正式版原文 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf 。**阅读日期/状态：** 2026-10-31，直接复核正式版§II–III、Definition 1、Propositions 2–3、Algorithm 2、Assumption 1及Theorem 1附近段落；分节阅读，非全文精读。**去重：** 与Run227已读的2016 arXiv:1608.08683为同一研究工作的预印本/正式版，2018正式版题名增加“Nonlinear”，更新版本关联但**不新增已读篇数**。**研究问题：** 离散切换非线性系统中如何计算受控不变内近似和分区控制器。**方法/模型：** 有限控制模式、连续映射、区间包含函数、前驱与细分固定点。**重要定理/假设：** Proposition 2为受控不变的前驱包含判据；Assumption 1为Lipschitz条件；Theorem 1的有限终止/内近似保证有额外鲁棒裕度与精度条件，不能省略。**主要结论：** 在其有限切换模式及鲁棒不变性前提下，可通过区间细分计算具有控制器的内近似。**局限：** 本课题连续推力、控制依赖的逐拍不可见残差、部分观测SMF，不能直接照搬。**与课题关联：** Run228为四状态冻结模型实现严格区间后继与并集覆盖的保守充分认证；仅对狭窄桥给出独立严格反例。**可复用技术：** 区间外包、细分、单元策略与鲁棒裕度审计。**待查：** 连续输入细分及扰动量词如何得到可认证非空四状态RCI，如何提升至SMF信息纤维与MPC递归可行性？

**本轮工件：** [Run228研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run228_research_log.md)；`verification/check_four_state_bridge_graph.py`。未将算法失败视作RCI不存在证明。

## Run227 新增分节原文阅读：区间分区不变控制（2026-10-31；去重已读89篇）

**Yinan Li; Jun Liu（2016）**，*Invariance Control Synthesis for Switched Systems: An Interval Analysis Approach*；arXiv:1608.08683，https://arxiv.org/abs/1608.08683 ，原文 https://arxiv.org/pdf/1608.08683 。**阅读日期/核验层级：** 2026-10-31，直接阅读§I–III、§IV Algorithm 2/3及Theorems 1/2、§V Theorem 4与Proposition 8；分节阅读，非全文逐页精读；在统一日志与READ_PAPERS中核对题名及编号未重复，去重已读88→89。**研究问题：** 如何计算离散切换非线性系统的受控不变集并合成分区控制器。**方法/模型：** 有限模式、连续子系统映射、区间包含函数、细分及前驱内外近似。**重要假设/定理：** Proposition 2给出Omega⊂Pre(Omega)判据；Theorem 1在紧且full集合与Assumption 1的区间宽度界下给出前驱内外包；Theorem 2给出指定假设下外近似有限终止；Theorem 4在额外正裕度鲁棒受控不变条件下给出有限分区控制器，Proposition 8验证算法输出非空时的策略。**主要结论：** 在论文有限模式框架中可用区间细分合成受控不变集近似及分区策略；内近似需要额外鲁棒性条件。**局限：** 本仓库连续推力、控制依赖对抗残差、间歇位置观测与SMF信息纤维不满足论文的直接应用条件。**与课题关联：** Run227证明终端集合必须允许跨越小倾角桥。**可复用技术：** 区间外包、分区、后继闭合和控制模式记录；需独立处理forall r。**待查问题：** 如何为四状态模型构造经认证的非空闭合单元策略图，并进一步提升至输出反馈信息结构？

**本轮自有证据：** [Run227研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run227_research_log.md)。双模式候选与轴对齐终端盒均严格失败，不是该论文原有定理。

## Run226 新增分节原文阅读：隐式鲁棒受控不变集（2026-10-31；去重已读88篇）

**Zexiang Liu、Tzanis Anevlavis、Necmiye Ozay、Paulo Tabuada（2021）**，*Automaton-based Implicit Controlled Invariant Set Computation for Discrete-Time Linear Systems*；arXiv:2109.12378，https://arxiv.org/abs/2109.12378 。**阅读日期/核验层级：** 2026-10-31，直接阅读arXiv HTML原文§II–IV-A、Definitions 2–3、Assumptions 1–3、Proposition 2、Theorems 1–2及相关说明；不是全文逐页精读。此前唯一日志及READ_PAPERS均未包含此题名/编号，本轮新增一篇去重分节已读，计数87→88。**研究问题：** 如何为受约束离散线性系统构造可用于安全监督的鲁棒受控不变集合，避免显式高维投影的计算负担。**方法/模型：** 线性系统 `x+=Ax+Bu+d`，多面体安全集/扰动集，参数化有限自动机扰动反馈，先在增广状态求鲁棒正不变集，再投影/取凸包得到隐式RCIS。**关键定义、定理及假设：** Definition 2规定扰动当前不可见时 `forall x in C, exists u, forall d`；Definition 3在扰动可见时交换为 `forall x, forall d, exists u`，两者不能混淆。Assumptions 1–3包括（可通过状态反馈处理的）幂零A、多面体S/D及有限扰动顶点；Theorem 1将增广RPIS投影凸包联系到RCIS；Theorem 2在指定幂零/有限自动机条件下给出有限可达集闭式表示。**主要结论：** 特定线性系统可得到隐式不变集和控制器参数约束，减少显式求核的复杂度。**局限：** 本仓库的推力调度非线性、控制依赖残差界、位置间歇观测不自动满足论文假设；不能据此声称四状态/六状态RCI存在。**与课题关联/可复用技术：** 非可见扰动的量词、增广策略状态和隐式终端证书的设计框架；本轮Run226三步证书独立推导，不属于该论文结果。**待查：** 能否对冻结四状态模型构造经严格外包的分区线性策略图、保留正确输出反馈信息纤维并实现可核验的终端不变性？

**本轮自有证据：** [Run226研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run226_research_log.md)。两点属于Pre³(X)，另两点属于Pre²(X)但严格不属于Pre³(X)；未证明非空RCI核。

## Run225 二步鲁棒前驱与文献复核（2026-10-31；去重已读仍87篇）

**Ilya Kolmanovsky; Elmer G. Gilbert (1998)**, *Theory and computation of disturbance invariant sets for discrete-time linear systems*, *Mathematical Problems in Engineering* 4(4):317–367；DOI https://doi.org/10.1155/S1024123X98000866；出版商 https://onlinelibrary.wiley.com/doi/10.1155/S1024123X98000866 。**核验日期/层级：** 2026-10-31，重新核对出版商摘要、作者、出版信息；**未阅读正文，不新增已读计数**。**研究问题：** 有界扰动 LTI 系统在状态约束域中的最大扰动不变集。**方法/模型：** 摘要指出 Pontryagin 差、最大不变集生成算法、有限确定性条件及 Lyapunov 稳定系统扩展。**重要定理/假设：** 正文具体定理编号与适用条件未核验，不能引用为本轮非线性模型证明。**主要结论：** 摘要称可生成最大不变集的计算表示并给出数值示例。**局限：** LTI/扰动不变性框架，不能直接代替本仓库非线性推力调度和因果控制策略分析。**本课题关联/可复用：** 前驱迭代、集合差与终端核的理论背景；本轮二步包含/排除证书独立推导。**待查：** 受控不变与纯扰动不变的量词区别、非线性/部分观测情形的可计算内核、有限终止性。

**本轮自有结果：** [Run225研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run225_research_log.md)；两个二步可行见证、两个一步可行但二步严格排除状态。不是完整鲁棒终端核；去重已读仍87篇。

## Run224 四状态一步鲁棒前驱与文献核验（2026-10-31；去重已读仍87篇）

**Ilya Kolmanovsky；Elmer G. Gilbert（1998）**，*Theory and computation of disturbance invariant sets for discrete-time linear systems*，*Mathematical Problems in Engineering* 4(4):317–367；DOI https://doi.org/10.1155/S1024123X98000866；出版商 https://onlinelibrary.wiley.com/doi/10.1155/S1024123X98000866 。**核验日期/层级：** 2026-10-31，出版商摘要及书目复核，**未阅读正文、不新增已读计数**。**研究问题：** 有界扰动离散LTI系统在约束域中的最大扰动不变集。**模型/方法：** 摘要说明Pontryagin差、最大不变集生成算法及有限确定性条件。**重要假设/定理：** 具体编号及条件未核验，不能直接迁移至非线性推力调度模型。**主要结论：** 摘要指出给出计算表示、Lyapunov稳定系统扩展及数值例子。**局限：** 主要研究LTI系统，本仓库需要独立证明非线性、控制—扰动量词和输出反馈条件。**关联/可复用：** 鲁棒前驱与终端不变集的概念参考；Run224的一步Taylor区间证书是自行推导，不是该文定理。**待查：** 正文中有限终止条件、控制不变与扰动不变的区别、如何形成可计算内核。

**本轮自有结果：** [Run224研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run224_research_log.md)。安全盒第一轮前驱有两个严格可行见证和两个严格排除点；不构成非空RCI核证明。去重已读87篇不变。

## Run223 双侧倾角必要条件与文献核验（2026-10-31；去重已读仍87篇）

**Kolmanovsky, Ilya; Gilbert, Elmer G.（1998）**，*Theory and computation of disturbance invariant sets for discrete-time linear systems*，*Mathematical Problems in Engineering* 4(4):317–367；DOI https://doi.org/10.1155/S1024123X98000866 ，出版商 https://onlinelibrary.wiley.com/doi/10.1155/S1024123X98000866 。**核验日期/层级：** 2026-10-31，出版商摘要及书目核验，**未阅读正文，不计入新增已读篇数**。**研究问题：** 有界扰动离散LTI系统的最大扰动不变集。**方法/模型：** 论文摘要描述Pontryagin差、最大不变集计算及多模态调节。**重要定理/假设：** 具体编号和假设待正文核验，不能推断其适用非线性推力调度。**主要结论：** 摘要指出给出不变集计算算法及相关数值例子。**局限：** 直接讨论LTI系统，不能无额外证明移用于四状态非线性动力学。**本课题关联/可复用：** 下一轮鲁棒前驱与终端可生存核审计。**待查：** 原文前驱递推的量词、收敛和有限终止条件。

**Franco Blanchini（1999）**，*Set invariance in control*，*Automatica* 35(11):1747–1767；DOI https://doi.org/10.1016/S0005-1098(99)00113-2 。**核验日期/层级：** 2026-10-31，DBLP书目核验，**未阅读正文，不计入新增已读篇数**。**研究问题：** 控制集合不变性。**方法、重要定理/假设、主要结论、局限：** 未见原文，待核验。**关联/可复用：** 四状态终端受控不变性理论背景。**待查：** 非线性受控不变集的适用条件与前驱算子。

**本轮自有结果：** [Run223研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run223_research_log.md)，使用有理数Taylor上界证明任意非空RCI集合必须具有双侧倾角投影。不是上述论文定理。统一去重已读数仍87篇。

## Run222 终端不变集阻塞与文献核验（2026-10-31；去重已读仍87篇）

**Mayne, Raković, Findeisen, Allgöwer（2006）**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222；DOI https://doi.org/10.1016/j.automatica.2006.03.005 。**阅读日期/层级：** 2026-10-31，对Run221已阅读§2–4、Propositions 1–3、Theorems 1–2、A1–A3笔记及公开摘要定向复核，非重新全文精读。**研究问题/模型/方法：** 有界扰动约束线性系统的输出反馈Tube MPC；观测误差RPI、跟踪误差管、名义收紧及终端集合。**关键假设：** 误差集合有效、终端不变/下降条件及初始可行性。**主要结论：** 在所列条件下可保证约束与稳定性。**局限：** 不自动覆盖推力调度、姿态小角度不足以抵消横向残差的情况。**本课题关联/可复用：** Run222验证终端非空性这一前提在四状态扩展中失败；不能引用论文为失败模板背书。**待查：** 扩大倾角的联合四状态终端核是否非空？

**Franco Blanchini（1999）**，*Set invariance in control*，*Automatica* 35(11):1747–1767；DOI https://doi.org/10.1016/S0005-1098(99)00113-2；书目 https://dblp.org/rec/journals/automatica/Blanchini99.html 。**核验日期/状态：** 2026-10-31，仅DBLP书目元数据核验，**未阅读正文，不计入已读篇数**。**研究问题：** 控制不变性理论综述（仅根据题名/书目定位）。**方法、具体定理假设、主要结论、局限：** 待原文阅读核验，不编造。**本课题关联/可复用：** 后续审计四状态鲁棒受控不变核的基础参考。**待查：** 具体鲁棒可生存核算法与适用假设。

**本轮自有结果：** [Run222研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run222_research_log.md)，严格有理数漂移反证，仅适用于冻结横向残差不确定性合同，不是文献原定理。论文去重已读数仍87篇。

## Run221 定向原文阅读与终端安全基线（2026-10-31；去重仍87篇）

**Mayne, Raković, Findeisen, Allgöwer（2006）**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222；DOI https://doi.org/10.1016/j.automatica.2006.03.005；原文 https://www2.ee.ic.ac.uk/publications/p5346.pdf 。**阅读日期/层级：** 2026-10-31，直接阅读§2–4、Propositions 1–3、Theorems 1–2、A1–A3与终端条件，非全文逐页精读。**问题/模型/方法：** 有界状态与输出扰动的约束线性系统，Luenberger观测器、两个误差RPI、名义Tube MPC及Pontryagin收紧。**关键假设：** 误差闭环Schur稳定、估计误差与控制误差的RPI、初始误差属于这些集合、终端不变与Lyapunov下降条件。**结论：** 在这些前提下得到鲁棒约束满足及稳定性。**局限：** 不直接覆盖15模式位置丢包、推力跳变与控制相关非线性残差。**关联/可复用：** Run221严格构造孤立姿态通道误差RPI与终端名义集合、证明移位可行；并未满足全系统A1–A3，不引用该文证明本项目六状态稳定性。**待查：** 如何在横向—姿态耦合及不确定推力下获得非空的终端不变集合及终端下降函数？

**Lorenzetti, Pavone（2020）**，*A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*，ECC 2020，DOI https://doi.org/10.23919/ECC51009.2020.9143979；arXiv https://arxiv.org/abs/1911.07360；原文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。**阅读日期/层级：** 2026-10-31，直接阅读§II–IV-D式(7)–(11)，非全文重读。**问题/方法：** 有界测量/过程噪声下的LTI输出反馈Tube MPC，以固定误差截面和收紧名义优化控制复杂度。**关键假设：** 线性模型、可稳定化/观测性及有界噪声，存在RPI与终端控制/代价下降条件。**结论：** 在其条件下可构造高效的Tube MPC。**局限：** 不包含本仓库推力调度和缺测信息状态；固定截面可能保守。**关联/可复用：** Run221复用其固定截面、名义终端/移位设计思想，但没有完整终端下降或20ms最坏运行时间证据。**待查：** 相同终端保证和计算预算下，测量条件化SMF/CZ能否改善四状态控制可行域？

**本轮自有证据：** [Run221研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run221_research_log.md)；32条48拍确定性闭环、精确不变性与移位证书。上述两篇均已在历史阅读记录中出现，不增加去重篇数；不把本轮工程实现写成文献原定理或新的理论创新。

## Run220 文献核验与双约束支持算法（2026-10-31；去重仍87篇）

**Scott、Raimondo、Marseglia、Braatz（2016）**，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，Automatica 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。本轮阅读层级：公开摘要及仓库已有Definition 3、Proposition 1/Section 5笔记交叉核验，非全文重读。研究问题：有界噪声线性系统集合估计；方法：CZ保留线性映射、集合交与Minkowski和相关性。关键前提：有界误差与有效集合表示。结论：可精确表示多面体但复杂度需管理。局限：不直接给出本仓库Tube MPC终端安全保证。关联/可复用：历史联合半空间的控制相关支持；Run220双乘子证书为本仓库自行推导，并非论文定理。待查：真实tick193联合收益及在线预算。

**Köhler、Müller、Allgöwer（2021）**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427 。本轮阅读层级：公开摘要与仓库既有定理条件笔记交叉核验，非全文重读。研究问题：噪声输出和扰动下的鲁棒MPC；方法：在线估计误差界结合homothetic tube。关键前提：可靠在线界、检测性/增量可稳定性及相应终端条件。结论：可在这些假设下改善保守性并实现鲁棒约束满足，含10状态四旋翼示例。局限：不自动适用于仓库四状态有限Backup。关联/可复用：将可证上界用于MPC收紧；待查：终端受控不变集、递归可行性及实际运行时间。

**本轮自有算法与证据：** [Run220研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run220_research_log.md)。合成双约束支持从1降至0；GitHub Actions完整checkout实际第193拍12个候选第二半空间的额外可认证增益为0，不能由此证明完整后验无收益。不得将本轮标成新增已读论文。

# PAPER_READING_LOG — 无人机 MPC + SMF 论文阅读记录

> 首次整理：2026-10-30（Run200）。从 [READ_PAPERS.md](READ_PAPERS.md) 的85条历史“已阅读/核对”记录迁移，按**论文题名去重为84篇**；Robbins等《Online Constraint Tightening...》的Run126/161/170记录已合并在同一条下，原有阅读说明均保留。历史文件不修改，以避免破坏依赖其SHA-256的既有可复现实验。此后本文件是新增阅读和修订的唯一入口；旧文件只作为历史快照。
>
> 证据口径：“原文精读”需有明确章节/公式/定理；“正文片段核对”不能推断未见部分；“仅摘要核对”不能视作完整论文阅读。历史记录中缺失的作者、日期、定理假设、局限或待查问题一律保留为**待核验**，不编造。未来每条统一补齐：题名、作者、年份、DOI/arXiv/正式链接、阅读日期及层级、研究问题、模型与方法、关键假设/定理、结论、局限、对课题的关系、可复用技术、待查问题。

## Run219 定向复核：共享扰动历史与控制相关支持（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有论文，公开原稿摘要及集合估计定位复核
- **题名/作者/年份/正式出处：** Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，2016，*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；公开原稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期及核验状态：** 2026-10-31；本轮核对原稿摘要、引言中集合估计问题、CZ交/投影/Minkowski运算的研究定位；历史Run212/216/218已有Definition 3、Proposition 1等分节笔记，**本轮没有重新全文精读**，不新增已读计数。
- **研究问题与模型/方法：** 有界过程扰动和测量误差下的集合状态估计，使用受约束Zonotope保留集合相关性并通过保守降阶控制表示复杂度。
- **关键假设/定理：** 线性集合运算需满足所采用的有界误差模型和表示合同；历史阅读记录已核对CZ运算命题。本轮的共享扰动权重半空间由仓库Euler模型自行推导，**不是Scott等的新增定理**。
- **主要结论/局限：** CZ允许在足够表示复杂度下保留相关约束，但不自动保证鲁棒MPC的终端安全性、20ms计算预算或递归可行性。
- **与课题关联及可复用技术：** Run219证明对位置包135、165、180先合并共享扰动再取支持，可排除Run218旧关键支持极大面，精确改善 `5212367/450000000`；然而五拍速度约束仍阻塞。该单条H半空间**不是完整CZ后验**。
- **待查问题：** 如何以有限条共享扰动约束和可验证降阶实现连续SMF更新；是否能在同等测量信息、控制策略与计算预算下恢复鲁棒MPC准入并补齐终端不变性？

**本轮自有证据（非文献结论）：** [Run219研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run219_research_log.md)；原极大面排除裕度 `5212367/500000000`，控制相关支持改善 `5212367/450000000`，剩余单行裕度约 `-0.02473733102`。去重87篇不变。

## Run218 定向阅读：跨块历史约束的零增益支持证书（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——已有论文，本轮原稿局部复核
- **题名/作者/年份/出版：** Joseph K. Scott, Davide M. Raimondo, Giuseppe Roberto Marseglia, Richard D. Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, 2016, *Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf。
- **阅读日期与级别：** 2026-10-31，核对作者原文第2节集合表示与运算、Definition 3和第3节开头；**本轮不是全文重读**。
- **研究问题/方法/模型：** 在有界误差离散系统中，用受约束Zonotope的生成元与线性等式约束表达非对称相关集合；研究线性映射、广义交、Minkowski和及保守降阶。
- **重要假设/结论：** 不限制表示复杂度时可表达任意凸多面体；在所定义的表示和运算下部分集合运算可精确计算；复杂度与精度存在权衡。该结论不保证添加任意历史条带后控制相关支持必然收紧。
- **局限/课题关联/可复用技术：** Run218在第193拍发现一个属于Run216乘积外包的关键支持极大点，同时满足全部6条Run217跨块必要条带，故即使联合使用这些条带该方向增益仍精确为0；无需再对相同6条带重复昂贵的4D LP。此结果不说明完整CZ历史后验同样无增益。
- **待查问题：** 保留共享扰动和多包观测一致性的完整历史约束能否排除该极大点？如何给出可检查的可行/不可行证书？

### Köhler、Müller、Allgöwer（2021）——已有论文，本轮原稿局部复核
- **题名/作者/年份/链接：** Johannes Köhler, Matthias A. Müller, Frank Allgöwer, *Robust output feedback model predictive control using online estimation bounds*, 2021, arXiv https://arxiv.org/abs/2105.03427；公开稿 https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf。
- **阅读日期与级别：** 2026-10-31，核对摘要、第I节贡献、第II节问题设置及Assumption 1有界扰动；**不是全文重读**。
- **研究问题/方法/模型：** 在线验证状态估计误差界并结合homothetic Tube MPC实现带噪声与扰动的输出反馈约束控制；论文给出非线性四旋翼示例。
- **重要假设/结论：** 有界扰动、检测性/稳定性和相应估计误差、终端/优化条件是其递归可行与约束保证的组成部分；本仓库尚未建立这些条件。
- **局限/课题关联/可复用技术：** 本轮只证明一条有限时域安全审计行在六条历史必要约束下未改善，不是MPC递归可行性结果。在线可靠支持界可作为未来Tube MPC约束收紧的候选接口。
- **待查问题：** 何种紧凑历史一致集合能在20ms预算内提供真正的控制相关支持改善，并连接可验证终端安全集？

**本轮自有负面证据（非论文定理）：** [Run218研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run218_research_log.md)；关键方向6条跨块H-strip联合支持增益精确为0，五步负速度行仍严格阻塞；完整仓库集成尚未执行。去重87篇不变。

## Run217 定向核对：跨块历史相关性与控制相关支持（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有论文，本轮书目/摘要核对
- **题名、作者、年份与出版：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf。
- **阅读日期及核验级别：** 2026-10-31；本轮重新核对作者稿摘要、书目信息，并对照Run216已记载的Definition 3、Proposition 1、Theorem 1及Section 5定向笔记；**本轮未重新全文精读**。
- **研究问题/模型/方法：** 有界噪声线性系统的集合状态估计；以受约束Zonotope保留集合交、线性映射与Minkowski和中的相关性，并在复杂度增长时保守降阶。
- **重要假设/定理与结论：** CZ在不限制复杂度时可表达凸多面体，若表示适当可精确执行基本集合运算；不意味着任意H-strip程序已经实现CG形式CZ，更不自动给出鲁棒输出反馈MPC递归可行性。
- **局限/本课题关联/可复用技术：** Run217使用冻结Euler四状态模型和已知历史施加力矩构造4D跨块必要约束，再以精确一维对偶计算控制相关支持；这是相关性保留思想的特定实现，但不是该文的CZ递推。当前多条带只逐条外包，实际第193拍尚未执行完整仓库集成，20ms实时性未满足。
- **待查问题：** 跨块条带在第193拍是否使五拍速度约束的负裕度转正？多条带联合支持是否可增量优化？存在姿态模型扰动时如何扩大可靠半径？如何与终端受控不变性闭合？

## Run216 定向复核：联合历史支持与控制相关安全准入（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有论文，作者原文分节复核
- **题名、作者、年份、出版信息：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开原文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期及证据层级：** 2026-10-31；直接核对Definition 3、Proposition 1、Theorem 1、Section 5估计递推及复杂度说明；不是全篇重新精读。
- **研究问题与方法/模型：** 用CG表示的constrained zonotope保留有界误差状态估计中的线性映射、集合交及Minkowski和的相关性，并在复杂度增长后做保守降阶。
- **重要假设/定理：** Proposition 1给出CZ三种集合运算的精确恒等式；Theorem 1指出不限制表示复杂度时，CZ可表示任意凸多面体。该等价性**不表示**任意H多边形程序已实现CG形式的CZ递推。
- **主要结论与局限：** 相关性保留有潜在精度优势，但生成元、约束和计算成本会增长；该论文不直接证明本仓库的15-mode推力调度、间歇量测和五拍备份递归可行。
- **与课题关联/可复用技术：** Run216用二维H多边形顶点支持直接进入两层Backup，避免预测盒重置；真实第193拍仍被第5拍速度下界阻塞，说明仅保留(p,v)、(phi,omega)块内历史条带不够。下一步考虑完整4D跨块约束及可验证压缩。
- **待查问题：** 如何在同等历史信息下保存v与phi/omega的动态耦合，并对第193拍临界支持给出可检查的精确/对偶证书和20ms内的计算方案？

### Köhler、Müller、Allgöwer（2021）——既有论文，摘要与既有定理笔记核对
- **题名、作者、年份、链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler、Matthias A. Müller、Frank Allgöwer；2021；arXiv https://arxiv.org/abs/2105.03427 。
- **阅读日期及证据层级：** 2026-10-31；核对arXiv公开摘要与仓库既有Assumption 7/Theorem 4笔记，未重新全文精读。
- **研究问题与方法/模型：** 通过在线验证估计误差界，将输出反馈估计与homothetic Tube MPC约束收紧结合；含非线性四旋翼示例。
- **重要假设/定理：** 可靠估计误差界、增量稳定/可检测性、有效终端条件与初始可行性等是全时域保证的前提，不能从有限步Backup的局部准入直接推导。
- **主要结论与局限：** 在线估计界可改善性能/保守性，但其证明条件尚未由本仓库四状态实验满足。
- **与课题关联/可复用技术：** 控制相关支持函数可用于局部鲁棒约束审计；仍须补齐终端不变性及真正滚动MPC。
- **待查问题：** 能否构造一个范围适中、计算可行的终端安全基线，再公平比较CZ与区间SMF？

**本轮自有负面证据（非文献定理）：** [Run216研究日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run216_research_log.md)；第193拍联合H外包五拍Backup仍拒绝，精确临界行裕度约-0.03632037，原型中位计算约99ms，超出20ms。去重文献仍87篇。

## Run214 定向复核：滚动历史线性约束与 CZ 联合相关性（2026-10-31；已计数去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——已有文献，公开正文定向复核
- **题名、作者、年份、正式信息：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036 。
- **阅读日期/证据层级：** 2026-10-31；核对公开论文 PDF 的引言及 CZ 交运算、状态估计方法概述，并复核仓库 Run212 对 Definition 2/3、Proposition 1、Section 5 的阅读记录；**本轮不宣称全文重读**。
- **研究问题与模型/方法：** 如何在有界噪声线性系统中兼顾集合估计精度与运算成本；使用 CZ 表示、交集、投影、Minkowski 和保守降阶。
- **关键假设/定理：** 相关集合运算在其表示合同下成立；精确交集与无损降阶是两回事。Run214 尚未构造 CZ，不能直接继承其数值精度结论。
- **主要结论/局限：** CZ 可以保存一般线性耦合约束，但高阶表示的计算成本需要降阶；论文并未直接保证本仓库15-mode输出反馈安全闭环的终端可行性。
- **与课题关联及可复用技术：** Run214 的20个三包一维支持交集仍存在危险联合盒角点；下一步可用 CZ 保存 `(p,v,phi,omega)` 关联，而非继续增加单变量独立支持界。
- **待查问题：** 能否在相同测量历史与0.02秒控制周期内，得到可靠且可验证的联合支持/可行性证书？

### Rego、Raffo、Scott、Raimondo（2020）——已有文献，本轮仅摘要与书目复核
- **题名、作者、年份、正式信息：** *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*；Brenner S. Rego、Guilherme V. Raffo、Joseph K. Scott、Davide M. Raimondo；2020；*Automatica* 111:108614；DOI https://doi.org/10.1016/j.automatica.2019.108614；arXiv https://arxiv.org/abs/1908.09950 。
- **阅读日期/证据层级：** 2026-10-31 仅核对摘要与正式书目；**历史 Run179 已有分章节全文精读记录，本轮不重复声称精读**。
- **研究问题与模型/方法：** 非线性有界扰动系统的 CZ 预测外包与量测交集，采用 mean-value 和 Taylor 扩展。
- **关键假设/定理：** 适用性依赖有效非线性映射外包、误差界与量测集合；Run214 的四状态线性 Euler 恒等式不需要使用其非线性 Taylor 扩展。
- **主要结论/局限：** 相对简单集合外包，CZ 可能保留更多相关性；不能将其示例结果当成本课题的控制安全证明。
- **与课题关联及可复用技术：** 六状态/非线性扩展的候选估计基线；当前先实现可验证线性联合 CZ 与复杂度控制。
- **待查问题：** 对四状态离散动力学，如何实现精确线性 CZ 预测/交，再决定是否有必要采用非线性扩展？

**本轮自有负面结果：** 第193拍最近6个位置包的20组精确支持函数将速度下界提高 `57617501/1440000000 m/s`，但两层因果 Backup 仍拒绝；保留为外包证书阻塞，不推断物理不可生存。参见 [Run214日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run214_research_log.md)。

## Run213 定向核验：历史一致外包能否转化为控制准入（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有文献，摘要及Run212正文笔记复核
- **题名、作者、年份、正式信息：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；https://doi.org/10.1016/j.automatica.2016.02.036 。
- **阅读日期及层级：** 2026-10-31；核对公开原文摘要、Run212已核对的Definitions 2–3、Proposition 1和Section 5笔记；本轮未重新全文精读。
- **问题/方法：** 有界误差集员状态估计；通过CZ的线性映射、Minkowski和广义交保留状态相关性。
- **关键假设/结论：** CZ表示中的生成元约束与有效测量误差集是运算成立的前提；集合运算有精确公式，但规模会增长。
- **局限：** 不是现成的15-mode四旋翼鲁棒MPC终端不变集或安全定理。
- **课题关联/可复用：** Run213将Run212三包历史速度外包与当前SMF盒相交，使真实可达第192拍两层因果backup从空恢复为全力矩区间。该交集不是CZ实现；下一步可复用CZ保留跨步联合约束。
- **待查问题：** 以固定预算持续保留相关性后，是否能阻止第193拍再次拒绝？

### Köhler、Müller、Allgöwer（2021）——既有文献，摘要及Run211理论条件复核
- **题名、作者、年份、链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler、Matthias A. Müller、Frank Allgöwer；2021；https://arxiv.org/abs/2105.03427 。
- **阅读日期及层级：** 2026-10-31；arXiv摘要与既有Run211 Assumption 7、Theorem 4阅读笔记核对；非全文重读。
- **问题/方法：** 有界估计误差的在线更新、homothetic tube和输出反馈MPC约束收紧。
- **关键假设/结论：** 递归可行与鲁棒约束满足依赖有效在线估计误差界、终端反馈/集合及初始可行性等条件。
- **局限：** 本仓库当前尚无所需终端条件；Run213一次有限步准入不能套用其全时域结论。
- **课题关联/可复用：** 估计界改善须通过控制准入与终端可行性双重检验，不能仅用集合宽度代表控制性能。
- **待查问题：** 如何为15-mode推力调度与间歇测量建立可计算终端安全策略？

**本轮自有证据：** [Run213日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run213_research_log.md)；第192拍恢复准入，但第193拍仍拒绝；去重论文数保持87。

## Run212 定向正文复核：历史一致集员估计与 CZ 集合运算（2026-10-30；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有文献，本轮原文分节核对
- **题名：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*。
- **作者、年份、出版信息：** Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036 。
- **可核验原文：** https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期与证据层级：** 2026-10-30；本轮直接核对作者公开原文 Definitions 2–3、Section 3.1 Proposition 1及Section 5估计递推片段；不是全篇重新精读。
- **研究问题：** 在有界扰动/量测误差下，如何用兼顾集合表达能力和运算复杂度的表示，保留状态估计中的测量一致性？
- **方法/模型：** CZ 表示 `{Gξ+c: ||ξ||∞<=1, Aξ=b}`，线性映射、Minkowski和广义测量交的闭合运算；Section 5 给出有界误差状态估计集合递推。
- **重要假设/定理：** Definition 3定义CZ；Proposition 1给出上述三种集合运算的精确恒等式，依赖正确的线性测量映射与有效有界集合；约束和生成元数量可能随时间增长。
- **主要结论：** CZ可在不立即丢失所有测量交相关性的情况下传播有界状态集合，并提供复杂度约简方法；集合运算本身不是本课题原创贡献。
- **局限：** CZ阶数/约束规模增长，降阶可能引入保守性；不能直接推导15-mode、未来推力跳变和无终端集合的MPC递归可行性。
- **与本课题关联/可复用：** Run212通过三次位置返包和连续姿态观测，精确排除Run211独立盒的旧速度下端；后续可将多包支持界/历史线性约束接入CZ信息状态和控制相关支持函数。Run212目前只实现严格支持外包，**不是**完整CZ后验。
- **待查问题：** 同一信息、同一控制过滤器、可比较计算预算下，保留完整历史相关性是否能让第192拍首力矩backup非空？如何限制CZ约束规模而不丢失安全证书？

**本轮自有证据（非文献定理）：** 精确三包支持界把第192拍速度下端由-2.4931037251954926收紧至-2.419767402278826 m/s，严格改善7040287/96000000 m/s；不声称已实现鲁棒MPC递归可行。详见[Run212日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run212_research_log.md)。

## Run211 定向复核：有限候选名义 MPC 与终端安全条件（2026-10-30；去重87篇不变）

### Köhler、Müller、Allgöwer（2021）——历史已读文献，本轮定向正文核验
- **题名：** *Robust output feedback model predictive control using online estimation bounds*。
- **作者/年份/来源：** Johannes Köhler、Matthias A. Müller、Frank Allgöwer；2021；arXiv:2105.03427，https://arxiv.org/abs/2105.03427 ；本轮未另行核实期刊DOI。
- **阅读日期与层级：** 2026-10-30；直接核对 arXiv HTML 的 Section II-A、Section IV-B、Assumption 7、Theorem 4及递归可行性证明片段；不是全篇重新精读。
- **研究问题：** 有噪声输出与有界扰动时，怎样利用在线可靠估计误差界减少鲁棒输出反馈MPC的约束收紧保守性？
- **方法/模型：** 可检测、增量可稳定的非线性系统；在线状态估计误差上界、homothetic tube、MPC终端约束和旧解移位。
- **重要假设/定理：** Assumption 7要求终端反馈、终端集合后继封闭、约束与终端代价条件。Theorem 4还要求其余观测器/增量Lyapunov条件、初始可行性及可靠初始误差界，才得出全时域递归可行与约束满足。
- **主要结论：** 在线有效估计误差界可以减少相对离线统一最坏界的保守性，并在上述前提下保证鲁棒约束满足。
- **局限：** 该理论不能直接继承到Run211独立区间盒、15-mode间歇测量、任意推力跳变且无终端RCI的有限候选名义优化。
- **与课题关联/可复用：** 可复用“在线估计误差界—约束收紧—终端移位”证明清单；Run211第192拍盒角点反例提示应优先检查历史相关性与误差界，而非仅优化名义轨迹。
- **待查问题：** 以历史一致CZ/轨迹可行集代替区间盒后，第192拍的伪角点是否被排除，能否给出更紧的控制相关支持函数？

### Wabersich、Zeilinger（2021）——仅出版社摘要与书目核验，不新增已读计数
- **题名：** *A predictive safety filter for learning-based control of constrained nonlinear dynamical systems*。
- **作者/年份/正式出版：** Kim Peter Wabersich、Melanie N. Zeilinger；2021；*Automatica* 129, Article 109597；DOI https://doi.org/10.1016/j.automatica.2021.109597 。
- **阅读日期与层级：** 2026-10-30；出版社摘要、引言公开节选及正式书目核验，**未全文精读、未核实定理编号**。
- **研究问题：** 如何对建议控制输入进行在线预测安全过滤，在存在模型不确定性和硬约束时寻找安全备份轨迹？
- **方法/模型：** 非线性受约束系统、数据驱动不确定性描述、模型预测安全过滤与备份轨迹。
- **重要假设/定理：** 公开摘要说明安全结论依赖模型不确定性和安全备份设计；具体假设、终端集合构造与证明细节**待全文核验**。
- **主要结论：** 论文提出预测安全过滤框架并报告非线性和四旋翼仿真案例。
- **局限：** 与本仓库四状态间歇SMF和推力调度的模型、量词与安全终端合同不相同；不能借其结论为Run211认证。
- **与课题关联/可复用：** 作为安全过滤的成熟方法基线；比较“名义计划可行”和“有终端备份的递归安全证书”的差异。
- **待查问题：** 全文中安全终端和备份可行性条件是否能在15-mode信息状态上构造；需要先核验正文而非推断。

**本轮自有证据（非文献定理）：** Run211有限候选8拍名义MPC在指定确定性轨迹中未改善Run210准入（191/200/200 → 133/200/81），并严格发现第192拍独立区间外包盒存在5拍速度不可认证角点；角点未证实与完整观测历史联合相容，不能称为物理不可生存。参见 [Run211日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run211_research_log.md)。

## Run210 新增定向正文阅读：SMF 与终端安全集的严格区分

### Didier、Wabersich、Zeilinger（2021）——新增第87篇去重文献
- **题名：** *Adaptive Model Predictive Safety Certification for Learning-based Control -- Extended Version*。
- **作者、年份、出版信息：** Alexandre Didier、Kim P. Wabersich、Melanie N. Zeilinger；2021；arXiv:2109.13033，相关 CDC 2021 会议论文；本轮未核实会议 DOI，不编造。
- **来源：** https://arxiv.org/abs/2109.13033 。
- **阅读日期及证据层级：** 2026-10-30；核对 arXiv HTML 正文 Sections II-A、II-B、III-A，Assumptions 1–2、Definition 1、Algorithm 1、Theorem 1；不是逐页全文精读。
- **研究问题：** 有界参数/扰动不确定下，如何对任意建议控制器构造具有安全终端和可恢复备份的自适应模型预测安全认证？
- **方法/模型：** 线性参数仿射系统、紧参数集合和有界加性扰动；在线参数集员辨识、鲁棒 tube、MPSC 有限时域优化及终端 safe set/backup 策略。
- **重要假设/定理：** Assumption 1 参数仿射依赖；Assumption 2 真实参数始终包含于逐步嵌套的参数集合。Definition 1 要求终端 safe set 上存在对未来全时域有效的备份控制。Theorem 1 的安全结论依赖上述假设和 Algorithm 1 的可行初始条件与终端备份，不适用于只有四拍安全准入的本仓库。
- **主要结论：** 可用模型更新与备份计划扩张改进安全过滤的可行集合；其证明的关键是终端可持续安全性，不是单纯有限步不越界。
- **局限：** 本文参数 SMF 与本课题状态后验 SMF 不同；未直接覆盖15-mode间歇位置测量和任意推力跳变。其安全结论不能从 Run210 的必要制动区间直接继承。
- **与本课题关联/可复用：** 用作后续 MPC 安全过滤的强基线；复用“终端 safe set＋旧备份移位/回退”的证明结构，严格区分可行核必要条件与终端充分条件。
- **待查问题：** 是否能在四状态模式图上构造可计算的终端备份集合，避免 Run210 正扰动第192拍拒绝？状态 SMF 外包能否保留相关性并支持该终端集合？

**本轮核验但不新增已读条目：** Wabersich、Zeilinger（2021），*A predictive safety filter for learning-based control of constrained nonlinear dynamical systems*，*Automatica* 129:109597，https://doi.org/10.1016/j.automatica.2021.109597；本轮只核对出版社摘要和书目，未逐式研读，不计入87篇。


## Run209 新增分章节阅读：Zonotope viability / discriminating kernel 与四旋翼

### Mitchell、Budzis、Bolyachevets（2019）——新增第86篇去重文献
- **题名：** Invariant, Viability and Discriminating Kernel Under-Approximation via Zonotope Scaling。
- **作者、年份及出处：** Ian M. Mitchell、Jacob Budzis、Andriy Bolyachevets；2019；arXiv预印本。
- **来源：** https://arxiv.org/abs/1901.01006 （未核实正式期刊 DOI，不编造）。
- **阅读日期与层级：** 2026-10-30，arXiv正文分章节阅读，核对 Sections 3.2、5.3、6（Proposition 6.2、Section 6.1 四旋翼例）、8；非逐页全文精读。
- **研究问题：** 对有状态/输入约束与对抗扰动的离散仿射系统，如何可扩展地构造不变、viable 和 discriminating kernels 的内近似，而不是仅做前向可达外包？
- **模型与方法：** center-generator zonotope、生成元缩放、凸规划；输入依赖状态生成元与扰动生成元；示例含双积分器和六维四旋翼纵向模型的线性化/误差包络。
- **关键命题/假设：** Section 3.2 定义不同量词下的可行核；Proposition 6.2 给出控制/扰动约束满足时，候选 zonotope 包含于有限时域 discriminating kernel 的充分条件。要求相应仿射模型与有界扰动外包有效；不是任意非线性/间歇测量信息状态的无条件定理。
- **主要结论：** 通过控制生成元与扰动集联合综合，能够计算保守的安全可行域内近似；六维四旋翼算例提供 zonotope 安全集的数值结果，展示与 ellipsoid 基线相比可能降低保守性，但依赖其冻结模型与误差界。
- **局限：** 有限时域、离散仿射近似与模型误差包络，未直接解决本仓库15-mode间歇位置测量、当前推力可见/未来推力跳变、条件化 SMF 信息状态与无限时域递归可行性。
- **与课题关联/可复用：** Run209 发现实际可达状态存在五拍内不可避免的姿态硬约束违约；因此必须在鲁棒安全过滤器前端建立 viability 必要条件，并以本文的 zonotope kernel 内近似作为可比的充分安全域基线。注意内近似失败不能证明全局无解；本轮的物理制动反例来自独立精确公式。
- **待查问题：** 是否能在相同计算预算内将姿态制动约束与 SMF/CZ 后验联合，建立既不丢弃位置—速度相关性又能保证因果控制的可行安全子域？如何向六维模型移植并保留有界扰动保证？

**未计入已读总数的候选：** Jean-Pierre Aubin（1990），A Survey of Viability Theory，SIAM J. Control Optim. 28(4):749–788，https://doi.org/10.1137/0328044；本轮仅核对出版社书目和摘要，尚未研读正文，待后续精读。

## Run208 新增书目/摘要核验：两阶段可调鲁棒优化的仿射后继策略

### Bertsimas、Goyal（2011）——新增第85篇去重文献
- **题名：** *On the Power and Limitations of Affine Policies in Two-Stage Adaptive Optimization*。
- **作者/年份/出处：** Dimitris Bertsimas、Vineet Goyal；2011；*Mathematical Programming*。
- **DOI/来源：** https://doi.org/10.1007/s10107-011-0444-4；MIT作者终稿书目及摘要 https://dspace.mit.edu/entities/publication/8fea3eec-4824-4b5c-8bb1-b7093e0bc2f2 。
- **阅读日期/证据层级：** 2026-10-30；**仅正式书目与摘要核对，未阅读全文或逐式核验**，不将此条记作精读。
- **研究问题/模型/方法：** 在右端项不确定的两阶段可调鲁棒线性优化中，比较第二阶段仿射决策规则与完全可调策略的最坏代价。
- **已核实主要结论：** 摘要指出仿射策略在一般不确定集合上可能严格次优，同时分析了某些集合结构下的适用性；具体近似比与最优性条件未逐式复核。
- **关键假设/定理：** 本轮仅核对摘要所述两阶段线性优化及不确定右端项；正文的定理编号、全部假设和证明**待核验**。
- **局限：** 论文不涉及四旋翼动力学、SMF、15-mode间歇测量或推力相关扰动；不能将其近似比定理直接移植到本仓库。
- **与本课题关联/可复用：** Run208 采用下一可见推力的仿射后继力矩规则，属于经典 adjustable robust optimization 思想。可复用“第一阶段共享动作、第二阶段仅依赖已揭示信息”的非预见性建模，但需对本仓库单独建立集合包含与硬约束证书。
- **待查问题：** 在后继姿态/位置观测可见的连续信息空间中，能否用有限复杂度观测仿射/分区策略给出严格可靠的控制可行域，并量化相对测量无关两层桥的严格收益？

**本轮复核的历史文献：** Köhler、Müller、Allgöwer（2021），*Robust output feedback model predictive control using online estimation bounds*，https://arxiv.org/abs/2105.03427；本轮只核对摘要及Run206/207已有定理阅读笔记，没有重新阅读全文。它要求的终端及递归可行性前提尚未由Run208满足。

**Run208 自有结果（不是上述论文定理）：** 四状态精确有理数两层 backup 允许下一拍非零力矩，在合法可达交变历史第95拍将Run207空准入区间严格扩展为非空；第96拍仍拒绝。新策略不使用下一测量数值，尚未证明测量条件化增益或无限时域安全。见 [Run208日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run208_research_log.md)。

**去重计数：历史84篇 + 本轮新增Bertsimas–Goyal 1篇 = 85篇；阅读层级严格区分。**

## Run207 定向核验：因果移位桥与终端可行性的差异（既有84篇，不重复计数）

### Köhler、Müller、Allgöwer（2021）
- **题名/作者/年份/链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler, Matthias A. Müller, Frank Allgöwer；2021；https://arxiv.org/abs/2105.03427 。
- **本轮日期/证据层级：** 2026-10-30；核对 arXiv 正式题名、作者、摘要及 Run206 已有的 Algorithm 1、Assumption 7、Theorem 4 历史精读记录；本轮未重新逐式阅读全文。
- **问题/方法/结论：** 有界测量噪声与扰动下，结合在线有效估计误差界、homothetic tube、约束收紧和终端条件，建立鲁棒输出反馈 MPC 的约束保证。历史精读记录指出递归可行性依赖初始可行性、增量稳定/可检测及终端条件。
- **局限/课题关系/可复用/待查：** 论文没有直接认证本仓库15-mode位置丢包、任意推力调度的盒重置一步桥。可复用“旧计划移位须保留终端可行性”的证明检查顺序；下一步需明确本仓库是否存在后继测量条件化的安全控制策略，不能把一次可移位等同于无限时域递归可行。

### Lorenzetti、Pavone（2020）
- **题名/作者/年份/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；Joseph Lorenzetti, Marco Pavone；ECC 2020；DOI https://doi.org/10.23919/ECC51009.2020.9143979 ；作者版 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **本轮日期/证据层级：** 2026-10-30；核对论文摘要及 Run204/205 已有的固定截面 tube、RPI 相关阅读笔记；不宣称本轮全文精读。
- **问题/方法/结论：** 离散线性系统中以固定截面 tube 和 RPI 误差集进行输出反馈鲁棒 MPC 设计，降低在线复杂度。
- **局限/课题关系/可复用/待查：** RPI 终端及误差管束不能由 Run207 的五拍盒重置安全约束替代。下一步可借鉴其终端设计和误差耦合思路，但需要在本仓库四状态调度与观测图上独立建立不变性。

**Run207 自有结论：** 260项精确有理约束可保证同一当前力矩之后，任意合法下一观测后验均有四拍零力矩备份；交变扰动可达场景第95拍该更强桥条件拒绝，而四拍零力矩备份仍可行。这是特定控制模板的一步条件性充分保证，不是上述论文的定理，也不是终端 RCI。详见 [Run207 日志](../../archive/legacy_planar_direct_control_20261103/docs/research/run207_research_log.md)。

## Run206 定向复核：真实可达后验与有限时域 backup 的区别（仍为历史84篇）

### Köhler、Müller、Allgöwer（2021）
- **题名/作者/年份/链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler, Matthias A. Müller, Frank Allgöwer；2021；arXiv:2105.03427，https://arxiv.org/abs/2105.03427；作者全文 https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf 。
- **阅读日期/层级：** 2026-10-30；本轮定向重读作者全文 Section III-C（set-membership bounds）、Section IV Algorithm 1、Assumption 7、Theorem 4 及旧计划移位证明；承接 Run200 既有深读，不宣称重读全部定理。
- **研究问题/方法：** 有界扰动及噪声下的非线性鲁棒输出反馈 MPC；使用在线有效的估计误差界、homothetic tube、约束收紧及终端成分。
- **关键假设/结论：** Theorem 4 需要 Assumptions 1、3、4、5、7，δ-IOSS 与 δ-ISS CLF、初始优化可行及有效初始误差界；移位候选与终端包含支撑递归可行性及真实约束满足。单步/四拍备份安全准入不满足这些前提。
- **局限/课题关联/可复用技术/待查：** 论文提供输出反馈 MPC 证明骨架及四旋翼数值示例，但未直接认证本仓库15-mode位置缺包与推力每拍任意跳变。下一步需证明任意合法后继观测下存在同一当前动作和可行后继备份；不能仅把更紧的后验解释为安全控制器。

### Alamo、Bravo、Camacho（2005）
- **题名/作者/年份/链接：** *Guaranteed state estimation by zonotopes*；Teodoro Alamo, José Manuel Bravo, Eduardo F. Camacho；Automatica 41(6):1035–1043（2005）；DOI https://doi.org/10.1016/j.automatica.2004.12.008 。
- **阅读日期/层级：** 2026-10-30；仅正式书目、摘要和历史笔记交叉核对；**未取得可逐式核验的全文**，不引用具体未核实定理。
- **研究问题/方法/结论：** 以 zonotope 构造有界过程/测量不确定性下的可靠状态集合外包；说明保证包含与集合收紧是既有集合估计技术。
- **局限/课题关联/可复用技术/待查：** 该估计文献不提供本仓库四拍控制准入或递归终端保证；Run206 的两包速度约束是冻结离散积分恒等式，非新型 zonotope 方法。后续比较区间、CZ 与测量条件化支持函数时需控制同一信息和计算预算。

**Run206 自有结果（不是上述论文的定理）：** 真实零初态、合法扰动/观测历史的精确 Fraction 递推中，纯区间估计在第55/63/57拍首次拒绝四拍 backup；两包速度约束后对应100拍内未拒绝/第96拍拒绝/100拍内未拒绝。它仅证实三条指定轨迹上有限前缀安全和过滤器保守性差异，Gate A 仍 blocked。

## Run205 定向复核：移动中心信息盒的四拍控制准入（历史84篇内，不重复计数）

### Lorenzetti、Pavone（2020）
- **题名/作者/年份/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；Joseph Lorenzetti, Marco Pavone；ECC 2020；DOI https://doi.org/10.23919/ECC51009.2020.9143979；作者全文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **阅读日期/证据层级：** 2026-10-30；核对摘要与作者版中的输出反馈单管束、RPI和终端条件定位；承接历史 Run203/204 已有章节复核，不声称本轮逐定理重读。
- **研究问题/模型/方法：** 离散 LTI、加性有界扰动及测量噪声的输出反馈鲁棒 Tube MPC；估计误差/跟踪误差集合、约束收紧、终端控制。
- **关键前提/结论：** 论文的递归可行性与鲁棒约束保证依赖适当 RPI/终端包含及初始可行性等条件；本轮仅固定四拍开环 backup，未满足这些条件。
- **局限/课题关联/可复用技术/待查：** 不直接覆盖15-mode间歇位置观测与未来推力任意跳变。可复用终端约束与移位可行性证明框架；待查观测条件化、控制先于后继边的统一递归策略。

### Scott、Raimondo、Marseglia、Braatz（2016）
- **题名/作者/年份/链接：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott, Davide M. Raimondo, Giuseppe Roberto Marseglia, Richard D. Braatz；Automatica 69:126–136 (2016)；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期/证据层级：** 2026-10-30；核对摘要、Introduction 和集合表示/精确交投影运算的定位，结合 Run202 的既有深入记录；本轮未逐式复核全文。
- **研究问题/模型/方法：** 用 constrained zonotope 表示有界不确定状态集合并执行集合估计/故障检测。
- **关键前提/结论：** 不限制表示复杂度时 CZ 可表示凸多面体，且标准集合运算有代数表达；不能由此自动得到控制律、稳定性或递归可行性。
- **局限/课题关联/可复用技术/待查：** Run205 仅使用独立坐标区间外包，舍弃 CZ 相关性；下一轮需对可达的条件化 CZ 后验使用支持函数/外包并比较与区间过滤器的保守性。

**Run205自有结果（不是上述论文的结论）：** 固定四拍开环 backup 下，移动中心盒的原始硬约束可接受力矩区间可由精确有理数和未来推力顶点穷举计算；合成中心未证明可由冻结初态到达，Gate A 仍 blocked。

## Run204 定向复核与证据边界（仍为历史84篇，不新增计数）

### Athanasopoulos、Smpoukis、Jungers（2017）
- **题名/作者/年份/链接：** *Invariance in Constrained Switching*；Nikolaos Athanasopoulos, Konstantinos Smpoukis, Raphaël M. Jungers；2017；https://arxiv.org/abs/1702.00598；相关期刊版本题名为 *Invariant Sets Analysis for Constrained Switching Systems*，DOI https://doi.org/10.1109/LCSYS.2017.2714840（区分版本）。
- **阅读日期与层级：** 2026-10-30；核对 arXiv 摘要、Introduction、图约束切换与 invariant multi-set 定义/基本描述；未重新证明全文定理。
- **研究问题/模型/方法：** 有向自动机约束切换的离散线性扰动系统，按图节点定义 invariant multi-set，以前向/后向可达映射研究不变集合。
- **关键前提/结论：** 系统切换序列受合法图边约束，图索引集合必须满足相应边的后继包含；稳定性与普通单一不变集存在性不能简单等同。具体近似定理有稳定性等前提，本轮不援引未核实的适用性。
- **局限/课题关联/可复用/待查：** 文中主要为切换系统不变性框架，不直接解决本仓库“控制先于未知边、观测更新改变后验”的信息状态；可复用图索引不变性表述。Run204 对固定原点直积物理状态盒的排除是**本仓库冻结合同自己的推导**，不是该论文定理。下一步构造移动中心/相关后验集合上的因果后继包含。

### Lorenzetti、Pavone（2020）
- **题名/作者/年份/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；Joseph Lorenzetti, Marco Pavone；2020 ECC；DOI https://doi.org/10.23919/ECC51009.2020.9143979；作者全文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **阅读日期与层级：** 2026-10-30；核对作者全文 Section II Assumptions 1–2、Section III-A RPI定义、Section IV-A/B/C 的式(7)–(9)与终端结构，结合原有Run203深读记录。
- **研究问题/方法：** 离散LTI、加性有界扰动/测量噪声下的输出反馈 Tube MPC；Luenberger估计、误差RPI、名义轨迹约束收紧和终端约束。
- **关键假设/结论：** 论文要求可控可观、紧有界噪声集合、合适的稳定估计器和反馈及终端条件；本轮区间SMF+饱和中点LQR没有满足其终端/误差管束条件，不能转移递归可行性结论。
- **局限/关联/复用/待查：** 原文LTI与持续观测结构不覆盖未来推力任意跳变及15-mode位置缺包；可复用终端—RPI—约束收紧—移位的证明架构。待查如何将后验移动中心和未来观测分支纳入同一可计算控制条件。

### Ping、Yao、Ding、Li（2022）
- **题名/作者/年份/链接：** *Tube-Based Output Feedback Robust MPC for LPV Systems With Scaled Terminal Constraint Sets*；Xubin Ping, Junying Yao, Baocang Ding, Zhiwu Li；IEEE Transactions on Cybernetics 52(8):7563–7576，2022；DOI https://doi.org/10.1109/TCYB.2020.3041334；PubMed PMID 33417577。
- **阅读日期与层级：** 2026-10-30；**仅正式摘要复核**，没有重读正文定理/公式；延续历史Run131的同级证据。
- **问题/方法/结论：** 有界扰动和噪声的离散LPV输出反馈Tube RMPC，离线设计查找表、在线约束收紧与scaled terminal；论文声称递归可行性/稳定性，具体定理前提需原文核对。
- **局限/关联/复用/待查：** 与本课题的LPV、输出反馈和终端收紧高度相关，但不能把其scaled terminal当作新机制；尚未核对是否支持任意快速推力跳变、间歇位置包及CZ相关性。下一步按原文逐式核对再移植。

**Run204自有实验（非论文结论）：** 15-mode五边环排除固定原点直积物理状态盒族，为精确类特定反证；四状态区间SMF中点饱和反馈9条150 tick数值探针显示多种硬约束失败。不能由此推断一般鲁棒输出反馈Tube MPC不可行。

## Run203 定向复核（历史84篇内，不重复计数）

### Lorenzetti、Pavone（2020）
- **题名/出处/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；ECC 2020；DOI https://doi.org/10.23919/ECC51009.2020.9143979；作者全文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **阅读日期/层级：** 2026-10-30，定向重读 Section IV-C/D/E，式(9)–(13)及 Proposition 1；原84篇已有记录。
- **问题、模型和方法：** LTI离散系统、有界加性过程/测量噪声、输出反馈Tube MPC；名义优化使用终端集合与收紧约束，误差RPI支撑真实状态/输入约束。
- **关键假设/结论：** 终端控制满足正不变包含、名义约束可行，误差初态在RPI且初始优化可行，才能得到递归可行与鲁棒约束满足；本轮三拍安全准入没有这些条件。
- **局限/本课题关联/复用：** 持续观测的LTI和固定管束结构不能直接覆盖15-mode间歇位置观测及未来推力任意跳变。复用其“终端不变—误差管束—约束收紧—旧解移位”证明结构。
- **待查：** 对模式相关SMF后验如何形成因果统一的后继终端包含，不误用三拍硬约束PASS。

### Athanasopoulos、Smpoukis、Jungers（2017）
- **题名/出处/链接：** *Invariance in Constrained Switching*；arXiv:1702.00598，https://arxiv.org/abs/1702.00598；相关期刊版本 *Invariant Sets Analysis for Constrained Switching Systems*，IEEE Control Systems Letters 1(2):256–261，DOI https://doi.org/10.1109/LCSYS.2017.2714840（版本题名有别，勿混淆）。
- **阅读日期/层级：** 2026-10-30，摘要、Introduction及仓库Run135/136历史阅读记录的交叉核对；本轮未重新逐式验证全文所有定理。
- **问题、模型和方法：** 由有向自动机约束切换序列的离散线性扰动系统；使用节点索引的不变多集合研究可行的后继包含。
- **关键结论/限制：** 图约束可以让不变集合依赖模式；外逼近算法的收敛保证还需稳定性、扰动集合等前提，不可直接移植至本仓库秩亏噪声和控制前于后继边的量词结构。
- **本课题关联/可复用/待查：** 15-mode终端候选必须逐合法边满足一拍包含；下轮需验证是否存在因果反馈，且同一当前控制必须覆盖所有未揭示的后继边。

**Run203 自有结果（非论文结论）：** 在冻结四状态模型、指定零观测历史及Run202精确有理后验外包下，三拍未来推力端点枚举给出原硬约束局部PASS；永久零力矩72拍速度越界构成反例。证据只属于有限时域审计，不是RCI、递归可行性或稳定性证明。

## Run202 定向重读与新推导（原84篇内，不重复计数）

### Scott、Raimondo、Marseglia、Braatz（2016）
- **题名：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；*Automatica* 69:126–136；DOI：https://doi.org/10.1016/j.automatica.2016.02.036；作者版：https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf
- **阅读日期/层级：** 2026-10-30，原文 Definition 2（式(6) generalized intersection）、Definition 3（式(9) CZ），Section 3.1；属于原84篇的定向重读。
- **问题/方法/假设：** 有界噪声下离散线性系统的集合状态估计；CZ以 `c+Gξ, ||ξ||∞≤1, Aξ=b` 表示，并可通过增加有界噪声生成元与等式约束精确更新测量一致集合。若不压缩生成元与约束，其规模持续增长。
- **结论/局限：** 精确线性像、Minkowski和及 generalized intersection 是既有技术；本轮四状态代码只是实例化。它不提供 MPC 终端不变性或实时求解保证；浮点 LP 投影支持不自动变成数学证书。
- **本课题复用/待查：** 固定推力下按真实姿态/位置观测更新 `(px,vx,phi,omega)` 的精确 CZ；下一步比较控制相关后验支持、固定预算约减与实际控制准入，避免把 CZ 本身当创新。

### Lorenzetti、Pavone（2020）
- **题名：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；2020 ECC；DOI：https://doi.org/10.23919/ECC51009.2020.9143979；全文：https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf
- **阅读日期/层级：** 2026-10-30，Section II 问题模型、Section IV 的管束误差/约束收紧与终端条件；原84篇中的定向重读。
- **问题/方法/假设：** 线性离散定常系统、有界加性扰动与噪声，使用输出反馈鲁棒 MPC 与离线 RPI/终端约束；递归可行性不能仅由状态估计集合包含推出。
- **局限/关联/待查：** 本项目有间歇位置测量、当前推力可见但未来任意跳变的 LPV 合同，不符合直接套用其 LTI/持续观测证明的前提。需要独立的模式相关 backup、控制误差管束和终端证书。

**Run202新推导（非论文原定理）：** 对零位置/姿态观测历史、固定已知推力，利用两次位置观测消去初始速度，得到严格返包后速度界 `|v_n|≤2σp/(nh)+h(n+1)(Tσφ+d(T))/2`；15 tick 低/高推力下相对独立区间预测可靠收紧35.1%/36.0%。精确 CZ 递推和该恒等式是冻结模型审计，不宣称新通用滤波算法或鲁棒控制定理。

## Run200 定向复核与课题判断（下述三篇已在历史84篇内，不重复计数）

### Köhler、Müller、Allgöwer（2021）
- **题名/链接：** *Robust output feedback model predictive control using online estimation bounds*；https://arxiv.org/abs/2105.03427
- **阅读日期/层级：** 2026-10-30，原文 Section IV-B 的 Algorithm 1、Assumption 7、Theorem 4 及其证明中旧解移位部分；既有 Run127 记录亦注明精读。
- **问题与方法：** 有界扰动和噪声下的非线性输出反馈 MPC，使用在线估计误差界和 homothetic tube，满足可行性与约束保证。
- **定理假设/结论：** Theorem 4 需要 Assumptions 1,3,4,5,7、δ-IOSS Lyapunov、δ-ISS CLF、初始优化可行及初始估计误差界；证明依赖终端闭合和 shifted-plan 递推。数值例包含10状态四旋翼。
- **局限/关联/复用：** 不可把其保证直接转移至仓库有推力相关 residual、缺测图的四/六状态合同；复用的是“后验有效界—收紧—终端—移位”证明骨架，不主张方法首创。
- **待查：** 将旧计划收紧的单调性与本仓库15-mode信息集、未来未知推力调度统一建模。

### Scott、Raimondo、Marseglia、Braatz（2016）
- **题名/链接：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*，Automatica 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf
- **阅读日期/层级：** 2026-10-30，Definition 3、Proposition 1、式(11)–(13)；既有 Run126/129/164/167/174 等多轮核查。
- **问题与方法：** 有界误差状态估计中的集合交、线性像、Minkowski和；CZ通过等式约束表示复杂相关性。
- **关键结论：** generalized intersection 对给定实际测量的一致状态集可精确表达，复杂度随运算增长。
- **局限/关联/复用：** CZ 运算本身不提供控制终端不变性或递归可行性；本轮先用区间精确交集作为标量 SMF 基线，再与 CZ 强基线比较。
- **待查：** 实际四状态后验约束如何在固定复杂度预算下安全外包而不破坏终端包含。

### Mulagaleti、Mejari、Bemporad（2025）
- **题名/链接：** *Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate*，IEEE TAC 70(2):1259–1266；DOI https://doi.org/10.1109/TAC.2024.3454528；预印本 https://arxiv.org/abs/2309.02384
- **阅读日期/层级：** 2026-10-30，Definition (4)–(6)、Section II 的调度可见性与后继全称量词；既有 Run197–199 重读综合 SDP。
- **问题与方法：** 已知当前 LPV scheduling 参数、后继参数在变化率集合内，联合综合参数依赖 RCI 与 vertex control。
- **关键假设/结论：** 当前参数可见后选控制；对所有后继参数与扰动同一个当前控制须满足后继集合包含。固定法向、configuration 和 SDP 是充分综合类。
- **局限/关联/复用：** 本仓库未来推力允许全区间跳变，不能虚构较小变化率界；Run199 的浮点 PrimalInfeasible 仅否定特定数值模板，不能推出一般控制不可行。
- **待查：** 将本轮标量移位证明中的 terminal inclusion 换成当前推力条件化、未来任意跳变的共同后继包含。

## 历史已阅读/核对论文条目（84篇，85条历史记录去重合并，原始阅读说明保留）

## Athanasopoulos, Smpoukis, Jungers — Invariance in Constrained Switching Systems
- 年份/全文：2017；[arXiv:1702.00598](https://arxiv.org/abs/1702.00598)。
- Run 135 精读：pp. 2--6，Assumptions 1--4、Definitions 1--3、Proposition 1、Theorems 1--3。
- Run 136 新增精读：Sections 2.1--3.2、6，重点 forward reachable recursion (7)--(16)、Theorem 2 的缩放外包及 T-product lift。确认外包定理要求每个标签扰动为 full-dimensional C-set；本项目逐拍秩亏 disturbance image 不可直接套用。
- 方法/关键结论：以图节点索引 invariant multi-set；逐边 one-step reachable inclusion 与不变性等价；在稳定、强连通和 C-set disturbance 假设下，forward reachable multi-set 收敛到 minimal invariant multi-set，并可构造有限外逼近；约束内还可后向求 maximal admissible multi-set。
- 与本项目关系：15-mode estimator-error invariant family 和 reachable-sum 外逼近已有直接理论，不能作为创新。当前部分边扰动低维，不满足其 C-set 内点假设；Run 135 的 scalar Bellman contraction 独立证明，下一轮几何外逼近不能无条件照搬其定理。

## Scott, Raimondo, Marseglia, Braatz — Constrained zonotopes: A new tool for set-based estimation and fault detection
- 年份/出处：2016, *Automatica*, 69:126–136；DOI：https://doi.org/10.1016/j.automatica.2016.02.036
- 方法/关系：CZ 定义、精确集合运算与复杂度约减；是本项目 CZ 基础，因此“CZ 保留相关性”不是创新。
- Run 126 新增核查：重读 Sections 3.1、4.1–4.3、Appendix Algorithm 1 与 (A.9)–(A.10)，并在冻结 Run-123 后验复现 lift-then-reduce 外包及控制准入临界复杂度。该复现是强基线，不是新算法。
- Run 129 新增核查：逐式重读 Appendix (A.9)–(A.10) 的基生成元放大、残余坐标逆缩放与删除顺序。论文维护几何外包，不维护到给定终端内集的包含映射；本轮携带谱系只是实现审计，不能宣称替代或改进 Scott 方法。
- Run 164 定向重读全文 Sections 2.2、3.1--3.2 的 generalized intersection、线性像与集合表示。
  CZ 可精确表示多面体和线性等式切片；固定观测值后的 fiber 是标准 generalized intersection，
  因而本轮的 fiber support LP 是已知集合运算的实例，不作 CZ 算法创新声明。
- Run 167 精读 Section 2 Definition 2、Section 3.1 Proposition 1及证明、Section 5式(31)--(33)。
  bounded-error posterior是预测集与**已实现观测**逆像的相交；精确相交或任何可靠外包都不能删除
  与先验和噪声合同一致的极端观测。因此它能缩小单个观测后的fiber，却不能自动保证所有可能观测
  的全局创新范围满足控制阈值。
- Run174 重读 Section 2 Definition 2、Section 3.1 Proposition 1及证明、Section 5估计递推。
  generalized intersection只保留与实际观测一致的预测状态；它不改变真实plant状态，因此不能
  将“posterior收缩”解释为“物理速度重置到配置初始盒”。
- Run185 核对作者版摘要与Section 1的问题定位；未重新精读降阶算法。CZ精确线性像、交集及
  固定复杂度外包仍是后续强基线；本轮单对耦合法向保留相关性不构成CZ算法创新。

## Alamo, Bravo, Camacho — Guaranteed state estimation by zonotopes
- 年份/出处：2005, *Automatica*, 41(6):1035--1043；DOI：https://doi.org/10.1016/j.automatica.2004.12.008
- Run 164 阅读层级：核查正式摘要、问题设定和可访问正文片段；未取得可稳定逐页引用的完整作者稿。
- 方法/关键结论：把先验预测与有界测量一致条带求交，并构造含真状态的一族 zonotope 外包；
  测量更新的对象是给定实际观测后的 consistent-state set，而非把所有可能观测重新并成一个集合。
- 与本项目关系：支持“先按可见观测形成 fiber、再查询控制方向 support”的信息时序；本轮不引用其
  外包最优性定理，也不据此声称新 SMF 更新。

## Kopetzki, Schürmann, Althoff — Methods for Order Reduction of Zonotopes
- 年份/出处：2017, CDC, 5626–5633；DOI：https://doi.org/10.1109/CDC.2017.8264508；作者全文：https://mediatum.ub.tum.de/doc/1442501/1442501.pdf
- Run 129 精读：Introduction、Section II 的 box/transformation methods、Section III 的 PCA/clustering/constrained optimization、Section IV 的约束与评价。
- 方法/关键结论：系统比较 zonotope 外包约减，以体积或几何误差评价；可通过变换、聚类或优化构造较紧外包。
- 与本项目关系：它是普通几何 order reduction 的强基线，但不处理 CZ equality slice，也不保证压缩集仍落在指定 terminal inner set 内。几何更紧不能替代终端包含证书。
- 本项目状态：Run 129 排重基线；不把几何约减本身当作创新。
- Run 130 新增核查：精读 Section III-D。该节直接优化 reduced generator matrix `C`，用 `sum_j |C^{-1}G|_{ij} <= 1` 保证原 zonotope 被包含，并用 determinant/volume 目标和 `fmincon` interior-point 求解。因此“非-Scott + 包含硬约束的 outer reduction”已有直接近邻。

## Robbins, Glunt, Thompson, Pangborn — Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations
- 年份/出处：2026, ACC 2026, pp. 585–592；IEEE：https://ieeexplore.ieee.org/document/11616451；机构记录：https://pure.psu.edu/en/publications/online-constraint-tightening-for-mpc-using-constrained-zonotope-r/
- Run 126 核查层级：取得正式摘要、书目信息和章节目录；正文在 Introduction 后要求机构/会员访问，未完成全文精读。
- 已知覆盖：摘要明确包含 nonlinear error reachability、在线 MPC tightening、无需优化的 CZ-to-zonotope 外包和 LTV 数值例。
- 边界：不能据摘要推断具体外包公式、复杂度、终端/递归可行性或是否保护控制方向；首次性保持未知。
- Run 161 新增核查（2026-10-11）：IEEE 与 Penn State 页面确认 ACC 2026 页码585--592及正式摘要；
  仍未取得正文。本轮只把它作为“online CZ reachability/tightening 已有”的排重线索，不引用算法或定理。

### Run170 补充核对（同一论文去重合并）
- 年份/出处：2026 American Control Conference；IEEE Xplore document 11616451。
- Run170阅读层级：仅核查IEEE摘要，全文未取得，首次性未知。
- 摘要层面内容：用CZ及非线性polyhedral envelopes在线传播误差；以无需优化的CZ到zonotope
  外包接Pontryagin差收紧，并在LTV MPC数值例上比较。
- 与本项目关系：这是联合非线性误差传播与在线收紧的最强近邻线索；未读正文前不能声称缺测
  SMF、跨时刻递归可行性或固定预算严格优势未被覆盖。

## Le, Stoica, Dumur, Alamo, Camacho — Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation
- 年份/出处：2011, CDC-ECC；DOI：https://doi.org/10.1109/CDC.2011.6161131
- 方法/关系：zonotopic SMF + tube output-feedback MPC；直接说明该组合不是创新。

## Rego, Raffo, Scott, Raimondo — Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems
- 年份/出处：2020, *Automatica*, 111:108614；DOI：https://doi.org/10.1016/j.automatica.2019.108614
- 方法/关系：CZ mean-value/Taylor guaranteed nonlinear propagation/update；四旋翼非线性阶段的重要传播基线。
- Run 179 全文精读 Section 2、Section 3.1、Sections 4.1--4.5、Theorems 1--3、Lemma 1、
  Corollaries 1--2、Remarks 8--10及式(22)。其固定阶外包递推针对已知输入和已实现测量下的
  单个posterior；可作为单fiber传播原语，但不表示连续可见`d`上的information-family策略图。

## Cong, Wang, Zhou — Stability of linear set-membership filters with respect to initial conditions: An observation-information perspective
- 年份/出处：2025, *Automatica*；DOI：https://doi.org/10.1016/j.automatica.2024.111993
- 方法/关系：Observation-Information Tower、CZ-SMF 初值稳定性；须与控制闭环稳定性区分。

## Qiu, Yang, Zhu, Mousavinejad — Output feedback model predictive control based on set-membership state estimation
- 年份/出处：2020, *IET Control Theory & Applications*；DOI：https://doi.org/10.1049/iet-cta.2019.0881
- 方法/关系：ellipsoidal SMF + output-feedback MPC；是 CZ 方法必须比较的几何基线。

## Köhler, Kötting, Soloperto, Allgöwer, Müller — A robust adaptive model predictive control framework for nonlinear uncertain systems
- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.5147
- 研究问题：递归模型/参数更新后，如何仍保证 robust recursive feasibility 与 constraint satisfaction。
- 方法/关键结论：set-membership estimation 提供逐步更准确的参数不确定集合；论文明确推导 estimation algorithm 与 tube/set-based RAMPC 所需的 monotonicity / non-increasing 条件，并在 incremental-Lyapunov tube 中给出可实现条件。
- 与本项目关系：第28章 exact CZ shift-nesting 属于同一“更新必须与旧预测兼容”的大理论边界；因此 nesting 本身不是创新。真正未闭合的是 fixed-complexity CZ reduction 是否保持这种兼容性。
- 局限：处理参数不确定性 RAMPC，不是当前 output-feedback CZ state posterior 的固定复杂度压缩接口。
- 本项目状态：作为 recursive-update monotonicity 的强基线。

## Lu, Cannon, Koksal-Rivet — Robust adaptive model predictive control: Performance and parameter estimation
- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.5175
- 方法/关系：固定复杂度参数/预测集合 + robust tube MPC；证明 recursive feasibility 与 ISS，是 fixed-complexity 强基线。
- Run 161 新增精读：开放全文 Sections 3.1--3.2、Lemma 1、Section 4.1 Proposition 1、
  Section 5.2 Theorem 3。固定法向参数集合更新保持真参数包含和嵌套，预测 tube 对整个参数集与
  disturbance robustify；递归可行性另由旧解移位与 terminal 条件证明。该结构支持“可靠在线集合
  可降低保守性”，但其对象是常参数集合，不能把本项目 state posterior 直接当作 future residual。
- Run 166 重新精读开放全文 Sections 3.1--3.2、Lemma 1、Section 4.1 Proposition 1及证明，
  并复核Section 6.1的同更新律比较。固定复杂度外包须同时保持真参数包含与跨时刻嵌套；旧解移位
  和terminal条件另行承担递归可行性。因此本轮只能把可见state范围作为独立初始化合同，不能用其
  替代future process residual或物理input authority。

## Peschke, Mönnigmann — Robust adaptive tube tracking model predictive control for piece-wise constant reference signals
- 年份/出处：2023, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.6814
- 方法/关系：nominal model/reference 在线变化时的 adaptive tracking MPC；明确 nominal-model update 会使 nominal-centered tube 的 recursive-feasibility proof 更困难。

## Köhler et al. — Robust adaptive MPC using control contraction metrics
- 年份/出处：2023, *Automatica*；DOI：https://doi.org/10.1016/j.automatica.2023.111169
- 方法/关系：CCM + set-membership + adaptive tube，含 planar quadrotor；四旋翼阶段强近邻。

## Andrade, Normey-Rico, Raffo — Tube-Based Model Predictive Control Based on Constrained Zonotopes

- **书目信息/版本**：Richard Andrade, Julio E. Normey-Rico, Guilherme V. Raffo, *Tube-Based Model Predictive Control Based on Constrained Zonotopes*, *IEEE Access*, vol. 12, pp. 50100–50113, 2024, DOI https://doi.org/10.1109/ACCESS.2024.3381622。公开全文：https://www.researchgate.net/publication/379286185_Tube-based_Model_Predictive_Control_based_on_Constrained_Zonotopes 。**2026-11-03实际阅读**：公开PDF正文§I–V，重点核验§II LMI反馈/RPI可达集、§III CZ-MPC、§IV HIL模型和§V计算结果；全文已读。
- **对象与模型**：对象是带悬吊载荷的**倾转旋翼（tiltrotor）UAV**，不是四旋翼/普通多旋翼。广义坐标q包含载荷位置3、Euler姿态3、载荷摆角2、左右推进器倾转角2，共10个广义坐标；物理状态xs=[qdot;q]为20维。为跟踪x/y/z/yaw，增广4个积分状态，最终控制误差模型为**24状态LPV/LTV**。输入u=[f_r,f_l,τ_r,τ_l]，即左右两个推进器推力和左右倾转伺服力矩；不是四电机独立推力。
- **测量与估计**：论文假设离散系统全部状态可由测量和/或估计提供；但HIL中Gazebo插件的virtual sensor直接读取physics engine状态向量，未实现真实传感器噪声、观测器或丢包模型。不能将其作为输出反馈SMF/CZ证据。
- **Tube/CZ MPC**：LPV不确定性用加性集合W表示；离线通过LMI求反馈K，基于zonotope reachability计算RPI误差集；名义状态集与输入集用constrained zonotopes表示，在线MPC直接优化CZ生成元变量。Gurobi求解；HIL平台为ProVANT/Gazebo，嵌入式计算机NVIDIA Jetson TX2。
- **实时与实验边界**：采样时间12ms；标准多面体MPC最常见求解时间约29ms，CZ-MPC约20.9ms，约快30%，但**两者典型计算时间仍超过12ms采样周期**。实验是HIL，不是真实飞行。论文宣称鲁棒渐近稳定依赖LPV不确定集合、离线RPI集及LMI反馈设计条件，不能移植成四旋翼/SMF输出反馈定理。
- **可迁移与局限**：可迁移的是高维LPV下离线RPI zonotope、CZ名义状态/输入集合和生成元变量优化；不能把24状态倾转旋翼＋吊载模型当作四旋翼12状态先例，也不能把virtual sensor当作状态估计。它是高阶CZ Tube MPC计算方法的对照，不改变四旋翼模型排序。
## Dey, Bhasin — Output Feedback MPC with Adaptive Tubes
- 年份/出处：2026, arXiv:2605.23661
- 方法/关系：adaptive observer 的 state/model/initial-condition estimates 联动 tightening、terminal ingredients 和 tube geometry；作者建立 recursive feasibility 与 robust exponential stability。与本项目 recenter/update gate 高度相邻，必须全文排重。
- Run 131 新增核查：精读 IV-C--IV-F、Criterion 1、Algorithm 1、Theorem 2 与 Appendix IV。terminal set 可随 estimates 更新，但必须通过 consecutive compatibility criterion；失败时保持旧 point estimate/回退集合，backup setup 与旧解移位封闭递归可行。故 adaptive terminal、更新准入与 fallback 不能作为本项目创新。
- Run 148 新增重读：Sections IV-A--F、Assumptions 2--4、Criterion 1、Theorem 2 与 Appendix IV。论文以 `X tilde_{t,i}` 外包 estimation error、Pontryagin difference 收紧 state-estimate constraints，再用 homothetic observer-state tube；其输出模型无 measurement noise，也不保留 bounded-dropout observation histories 内 `(eta,e)` 的路径相关联合像。因此它是在线收紧/terminal/recursive-feasibility 强基线，但不直接替代本轮三种 correlated return seed。
- Run 162 新增重读：Criterion 1、Algorithm 1、Theorem 2与Appendix IV的fallback量词。更新不兼容时
  保留旧estimate/集合，递归可行性仍依赖旧解移位和terminal闭合；不能通过删除环境允许的
  uncertainty/dropout分支恢复可行性。

## Dey, Dhar, Bhasin — Adaptive Output Feedback Model Predictive Control
- 年份/出处：2022, arXiv:2209.08908；全文：https://arxiv.org/abs/2209.08908
- Run 131 精读：IV-A、IV-D--IV-F、Algorithm 1 与 recursive-feasibility proof。
- 方法/关键结论：固定 estimation-error RPI set 加到 estimated-state homothetic tube，形成包含 true state 的 `homothetic and invariant` two-tube；terminal set 与 shifted candidate 保证 recursive feasibility。
- 与本项目关系：两层 output-feedback tube 在 2022 年已有直接先例；本项目差异只能落在 intermittent CZ-SMF、固定 support-query budget 与 mode-indexed backup family 的联合接口。

## Dey, Bhasin — Adaptive Output Feedback MPC With Guaranteed Stability and Robustness
- 年份/出处：2025, *IEEE Transactions on Automatic Control*, 70(12):8345--8352；DOI：https://doi.org/10.1109/TAC.2025.3584302；预印本：https://arxiv.org/abs/2502.04048
- Run 131 精读：IV-A--IV-D、Assumption 4、Theorem 1--2。
- 方法/关键结论：时间相关 estimation-error sets 与 state-estimate homothetic tube 构成 two-tier tube；fixed terminal set/feedback 封闭 shift，保证 recursive feasibility 和 robust exponential stability。
- 与本项目关系：“在线估计信息 + 独立 terminal 骨架”的宽泛结构已覆盖，不能改名为新架构。

## Köhler, Müller, Allgöwer — Robust output feedback model predictive control using online estimation bounds
- 年份/出处：2021, arXiv:2105.03427；全文：https://arxiv.org/abs/2105.03427
- Run 131 精读：III-C、IV-B，Assumption 7、Theorem 4 及证明。
- 方法/关键结论：当前/未来有效 estimation-error bounds 与 observer/nominal mismatch 共同进入 homothetic tube；augmented terminal ingredients 封闭旧解移位和递归可行性；含 10-state quadrotor 数值例。
- 与本项目关系：在线 estimator information 用于 finite-horizon tightening、保守 terminal envelope 负责尾端的分工已有强近邻。
- Run 137 新增重读：pp. 9--10 的 Assumption 7、Theorem 4 与 shift proof。其 estimation bound `e` 和 tracking bound `s` 已联合进入 constraints/terminal；本项目不能把 12 维联合误差图本身当作创新，差异必须来自间歇 CZ 几何在同预算下的可认证收益。
- Run 138 新增重读：从 arXiv 源码核查 “Homothetic tube-based MPC”“Simplified constraint tightening”、两组 terminal assumptions/theorems及 shift proof。真实输入约束对 feedback、estimation error 与 tracking error 联合成立；预先固定 nominal/correction 盒至多是 benchmark contract，不能替代 joint tightening 或 terminal proof。

## Lorenzetti, Pavone — A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme
- 年份/出处：2020, ECC；全文：https://arxiv.org/abs/1911.07360
- Run 137 精读：Sections IV-B、IV-E--IV-G，式 (8)、(12)--(15)、Propositions 1--2。
- 方法/关键结论：以 `estimation error + estimate-to-nominal control error` 为增广状态，计算一个 coupled RPI；其线性像同时收紧 performance/state 与 input constraints，并结合 nominal terminal MPC 给出 robust constraint satisfaction。
- 与本项目关系：这是 augmented `(eta,d)` ancillary RPI 的直接强基线。“联合估计和控制误差”不是创新；本项目首先必须冻结 nominal/correction input allocation，再比较 15-mode CZ/zonotope 几何是否能在同预算下比 constant-cross-section RPI 更紧。
- Run 138 新增重读：Sections IV-A--B、IV-E--F，尤其 `u=bar u+K(hat x-bar x)`、coupled error 式 (12)、input tightening 式 (13) 与 Proposition 1。最终 nominal input set 由 coupled RPI 的 correction 投影通过 Pontryagin difference 得到；固定输入切分只可用于前置 existence probe。
- Run 139 新增重读：Sections IV-B、IV-E--G，式 (8)、(12)--(15)、Propositions 1--2。其 RPI 对象是在固定可实现反馈 `K(hat x-bar x)` 后形成的 autonomous augmented-error system；因此 fixed-policy RPI 与逐状态存在控制的 RCI 量词不可混用，且控制只读取 estimate-to-nominal error，不读取真实 estimation error。

## Mejari, Mulagaleti, Bemporad — Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems
- 年份/出处：2023, *IEEE Control Systems Letters*, 7:3818--3823；DOI：https://doi.org/10.1109/LCSYS.2023.3346128；全文：https://arxiv.org/abs/2309.06998
- Run 139 精读：Section III-C、Lemma 3、Problem 1、Section IV。
- 方法/关键结论：RCI 的量词明确要求对每个状态与给定 scheduling parameter 存在 admissible input，使后继对全部 disturbance/model realization 留在集合；configuration-constrained polytope 的 vertex inputs 通过凸插值定义 invariance-inducing controller。
- 与本项目关系：若采用 controlled-RCI 语义，controller parameterization 与 `exists control` 的位置必须显式冻结。本文允许 controller 使用完整 state；本项目的 augmented state 含不可观测 `eta=x-hat x`，所以还必须收紧为对 observation fiber 共用同一控制的 partial-information RCI。
- 本项目状态：RCI 量词与 vertex-policy 的强基线；不把 configuration-constrained set 或 controller/set co-design 声称为创新。
- Run 192 重读 Section III-C、Lemma 3、Problem 1与Section IV。其充分RCI条件同时约束
  configuration cone、vertex后继、状态和输入；仓库现有单一cone Farkas否证不能外推到
  orientation family或plant不可行。本轮不再继续局部cone邻接枚举。
- Run 193 重读 Section III-C、Lemma 3及证明、Problem 1、Sections IV--V。正文顶点输入
  `u^i`不依赖当前调度参数，属于共同vertex-input策略；可作为保守基线，但不能覆盖冻结合同
  已允许的`tau(x,T)`全部权限。
- Run 194 重读 Section III-C、Lemma 3、Problem 1、Sections IV--V，专门核查固定法向、可变
  offset和vertex-input充分证书。本轮同心`alpha*S4`只是其严格受限子类；该子类失败不能否定
  independently variable offsets或configuration-constrained联合综合。
- Run 195 定向精读Lemma 3证明(77)--(81)及Sections IV--V的式(85)--(88)。非PD CC-RCI
  为每个集合顶点配置一个输入并共同覆盖调度顶点；仓库旧19-pair LP正确复现了这一保守基线，
  但它不能代替冻结合同允许的当前推力可见端点相关力矩。

## Mulagaleti, Mejari, Bemporad — Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate
- 年份/出处：2025, *IEEE Transactions on Automatic Control*, 70(2):1259--1266；
  DOI：https://doi.org/10.1109/TAC.2024.3454528；全文：https://arxiv.org/abs/2309.02384
- Run 192 精读：problem statement、Sections 3.1--3.2、式(14)--(28)及算法步骤。
- 方法/关键结论：以实时可测scheduling parameter及其有界下一参数集合构造
  parameter-dependent configuration-constrained RCI和parameter-dependent vertex controls；
  后继必须落入全部允许下一参数集合对应RCI的交集，同时满足状态和输入约束。
- 与本项目关系：若未来显式加入并认证推力执行器状态/变化率，该文是直接强基线；当前
  frozen benchmark只有逐点`T`区间，最小通用rate bound等于全区间宽度，不能获得transition
  reduction。PD-RCI与configuration geometry均不作为创新。
- Run 193 重读式(4)--(6)、Sections 3.1--3.2、式(12)--(25)及算法。其定义明确先读取当前
  scheduling parameter，再使用`u=u(x,p)`，同时覆盖全部允许`p+`；因此仓库旧
  `exists tau forall T` predecessor比真实信息合同更强，必须纠正为调度可见控制。
- Run 194 重读Sections 1、3.1--3.4的PD-RCI定义、PD-vertex control及SDP充分条件。任意未来
  推力跳变使后继参数集合仍为全区间；本轮只用其当前参数可见控制权限，不复现PD-set SDP。
- Run 195 精读定义(4)--(6)、Proposition 2及证明、PD vertex law(14)--(15)、Sections
  3.2--3.4的式(16)--(27)。当前参数在控制前可测且`u=u(x,p)`，因此本轮为160个状态顶点
  分配低/高推力独立力矩；未来参数全区间覆盖仍未因该权限而缩小。
- Run 196 精读Definition/Problem、Proposition 2、式(14)--(15)、(21)--(28)、SDP(33)与
  Section IV-A。仿射offset给出仿射vertices，和仿射LPV dynamics/vertex control相乘后，
  式(27)是关于当前参数的可能非凸二次不等式；作者用S-procedure/LMI给充分条件。故参数相关
  offset不能沿用Run195的endpoint-only LP认证。
- Run 197 重读式(26)--(28)、Remarks 4--5与SDP(33)。论文的一般多维多面体参数域用
  S-procedure 给充分 LMI，并明确记录潜在 duality gap；本仓库的单标量闭区间可改用单二次
  约束 S-lemma 的精确特化，但 fixed normal/configuration 与共同后继 core 仍会保守。
- Run 198 重读式(28)、SDP(33)、算法步骤4与Section IV求解环境。正文以YALMIP建模并用
  MOSEK求解SDP；solver success本身不是有理不变性证书。本仓库的每个`2 x 2` LMI可精确
  改写为三维Lorentz cone，但当前运行环境没有相应SOCP/SDP求解器。
- Run 199 重读式(26)--(28)、SDP(33)、算法步骤4及Section IV求解设置。锁定Clarabel求解
  仓库受限实例后得到可重放浮点不可行ray；这只否定当前fixed-normal、affine-offset、
  common-core充分模板的数值实例，不否定论文一般PD-RCI参数化。

## Pólik, Terlaky — A Survey of the S-Lemma
- 年份/出处：2007, *SIAM Review*, 49(3):371--418；
  DOI：https://doi.org/10.1137/S003614450444614X；
  作者存档：https://optimization-online.org/2004/10/968/
- Run 197 精读：Theorem 2.2 的 S-lemma、严格可行（Slater）条件，以及 Section 3 的
  S-procedure 形式。
- 方法/关键结论：对单个二次约束，存在严格可行点时，约束域上另一二次函数非负等价于存在
  一个非负标量乘子，使组合后二次函数全局非负；全局二次非负可写成PSD矩阵条件。
- 与本项目关系：归一化推力区间由 `s^2-1<=0` 描述，`s=0`严格可行，因此每条二次
  facet residual 的区间非负可精确写成 `2 x 2` LMI。此为经典定理直接推论，不是创新；
  多参数、多约束或更高次条件不能无条件沿用本轮“精确”标签。
- Run 199 复核Theorem 2.2与Slater条件，确认区间二次到`2 x 2` LMI的变换本身精确；
  本轮数值不确定性来自大规模锥综合和浮点ray，而不是S-lemma特化。

## Fawzi — On Representing the Positive Semidefinite Cone Using the Second-Order Cone
- 年份/出处：2019, *Mathematical Programming*, 175:109--118；
  DOI：https://doi.org/10.1007/s10107-018-1233-0；
  作者存档：https://www.repository.cam.ac.uk/handle/1810/270667
- Run 198 精读：Introduction式(1)、Theorem 1及其表示范围说明。
- 方法/关键结论：`2 x 2`实对称PSD cone与三维Lorentz cone线性同构；一般`3 x 3` PSD
  cone则不存在有限SOCP lift。本轮只用前一精确等价，绝不外推到一般SDP。
- 与本项目关系：6080个S-lemma矩阵恰好全部为`2 x 2`，所以冻结综合可作为SOCP而非一般
  SDP求解；这只改变实现接口，不改变fixed-normal/common-core保守性，也不是创新。

## Goulart, Chen — Clarabel: An Interior-Point Solver for Conic Programs with Quadratic Objectives
- 年份/出处：2026, *Mathematical Programming Computation*；
  DOI：https://doi.org/10.1007/s12532-026-00320-7；
  正文：https://link.springer.com/article/10.1007/s12532-026-00320-7
- Run 198 定向精读：Section 2.1的解/不可行解释、Section 2.2支持的nonnegative、second-order、
  PSD与zero cones，以及实现/数据可得性说明。
- 方法/关键结论：Clarabel以homogeneous embedding的内点法求一般conic program，并原生支持
  Lorentz cone与不可行性证书语义；它是本问题可复现求解器候选。
- 与本项目关系：当前环境未安装Clarabel，故本轮只冻结求解能力门，不报告数值可行/不可行。
  将来即使安装并返回optimal，仍须把候选送入独立全区间检查器。
- Run 199 重读Sections 2.1--2.2的锥、homogeneous embedding与不可行语义，并锁定
  `clarabel==0.11.1`。两种equilibration设置均返回`PrimalInfeasible`，但只按独立浮点ray
  审计记为`NUMERIC_CHECK`，未升级为精确不可行证明。

## Gupta, Mejari, Falcone, Piga — Computation of Parameter Dependent Robust Invariant Sets for LPV Models with Guaranteed Performance
- 年份/出处：2023, *Automatica*, 151:110920；DOI：https://doi.org/10.1016/j.automatica.2023.110920；全文：https://arxiv.org/pdf/2009.09778
- Run 196 精读：Sections 3--5，Definition 1、Problems 1--2、Lemma 3、式(11)、
  (14)--(28)、多项式条件(20)--(21)与LMI条件(37)--(40)。
- 方法/关键结论：当前scheduling parameter可测，但未来值未知；PD-RCI一步包含必须对全部
  future scheduling成立，等价进入全部未来切片的交。参数相关invariance/constraint条件写成
  多项式矩阵不等式，并以Polya relaxation转为充分LMI/SDP条件。
- 与本项目关系：直接否定“参数相关set后仍只需检查当前参数顶点”的无依据简化；其LMI是
  强综合基线，但充分松弛和参数化与当前19-pair offset family不同，不能直接宣称已闭合Gate A。

## Mejari, Gupta, Piga — Data-Driven Computation of Robust Invariant Sets and Gain-Scheduled Controllers for Linear Parameter-Varying Systems
- 年份/出处：2023, *IEEE Control Systems Letters*, 7:3355--3360；
  DOI：https://doi.org/10.1109/LCSYS.2023.3329291；全文：https://arxiv.org/abs/2309.01814
- Run 193 阅读：问题陈述、invariance定义及gain-scheduled controller构造相关段落。
- 方法/关键结论：利用实时可用的scheduling signal综合LPV gain-scheduled feedback与多面体
  RCI，并对调度集合和有界扰动鲁棒。
- 与本项目关系：再次确认当前推力可见反馈不是新机制；本文数据驱动不确定模型合同也不是
  当前已知模型合同的必要组成。
- Run 194 全文阅读pp.1--6，重点Problem 1、Section III-C、Theorem 1和算法。其
  gain-scheduled feedback是本轮vertex-control之外的另一强基线；同心模板失败不否定该类。

## Köhler, Soloperto, Müller, Allgöwer — A computationally efficient robust model predictive control framework for uncertain nonlinear systems
- 年份/全文：2020 extended version；https://arxiv.org/abs/1910.12081
- Run 192 精读：Sections II--III、Assumptions 1--6、MPC (11)、Theorem 1及其shift proof、
  Proposition 4；另核对Section IV的additive/LPV special cases。
- 方法/关键结论：用incremental Lyapunov函数与ancillary feedback的标量界在线传播tube size，
  对state/input-dependent uncertainty收紧约束；在terminal controller/set/cost和tube terminal
  条件全部成立时证明递归可行、硬约束满足与实用稳定。
- 与本项目关系：说明调度一致`W(T)`只是一个必要接口；common-`P`稳定、有限轨迹或单次RCI
  可行都不能替代terminal append与shift proof。该文是full-state nonlinear tube MPC，未直接
  解决本项目间歇测量的因果output-feedback信息状态。

## Ping — Dynamic Output Feedback Robust Model Predictive Control via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems
- 年份/出处：2015, *Journal of Applied Mathematics*, Article 875850；DOI：https://doi.org/10.1155/2015/875850
- 方法/关系：zonotopic estimation-error set 刷新后用辅助 feasibility condition 决定是否采用更新；失败时继承旧 controller parameters。“更新前 feasibility gate”不是创新。
- Run 131 新增核查：精读 4.2--4.4、Algorithm 8、Theorem 9；确认其含 zonotope order limit、在线 set refresh、一步 feasibility gate 及失败时继承旧 controller parameters。不能把 `SMF update + gate + fallback` 作为新机制。

## Hassaan, Pati, Shen, Yong — Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data
- 年份/出处：2021, *IFAC-PapersOnLine*, 54(5):103--108；DOI：https://doi.org/10.1016/j.ifacol.2021.08.482；作者全文：https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf
- Run 132 精读：Sections 2.2、3.1--3.2，Assumptions 1--3、Theorems 5--7。
- 方法/关键结论：以周期有限长度语言描述间歇时延/缺测，构造 time-varying estimator/control tubes；一个对全部周期相位有效的 common nominal terminal set 与 feedback gain 足以用旧解移位证明 recursive feasibility，并得到 robust exponential stability。
- 与本项目关系：直接覆盖 `finite dropout language + time-varying tube + terminal shift`。mode-indexed terminal family 不是默认必要条件；本项目必须先复现其 worst-phase common-terminal baseline，再证明 indexing 的严格收益。
- 局限：误差集合采用 hyperbox，系统为线性/时变而非本项目完整六自由度非线性四旋翼；没有固定预算 CZ support-query 接口。
- Run 133 新增核查：重读 Section 3.1.2、Lemma 4、Assumptions 1--2 与 Theorem 6。确认 tracking controller/control-error tube 先吸收过程噪声与 estimation error；common `K_f,X_f` 随后作用于已经收紧的 nominal system。二者不是同一个 joint controller/RPI synthesis 问题。
- Run 135 新增核查：重读 Definition 1、system/timing 与 Section 3.1.1。其 estimator 采用 finite/periodic equalized-recovery error tubes，未来 delay pattern 未知时对全部允许模式取 worst case；并不要求一个 time-uniform invariant estimation-error family。故本轮统一固定点只是更强、更保守的 backup 基线。

- **背景第14轮复读（2026-11-02）**：再次直接核对作者PDF pp.1–6：§2.2 的LTV时间戳输出与周期有限长度语言，Definition 1的equalized recovery，§3.1的点估计+时变hyperbox误差界、Lemma 4的因果tracking tube，§3.2的Assumptions 1–3/Theorems 5–7，以及§4双积分器算例。实际算例 \`A=[[1,1],[0,1]], B=[1,1]^T, C=[1,1]\`、\`X=[-50,3]^2,U=[-3,3]\`、\`w∈[-0.05,0.05]^2,v∈[-0.01,0.01]\`、\`T_d=5,T_p=13\`；不是四旋翼或真实(T,τ)，无20ms实测。Theorem 5硬约束依赖先认证估计/跟踪误差管；Theorem 6需初始可行与跨相位共同终端 \`X_f,K_f\`；Theorem 7还需Lyapunov下降，结论是到有界集合的鲁棒指数稳定。论文已有**有限失测语言+时变tube+共同终端移位**先例；本项目必须先测试其worst-phase common-terminal baseline，不得仅凭mode-indexed声称创新。此复读不新增去重论文。详细来源及仓库差异见 \`docs/research/model_selection/background_run_20261102_0739_hassaan_terminal_audit.md\`。

## Rutledge, Yong, Ozay — Finite horizon constrained control and bounded-error estimation in the presence of missing data
- 年份/出处：2020, *Nonlinear Analysis: Hybrid Systems*, 36:100854；DOI：https://doi.org/10.1016/j.nahs.2020.100854；作者全文：https://www.kwesirutledge.info/static/pdf/nahs2020.pdf
- Run 132 精读：Sections 3--4、Definition 2、equalized-recovery formulation 与 synthesis。
- 方法/关键结论：missing-data language 可表达连续丢包上界；prefix-based affine feedback 在 bounded process/measurement noise 与 state/input constraints 下保证 finite-horizon equalized recovery。Remark 3 明确指出可适配 zonotope 等 set template。
- 与本项目关系：bounded-dropout language、按前缀/模式合成反馈及 set-valued bounds 均已有近邻；有限时域结果本身不闭合 receding-horizon terminal proof。
- Run 160 阅读层级：作者全文本轮抓取超时，仅复核摘要/引言中的 equalized-recovery 问题设定，
  不引用其定理。该工作允许缺测期间使用不同中间界后恢复；当前合同要求每拍位置硬约束，故
  本轮第13 miss反证不能借 equalized recovery 绕过。

## Hassaan, Shen, Yong — Path-Dependent Controller and Estimator Synthesis with Robustness to Delayed and Missing Data
- 年份/出处：2021, HSCC；DOI：https://doi.org/10.1145/3447928.3456655；作者全文：https://qiangs.github.io/Papers/Conf_HSCC2021Hassaan.pdf
- Run 132 精读：Sections 2--5，fixed-length/reduced event language、path-dependent controller/estimator synthesis 与 examples。
- 方法/关键结论：为 time-varying affine systems 合成 path-dependent finite-horizon controller/estimator；通过 reduced event language 处理相同可观察历史的因果冲突，并以 polytopic intermediate bounds 改善只按 worst-case word 的设计。
- Run175 重读 Problem 1、Section 3与Theorems 3.2/3.4：控制器/估计器是待合成的存在量，保证对全部固定长度缺测/时延语言实现equalized recovery；不能把所有允许控制输入当成对手扰动来否定回返。
- 与本项目关系：按 dropout mode/path 索引 controller、estimator 或 error bound 不是创新；15-mode indexing 只能作为实现结构。

## Ghaemi, Del Vecchio — Control for Safety Specifications of Systems with Imperfect Information on a Partial Order

- 年份/出处：2014，IEEE Transactions on Automatic Control；作者全文：https://web.mit.edu/ddv/www/papers/RezaTACfinal.pdf
- Run176 精读：§II 的information-state定义与Problems 1--2，§III Theorem 1及证明，§IV Theorem 4及证明。
- 方法/关键结论：开环安全集采用`exists control / forall disturbances`；闭环控制映射以测量历史诱导的information state为输入，并对全部允许测量信号保持安全。极端输入判据依赖input/output order-preserving及连通性等结构假设。
- 与本项目关系：支持受控回返的正确量词和information-state策略接口；当前非线性四旋翼plant尚未证明满足其order-preserving假设，不能直接用极端推力替代五步鲁棒前驱。

## Wildhagen, Pezzutto, Schenato, Allgöwer — Self-triggered MPC robust to bounded packet loss via a min-max approach
- 年份/出处：2022, CDC extended version；arXiv：https://arxiv.org/abs/2204.00339
- Run 132 精读：problem formulation、min-max MPC、terminal control law、recursive feasibility/constraint/convergence argument。
- 方法/关键结论：在连续 packet loss 数有界时使用 min-max self-triggered MPC 与尾端控制律，对所有允许 loss realization 保证 recursive feasibility、constraint satisfaction 和 convergence。
- 与本项目关系：从网络化 MPC 方向再次覆盖 `bounded packet loss + terminal/shift proof`；但不是 SMF output feedback，也不消费 CZ posterior correlation。
- Run 163 精读 Sections II-B--II-C、Assumption 1、Section III、Algorithm 1与terminal ingredients：
  策略选择控制更新和采样间隔，可靠ACK只报告最近一次传输结果；连续丢包上界`P`仍是独立网络
  假设，min-max MPC覆盖所有满足该假设的loss sequences。故自触发调度不能单独认证缩短dropout语言。

## Mayne, Seron, Raković — Robust model predictive control of constrained linear systems with bounded disturbances
- 年份/出处：2005, *Automatica*, 41(2):219–224；DOI：https://doi.org/10.1016/j.automatica.2004.08.019
- 方法/关系：经典 bounded-disturbance robust/tube MPC 基线；当前 LQR+RPI 不能作为创新。

## Mayne, Raković, Findeisen, Allgöwer — Robust output feedback model predictive control of constrained linear systems
- 年份/出处：2006, *Automatica*, 42(7):1217--1222；DOI：https://doi.org/10.1016/j.automatica.2006.03.005
- Run174 阅读：正式摘要、引言、robust output-feedback MPC控制器结构与Theorem 1上下文；出版页正文受限，未逐式核查完整证明。
- 方法/关键结论：Luenberger估计误差由不变集包络，observer-to-nominal偏差由tube截面包络；二者共同支持收紧与真实约束满足。
- 与本项目关系：可靠输出反馈闭合依赖误差/tube不变集，不依赖观测把真实状态重置到初始物理盒。本轮只用这一结构作量词对照，不引用未核查证明细节。

## Raković, Kerrigan, Kouramas, Mayne — Invariant approximations of the minimal robust positively invariant set
- 年份/出处：2005, *IEEE Transactions on Automatic Control*, 50(3):406–410；DOI：https://doi.org/10.1109/TAC.2005.843854
- 方法/关系：mRPI 可控精度外逼近；有限 Minkowski 和必须补无限尾项才能作安全 tube。

## Kouramas, Raković, Kerrigan, Allwright, Mayne — On the Minimal Robust Positively Invariant Set for Linear Difference Inclusions
- 年份/出处：2005, CDC-ECC；公开全文：https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc05/pdffiles/papers/1964.pdf
- 本轮精读：Sections II–V，Assumption 1、Theorems 2–4、公式 (16)–(25)。
- Run 136 新增重读：Theorems 1--4 与公式 (11)--(23)，核对 finite reachable sum、`R_s subseteq alpha W` 和 `(1-alpha)^-1 D_s` 的逻辑。当前标签相关秩亏扰动不满足公共 full-dimensional `W` 假设，故仅作为理论边界，不作为本轮证书。
- 方法/关键结论：若扰动是含原点内点的 C-set 且无扰动系统绝对渐近稳定，则可由有限 reachable sums 和缩放构造包含 mRPI 的 RPI 外近似，并控制 Hausdorff 误差。
- 与本项目关系：该结果的方向是外近似，不能证明重定心候选位于原 mRPI 内；当前四维合同的 `W=D0 G[-1,1]` 为秩一线段，也不满足其 C-set 假设。不能无条件套用缩放公式。
- 本项目状态：终端集合替代方案的条件性基线，不是当前包含证书。

## Sadraddini, Tedrake — Linear Encodings for Polytope Containment Problems
- 年份/出处：CDC 2019；DOI：https://doi.org/10.1109/CDC40024.2019.9029363；arXiv:1903.05214；全文：https://groups.csail.mit.edu/robotics-center/public_papers/Sadraddini19.pdf
- Run 128 重读：Section III Theorem 1 与 (11)–(17)、Theorem 2，Section IV-A Theorem 3 与反例、Table I。
- 方法/关键结论：为 AH-polytope-in-AH-polytope 给出线性充分包含编码；zonotope 特例使用生成元的仿射系数映射。一般编码不保证必要性，论文明确给出真包含但 zonotope 证书失败的反例。
- 与本项目关系：可把 CZ 终端误差集可靠地证入有限 mRPI 内近似；可行即证明，不可行不能当作不包含反例。Theorem 1 要求 primitive inbody 满维，CZ equality slice 必须先在 affine hull 内参数化。当前 539–605 / 602-generator 实例的通用编码达到约 160–180 万变量，不适合作为在线 fixed-budget admission。
- 本项目状态：Run 125 的终端包含基线；Run 128 将其降级为离线充分审计工具，不作为在线算法。
- Run 129 新增核查：Theorem 3 的行 `l1` 生成元映射可与 CZ 等式自由度组合为逐行小 LP；这是已知充分证书的结构化特化。首个 Scott 消元的 4 个超限行均有精确对偶下界大于 1，因此该特化首步失败；失败不否定真实集合包含。
- Run 130 新增核查：阅读 17 页 expanded arXiv 版本，重点 Section V-B、Proposition 6 与式 (30)。作者已经把 reduced generator matrix 与 containment maps 联合优化，用双向包含近似 Hausdorff distance；双线性等式使问题非凸，使用 projected sequential LP/交替求解并依赖初始化。把 terminal containment witness 当作 reduction 硬约束不是空白机制。

## Diaconescu et al. — Zonotope-Based Elastic Tube Model Predictive Control
- 年份/出处：2026, arXiv:2509.19824v2（2026-05-17 修订）；全文：https://arxiv.org/abs/2509.19824
- Run 129 精读：Sections 3.1、3.4 的包含 Lemma/Proposition/Corollary 与预计算 inclusion matrix。
- 方法/关键结论：在 zonotopic elastic tube MPC 中以仿射生成元映射和逐行范数约束编码包含，并预计算固定 inclusion matrix 以减少在线辅助变量。
- 与本项目关系：“携带或预计算包含矩阵”已有明确近邻，不能作为创新。其对象是缩放 zonotope，不是 Scott CZ 消元中的 equality-adjusted terminal witness。
- 本项目状态：certificate-carrying containment 的强近邻与首次性约束。

## Hellwig, Schäfer, Qian, Platzer, Althoff — From Zonotopes to Proof Certificates: A Formal Pipeline for Safe Control Envelopes
- 年份/出处：iFM 2025，LNCS 16194（卷出版 2026）；DOI：https://doi.org/10.1007/978-3-032-10794-7_13
- Run 128 精读：pp. 10–11，containment witness、残差裕量及 Theorem 3.5。
- 方法/关键结论：把 zonotope containment 的浮点优化 witness 转成可由形式系统检查的证书；可用精确有理数，或在 `||HΓ-G||` 残差和右逆范数约束下预留严格裕量。
- 与本项目关系：终端包含不能只保存 solver success；必须归档映射 witness，并独立检查等式、box 行预算和数值裕量。
- 局限：处理 zonotope witness，不直接消除 CZ equality，也不解决当前百万变量在线规模。
- 本项目状态：可靠证书实现规范。

## Kulmburg, Schäfer, Althoff — Approximability of the Containment Problem for Zonotopes and Ellipsotopes
- 年份/出处：2025，*IEEE Transactions on Automatic Control*, 70(12):8104–8119；DOI：https://doi.org/10.1109/TAC.2025.3583624
- Run 128 阅读：期刊元数据、摘要和 arXiv 记录；全文获取失败，未核查定理编号或证明。
- 方法/关系：摘要显示其分析 zonotope/ellipsotope containment 松弛的近似质量。不能凭摘要把它当作无损、低复杂度 CZ-in-zonotope 判据。
- 本项目状态：最近邻线索，首次性保持未知，待取得全文。

## Froese et al. — Parameterized Hardness of Zonotope Containment and Neural Network Verification
- 年份/出处：2025 preprint；全文：https://arxiv.org/pdf/2509.22849
- Run 128 精读：Section 3.1、Theorem 3.1 及一般复杂度结论。
- 方法/关键结论：固定物理维数 `d` 时，可枚举 `O(n^(d-1))` 个顶点判定 zonotope containment；一般问题具有困难性。
- 与本项目关系：解释为何不应预设高生成元一般包含有便宜完整证书。该结果针对 zonotope，不直接覆盖有 equality 的 CZ。
- 本项目状态：复杂度背景，不是当前在线实现方案。

## McCormick — Computability of global solutions to factorable nonconvex programs: Part I — Convex underestimating problems
- 年份/出处：1976, *Mathematical Programming*, 10:147–175；DOI：https://doi.org/10.1007/BF01580665
- 方法/关系：单 bilinear term 的经典 convexification 基础；box-domain 线性 support 下普通 CZ 不会比 exact convex hull 更紧。

## Müller, Serrano, Gleixner — Using Two-Dimensional Projections for Stronger Separation and Propagation of Bilinear Terms
- 年份/出处：2020, *SIAM Journal on Optimization*；DOI：https://doi.org/10.1137/19M1249825
- 方法/关系：非矩形二维可行域可产生比 box McCormick 更强的 separation；支持利用真实 posterior/scheduling 域，但不提供 Tube MPC 递归可行性。

## Kochdumper, Althoff — Constrained polynomial zonotopes
- 年份/出处：2023, *Acta Informatica*, 60:279–316；DOI：https://doi.org/10.1007/s00236-023-00437-5
- 方法/关系：支持 quadratic/higher-order maps；“用 polynomial zonotope 表示乘积”已有成熟理论，只能作为实现工具。

## Kochdumper, Althoff — Sparse Polynomial Zonotopes: A Novel Set Representation for Reachability Analysis
- 年份/出处：2020, *IEEE Transactions on Automatic Control*；DOI：https://doi.org/10.1109/TAC.2020.3024348；预印本：https://arxiv.org/abs/1901.01780
- Run171 精读：§§1.1--1.2、Definition 1、Propositions 1--4。
- 方法/关键结论：用 dependent factors 与全局 identifier 保留同一不确定因子在多项式项中的重复依赖；identifier 合并可保持依赖关系，并给出 zonotope、polytope 与 Taylor model 等表示到 SPZ 的转换。
- 与本项目关系：共享非线性因子表示是成熟 reachability 基线，不构成本项目创新；若一个输入点精确满足真实单步图，任何可靠 SPZ/CZ 图外包都必须保留其像。能否排除 Run169 点取决于从初始集出发的跨时刻联合可达集，而非单步换一种集合表示。

## Jafarpour, Harapanahalli, Coogan — Interval Reachability of Nonlinear Dynamical Systems with Neural Network Controllers
- 年份/出处：2023, L4DC, PMLR 211:12--25；全文：https://proceedings.mlr.press/v211/jafarpour23a/jafarpour23a.pdf
- Run172 精读：§2 的可达集、decomposition function、inclusion function和嵌入系统；§5 Theorem 2 的区间可达外包。
- 方法/关键结论：从初始区间和扰动区间出发，通过mixed-monotone嵌入系统计算包含真实非线性闭环可达集的超矩形，并以分割平衡紧度和计算量。
- 与本项目关系：支持“必须从初始集跨时刻传播”的量词；本文针对连续时间NN闭环，不能直接替代本仓库离散Euler真值模型的证明。Run172只采用同一包含原则，给出项目特定的标量归纳界。
- Run173 新增精读：§5 Theorems 2--3与Remark 4、§6 Algorithm 1。每步对外包重分割并取并集可改善紧度，但所有子外包仍必须覆盖对应真实轨迹；本项目的分层解析盒是项目特定特例，不是新可达算法。

## Bujarbaruah, Nair, Borrelli — A Semi-Definite Programming Approach to Robust Adaptive MPC under State Dependent Uncertainty
- 年份/出处：2020, European Control Conference；预印本：arXiv:1910.04378
- 方法/关系：set-membership refinement + state-dependent uncertainty envelope + robust MPC；“SMF 信息进入 state-dependent robustification”已有先例。

## Hanema et al. — Stabilizing non-linear model predictive control using linear parameter-varying embeddings and tubes
- 年份/出处：2021, *IET Control Theory & Applications*；DOI：https://doi.org/10.1049/cth2.12131
- 研究问题：利用 nonlinear system 的 LPV embedding 构造可稳定 MPC，同时处理未来 scheduling parameter 未知。
- 方法/关键结论：限制 state evolution 于时变集合，并利用 scheduling-state 关系构造 future scheduling tube；相较静态 bounds 得到更紧未来 bounds，并以该结构建立 recursive feasibility/stability。
- 与本项目关系：第27–28章的未来 `phi` scheduling intervals 与 shift nesting 有直接近邻，因此“state set -> scheduling tube”不能作为创新。差异只能落在 CZ-SMF measurement posterior、certified finite-normal support 与 fixed-complexity reduction compatibility。
- 局限：不是 set-membership output-feedback CZ 压缩问题。
- 本项目状态：作为 scheduling-tube 强基线。

## Abbas — Linear parameter-varying model predictive control for nonlinear systems using general polytopic tubes
- 年份/出处：2024, *Automatica*, 160:111432；DOI：https://doi.org/10.1016/j.automatica.2023.111432
- 方法/关系：anticipated scheduling bounds + general polytopic tubes；“更紧未来 scheduling interval 降低保守性”不是新机制。

## Fleming, Hawari — Robust Tube MPC Using Gain-Scheduled Policies for a Class of LPV Systems
- 年份/出处：2024, *IEEE Control Systems Letters*, 8:1589–1594；DOI：https://doi.org/10.1109/LCSYS.2024.3412652
- 方法/关系：gain-scheduled policy、parameter-rate bounds、online polyhedral tubes，证明 recursive feasibility/exponential stability；decision/scheduling-dependent tube 已有成熟理论。

## Girard — Reachability of Uncertain Linear Systems Using Zonotopes
- 年份/出处：2005, HSCC, LNCS 3414:291–305；DOI：https://doi.org/10.1007/978-3-540-31954-2_19
- 研究问题：用 zonotope 可扩展地计算不确定线性系统 reachable sets，并控制表示复杂度。
- 方法/关键结论：zonotope 传播配合 generator/order reduction；经典 generator-box 外包模式保证单次 outer enclosure，但其目标不是跨两个嵌套集合保持 reduction operator 的 monotonicity。
- 与本项目关系：第29章使用同类 generator-box reduction 构造 shift-support reversal；普通 order reduction 本身不能作为创新。
- 局限：不处理 SMF measurement posterior 与 MPC shifted-candidate support compatibility。
- 本项目状态：作为 naive fixed-order reduction 基线。

## Raghuraman, Koeln — Set operations and order reductions for constrained zonotopes
- 年份/出处：2022, *Automatica*, 139:110204；DOI：https://doi.org/10.1016/j.automatica.2022.110204；预印本：https://arxiv.org/abs/2009.06039
- 研究问题：提高 zonotope/CZ 在控制集合运算中的实用性，并提供复杂度约减方法。
- 方法概要：扩展 halfspace intersection、convex hull、RPI、Pontryagin difference 等 CZ 运算，并研究 zonotope/CZ order reduction。
- 与本项目关系：说明“CZ order reduction”已有系统理论；本项目若有贡献必须落在 reduction error 与 recursive-feasibility control normals 的联动证书，而不是提出一般 reduction。
- 局限：没有给出本项目所需的 rolling SMF shift-support ledger。
- 本项目状态：作为 fixed-complexity CZ 强基线。
- Run 130 新增核查：精读 Section 5。其 zonotope/CZ order reduction 直接采用 Sadraddini--Tedrake containment encoding；CZ 经 nullspace/AH-polytope 表示构造 LP，可删一个 generator/constraint 后再缩放。该节做 inner approximation，不能作为 reliable SMF posterior 的 outer enclosure，但已排除“CZ reduction + containment constraint”本身的首次性。
- Run188 精读§2、§3开头、式(1)--(3)及Theorem 4相关表示讨论。普通zonotope中心对称；CZ的等式约束可打破中心对称性、表示任意凸polytope，并对generalized intersection闭合。因此五参数center/radius在非中心对称measurement posterior上的失败是既有表示边界，不是创新。

## Robbins, Siefert, Pangborn — Exact Representation Complexity Reduction for Constrained Zonotopes with Applications to Dynamic Systems and Control
- 年份/出处：2026, *American Control Conference (ACC 2026)*；IEEE Xplore 收录日期 2026-08-13。
- 稳定链接：https://ieeexplore.ieee.org/document/11615961
- 研究问题：反复集合运算会使 zonotope/CZ representation complexity 增长；哪些 generators/constraints 是表示冗余，能否在保持集合完全不变时删除？
- 方法/关键结论：形式化 irredundant zonotopic representation 与多类 redundancy，给出检测/删除算法；数值例包含 robust controllable sets 和 ReLU domain partitioning。其 reduction 是 exact representation reduction，不是 approximate outer enclosure。
- 与本项目关系：该方法不改变集合，所以 exact-CZ 的 shift nesting 和所有 support 都自动保持；它应成为压缩流水线第一阶段，先 exact-prune，再讨论 approximate fixed-budget reduction。
- 可借鉴点：把“表示复杂度”与“集合几何近似误差”明确分离，避免把可精确删除的冗余误算成必须牺牲 tightness 的 fixed-order 问题。
- 局限：exact pruning 不能保证长期 propagation/update 后一定达到预设固定 generator/equality budget；也没有解决 independent approximate reductions 导致的 control-normal support reversal。
- 本项目状态：已采用为设计原则；不把 exact redundancy removal 声称为本项目创新。

## Hanema, Lazar, Tóth — Stabilizing tube-based model predictive control: terminal set and cost construction for LPV systems
- 年份/出处：2017, *Automatica*, 85:137–144；DOI：https://doi.org/10.1016/j.automatica.2017.07.046；扩展版：https://arxiv.org/abs/1702.05393
- 研究问题：LPV tube MPC 如何构造 terminal set/cost 并建立 recursive feasibility 与 stability。
- 方法/关键结论：采用 controlled periodically contractive terminal sets 与适合集合的 Lyapunov-like terminal cost；给出满足参数化假设时的递归可行性与渐近稳定性，并构造 periodic homothetic tube 参数化。
- 与本项目关系：第31章保留推力 T 的横向—姿态模型天然是 LPV family；因此“LPV terminal family/periodic contractive set”不能作为创新，只能作为 ancillary/terminal 证明工具。
- 可借鉴点：若 common quadratic certificate 过强，可转向 periodic/finite-step contractive terminal construction，而不是回到语义错误的 fixed-hover LTI。
- 局限：不使用 CZ-SMF measurement posterior，也不研究 posterior correlation 在真实 input normals 上的 tightening value。
- 本项目状态：下一阶段 ancillary/terminal synthesis 的主要理论基线。

## Ping, Yao, Ding, Li — Tube-Based Output Feedback Robust MPC for LPV Systems With Scaled Terminal Constraint Sets
- 年份/出处：2022, *IEEE Transactions on Cybernetics*, 52(8):7563–7576；DOI：https://doi.org/10.1109/TCYB.2020.3041334
- 研究问题：有 bounded disturbance/noise 的离散 LPV 系统如何做低在线复杂度 output-feedback tube RMPC。
- 方法/关键结论：离线优化并存储 nested RPI estimation-error sets 与 RCI control-error sets；在线依据时变 estimation-error bounds 搜索控制参数，并使用 scaled terminal constraint sets；论文给出 recursive feasibility 与 robust stability 保证。
- 与本项目关系：LPV + output feedback + nested error sets + scaled terminal 已有强近邻，因此第31章不能把这些结构本身作为创新。差异若存在，只能落在 CZ-SMF posterior correlation 如何被真实 state/input/terminal support normals 消费并形成可认证的 tightening 改善。
- 可借鉴点：其 nested RPI/RCI lookup 与 scaled terminal 是当前语义一致 ancillary synthesis 的直接比较基线。
- 局限：不是 constrained-zonotope posterior 的 control-normal support certification问题。
- 本项目状态：列为后续 LPV output-feedback 基线。
- Run 131 核查层级：本轮仅取得正式摘要；摘要支持 nested RPI/RCI lookup、在线 tightening 与 scaled terminal 的定位，但未据此引用定理编号或证明细节。


## Tahir, Jaimoukha — Robust Positively Invariant Sets for Linear Systems subject to model-uncertainty and disturbances
- 年份/出处：2012, IFAC Proceedings Volumes 45(17):213–217；DOI：https://doi.org/10.3182/20120823-5-NL-3013.00032
- 研究问题：在线性离散系统存在 model uncertainty、additive disturbance 以及 state/input constraints 时，如何联合计算 controller 与 robust positively invariant set。
- 方法/关键结论：将 RPI set 与反馈律一起放入 LMI 优化；论文强调不要求先给定 controller 或初始 invariant set，并在固定 K、无模型不确定性的特例下给出更简单的优化。
- 与本项目关系：第34–35章的“约束感知 ancillary synthesis”已有直接方法学基础，因此 controller/invariant co-design 只能作为 baseline 工具，不能作为创新。
- 局限：其 uncertainty class 与当前 thrust-scheduled、state-dependent nonlinear remainder 不完全相同；不能直接替代本项目的 vertex-consistent residual contract。
- 本项目状态：列为下一阶段 joint state/input synthesis 的 baseline。
- Run 133 精读：Sections 2--3、Definition 3、Theorem 5、Remarks 6--9。其 joint feedback/hyperrectangle synthesis 针对 norm-bounded model uncertainty 与 additive box disturbance；一般条件是充分的，无结构 norm-bounded uncertainty 特例可达精确性。该描述不直接保持本项目同一 `T` 决定 `(A(T),W(T))` 的 correlated graph；独立外包不能用于否定 vertex-consistent certificate。

## Tahir — Efficient computation of Robust Positively Invariant sets with linear state-feedback gain as a variable of optimization
- 年份/出处：2010, ICEEE；DOI：https://doi.org/10.1109/ICEEE.2010.5608613
- Run 133 精读：Sections II--IV，式 (1)--(25)，Remarks 3--12。
- 方法/关键结论：对 LTI + additive box disturbance 同时优化 linear feedback 与 RPI set；固定形状椭球采用 S-procedure 得到充分 SDP，origin-centered axis-aligned box 采用 Farkas 条件，并可加入 state/input constraints；固定 K 时部分问题退化为 LP。
- 与本项目关系：这是 ancillary/tracking disturbance-RPI 层的直接 baseline，不是 Hassaan nominal terminal `K_f,X_f`。box 类已由第37章严格排除；ellipsoid 类仍需适配 arbitrary-jump thrust LPV 和 paired residual。
- 本项目状态：准入为方法基线，不直接实现现有公式。

## Tahir, Jaimoukha — Robust feedback MPC of constrained uncertain systems
- 年份/出处：2013, *Journal of Process Control*, 23(2):151--163；DOI：https://doi.org/10.1016/j.jprocont.2012.08.003
- Run 133 阅读层级：仅正式摘要，未取得可核验全文。
- 摘要层面关系：区分把状态导入 invariant terminal set 的 outer MPC controller 与保持 RPI 的 inner controller，支持本轮双层语义纠正。
- 限制：未核查正文、定理或算法，不据此声明其 uncertainty class 覆盖本项目。

## Ben Sassi, Girard — Controller synthesis for robust invariance of polynomial dynamical systems using linear programming
- 年份/出处：2012, *Systems & Control Letters*, 61(4):506–512；DOI：https://doi.org/10.1016/j.sysconle.2012.01.004；预印本：https://arxiv.org/abs/1107.1580
- 研究问题：bounded disturbances 和 input constraints 下，如何联合求 controller 与 invariant set。
- 方法/关键结论：给定候选 polyhedral invariant 后，把 controller synthesis 写成多项式优化并用 LP relaxation；随后迭代更新 controller 与 invariant polytope。
- 与本项目关系：再次说明“同时搜索反馈和不变集”已有成熟工作。若本项目采用类似 co-design，只能作为认证工具。
- 局限：不是 constrained-zonotope SMF posterior 与 Tube MPC 的接口问题，也不处理当前特定 LPV scheduling 语义。
- 本项目状态：作为 polyhedral joint synthesis 的方法基线。

## Wehbeh, Kerrigan — State-Dependent Uncertainty Modeling in Robust Optimal Control Problems through Generalized Semi-Infinite Programming
- 年份/出处：2025, arXiv:2503.10389；稳定链接：https://arxiv.org/abs/2503.10389
- 研究问题：当 uncertainty set 本身依赖 state/control decision 时，如何避免用全局 uniform uncertainty set 造成额外保守性。
- 方法/关键结论：用 generalized semi-infinite programming 表示 decision/state-dependent uncertainty，并通过 local reduction 求解；文中包含 planar quadrotor 案例，展示相对 uniform uncertainty bounds 的保守性改善。
- 与本项目关系：第35章的 vertex-consistent residual 修正属于同一建模原则：已知 scheduling parameter T 时，应保留 d_x(T) 的依赖关系，而不是无条件替换为 d_x(T_max)。
- 局限：该工作不是 SMF/CZ output-feedback Tube MPC，也没有解决本项目的 recursive-feasibility shift certificate。
- 本项目状态：作为“不得丢失 uncertainty dependence”的强建模基线。
- Run 134 精读：Sections II、V 及 planar quadrotor 案例。其 uncertainty set 可显式依赖 state/control，支持保留实际推力与余项的共同图；但方法针对有限时域 robust optimal control，没有给出间歇 output-feedback RCI 或 old-plan shift certificate。
- Run 137 新增重读：Sections II--IV、Theorems 1--2 与 Section V。再次确认 `T=bar T+delta T` 决定 `d_z(T)` 的图可用 GSIP 表达；但 local-reduction 求解结果不能替代 compact invariant-set 与 recursive-shift 证明。
- Run 139 新增精读：Sections II--IV、Theorems 1--2。robust constraints 只对与同一 state/control decision 相容的 uncertainty set 量化；这要求 joint `(eta,d)` graph 保留同一 actual thrust 与 residual primitive，不能把 dynamics endpoint、residual width 和两个 error coordinates 独立笛卡尔化。

## Mulagaleti, Bemporad — Learning Quasi-LPV Models and Robust Control Invariant Sets with Reduced Conservativeness
- 年份/出处：2025, *IEEE Control Systems Letters*；DOI：https://doi.org/10.1109/LCSYS.2025.3569637；全文：https://arxiv.org/abs/2505.07287
- Run 134 精读：Introduction、Section 2.1、Propositions 1--2、Section 3.1、Proposition 3 与 Corollary 1。
- 方法/关键结论：对 self-scheduling quasi-LPV 模型构造 configuration-constrained polytopic RCI；在候选 RCI 内求 scheduling 下界以缩小 multiplicative uncertainty hull，并允许 vertex controls。文中 Remark 1 提示可扩展到 `p(x,u)`，正文证书主要按 `p(z)` 展开。
- 与本项目关系：非轴对齐 polytope、configuration constraints、vertex control 和利用 self-scheduling correlation 均已有直接近邻；不能作为创新。本项目额外义务是 intermittent-SMF estimation error、nominal/correction input allocation 与实际 thrust 同时决定 dynamics/residual 的联合图。
- 本项目状态：最强 qLPV ancillary RCI baseline；待完整合同后再做同条件数值比较。
- Run 137 新增重读：Section 2.2.2 Proposition 2、Section 3.1 与 Corollary 1。configuration-constrained RCI 已把 vertex controls、state-dependent scheduling 下界和 hard input constraints放入证书；当前先缺的不是集合类，而是 nominal input reserve。

## Wehbeh, Kerrigan, Scaccia — Generalized Semi-Infinite Programming for Robust Optimal Control with Decision-Dependent Uncertainty
- 年份/出处：2026 preprint，arXiv:2609.01538v1，2026-09-01；全文：https://arxiv.org/abs/2609.01538
- Run 134 精读：Introduction、Sections II--IV、Theorems 1--3、Algorithm 1、Sections V--VI。
- 方法/关键结论：将满足正则条件的 GSIP 变换为 existence-constrained SIP，用 adaptive discretization 与 worst-case separation oracle求解；把状态轨迹并入不确定变量，可处理 state/control-dependent uncertainty。收敛定理要求有限 master/oracle 子问题全局求解。
- 验证边界：数值例使用多起点局部 NLP；论文明确因此不满足理论中的全局子问题条件。Monte Carlo 不能替代 oracle nonpositive 的稳健证书。
- 与本项目关系：可为实际 thrust、误差、名义状态与 residual 的联合图提供语义/求解基线，但不直接给出 invariant tube、间歇 output feedback 或 recursive-feasibility shift theorem。
- 本项目状态：强 decision-dependent uncertainty baseline；不能把一次局部 solver success 当作 RCI 证明。
- Run 149 重读 Introduction、Section II Assumption 1、Lemma 1、Theorem 1/Remark 1、
  Section IV Assumption 2 与 Theorem 3。当前 `r_z(barT+deltaT)` 使 disturbance image 依赖
  correction decision，属于 GSIP 语义；该文不提供 invariant information ensemble 或
  recursive-feasibility 证明，本轮只用其判定 scheduled-residual 分支的问题类别。
- Run 150 核对2026-09-01 v1元数据并复核上述全文章节的准入边界。fixed-envelope
  translated shape 已在 mode 4 出现与 current correction 无关的 `e_p` width obstruction；
  因此本轮不启动 GSIP。该结果不否定历史 control-dependent shapes，只有先得到可闭合的
  history-conditioned intrinsic family 后才评估 scheduled tightening。

## Hanema, Lazar, Tóth — Heterogeneously Parameterized Tube Model Predictive Control for LPV Systems
- 年份/出处：2020, *Automatica*；全文：https://arxiv.org/abs/1910.08449
- Run 134 重读：Introduction 与 LPV problem setting。
- 方法/关键结论：对当前可测、未来未知的外生 scheduling signal构造 heterogeneously parameterized tubes，并证明 LPV tube MPC 的递归可行性/稳定性性质。
- 与本项目关系：是 arbitrary-future scheduling 的强 baseline；但 `delta T=kappa(e-eta,...)` 时实际 thrust 是 feedback-dependent，不能直接套用其外生 scheduling 假设。
- 本项目状态：保留为外生 LPV 对照，不作为当前六状态 ancillary 合同的直接证书。


## Kothare, Balakrishnan, Morari — Robust constrained model predictive control using linear matrix inequalities
- 年份/出处：1996, *Automatica*, 32(10):1361–1379；DOI：https://doi.org/10.1016/0005-1098(96)00063-5；公开技术报告：https://authors.library.caltech.edu/records/t7km1-0q967
- 研究问题：模型不确定性下如何把 worst-case 性能、输入/输出约束和 state-feedback synthesis 统一进入 robust MPC。
- 方法/关键结论：把 worst-case infinite-horizon objective 的上界以及 input/output constraints 转成 LMI convex optimization；可行 receding-horizon state-feedback 对所考虑的不确定 plant family 给出 robust stabilization。
- 与本项目关系：第36章之后的 joint state/input ancillary synthesis 可以借用这类 constraint-aware synthesis 思路，但“把约束直接放进 K 的设计”本身不是创新。
- 局限：该工作不是 CZ-SMF posterior、不是本项目的 thrust-scheduled residual W(T)，也不提供当前 output-feedback set-membership 接口。
- 本项目状态：作为 certificate-based ancillary synthesis 的经典 baseline。
- Run 133 阅读层级：仅核对 Caltech 正式页面与摘要；未取得可稳定阅读的全文，故不引用定理编号，也不声称其 LMI 直接覆盖 correlated `(A(T),W(T))` 与 intermittent output feedback。


## Lorenzen, Cannon, Allgöwer — Robust MPC with recursive model update
- 年份/出处：2019, *Automatica*, 103:461–471；DOI：https://doi.org/10.1016/j.automatica.2019.02.023；accepted manuscript：https://ora.ox.ac.uk/objects/uuid%3A78236757-fb85-4510-8e17-d75177b667d8
- 研究问题：在线 parameter/model update 后，如何在保持 robust constraints 与稳定性保证的同时减少 MPC 保守性。
- 方法/关键结论：把 online set-membership system identification 与 homothetic prediction tubes 结合；论文将 robust constraint satisfaction 和 closed-loop stability 的要求分开处理，并给出 recursive model update 下的稳定/约束保证。
- 与本项目关系：说明“在线更精确 uncertainty set 可减少保守性”已有成熟理论背景。第36章的 scheduling-conditioned residual 只能作为更强 baseline，不是创新点。
- 局限：处理 parametric model uncertainty，不是当前 state-estimation CZ posterior，也不是四旋翼 thrust-conditioned nonlinear remainder。
- 本项目状态：作为后续 SMF/CZ 保守性比较必须超过的 adaptive robust MPC baseline。

## Goulart, Kerrigan, Maciejowski — Optimization over State Feedback Policies for Robust Control with Constraints
- 年份/出处：2006, *Automatica* 42(4):523--533；DOI：
  https://doi.org/10.1016/j.automatica.2005.08.023；作者存档：
  http://hdl.handle.net/10044/1/724
- Run 157 精读：Introduction、Sections 2--4，重点核对 affine state-feedback 与 causal
  affine disturbance-feedback 的等价参数化、polytopic uncertainty 下的凸约束接口。
- 方法/关键结论：对有界加性扰动和多面体混合约束，有限时域 affine feedback 可改写为对
  过去扰动的因果仿射策略，并转成 LP/QP/SOCP；这已覆盖“用仿射反馈改变 reachable-set
  shape 并 robustify 输入/状态约束”的一般思想。
- 与本项目关系：Run157 的 `delta T=K_v d_v` 只是该成熟参数化在两个已知 exact generator
  fibers 上的一步实例；本项目的差异仅在 noisy-output information fiber、缺测自动机和共享
  estimator/plant residual，不能据此声称新的仿射反馈算法。
- 局限：论文是全状态/扰动反馈有限时域框架，不直接给出当前15模态信息集合的 recurrent
  target inclusion，也不证明 SMF--MPC 递归可行性。

## Goulart, Kerrigan — Output Feedback Receding Horizon Control of Constrained Systems
- 年份/出处：2007, *International Journal of Control* 80(1):8--20；DOI：
  https://doi.org/10.1080/00207170600892949；作者存档：
  http://hdl.handle.net/10044/1/4386
- Run 158 精读：problem formulation、finite-horizon affine output-feedback reformulation、
  robust constraint conditions 与 invariant error outer-approximation 部分。
- 方法/关键结论：固定线性 observer 下，带状态扰动和测量误差的 constraint-admissible affine
  output-feedback 问题可等价凸化；永久约束保证还要求 observer error 的 invariant bound 与
  receding-horizon terminal/shift 条件，不能由一步安全外推。
- 与本项目关系：mode-9 同一当前输入覆盖 success/miss 是该 robust causal policy 量词的
  packet-automaton 特化；本轮 exact branch witness 只是局部实例，不是其算法的新版本。
- 局限：论文不含 bounded-dropout automaton、joint `(eta,e)` information set、共享 residual
  primitive 或 actual-thrust-dependent residual，因此不能替代当前 target-family 闭合证明。
- Run 159 定向重读：finite-horizon robust constraints、输入/状态约束与无限时保证条件。
  本轮支持函数下界只是其 affine output-feedback 约束思想在一条 dropout history 上的精确
  必要条件；不构成新的综合算法，也不提供 terminal/shift 结论。
- Run 160 重读同一正文范围。通过把信息权限放宽到任意 full-state causal policy，本轮必要
  下界比 affine output-feedback 可行域更乐观；其失败可否定当前 seed/输入盒，但仍不是一般
  output-feedback 算法或无限时定理。

## Hempel, Kominek, Werner — Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix
- 年份/出处：2011, CDC-ECC；DOI：https://doi.org/10.1109/CDC.2011.6160901；全文：https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf
- Run 140 精读：Sections II--III、Definitions 1--2、Theorem 1、式 (3)--(11)。Run 141
  为 full-state/causal predecessor 比较重读 Section III-A--C、Definition 2、Theorem 1
  及控制输入计算，确认同一 noisy output 的 observation fiber 必须共用一个输入。Run 142
  重读式 (3)--(10) 与 Section V：其 Farkas 条件验证给定 OFCI polytope 并在线求输入，
  论文明确仍缺直接计算 OFCI polytope 的算法。
- 方法/关键结论：对每个 admissible noisy output 及当前已知 scheduling，选择一个只依赖输出/调度的输入，使与该输出一致的全部状态和所有过程/测量扰动满足多面体不变；给出 Farkas 验证及在线/显式 PWA 控制计算。
- 与本项目关系：直接支持 observation-fiber 共用输入的量词；因此该量词不是创新。其 scheduling 外生且当前可测，本项目 actual thrust 由 correction 决定且下一 packet outcome 未知，不能直接套用其 LPV 顶点条件。
- 本项目状态：partial-information RCI 的最强直接有限维基线。
- Run 143 重读：Section III-A--C、Definition 2、Theorem 1、式 (3)--(10)，用于核对
  joint `(eta,e)` 候选上仍必须按相同可见 `d=e-eta` fiber 共享输入；该量词不是本项目创新。
- Run 144 重读：同一章节用于核对 mode 4/9 的未知 success/miss 分叉在当前时刻仍只能
  使用同一个 fiber control；本轮的零输入内证书只是其量词的特例，不是新算法。
- Run 146 精读：Section III-A--C、Definition 2、Theorem 1、式 (3)--(11)，复核第二层
  predecessor 中每个 `d` 对应的完整隐藏 `eta` 纤维及未知 packet successor 必须共享当前
  输入；给定候选的验证与控制计算已有直接近邻。
- Run 147 重读同一章节：用于确认初始化 all-miss history 的完整 hidden `eta` fiber 不能
  按真值拆分；zero correction 生成一个中心化 return image，不是 output-feedback controller
  synthesis。Run 149 纠正：该中心位置不是任意 policy 必须容纳的 target。
- Run 155 重新精读 Section III-A--C、Definition 2、Theorem 1、式 (3)--(14)。再次确认
  同一 noisy-output fiber 的完整相容状态只能使用一个 output-dependent input，且输入约束与
  鲁棒后继属于同一量词；仿射输入在凸 fiber 上的可行性仍依赖凸输入集。
- Run 180 全文重读 §II、§III-A--C、Definitions 1--2、Theorem 1、式(3)--(14)与
  Algorithm 1，定向核查固定 output cell、PWA input 与逐 facet robustification。该框架已覆盖
  本轮 fiber-shared affine policy/target-normal oracle 的方法思想；当前差异只在 packet edge、
  joint `(eta,e)` 坐标和 actual-thrust-dependent residual 的可靠实例化。
- Run 181 重新下载全文并精读 §III-A--C、Definition 2、Theorem 1、式(3)--(14)与
  Algorithm 1，专门核查“当前输入先于未知 packet label”的 mode-4 双边证书。论文要求每个
  noisy-output fiber 共用输入并逐 facet robustify，但其 LPV scheduling 在控制时可知、扰动集
  固定；本轮仍只是在项目的 unknown-edge/shared-residual 合同上可靠实例化，不作创新声明。
- Run 182 重新下载全文，定向精读 §III-C、式(9)--(14)与 Algorithm 1。各 facet 的参数解必须
  覆盖完整 `Y(Omega)`，再交集细化为共同凸分区并在每区求单值 PWA control。因此有限 output
  partition、完整覆盖与 overlap refinement 均已有直接基线；Run180/181 若不验证 target
  `d`-cell 覆盖，就还不是可执行 partition graph。

## Houska — Intrinsic Separation Principles
- 年份/出处：2023 预印本、2026 *Automatica* 183:112661；DOI：https://doi.org/10.1016/j.automatica.2025.112661；全文：https://arxiv.org/pdf/2307.04146
- Run 182 重新下载全文并精读 §4.2、§4.4、§6.1--6.7、Definitions 4--5、Lemma 2、
  Theorem 3 与式(25)--(29)。configuration-constrained polytopes 参数化固定复杂度 information
  ensembles；extreme vertex polytopes 上的 controls 经凸插值覆盖全部 information sets；式(29)
  直接综合 invariant terminal ensemble，§6.7给出 facets、ensemble parameters 与 extreme sets
  数的复杂度权衡。故固定预算 information-family 是本项目必须复现的强基线，不是创新声明。
- Run 183 重新打开全文并定向精读 §4.2、§5.5、§6.1--6.7、式(24)--(31)与 Theorem 3
  证明。原问题固定线性 `A,B,C` 和固定多面体 `W,V`；式(29)在每个 extreme information
  polytope 上配置一个共享控制，并以不变 ensemble 作终端条件。当前实际推力相关 `W(T)` 与
  packet-dependent measurement 不能直接代入；本轮只构造执行器全域固定包络和15-mode
  edge-product适配合同，不声称已复现式(29)的数值解。
- Run 184 重新精读 §6.1--6.7、式(25)--(30)、Theorem 3及证明。原式的posterior-measurement
  后选control时序不同于当前`control_precedes_successor_edge`；本轮采用每个source一组
  extreme controls、先传播后按edge测量的因果适配。axis-aligned box实例最终由21行exact
  Farkas证书否定；该否证只针对丢失位置--速度相关性的模板，不否定一般information ensemble。
- Run185 针对相关模板重读 §6.3--6.7、式(25)--(30)与Theorem 3。纠正坐标变换后，固定
  `(p,q)` parallelogram shape不能周期闭合；尚未构造`Z/H/Omega`、extreme-set controls或
  invariant ensemble，因而不援引Theorem 3外推一般模板不可行。
- Run186 精读 §6.2--6.5、式(25)--(27)及Theorem 3构造和证明开头。单个六facet集合的
  measurement-support映射只提供`Y/G/Lambda`层接口；连续measurement centers、`Z/H/Omega`
  与extreme information sets仍须另证，不能由一次严格支持收缩升级为invariant ensemble。
- Run187 重读§4.1--4.2、§6.2--6.5、式(7)、(25)--(27)及Theorem 3证明。sensor ensemble
  `V`已通过“存在同一measurement center”的集合量词覆盖连续观测域；对六facet模板，
  measurement-compatible coordinate可精确取`Z_1=(e_0+e_3)/2`。因此无需枚举未来center，
  但剩余`Z_2/H/Omega`及control-before-packet图仍须独立构造。
- Run188 重读§6.1--6.5、式(25)--(27)、Definition 7、Theorem 3及证明。`Z`坐标影响离散精度，`H/Omega`由所选参数多面体configuration决定；可逆线性换坐标保持同一参数多面体的极点数，不能据此声称减少extreme information-set预算。
- Run189 重读§3.1--3.2、§6.2--6.7、式(25)--(30)及Definition 7。参数多面体的几何极点还需按包含极大性过滤为真正extreme sets；仅用物理包含构造的有界域含完整安全盒这一支配成员，故ensemble边界退化为单元素，不能提供information-dependent control。
- Run190 重读§3.1--3.2、§6.1--6.5、Definition 7、式(56)--(57)及Theorem 3证明接口。真实位置条带生成连续多个互不包含的真正extreme sets，但其offset参数域可是一条仅有两个顶点的线段；真正boundary与finite extreme-vertex representatives必须分开计数。
- Run 144 精读：Sections 4.4、6.1--6.7，Definition 4、Lemma 2、Theorem 3、
  Problems (24)、(27)、(29) 与 complexity discussion。
- 方法/关键结论：以 information ensemble 表示未来可能的信息集集合；用
  configuration-constrained polytopes 和 extreme vertex polytopes 得到有限维凸近似，
  每个 extreme information set 配置一个控制，(29) 可计算 invariant polytopic
  information ensemble。
- 与本项目关系：joint information set、extreme-fiber control、固定模板 polytope 与凸
  优化均已有强近邻，不能作为创新。本项目只剩 packet graph、observer split、shared
  primitive 和 actual-thrust-dependent residual 的可靠实例化及完整闭环证据链可研究。
- 局限：其通用信息 ensemble 近似没有直接给出当前15模态 contract 的精确 candidate，
  也不替代 source-domain、input allocation、terminal/shift 的逐项证明。
- 本项目状态：一般信息集合成的最强直接基线；Run 144 仅实现一个受限一步内证书。

- Run 145 定向重读：Sections 4.2、6.1--6.5、Definition 4、式 (7)、(24)--(27)，
  用于界定15模态首次下降层。extreme information-set control 与多面体信息集合成已有
  一般方法；本轮逐模态零修正内投影只是一种受限实例。
- Run 146 定向重读：Sections 5.3、6.1--6.5、式 (38)、(43)，用于区分固定完整纤维模板
  与一般 information ensemble。完整纤维第二层若塌缩，只能淘汰该保守模板，不能否定
  保留条件纤维相关性的多面体信息集方法。
- Run 147 精读全文 HTML Sections 4.4、6.2、6.4--6.5、Lemma 2、Definition 7、
  Theorem 3 及证明。极端 information set、每集合共享控制和多面体 information tube 已有
  一般方法；本轮 rank-three correlated return seed 只是当前 packet/observer 合同的一项
  必要 reachable-set 实例证书，不作集合算法创新声明。
- Run 149 重读 Sections 3.5、4.2--4.3、5.3--5.4，Definition 1、Theorem 1及证明、
  式(18)--(20)，并复核 Sections 6.5--6.7。固定加性扰动集下，控制策略改变 tight
  information tube 的 extrinsic translations 而不改变 intrinsic equivalence class；本项目
  只有使用 Run136 global envelope 时才能直接采用这一 shape/center 分离，scheduled
  `W(T)` 不满足其固定扰动集接口。
- Run 150 重新逐页精读 pp.14--17 的 Sections 4.1--4.3、Definitions 4--6、Theorem 1
  及证明，pp.23--25 的式(18)--(19)/Theorem 2，pp.29--32 的 Definition 7、Theorem 3
  及证明。确认 translation functions 和 extreme-information-set controls 已覆盖一般方法；
  本轮只对 Run148 exact shape 给出实例级 width obstruction，不能宣称新算法或一般
  information-ensemble 不可行。
- Run 154 定向精读 Sections 4.2--4.3、6.3--6.5、Definitions 5--7、Theorems 1/3 与证明。
  一步 ensemble inclusion 的量词先固定同一 policy，再外包全部后继信息集；逐层更换策略不
  产生一张可执行控制器。凸外包产生的新 information sets/fibers 也必须纳入下一步闭合。
- Run 155 定向复核 Sections 6.4--6.5、Definition 7、Theorem 3 与证明中 extreme
  information-set controls 的连续凸权重组合。固定线性边、凸扰动和同一仿射可见策略时，
  convexification-created fibers 由仿射像/凸包交换律自动覆盖；这是该一般方法的直接特化，
  不是新算法，且不能用于 control-dependent `W(T)` 或跨离散标签混合。
- Run 156 重新精读 Section 6.5、Theorem 3 的完整证明，并复核 Section 4.2 Definitions
  4--6。证明中的控制 `mu(X)` 由当前 information set 的凸权重组合 extreme controls；因此
  零/label-only 策略失败不能外推为一般 information-ensemble feedback 失败。
- Run 159 重读 Sections 6.4--6.5、Theorem 3，确认一般 information-set feedback 已有完整
  近邻；本轮只淘汰一个 fixed-residual、bounded centered-affine path，不能外推为一般方法失败。
- Run 178 全文定向重读 Sections 2、3.1--3.3、Propositions 1--3 及 extreme-set/downward-
  closure 构造。information ensemble 对任意紧集求交的闭合和最小表示已有一般理论；仓库
  `T_0/T_1` 只能描述局部边，不能替代既有 60-state/45-recurrent information-family 合同。

## Villanueva, Müller, Houska — Configuration-Constrained Tube MPC
- 年份/出处：2022，arXiv:2208.12554；全文：https://arxiv.org/pdf/2208.12554
- Run 183 实际阅读：摘要、Introduction、§2.1--2.3、§3.1--3.4（pp.1--9）。论文针对具有
  加性/乘性不确定性的线性系统，用固定 facet directions、configuration cone 和 vertex maps
  联合参数化 tube facets/vertices，并把 vertex controls 纳入凸优化；论文明确以可表示 tube/
  policy 类的集合包含定义严格“更少保守”。
- Run 184 定向重读 §2.1--2.3、§3.1--3.4，用于逐项构造box的configuration cone与vertex
  maps。4-facet box及其vertex controls是现有框架的直接实例；不可行结论来自当前仅位置测量
  下的velocity-radius环，不是CCTMPC一般方法失败。
- Run185 精读 §3.4--3.5的Theorems 1--2、式(15)--(21)，§4.1--4.2的Corollary 4、
  式(25)--(27)与Remark 5。新增facet、configuration domain和vertex-control LP均属已有方法；
  固定parallelogram外包失败不能替代保留active velocity facets的六facet configuration检查。
- Run186 精读 §3.4--3.5、Definition 6、Lemma 1、Theorems 1--2、式(4)--(8)，并重读
  Corollary 4、式(15)--(18)。六法向的24行configuration cone和六个vertex maps均是该框架
  的直接实例；本轮贡献等级仅为项目基线的精确复现与measurement接口纠错。
- Run189 重读§3.4--3.5、Definition 6、Lemma 1、Theorems 1--2。configuration cone与vertex maps可把物理state containment写成参数线性约束，但有界性本身不保证多个不可比较的最大多面体。
- Run190 重读§3.4--3.5、Lemma 1、Definition 7及Theorem 2的vertex-map证明。测量生成的offset segment落在configuration cone内，但矩形上的斜facets冗余、segment处于退化边界；这不足以认证regular六facet meta configuration。
- 与本项目关系：`Y,G,Lambda` 的配置约束几何和 vertex-control machinery 是强基线工具，不能
  作为创新。本文是 full-state robust tube，不处理当前间歇测量 information ensemble；Run183
  只借其模板接口，尚未选择模板或证明相对固定/同伦tube的同预算优势。

## Badalamenti, Mulagaleti, Villanueva, Houska, Bemporad — Efficient Configuration-Constrained Tube MPC via Variables Restriction and Template Selection
- 年份/出处：2025 IEEE CDC；DOI：https://doi.org/10.1109/CDC57313.2025.11312697；全文：https://arxiv.org/pdf/2505.14440
- Run186精读：§3.1--3.2、§4.1、Problem (19)、Algorithm 1、Proposition 3，以及§5中
  10-state quadrotor的template/computation比较。
- 方法/关键结论：以configuration triple `(F,E,V)`表示固定facet/vertex结构；Algorithm 1
  逐次切除当前vertex、重算configuration triple并解RCI QP，使性能指标非增。论文明确讨论
  facet/vertex数量与在线变量、约束及保守性的折中，并给出10状态四旋翼例。
- 与本项目关系：手工给box增加一对耦合法向以及“template refinement”本身已被更强一般方法
  覆盖，不能作为创新。本项目可研究的差异只剩间歇测量information ensemble、控制先于packet
  label的因果图、可靠SMF接口及同预算闭环收益。
- 局限：论文是full-state robust tube/RCI template设计，不直接给出当前`Z/H/Omega`、
  measurement meta-update或15-mode packet graph证书。
- Run189 重读§3.5--3.6、§4.1、Algorithm 1及复杂度讨论。限制自由度和增添template facets已有系统方法；本项目若新增offset/shape约束，必须由information结构及闭环证书驱动，不能用任意caps制造预算结果。

## Kumar, Kothyari — Set-Theoretic Output Feedback Tracking Control via Linear Programming
- 年份/出处：2026, MTNS 2026；作者公开全文：
  https://www.researchgate.net/publication/407040373_Set-Theoretic_Output_Feedback_Tracking_Control_via_Linear_Programming
- Run 144 精读：Sections 2.3--3、Definition 4、Theorem 5、式 (14)--(29)。
- 方法/关键结论：对 `x+=Ax+Bu+Ew, y=Cx` 与静态 `u=Ky+Lr`，用 zonotope containment
  线性条件联合综合 output-feedback gain、state RCI 和 admissible reference set。
- 与本项目关系：这是截至本轮检索到的2026直接 zonotopic output-feedback RCI 近邻，排除
  “zonotope + LP 联合求 gain/RCI”的首次性；其 OFCI 定义也要求同一 output fiber 共用输入。
- 局限：没有测量噪声、间歇包、observer 信息状态、mode graph 或 actual-input-dependent
  residual；因此不能直接认证 `(eta,e)` joint information candidate。
- 本项目状态：最新静态 output-feedback zonotope-LP 对照；不得把其 state RCI 结论移植为
  当前 partial-information RCI。

## Rungger, Tabuada — Computing Robust Controlled Invariant Sets of Linear Systems
- 年份/出处：2017, *IEEE Transactions on Automatic Control*, 62(7):3665--3670；DOI：https://doi.org/10.1109/TAC.2017.2672859；全文：https://arxiv.org/pdf/1601.00416
- Run 142 精读：pp.1--7，式 (4)--(10)、Lemma 1、Theorem 1 及 Section 4 的 Pontryagin difference/projection 实例。
- 方法/关键结论：从 `R_0=X, R_{i+1}=pre(R_i) intersect X` 的递减序列出发，区分一般不有限终止的 outer predecessor sequence、允许任意小约束放松的外 RCI 近似，以及用 disturbance inflation 获得的内 RCI 近似。
- 与本项目关系：给出二维多面体 predecessor、投影和证据等级的直接基线；但其控制器观察完整迭代状态。本项目只能在可见 `d` 上用该迭代，隐藏 `eta` 必须先按 observation fiber 统一 robustify。
- 本项目状态：Run 142 的 exact product-fiber predecessor 基线；迭代/投影不是创新。
- Run 145 定向重读：pp.1--6、式 (4)--(10)、Theorems 1--2 与 Remark 1。普通
  `R_1=X∩pre(X)` 只是 descending outer sequence 的一层，一般既非 RCI 也不能导出永久
  安全反馈；因此本轮15/15非空只能作为继续第二层的门槛。
- Run 146 重读：pp.1--6、式 (4)--(10)、Theorems 1--2，核对第二下降层仍只是有限
  predecessor 序列；无论非空或部分塌缩，都不能越级声称 RCI 或一般输出反馈不可行。
- Run 160 重读 Introduction、式(1)--(10)、Lemma 1 与 outer/inner RCI discussion。当前结论
  来自一条允许字符串上策略无关的硬约束必要条件，而不是有限 predecessor 非空/塌缩；仍只
  否定固定 seed/residual/input contract，不升级为一般 RCI 不存在。
- Run 194 重读定义、式(4)--(10)、有限确定讨论、Lemma 1、Theorems 1--2及证明。Run193的
  四层集合仍是一般descending outer sequence；本轮必须直接检查self-predecessor/vertex-control
  条件，不能由有限层非空推断RCI。

## Houska, Müller, Villanueva — Polyhedral Control Design: Theory and Methods
- 年份/出处：2024, arXiv:2412.13082；全文：https://arxiv.org/pdf/2412.13082
- Run 142 定向阅读：Sections 3.3--3.6、3.10，重点 pp.12--16 的 controllable/control-invariant/robust-control-tube 参数化与 pp.21--22 的 output-feedback 文献路由。
- 方法/关键结论：系统整理 vertex control、polyhedral projection、固定复杂度 polytope/zonotope 和 robust control tube/RCI 的凸优化表示。
- 与本项目关系：非轴对齐多面体、vertex input interpolation 和固定模板均已有成熟近邻；本项目若有贡献，必须来自可靠 SMF 信息接口、联合相关性及闭环 theorem，而不是集合参数化本身。
- 本项目状态：多面体综合与复杂度比较的综述基线。

## Baras, Patel — Robust Control of Set-Valued Discrete-Time Dynamical Systems
- 年份/出处：1998, *IEEE Transactions on Automatic Control*, 43(1):61--75；全文：https://terpconnect.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf
- Run 140 精读：Section IV-A--B、Lemma 4、Theorems 9--11、15--16。
- 方法/关键结论：把 observation history 诱导的信息状态作为充分统计量，将 output-feedback robust game 转为 information-state feedback game，并给出有限/无限时动态规划必要与充分条件。
- 与本项目关系：说明仅使用点估计偏差 `d` 的有限 policy class 一般是保守近似，不能宣称等价于所有 output-feedback controllers。
- 本项目状态：一般信息状态概念基线；不直接数值实现其无限维动态规划。
- Run 143 定向精读：Section IV-A 的 Information State Formulation、Lemma 4、Remarks
  8--10、Theorems 9--11，复核可行状态/历史相关性必须保留，且一般信息状态是无限维。
  这支持从 product `E_eta x D` 转向 joint set，但不能把 joint set 本身声明为创新。
- Run 152 重读 Section IV-A 的 Information State Formulation、Lemma 4 证明、Remarks
  8--10、Theorems 9--11 与 Corollary 4。由完整历史信息状态压缩到有限标签，必须另证
  初始化覆盖和递归模拟；`mode/age` 标签本身不是充分统计量证明。
- Run 177 再读 Section IV-A、Lemma 4、Remarks 8--10、Theorems 9--11、Corollary 4，专门核查
  五步非线性问题的初始条件与时序。配置 prior 经 tick-0 实际测量才形成 posterior，因此应量化
  posterior 族；有限时域 Bellman 后继还必须保留 tick-5 success/miss 的不同 mode。

## Kjellqvist — Minimax Dual Control with Finite-Dimensional Information State
- 年份/出处：2024, L4DC, *Proceedings of Machine Learning Research* 242:299--311；
  全文：https://proceedings.mlr.press/v242/kjellqvist24a/kjellqvist24a.pdf
- Run 143 精读：Sections 2.1--2.2、Assumption 2、Proposition 4、式 (11)--(18) 及结论。
- 方法/关键结论：当每个测量逆像最多含固定有限个元素时，把 worst-case history 压成
  有限维递归信息状态并写成 information-state dynamic program。
- 与本项目关系：当前有界实值测量噪声产生连续无穷 observation fiber，不满足 Assumption
  2；不能援引该文宣称当前 joint information set 有精确有限维递归。论文结论也明确把
  实值传感噪声列为该有限逆像结果之外的情形。
- 本项目状态：有限维压缩的反边界；任何固定复杂度 CZ/polytope 压缩仍需单独包含证明。

## Yang, Ozay — Efficient Safety Control Synthesis with Imperfect State Information
- 年份/出处：2020, CDC, pp. 874--880；作者链接：https://web.eecs.umich.edu/~necmiye/pubs/YangO_cdc20.pdf
- Run 140 阅读层级：仅核查摘要；正文抽取失败。
- 摘要层面内容：把 estimated-state dynamics 上的 perfect-information safety game 用作一般 noisy-measurement partial-information game 的两个保守近似，并区分初态信息条件。
- 本项目状态：支持保守性标注，不引用其定理作本轮证明。

## Yang, Ozay — Safety Control Synthesis for Systems with Missing Measurements
- 年份/出处：2021, *IFAC-PapersOnLine*, 54(5):97--102；DOI：https://doi.org/10.1016/j.ifacol.2021.08.481；作者链接：https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf
- Run 140 阅读层级：核查摘要与问题陈述；正文抽取失败。
- 摘要层面内容：用 automaton 描述 missing-measurement patterns，利用 causality 构造 product system，把 partial-information safety synthesis 化为 full-information game。
- 与本项目关系：15-mode bounded-dropout product construction 已有近邻，不能作为创新；其有限安全游戏不直接处理当前连续六状态与 control-dependent residual。
- Run 153 精读 Sections 4.1--4.4、Algorithm 1、Propositions 2--5 及式 (8)--(11)。string
  automaton 在成功测量时压缩缺测串并规定因果开环输入承诺；产品不变集的安全结论仍量化全部
  允许 return string、扰动与中间状态。它支持 `(mode,last_return)` 的离散语言实现，但不把
  连续联合信息集压成有限标签，也不允许以三个首次-return seed 代替真实初始化。
- Run 159 重读同一正文范围，专门核查长 dropout string 上每个中间状态的 safety 义务；因此
  `15->15` 在 mode 11 的位置失败已经足以阻断 final-success target constituent。
- Run 160 重读 Sections 2--4、Assumption 1 与 product safety 量词。15-tick string 的第13个
  miss 已违反中间状态必要条件，即使最终 success 可重置 estimator，也不能恢复该条安全路径。
- Run 165 重读全文 Sections 3--4、Definition 3、Propositions 2--5：控制器在缺测串开始前按可见
  信息选择因果输入承诺，安全量词覆盖允许串的每个扰动实现和中间状态。本轮极端可见fiber是该
  量词在冻结连续模型上的精确反例，不是string-automaton或product-game创新。

## Do, Prodan — Tube MPC via flatness for multicopter trajectory tracking
- 年份/出处：2024, European Control Conference；全文：https://hal.science/hal-04567082/document
- Run168精读：Sections II-A、III-A--B，式(18)--(25)。
- 方法/关键结论：将多旋翼跟踪误差化为带固定有界加性扰动`W`的系统，用mRPI集`Z`构造
  nominal tube，并以`X⊖Z`、`V⊖KZ`收紧约束；设计要求扰动与增益使收紧后集合非空。
- 与本项目关系：是固定全局余项包络的直接基线，但不从在线SMF信息集生成局部未来扰动界。

## Hu, Feng, Quirynen, Villanueva, Houska — Real-Time Tube MPC Applied to a 10-State Quadrotor Model
- **真实题名/作者/出版**：Haimin Hu, Xuhui Feng, Rien Quirynen, Mario Eduardo Villanueva, Boris Houska, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model*, 2018 American Control Conference (ACC), pp.3135–3140；DOI https://doi.org/10.23919/ACC.2018.8431112；作者公开正文 https://haiminhu.org/wp-content/uploads/2018/11/2018acc_1123_fi.pdf 。**2026-11-01纠正原总账误署名**“Hu/Bujarbaruah/Zhang/Borrelli”；保留本篇历史去重身份，不新增篇数。
- Run168精读：Theorem 1、式(8)、Lemma 1及对应证明。
- 方法/关键结论：用椭球tube与RFIT条件处理四旋翼非线性；`Omega_n(q,Q)`必须包含tube中每个
  状态和允许扰动对应的非线性余项，Lemma 1给出tube-dependent解析外包。
- 与本项目关系：是局部气动余项的最强方法基线。当前后验变小不够，必须认证整个15-tick未来
  tube并证明跨时刻闭合；本轮未复现其10状态控制器。
- Run169重读§II-A、Theorem 1、式(8)、Lemma 1及证明：RFIT与nonlinearity bounder量化tube中
  每个状态/扰动。故J14要求族中一个首步合法反例即可否定当前局部余项目标，无需用有限采样替代
  全量词，也无需继续传播其余14步。
- Run170纠错：上一句的“J14要求族”只对独立残差外包成立；没有从benchmark初始集出发的
  非线性轨迹证书时，不能把外包成员称作真实plant可达，也不能据此外推物理路线不可能。

- **2026-11-01背景第6轮重新核验状态：作者公开PDF第1–6页§II-A/B、§III-A–E（式(5)(7)(8)(10)、Theorem 1、Lemma 1）、§IV Table II分节已读**；未核对IEEE排版终版，不复现ACADO控制器。实际模型状态为`(p1,p2,p3,v1,v2,v3,pitch,roll,pitch_rate,roll_rate)`，10状态≠10自由度；控制为俯仰/滚转命令与垂向推力通道`(u1,u2,u3)`，`dot(v3)=-g+k_T u3`，忽略真实总推力倾斜的`T cos(phi)`耦合；外扰`w1,w2,w3`加在位置导数，而非本仓库平动加速度。论文采用当前全状态测量`xhat0`和低层`mu(t,x)`，**无位置-only有噪丢包、无状态/参数SMF/CZ**。
- **本轮约束/定理/实验复核**：一般式(2)状态多面体；10状态算例仅墙面`x1<=4`，输入`u1,u2∈[-pi/9,pi/9]`、`u3∈[0,2g]`，扰动椭球`Qw=diag(0.01,0.09,0.25)`。Theorem 1需椭球RFIT动力学及输入/非线性余项条件，§III-C讨论终端不变椭球而**明确不证明严格闭环稳定性**。§IV为ACADO/qpOASES数值仿真，非实飞；**高层Tube MPC平均81.6ms/RTI，低层显式反馈20μs，名义MPC 159μs**；椭球OCP有65状态/35控制优化变量，未给20ms WCET。不得用低层20μs宣传高层每20ms可求解。
- **本课题关联/可复用/待查**：可复用“对完整未来tube所有状态/扰动认证非线性余项、再验证终端RFIT”的论证结构；不能移植其垂向解耦、全状态反馈或实时性结论到仓库六状态`T cos(phi)`和位置失测SMF。与本轮垂向边界精确一步非可生存反例的关系见[背景第6轮日志](../research/model_selection/background_run_20261101_1537_vertical_hu2018.md)。待查：原六状态hover附近是否存在非空、可移位的局部信息状态安全前驱域？

## Rego, Raffo, Terra, Scott — Reachability Analysis of Nonlinear Discrete-Time Systems Using Polyhedral Relaxations and Constrained Zonotopes
- 年份/出处：CDC 2024；作者预印本2025，arXiv:2504.11663；DOI：https://doi.org/10.1109/CDC56724.2024.10886592；全文：https://arxiv.org/abs/2504.11663
- Run170精读：§II Problem Statement and Preliminaries，式(1)--(8)；§III Definition 3、式(10)--(11)及乘法的McCormick包络。
- 方法/关键结论：从`X0`与过程不确定集`W`递归外包非线性像；把factorable函数分解为共享
  中间因子，在lifted space中相交各因子的多面体包络，再投影为CZ。包络复杂度线性增长，仍需
  CZ降阶。该方法是保留非线性计算图依赖的直接基线，不是本项目创新。
- 与本项目关系：Run169的独立逐边残差primitive丢失了状态--风--气动残差的物理图；应先按该
  类方法构造联合外包，再接缺测SMF、控制收紧和递归可行性。本文不直接解决本项目的有界丢包
  信息状态、因果控制选择或四旋翼硬约束闭环定理。

## Ning — Data-Driven Synthesis of Robust Positively Invariant Sets: From State Feedback to Output Feedback
- 年份/出处：2026, arXiv:2608.23412；全文：https://arxiv.org/abs/2608.23412
- Run 140 阅读层级：核查摘要及 problem formulation，未精读证明。
- 已知内容：从 noisy offline data 对 LTI state-feedback 与 observer-based output-feedback 同时综合 gain 和 ellipsoidal RPI。
- 与本项目关系：是 2026 新近邻，但仍先冻结 observer-based closed loop；不覆盖 observation-fiber controlled RCI、bounded-dropout automaton 和 feedback-dependent residual graph。

## Lucia, Ernesto, Castelan — Set-theoretic output feedback control: a bilinear programming approach
- 年份/出处：2023, *Automatica*, **153:111004**；DOI：**https://doi.org/10.1016/j.automatica.2023.111004**；作者预印本：https://users.encs.concordia.ca/~wlucia/files/STOutput2023.pdf（预印本链接本轮未重新核验）。Run236据DBLP https://dblp.org/rec/journals/automatica/LuciaEC23.html 与交叉书目核实并纠正原日志误记的151:110861及错误DOI；历史Run141阅读层级不变。
- Run 141 精读：Sections 2--5、Definitions 2--3、Propositions 1--2、Algorithm 1、式 (7)--(31)。
- 方法/关键结论：联合综合静态输出反馈增益、terminal RCI 与嵌套 robust one-step controllable sets；rank-deficient output 情形采用不依赖隐藏状态的离线切换，满状态带噪情形才可用当前测量选择更小集合。集合包含和输入约束由 extended Farkas lemma 转成双线性条件。
- 与本项目关系：直接说明 output-feedback 与 full/noisy-state feedback 的信息权限及在线集合选择不同；因此读取隐藏 `eta` 的 vertex control 只能作乐观上界，不能作为当前 causal ancillary policy。
- 局限：论文处理 LTI、静态输出增益和嵌套多面体，不含 15-mode missing-data graph、实际推力相关余项或 SMF zonotope fiber。
- 本项目状态：作为 output-feedback set synthesis 的强方法基线；Run 141 只实例化因果性负对照，不复现其 bilinear synthesis。

## Run201 定向重读（2026-10-30；历史84篇中的 Lorenzetti & Pavone，不新增篇数）

- **论文：** Joseph Lorenzetti, Marco Pavone, *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, 2020, arXiv:1911.07360v2；原文 https://arxiv.org/pdf/1911.07360 。
- **阅读层级与范围：** 2026-10-30，原文 Section II Assumptions 1–2、Section III-A RPI 定义、Section IV-D 式(10)–(11)、Section IV-E/F 式(12)–(13)及 Proposition 1；其余章节本轮未重新核验。
- **问题/方法：** LTI 系统受有界过程与测量噪声影响时，用 Luenberger observer、耦合估计/控制误差的固定截面 RPI、nominal MPC 与约束收紧建立输出反馈鲁棒约束满足。
- **关键假设/结论：** 需要 (A,B) 可控、(A,C) 可观、误差闭环稳定、存在 RPI 与满足终端包含/下降的 nominal terminal ingredients，且初始误差落入 RPI、初始 MPC 可行；Proposition 1 在这些条件下保证约束满足。固定 RPI 本身不替代 terminal/shift。
- **局限：** 连续的线性观测器测量、LTI 与固定误差截面；不直接涵盖冻结仓库的15-tick位置缺测图、推力调度任意跳变及状态相关气动 residual。
- **本项目关联/可复用：** 用耦合误差状态与 support 收紧审计四状态 SMF-MPC 接口，不能把“一个 tube + RPI + 终端”宣称新贡献。本轮的横向不可辨识下界是必须满足的必要条件，尚不是 Lorenzetti 充分控制方案。
- **待查问题：** 对每 tick 姿态观测和每5/10/15 tick位置更新，能否建立有限复杂度且 shift-compatible 的条件化后验/backup policy，并通过原四状态 Gate A？


## Run215 定向正文复核（2026-10-31；Scott等2016，既有87篇内，不新增计数）

- **题名/作者/年份/出处：** Joseph K. Scott, Davide M. Raimondo, Giuseppe Roberto Marseglia, Richard D. Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, *Automatica* 69:126–136。DOI：https://doi.org/10.1016/j.automatica.2016.02.036；作者公开全文：https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **本轮实际阅读范围：** Definition 3 (9)，Proposition 1 (11)–(13)，Proposition 2 (19)–(20)，Theorem 1 (21)，Section 4 复杂度增长/降阶讨论，Section 5 (31)–(33) 状态估计递推；其余章节未在本轮精读。
- **研究问题/方法：** 在有界过程/观测误差下，用 CG 表示 \(Z=\{G\xi+c:\|\xi\|_\infty\le1,A\xi=b\}\) 保留集合交、线性映射与 Minkowski 和；通过约束/生成元降阶平衡精度和复杂度。
- **定理与假设：** Theorem 1 给出凸多面体与不限复杂度 CZ 表示的等价；Proposition 1 给出精确集合运算公式；Section 5 递推依赖线性离散动力学及紧有界扰动、量测误差。成员资格/非空通常需要 LP。
- **主要结论与局限：** 保留联合线性约束可避免过早区间外包；但约束数随递推增长，降阶须证明包含。论文没有为本仓库15-mode间歇测量和推力调度提供可直接套用的递归可行性定理。
- **本课题关联/可复用技术：** Run215先将位置—速度、姿态—角速度历史恒等式实现为精确有理数联合线性条带，并以三包位置支持严格排除第193拍旧盒角点。这是**H-表示外包**，虽可由 Theorem 1 转为CZ，却**没有实现CZ的CG表示、完整后验传播或降阶**；不将既有 CZ 理论宣称为新贡献。
- **阅读日期与待查问题：** 2026-10-31。需实现可复核的CG表示和联合支持优化，并在完整仓库/同等计算预算下验证能否恢复Run214第193拍控制准入；现有独立盒过滤仍拒绝。

---

## 背景第10轮 — Zhang、Walters、Xu（ACC 2022）采样CBF与误差界（2026-11-01；新增去重1篇）

- **题名/作者/出版：** *Control Barrier Function Meets Interval Analysis: Safety-Critical Control with Measurement and Actuation Uncertainties*；Yuhao Zhang, Sequoyah Walters, Xiangru Xu；2022 American Control Conference (ACC 2022)，DOI https://doi.org/10.23919/ACC53348.2022.9867681；作者预印本 arXiv:2110.00915v1 https://arxiv.org/pdf/2110.00915 。
- **阅读状态与范围：** 2026-11-01，公开PDF pp.1–7 §II-B/C、§III-A/C Propositions 1–2、§IV Assumptions 1–2/Proposition 3、§V Examples 1–3与式(20)；**分节已读，期刊/会议终版未逐式核验**，不是仅摘要。
- **研究问题：** 采样零阶保持控制中，如何在有界状态测量/执行误差与高相对阶安全约束下保持连续时间安全？
- **方法/模型与实际状态输入：** 一般连续控制仿射`xdot=f(x)+g(x)u`；区间Taylor模型/采样间可达管裕量、Lasserre下界、USDCBF-QP。Crazyflie实验采用**三维平移六状态双积分器**`(x,y,z,xdot,ydot,zdot)`与**三虚拟加速度**`(xddot,yddot,zddot)`，不是平面物理6状态T/tau。名义LQR控制。
- **实际量测/丢包与噪声：** §IV假设每个采样时刻完整状态估计`xhat`与真实状态误差2范数≤eps_x；不详述生成该估计的具体传感器融合链，不含位置丢包自动机；实验使用`eps_x=0.02`、虚拟输入执行误差`eps_u=0.01`，不能当作本仓库传感器合同。
- **状态/输入硬约束：** Crazyflie位置盒`x,y∈[-0.5,0.5], z∈[0,0.6]`，对三虚拟加速度的真实物理T/tau/PWM映射与饱和未在该例建模；理论输入域`U`需按执行误差做Pontryagin收紧`U⊖B_epsu`。没有本仓库六状态速度/倾角/角速完整硬盒。
- **定理与假设：** Proposition 1采样CBF相对阶1；Proposition 2高相对阶且初始辅助屏障非负；Proposition 3还要求每拍有界估计/执行误差、采样间可达外包、每拍安全输入集非空，才给前向安全充分条件。未给间歇位置SMF或终端信息RCI。
- **主要结论/实验与局限：** 两个数值例及Crazyflie约20s、50/100Hz实飞；线性六状态虚拟输入例报告平均QP计算约5ms，不是WCET，也不是实际T/tau饱和认证。实验样本内无违约不等于所有扰动下实飞保证；论文没有MPC、SMF/CZ状态集合递推、失测或终端递归可行性。
- **与本课题关联/可复用技术：** 可复用采样间可靠裕量、估计/执行误差分开外包和输入Pontryagin收紧的**审计清单**；仓库物理六状态横向位置对T的二阶增益在hover为0，力矩通道更高阶，不能移植论文三虚拟加速度的独立相对阶2 QP。Run256已严格否定独立盒速度无限认证，不等于论文的每拍有界全状态误差假设成立。
- **待查：** 对有噪间歇位置的关联H-rep/CZ后验，能否构造计算可行的六状态`(T,tau)`采样间安全裕量及共享因果终端前驱？背景任务不重复主任务代码。详见 `docs/research/model_selection/background_run_20261101_1935_zhang_sdcbf.md`。


## Run257 定向重读与四旋翼示例纠正（2026-11-02；Rego等2020，既有104篇内，不新增去重数）

- **题名/作者/发表：** Brenner S. Rego, Guilherme V. Raffo, Joseph K. Scott, Davide M. Raimondo (2020), *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, *Automatica* 111:108614，DOI https://doi.org/10.1016/j.automatica.2019.108614；作者预印本 https://arxiv.org/pdf/1908.09950 （v3），本轮未逐式核对期刊终版。
- **本轮已读范围：** 预印本PDF pp.2–3 §2–3.1 式(1)–(10)，pp.7–8 §4.4–4.5 式(22)/Remark 10，pp.10–12 §5.2 四旋翼例及Tables 5–6。其余章节本轮未重新精读。
- **研究问题/方法：** 一般非线性离散系统、已知施加输入、紧有界过程/量测噪声，使用CZ mean-value/Taylor外包预测与线性量测广义交集进行**状态**SMF；不是参数估计，也不是MPC。理论外包依赖正确的Jacobian/余项包含；交集可精确表达，降阶须保持包含。
- **实际四旋翼模型：** §5.2的仿真是12状态`(x,y,z,u,v,w,phi,theta,psi,p,q,r)`，输入`U1`总推力和`U2,U3,U4`差动推力/转矩通道；GPS/气压计/IMU提供有界误差位置、姿态、角速观测，速度不直接量测；无位置丢包自动机。采样0.01s、Euler离散。
- **关键局限与纠正：** 论文§5.2脚注10明确四旋翼仿真的轨迹跟踪控制**使用真实状态**，集合估计没有构成输出反馈MPC闭环；CZMV/ZMV平均半径比74.41%仅是其仿真条件下的结果。Table 6 CZMV平均迭代耗时约104.7–127.8ms（随约束数），超过0.01s采样周期；不能当作20ms可部署证据。此前Run256日志对示例是否包含四旋翼的概括不完整，本轮以原文更正：**确有12状态四旋翼仿真，但没有真实飞行或SMF闭环控制实验。**
- **与本课题关系：** Run257使用低复杂度两次位置条带与真实Euler运动学消元，得到第35拍成功读数速度投影宽度可靠上界1.0499925305899254m/s，严格优于独立盒3.1100396325m/s；这是**H-rep相关条带投影外包**，并非论文CZ算法复现或新定理。见`docs/research/run257_research_log.md`。
- **待查问题：** 将关联后验可递推化，处理下一次success/miss与保包含降阶，量化计算预算后再研究终端信息状态前驱；不把论文的估计保证冒充MPC递归可行性。


---

## 背景第16轮 — Kamel/Burri/Siegwart（2017）六旋翼8/9维级联LMPC/NMPC实飞对照（2026-11-02；新增去重第112篇）

- **题名/作者/正式出版**：Mina Kamel; Michael Burri; Roland Siegwart, *Linear vs Nonlinear MPC for Trajectory Tracking Applied to Rotary Wing Micro Aerial Vehicles*, *IFAC-PapersOnLine* **50**(1):3463–3469 (2017), 20th IFAC World Congress, DOI https://doi.org/10.1016/j.ifacol.2017.08.849 。ETH书目 https://www.research-collection.ethz.ch/entities/publication/0a5f376e-38a3-4d16-b6ff-643876ddbe2c ；作者预印本 arXiv:1611.09240v2 https://arxiv.org/pdf/1611.09240 ；公开代码 https://github.com/ethz-asl/mav_control_rw 。
- **阅读日期/范围/状态**：2026-11-02，**arXiv v2全7页已读**，重点pp.1–3 §1–4式(1)–(12)、p.4 §5–6式(13)–(15)、pp.4–6 §7–8 Tables1–2、Figs.3–9；**未逐页比对IFAC终版、未clone代码或复现实飞**。实飞平台明确是**Asctec NEO hexacopter六旋翼，非四旋翼**；只能作为多旋翼控制结构对照。
- **研究问题与控制任务**：外环三维位置、悬停、阶跃、激进轨迹跟踪，比较悬停线性LMPC与非线性NMPC；均采用独立姿态内环的级联结构。论文§3先给完整刚体动力学`(p,v,R,ω)`、旋翼转速平方推力/分配和气动阻力，但**优化器没有直接优化所有刚体状态或电机速度**。
- **实际状态与输入**：LMPC `x=(p_x,p_y,p_z,v_x,v_y,v_z,φ_I,θ_I)∈R⁸`，`u=(φ_I,cmd,θ_I,cmd,T_cmd)∈R³`，悬停小角度、heading-free姿态线性化；NMPC `x=(p_x,p_y,p_z,v_x,v_y,v_z,φ,θ,ψ)∈R⁹`，`u=(φ_cmd,θ_cmd,T_cmd)∈R³`，非线性平移+辨识一阶姿态内环，偏航速率假设瞬时跟踪。模型为三维平移/姿态外环，不是8或9个物理自由度；没有电机角速度、角加速度或三轴力矩直接决策。姿态闭环`τφ=.1901s,τθ=.1721s,kφ=.91,kθ=.96`，控制命令倾角±45°、总推力命令13.5–40.3N（六旋翼参数）。
- **实际量测/估计/不确定性**：IMU+Vicon动捕经EKF融合状态，增广EKF估计外部风力；是点状态/扰动估计而非状态SMF或参数SMF。没有有界位置噪声条带、间歇位置包丢失、CZ集合后验或失测自动机。预测期外力取常值，实飞风约11m/s不代表逐轨迹有界鲁棒保证。
- **MPC结构/约束/求解**：LMPC离散线性QP、CVXGEN；NMPC多重打靶非线性OCP、隐式RK4、ACADO SQP/Gauss–Newton RTI；两者100Hz更新、10Hz内部预测、N=20→2s。二次阶段/终端**代价**，外环命令角度/推力输入盒；未在式(9)/(15)给出终端受控不变集合、完整状态硬安全/旋翼力矩硬约束或输出反馈递归可行性定理。电机动力学和内环跟踪误差没有严格硬界。
- **实验与性能**：Asctec NEO六旋翼、ROS、Intel i7 3.1GHz；无风悬停RMSE LMPC1.84cm/NMPC2.05cm，约11m/s风中悬停2.7/2.5cm、激进轨迹10.8/7.1cm，阶跃上升1.6/1.0s。**平均**求解LMPC2.35ms/NMPC0.45ms，求解器不同，不能归因于NMPC普遍更省算力；未给20ms最坏时间上界。结果是实飞性能证据，不是SMF包含/硬约束保证。
- **局限/可复用技术/与课题关联**：可复用外环模型辨识、姿态内环时间常数、QP/RTI性能基线及ROS代码作为结构对照；六旋翼参数不能直接移植四旋翼，虚拟倾角/推力输入不能等同本仓库`(T,τ)`物理力矩输入。四状态固定推力垂向漂移、Run246/260–263安全/时滞问题不因论文实飞消失。条件性保留六状态平面物理模型为首选，分层MPC为备选；创新空间需由有噪失测状态SMF/CZ与真实输入约束/因果安全前驱的文献对照确认。
- **待查问题**：下一轮优先核验**真正四旋翼**分层/线性MPC实飞论文的实际电机接口、姿态内环误差与位置速度传感器合同。详细模型审计见 `docs/research/model_selection/background_run_20261102_1034_kamel_hexacopter_lmpc_nmpc.md`。


## Run264 定向重读（2026-11-02；Qiu等2020已登记，不增加去重数）

- **书目：** Quanwei Qiu, Fuwen Yang, Yong Zhu, Eman Mousavinejad, *Output feedback model predictive control based on set-membership state estimation*, *IET Control Theory & Applications* 14(4):558–567 (2020), DOI https://doi.org/10.1049/iet-cta.2019.0881；出版社开放全文 https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-cta.2019.0881 。
- **阅读日期、范围与状态：** 2026-11-02，出版社开放HTML正文§2 Assumptions 1–2、§3.1 Theorem 1、§3.2–3.4式(19),(34),(35)–(41)、§4式(45)–(57)、§5数值例；分节重读，数学公式有图片嵌入，未声称逐式核对所有公式或PDF页码。
- **研究问题、模型与输入：** LTV/LTI离散系统，已知矩阵，部分输出，输入向量u，紧有界过程及测量噪声；椭球**状态SMF**（非参数SMF）通过预测/测量更新与S-procedure/LMI保证真状态包含。MPC用有限时域minimax代价、椭球初始集合和状态/输入欧氏范数约束，经LMI/SDP求解；无四旋翼物理T/tau或失测自动机。
- **关键假设、定理与结论：** Theorem 1的集合包含依赖上一步已包含及LMI可行；§4的鲁棒终端不变椭球和局部反馈是额外条件，且§4明确假设**进入终端区域时真实状态已知**以使用局部Kx。持续扰动下结论为趋向包含原点的区域而非无扰原点渐近稳定；§5只报告二阶LTI、LPV、DC-DC转换器MATLAB/YALMIP/SeDuMi数值结果，未报告四旋翼、丢包、实飞或20ms最坏耗时。
- **局限、可复用技术与课题关联：** 可复用估计包含LMI、鲁棒预测约束和终端RPI的分层审计；**不能**把该文依赖真状态的终端局部反馈直接当作本项目隐藏速度+间歇位置输出反馈策略。Run264只延长固定历史的有限安全前缀，不构造该文终端RPI或证明递归可行。
- **待查问题：** 能否将真状态终端Kx替换为对同一有噪位置观测纤维共享的因果集合反馈，并使所有合法success/miss后验回到可移位信息集合？相关证书见 `docs/research/run264_research_log.md`。


## 背景第17轮：Izadi等四旋翼级联MPC时变推力约束与12维外环增广（2026-11-02）

- **书目/真实题名与版本**：Maedeh Izadi; A. T. J. R. Cobbenhagen; Ruben Sommer; A. R. P. Andriën; Erjen Lefeber; W. P. M. H. Heemels, *High-Performance Model Predictive Control for Quadcopters with Formal Stability Guarantees*, arXiv:2412.20277 (2024-12-28), https://arxiv.org/abs/2412.20277 、全文 https://arxiv.org/html/2412.20277 。正式期刊书目为 *High-performance model predictive control for quadcopters with time-varying constraints and formal stability guarantees*, *Automatica* 191:113141 (2026), DOI https://doi.org/10.1016/j.automatica.2026.113141 。**实际阅读2024 arXiv作者公开HTML，不冒称已逐页阅读2026期刊终版**。
- **阅读状态/范围/日期**：2026-11-02，**作者全文HTML分节已读** §2–11，重点§3式(16)–(19)、§4式(21)–(27)、§5式(28)、§6式(30)–(33)、§7 Theorems 8/10、§8–9 Theorem 11、§10实验、§11局限；附录A部分核对；未标PDF页码、未独立重证定理或复现。
- **问题与实际模型**：四旋翼三维位置/轨迹跟踪；真实刚体`(p3,v3,R∈SO(3),ω3)`、6物理自由度，真实输入质量归一化总推力`T≥0`及三轴力矩`τ3`。外环MPC**不是刚体12状态**：`x=(pbar-p,vbar-v,a_d,η)∈R12`，解耦三组4维`(p_tilde_i,v_tilde_i,a_{d,i},η_i)`，每轴优化`s_i`，虚拟加速度由动态滤波保证两次可微。几何非线性内环由`a_d`转换期望姿态/角速率并生成力矩；内环不是MPC。
- **MPC、约束与定理**：精确ZOH，3个线性动态/时变输入约束的凸非QP MPC，非二次Lyapunov终端代价；`ρ(t)=min(Tbar(t)-δ,Tmax-Tbar(t))`、`|a_{d,i}|≤ρ(t)/sqrt(3)`是非零/最大推力的保守充分内近似。Theorem 8要求`Δ(k+1)>exp(-h/γ)(1+h/γ)Δ(k)`以保持非空输入集；Theorem 10证明有条件外环UGAS；Theorem 11结合几何内环证明有条件级联UaGAS。**不是**本项目有噪失测SMF状态后验下的硬状态约束/递归安全证明。
- **量测/估计/丢包**：理论反馈依赖`p,v,R,ω`；§10.2高保真仿真包含电机、传感器噪声及状态估计，但正文未给可直接迁移的传感器逐项有界噪声/失测语言。无状态或参数SMF/CZ、无位置丢包/延迟自动机、无逐电机物理饱和与变化率的硬安全证明。具体IMU/GPS/Vicon传感器合同**未从公开正文确认**。
- **仿真/计算**：§10.1 MATLAB/CasADi `h=50ms,N=20`，三轴RMSE新`[0.26,0.07,1.75]m` vs基线`[0.48,0.14,2.43]m`；平均求解3.3ms vs0.25ms。§10.2 Avular Vertex One高保真**仿真非实飞**，`h=100ms,N=20,m=2.8kg,Tmax=80N`，新vs PID RMSE`[0.17,0.086,1.41]m` vs`[0.20,0.12,1.47]m`。未报告20ms最坏执行时间或真实飞行。
- **局限、可复用技术与创新边界**：可复用外环12维增广/三轴4维分解、时变推力内近似、精确ZOH及采样间隔约束审计；不能将其`s`虚拟输入等同本仓库`F(N),τ(Nm)`，需`F=mT`单位换算与内环误差合同。该文已有名义级联稳定性和时变推力约束贡献，本课题仍需有界间歇位置SMF/CZ＋共享因果输出反馈终端信息集合的独立证明。Run246/261负例与Run264有限桥不受该文定理直接覆盖。详细审计见 `docs/research/model_selection/background_run_20261102_1137_izadi2026_thrust_tv.md`。
- **待查问题**：下一轮全文核验真正四旋翼实飞低维/级联MPC的实际电机/力矩接口、传感器信息权限及执行误差边界。


---

## Run265 新增全文分节核验 — Quartullo等（2025，唯一去重第113篇）

- **题名、作者、正式书目**：Renato Quartullo, Gianni Bianchini, Andrea Garulli, Antonio Giannitrapani, *Robust Output Feedback Variable-Horizon MPC With Adaptive Terminal Constraints*, *IEEE Control Systems Letters* 9:883–888 (2025), DOI https://doi.org/10.1109/LCSYS.2025.3578491；作者公开PDF https://www3.diism.unisi.it/~giannibi/research/papers/ATCS_LCSS_2025.pdf 。2026-11-02实际阅读作者公开PDF pp.1–6，§II–IV、Algorithm 1、Theorems 1–2、式(1)–(26)；**公开作者稿全文已读，未逐式核对IEEE正式终版**。
- **研究问题/模型/输入**：离散LTI `x(k+1)=Ax(k)+Bu(k)+w(k)`，`y(k)=Cx(k)+n(k)`，有界凸过程/测量噪声；输出反馈可变时域Tube MPC在已知参考轨迹上有限时刻拦截目标。§IV六状态轨道交会`x=(p_3,v_3)`，输入`u=a_3`三轴虚拟加速度；**非四旋翼、无真实T/τ或旋翼分配**。
- **量测/估计/失测**：§IV每拍只测三维位置（噪声±0.01m），速度隐藏；固定增益Luenberger观测器，估计误差管束`S_tilde(k)`与控制偏差管束`S(k)`分离；**不是状态SMF/CZ后验逐次交集，不处理位置success/miss丢包**，不是参数SMF。假设`(A,B)`可稳定化、`(A,C)`可检测。
- **MPC/约束/理论**：状态/输入凸硬约束经Pontryagin差收紧；优化可变预测时域`N_k`、名义输入`v_k`、自适应**目标终端集合**`Z_f,k`。Assumption 1要求初始终端等式问题存在可行时域；Theorem 1在有界噪声与`bar_lambda>0`等条件下证明优化问题递归可行和代价下降；Theorem 2证明**有限时刻进入目标附近集合**，并非完成后无限时域终端信息RCI或鲁棒渐近稳定。无SMF/CZ状态后验、无四旋翼非线性物理约束。
- **实验/计算**：§IV HCW轨道交会仿真，采样11.7s、`N_k∈{1,...,30}`，Gurobi LP，100组Monte Carlo，平均求解约0.5s，平均最终距离约0.04m；仅数值仿真，无四旋翼/无人机实飞，**不能证明20ms WCET**。
- **局限/可复用技术**：可复用式(5),(10),(11)的误差外包、双管束收紧与式(15),(23)的移位候选/终端目标集合扩张思路。论文假设每拍输出、LTI和直接加速度输入，无法直接迁移本仓库间歇有噪位置、Euler`tau→v`三拍时滞、物理T/τ约束。§V将SMF和非线性系统作为未来扩展。其已有的输出反馈自适应终端贡献限制本课题创新宣称。
- **与Run265关联、阅读日期、待查问题**：2026-11-02；Run265在冻结四状态真值下证明零姿态零角速切片的三拍绝对速度必要带`|v|<=2.8785745575`，而非可移位终端RCI。下一步：是否存在覆盖Run260第60拍所有合法有噪后验、具有绝对状态/姿态关联且共享因果反馈可回返的非空信息集合？详见`docs/research/run265_research_log.md`。

---

## 背景第18轮：Borbolla-Burillo等四旋翼实飞级联LMPC与执行器混控（2026-11-02）

- **真实题名/书目**：Patricio Borbolla-Burillo; David Sotelo; Michael Frye; Luis E. Garza-Castañón; Luis Juárez-Moreno; Carlos Sotelo. *Design and Real-Time Implementation of a Cascaded Model Predictive Control Architecture for Unmanned Aerial Vehicles*. *Mathematics* **12**(5):739, pp.1–20 (2024-02-29). DOI https://doi.org/10.3390/math12050739；出版社PDF https://www.mdpi.com/2227-7390/12/5/739/pdf；实际阅读开放20页全文 https://www.researchgate.net/publication/378669203_Design_and_Real-Time_Implementation_of_a_Cascaded_Model_Predictive_Control_Architecture_for_Unmanned_Aerial_Vehicles。
- **阅读日期/状态/范围**：2026-11-02，**开放全文§1–6已读（pp.1–20）**，重点pp.3–8式(1)–(38)、pp.8–11式(39)–(55)、pp.11–18表2/4及§5.2实飞。出版社网页本轮429，未逐页核对期刊服务器PDF，不冒称独立复现。
- **问题/物理模型**：Quanser QDrone 2真实四旋翼三维轨迹跟踪与风扰悬停；完整6自由度非线性刚体物理模型包含位置3/速度3/姿态3/角速3共12状态坐标、四桨推力f_i=kω_i²；在线MPC为悬停小角度线性化分块：高度(z,ż)2状态、XY(x,ẋ,y,ẏ)4状态、姿态(φ,φdot,θ,θdot,ψ,ψdot)6状态，**不是一个全耦合12状态优化**。
- **控制输入/执行器**：高度MPC优化总推力U1；XY MPC优化虚拟期望俯仰/滚转(θ_d,φ_d)并后饱和±45°；姿态MPC优化力矩U2,U3,U4；式(55)4×4混控→PWM→电池电压下降补偿→4电机。质量1.5kg，每电机最大标称8.5N；未给每电机饱和/变化率的预测内联合硬约束与有界混控误差。
- **量测/估计/噪声/失测**：OptiTrack Flex13动捕120Hz位置、IMU姿态/角状态，MPC用位置、速度、角度、角速度反馈；速度误差/滤波器的可复现有界集合**未从全文确认**。没有有界位置失测自动机、状态或参数SMF/CZ；35s一次通信异常仅实验观察。
- **MPC/理论**：离散LTI二次跟踪+输入代价，式(52),(54)闭式无显式预测硬约束优化；外部姿态角饱和。高度N10/Ts0.25s、XY N10/Ts0.05s、姿态N15/Ts0.025s；没有可确认终端RPI、递归可行性/鲁棒稳定性定理、20ms WCET；求解器名称/最坏求解耗时**未报告**。
- **实验/结论**：QDrone 2实飞螺旋、8字轨迹、风机扰动，PIV基线；轨迹RMSE螺旋MPC0.17/PIV0.495、8字0.095/0.315；风机177km/h额定、3m远，PIV/MPC扰动时长不同，不能解释为同一最坏扰动。属于实验经验改善，非数学硬安全保证。
- **局限/关联/可复用技术**：可复用2+4+6分层线性化、混控矩阵/电池补偿作为**物理执行链审计样例**；但其动捕每拍信息、虚拟姿态输入、后饱和及未证明终端集合，不能直接迁移仓库有噪间歇位置SMF+物理T/τ的安全证明。Run246/261/265必要条件不受该实飞结果消除。详细见 `docs/research/model_selection/background_run_20261102_1236_borbolla_qdrone2.md`。
- **待查问题**：Bicego等的NMPC是否在优化中直接处理单向旋翼推力/推力变化率，四旋翼实飞与多旋翼对照的物理约束证据强度如何？


---

## 背景第20轮：Xu等(2023)四旋翼12维snap-LMPC与后置加权分配（去重新增第116篇）

- **书目/原始来源**：Zhixiong Xu; Li Fan; Wei Qiu; Guangwei Wen; Yunhan He (2023), *A Robust Disturbance-Rejection Controller Using Model Predictive Control for Quadrotor UAV in Tracking Aggressive Trajectory*, *Drones* 7(9):557, DOI https://doi.org/10.3390/drones7090557。出版社正式页面 https://www.mdpi.com/2504-446X/7/9/557 ，开放21页全文的ResearchGate镜像 https://www.researchgate.net/publication/373536445_A_Robust_Disturbance-Rejection_Controller_Using_Model_Predictive_Control_for_Quadrotor_UAV_in_Tracking_Aggressive_Trajectory 。出版日2023-08-29；2026-11-02核验。**状态：公开正文分节已读，非期刊PDF逐页精校**；实际阅读pp.3–20，重点§2式(1)–(7)、§3.1式(8)–(21)、§3.2–3.3、§3.4式(43)、§4表1/2/6/7与§5；附图细节和期刊最终PDF排版未逐页复核。
- **问题/数学模型**：标准单向固定桨四旋翼，完整物理动力学为6自由度、位置/惯性速度3+3、SO(3)姿态3自由度、机体角速度3，共12个局部刚体坐标；**在线外环LMPC的12维状态不是刚体状态**，而是`x=[p_x,p_y,p_z,v_x,v_y,v_z,a_x,a_y,a_z,j_x,j_y,j_z]^T`，输出`y=p_3`，输入`u=s_3`为三轴snap（位置四阶导数）；§3.1式(9)–(10)为四阶积分链的离散LTI/ZOH形式。外环虚拟snap不是电机输入。§2式(1)–(7)采用单桨`f_i=k_f omega_i²`、`n_i=k_n omega_i²`及旋翼响应模型，固定臂长`l`；内环使用SO(3)几何姿态控制，基于差分平坦性由`a_d,j_d,s_d`映射期望姿态/角速/角加速度。不是平面六状态模型，也未把真实内环跟踪误差作为鲁棒外环约束。
- **输入与真实执行器**：§2式(3)–(4)给`w=[tau_x,tau_y,tau_z,T]^T=D q`，`q=(omega_1²,...,omega_4²)`，矩阵行依次`[0,k_f l,0,-k_f l]`、`[-k_f l,0,k_f l,0]`、`[-k_n,k_n,-k_n,k_n]`、`[k_f,k_f,k_f,k_f]`。§3.4式(43)在外环与姿态内环之后解**独立的**加权最小二乘分配`min_q (w_d-Dq)^T Q(w_d-Dq)`，约束`q_min<=q<=q_max`，再转PWM；**允许分配残差非零**，不能从`q`满足盒约束推出期望`w_d`被精确实现。式(43)没有`q_k-q_{k-1}`逐桨速率约束。外环§3.1式(16)–(21)由电机转速/响应近似导出加速度与snap界，但假定单步姿态不变，作者明确承认极端工况仍可能转速饱和。
- **量测/估计**：§4全部MATLAB仿真，§4.2.4表6在状态上人工叠加观测误差：位置0.05m、速度0.05m/s、加速度0.03m/s²、姿态0.02rad、角速0.01rad/s。**没有可核验真实IMU/Vicon/GPS平台或实飞**；无间歇位置丢包、无隐藏速度SMF/CZ集合、无状态或参数集合估计。位置输出`y=p`是外环数学模型定义，仿真控制器还使用速度/加速度/jerk状态；不能把`y=p`误读为“仅位置传感器即可实现输出反馈”。
- **MPC/优化/理论**：§3.1式(15),(21)线性MPC QP，代价为位置参考误差及snap输入变化，预测域`N=50`、外环20Hz（`T_s=0.05s`）、内环200Hz；MATLAB+OSQP，i7-12700H/16GB笔记本平均求解约4ms。外环显式加速度和snap界；终端鲁棒不变集、鲁棒状态收紧、无限时域递归可行性、求解WCET **未报告/无法从所读正文确认**。§3.2作者给出姿态控制的Lyapunov稳定性分析，但其结论不能直接升级为**含饱和、外环QP、后置分配残差、失测**的全系统硬安全证明；SO(3)全局姿态收敛表述也须与拓扑/初值假设区分。
- **结果/证据级别**：§4仿真激进轨迹、Bernoulli 8字、翻转和噪声/外扰；对比PID+前馈、MPC+PID；§4.2.4在9–11秒施加三轴恒定外力(2.5,2,1.5)N，表7给位置MSE，报告位置环重规划时间<0.01s。**仅仿真改善**，无真实四旋翼飞行、无统计硬约束零违约或20ms最坏耗时证书。论文参数m=0.98kg、J=diag(0.00264,0.00264,0.00496)kg·m²，不可覆盖仓库1kg/J=0.02配置。
- **局限、可复用与创新边界**：可复用`D`混控矩阵、外环snap约束和“后置分配残差”的反例接口；不复用其LMPC名义约束作为SMF+Tube MPC硬安全证书。**新研究必须区别于**已知级联LMPC、差分平坦、加权分配及Bicego(2020)逐桨推力速率NMPC，集中验证间歇位置可靠后验、共同可实现输入、因果安全终端。背景第20轮矩阵/日志含严格的对称四桨`(T,tau_y)`可实现性代数推导；该推导是本轮研究者在论文式(3)基础上的推论，**不是论文定理**。
- **待查问题/下一轮**：对给定四桨上一拍推力集合、每桨推力上限及正负变化率，能否形成包含跟踪误差的`(T,tau_y)`共同可实现域并传给主任务检验？缺失实际`l,f_{max},\dot f`和误差辨识，不能给数值安全认证。

---

## 背景第21轮：Jacquet等(2020)四旋翼逐桨动态约束感知NMPC（2026-11-02，去重新增）

- **真实书目与原文**：Martin Jacquet; Gianluca Corsini; Davide Bicego; Antonio Franchi, *Perception-constrained and Motor-level Nonlinear MPC for both Underactuated and Tilted-propeller UAVs*, *2020 IEEE International Conference on Robotics and Automation (ICRA)*, pp.4301–4306, article 9197281, DOI https://doi.org/10.1109/ICRA40945.2020.9197281；研究机构公开6页会议正文 https://aerial-core.eu/wp-content/uploads/2021/01/Perception-constrained-and-Motor-level-Nonlinear-MPC-for-both-Underactuated-and-Tilted-propeller-UAVs.pdf；书目交叉核验 https://research.utwente.nl/en/publications/perception-constrained-and-motor-level-nonlinear-mpc-for-both-und/ 。**2026-11-02实际阅读公开PDF会议印刷页4301–4306（全文）**：§I–II式(1)–(11)，§III式(12)–(15)、Fig.3，§IV Fig.4–7及§V；未复现实验或逐页对照其他出版社版本。
- **控制任务与架构**：标准欠驱动四旋翼与倾斜旋翼六旋翼的轨迹跟踪、移动特征视场保持；NMPC直接在电机力矩等效层优化，**不是级联外环虚拟加速度+姿态跟踪器**。真实四旋翼实飞存在，但§IV-C明确实飞感知传感器**仍用模拟相机**，不能记成真实视觉感知闭环实飞。
- **状态、维数与物理模型**：式(1)–(4)刚体局部12维状态 $x_b=(p_3,v_3,\eta_3,\omega_3)$，其中Euler姿态 $\eta=(\phi,\theta,\psi)$、角速度为机体系；逐桨推力 $\gamma=(f_1,...,f_n)$ 是n维执行器状态，$\dot\gamma=u\in\mathbb R^n$ 为等效电机力矩输入（通过状态相关坐标变换）；完整优化状态另含P个视场余弦 $c_{\beta_i}$，总维数 $12+n+P$，四旋翼为 $16+P$。§II式(5)–(7)连续非线性刚体与混控 $G\gamma$；§III离散多重射击数值积分。四旋翼6物理自由度，**16+P状态不是16+P自由度**。具体机体质量、惯量、桨臂长、采样步长和预测节点N的数值**未从所读正文确认**。
- **输入、真实约束与物理权限**：§II-B式(8)逐桨 $\underline\gamma\le\gamma\le\bar\gamma$；式(9)状态相关的 $\underline{\dot\gamma}(\gamma)\le u\le\overline{\dot\gamma}(\gamma)$，界可由电机辨识取得。标准四旋翼 $\mathrm{rank}(G)=4$，倾桨平台可为5/6，不能混为同一执行权限。§III式(14e–g)把逐桨推力、推力速率和视场 $\cos\alpha\le c_\beta$ 直接放入预测优化；不是后置饱和/加权分配。
- **量测、估计与不确定性**：§III Fig.3为状态传感器/逐桨转速测量/特征检测预测器架构；§IV-A说明实飞地面笔记本、USB连接，论文未给可重现的IMU/GPS/Vicon逐项型号、状态噪声集合或隐藏速度状态SMF。§IV-B模拟相机60Hz、特征预测会用过时读数；§IV-C真实飞行**模拟相机**，并非真实视觉遮挡/丢包验证。无有界位置success/miss自动机、SMF/CZ状态集合或参数集合估计；特征预测器举例Kalman，但不等于集合滤波。
- **MPC/理论**：§III式(14)输出参考误差加权二次代价，非线性预测、逐桨硬幅值/速率与视场约束；MATMPC、固定步长Runge–Kutta、RTI单次线性化、qpOASES；实验计算在Intel i7-8850H/Ubuntu 16.04地面笔记本。§IV-C报告实际控制/求解频率150–400Hz，随约束复杂度变化；**未报告可独立确认的20ms最坏求解时延、N数值、终端代价/终端不变集合、鲁棒递归可行性或SMF输出反馈稳定性证明**。RTI约束名义满足的作者描述不能升级为不确定性下真实硬安全定理。
- **实验与局限**：§IV-B Simulink仿真：移动标记跟踪、四旋翼和倾桨六旋翼的感知悬停比较；§IV-C四旋翼真实飞行展示位置/视场指标与求解时间，安全考虑下动作不激进，且没有真实相机闭环；**未从全文确认可直接比较的RMSE统计、最坏约束违约率、SITL/HIL或公开复现代码版本**。没有位置丢包、SMF/CZ、终端信息不变集和鲁棒硬安全证书。
- **对本课题的可复用与创新边界**：这是标准四旋翼逐桨状态与速率**在MPC内部**约束的直接实飞先例；不能声称首次把电机动态或感知约束放入四旋翼MPC。与Bicego(2020)相互印证：需要上一拍逐桨推力状态/可靠集合，才能定义下一拍共同可实现的 $(T,\tau)$。与Run268的测量条带结合仍是**待验证的接口**，不是该论文已解决。下一轮唯一待查：获得实测逐桨速率和误差界后，主任务能否在全部第60拍非空观测纤维上认证非空共同可实现输入域？见背景第21轮日志。


---

## Run269 — 既有Köhler/Müller/Allgöwer (2021) 论文正文复核（2026-11-02；DOI/arXiv去重数不变）

- **题名、作者、版本**：Johannes Köhler; Matthias A. Müller; Frank Allgöwer, *Robust output feedback model predictive control using online estimation bounds* (2021), arXiv:2105.03427, https://arxiv.org/abs/2105.03427 ；作者公开正文 https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf 。本轮**分节重读**§II Assumption 1/Definitions 1–4、§III-C Theorem 2、§IV-B Assumption 7/Theorem 4、§IV-C Assumption 9/Theorem 5、§V十状态四旋翼数值案例；不是新读去重篇目，未逐式核对附录或其他终版。DOI：未从所读作者稿确认独立期刊DOI。
- **问题、实际模型/控制**：非线性有界扰动、有噪输出的鲁棒输出反馈MPC；§V四旋翼**10状态**`(z1,z2,z3,phi1,phi2,v1,v2,v3,omega1,omega2)`，三输入`(u1,u2,u3)`为虚拟姿态/竖直推力命令，Euler离散`h=0.05s`；不包含偏航或逐电机动态。量测5维位置和角度，每拍可得但带噪；**无每5拍位置机会或丢包自动机**，非真实四旋翼实飞。
- **估计、MPC与约束**：在线误差界可来自δ-IOSS、SMF非否证集合或MHE；homothetic Tube MPC对预测估计误差和跟踪误差分别收紧硬状态/输入约束。§V给位置、倾角、虚拟输入限制；离线LMI/SeDuMi、在线CasADi/数值求解；20ms最坏时延、逐桨推力/速率、丢包鲁棒终端均未报告或未证实。
- **定理/证据边界**：Theorem 2依赖Assumptions 1,3和初始可靠估计界；Theorems 4/5另依赖δ-IOSS、δ-ISS CLF、终端Assumptions 7/9和初始优化可行，给出其特定系统下递归可行与硬约束。§V仅10状态四旋翼仿真，不等于本项目冻结四状态失测安全、六状态物理安全或20ms WCET。Run269独立不可区分性证明显示，位置包连续miss时估计后验有不可消除的速度投影宽度；这一结论**不是论文定理**。
- **可复用技术、局限、待查**：估计误差/名义跟踪误差双层管束、预测误差界单调性与终端移位条件可作为候选证明结构。必须为实际位置丢包和力矩时滞建立新的可靠界；下一步检验第60拍位置成功后双状态纤维的读数条件化后继，不能仅以在线误差缩小宣称终端RCI。工件：`docs/research/run269_research_log.md`。


---

## 背景第22轮 — Wehbeh & Sharf (2024) 双向桨四旋翼scenario MPC与执行器参数边界（2026-11-02；新增去重论文）

- **书目/链接**：Jad Wehbeh, Inna Sharf, *Nonlinear scenario-based model predictive control for quadrotors with bidirectional thrust*, *International Journal of Robust and Nonlinear Control* **34**(18):12450–12475 (2024，2024-09-18在线), DOI https://doi.org/10.1002/rnc.7627；出版社开放HTML全文（按DOI可达）。独立arXiv版本：**未确认**。
- **阅读日期/范围/状态**：2026-11-02，出版社开放HTML §2.1–2.4、§3.1/场景QP、§4.3、§5.1–5.2、§6.1–6.3表1–5、§7；**正文分节已读**，附录1/2和Jothiraj(2020)原始桨电机实验数据未独立逐式核验。
- **任务/模型/自由度**：双向桨四旋翼悬停恢复和半翻滚；6自由度刚体，连续Newton–Euler状态 `(r_a3,v_a3,C_ab∈SO(3),ω_b3)`，局部12独立状态（姿态矩阵9元素≠9自由度）。§2.3在当前估计状态/输入附近对SO(3)小姿态误差线性化，零阶保持离散；不是4状态平面或16状态电机增广模型。
- **输入/执行器**：`u=(T1,T2,T3,T4)`为四桨**带符号**推力，式(5)映射总推力/三轴力矩；§2.2独立电机、正负对称、推力相关非线性速率约束，迭代线性化后进入QP。表2仿真`m=1kg,Tmax=7N/桨,t_ramp=0.2s,c=0.166m,J=(0.0122,0.0126,0.0239)kg·m²`；模型引用T-Motor Air 2213/920KV＋APC-3D 9×4.5对称桨的曲线拟合。**不是本仓库标准单向桨的可靠瞬时速率或ESC误差界**；平均斜率35N/s不能代替状态依赖速率。
- **量测/不确定性**：§5模拟陀螺/加速度计200Hz、GPS/磁力计10Hz，MEKF 200Hz融合，估计位置、速度、姿态和角速度；概率协方差与质量/惯量分布抽样，不是SMF/CZ。§3.1明确未补偿环境扰动；没有本仓库每5拍位置机会/最多连丢2包的有界输出合同。
- **MPC/理论**：det.MPC、scenario MPC、APSMPC/MDSMPC；局部线性化预测、二次输出跟踪与输入成本、终端**输出二次代价**，非已证终端不变集。表3控制50Hz、预测网格40ms、`N_p=8`、最大迭代5。逐桨非线性速率限制采用QP近似；QP求解器具体名称、硬状态约束鲁棒递归可行性/稳定性定理**未从所读正文确认**。
- **结果/证据级别**：MATLAB R2020a/i9-9900K仿真，悬停/半翻滚每任务每算法200次；表4悬停最大平均步成本det.MPC 7.39、MDSMPC(M=200) 3.67，仅统计成本不是零违约证明。§6.1相对QP**构建**耗时不含求解，N=8/M=200完整SMPC约195.7×、MDSMPC约23.1×det.MPC；未报告本课题20ms端到端WCET。无已核验实飞、HIL/SITL或有界噪声硬安全证书。
- **局限/可复用/创新性**：双向桨可负推力且过零动态特殊，不能把7N/0.2s当普通单向桨硬件参数。可复用电机动态辨识与约束线性化审计方法；不是SMF/CZ状态集合＋Tube MPC或终端信息RCI先例。独立Fraction对照仅在**假设**`l=0.166m,0≤f_i≤7N`时认证仓库`T∈[4.905,14.715]N,|τ|≤0.08Nm`的静态幅值极值`[65423/66400,260269/66400]N`；不是论文定理或真实执行器速率/误差/共享因果输入证书。
- **待查**：标准单向四旋翼ESC/桨的实际瞬时上升下降速率与误差界、真实桨臂及上一拍桨力可靠集合，随后才能评估共同`(T,τ)`域。独立日志：`docs/research/model_selection/background_run_20261102_1637_wehbeh_motor_identification.md`。

---

## 背景第23轮 — Didier等(2021) 四旋翼RAMPC实飞，参数SMF≠隐藏状态SMF（2026-11-02；新增去重）
- **书目**：Alexandre Didier, Anilkumar Parsi, Jeremy Coulson, Roy S. Smith, *Robust Adaptive Model Predictive Control of Quadrotors*, *2021 European Control Conference (ECC)*；DOI https://doi.org/10.23919/ECC54610.2021.9654893；作者稿 arXiv:2102.13544v3 https://arxiv.org/pdf/2102.13544；ETH开放档案 https://www.research-collection.ethz.ch/entities/publication/298c0646-9127-4e1a-9dbe-2601e9279ad0。IEEE最终页码**未确认**。
- **阅读状态/日期**：2026-11-02，**公开作者6页PDF全文p.1–6已读**，§II(1)–(12)、§III(13)–(14)、§IV、§V；未对照IEEE终版、未复现实验。
- **研究问题/实际状态输入**：四旋翼未知质量与共同旋翼效率下降时的鲁棒自适应约束控制。直接悬停线性化12状态`(Δp3,Δv3,ΔEuler3,Δ角速度3)`＋4个逐桨推力偏差输入；仅仿真。**真实27g Crazyflie实飞为2状态高度`(Δp_z,Δv_z)`、1输入总推力偏差的RAMPC**，x/y/偏航由LQR，姿态内环PID；物理四旋翼仍6DOF。仿真Euler离散0.1s，实飞MPC更新率/预测N未确认。
- **量测与不确定性**：实飞IMU加速度/陀螺、Vicon六相机200Hz，地面计算；未知质量倒数/旋翼效率是**参数SMF**，式(12)为有界噪声下参数非否证集膨胀，**没有隐藏速度状态SMF/CZ**、间歇位置包、延迟观测。
- **MPC结构/约束/理论**：线性仿射参数不确定、homothetic Tube RAMPC、二次阶段/终端代价、式(11g–i)管束包含与终端约束，仿真逐桨0–0.16N、位置±0.7m、姿态±π/2；递归可行/约束保证依赖有界扰动、λ收缩、初始可行及前作条件。**§II-D为性能在线更新悬停稳态输入，作者明确指出牺牲该部分鲁棒保证**。实飞OSQP求解小于5ms（非20ms全链路WCET），未核验逐桨变化率、ESC误差或实飞终端RCI。
- **结果/局限/可复用/待查**：仿真直接12状态RAMPC，真实飞行仅高度2状态；真实30%共同旋翼效率削减后恢复，未实飞施加风，未给本项目无限时域硬安全。可复用参数集合更新、收紧、低维级联工程证据；不能把参数SMF替代有噪间歇位置状态SMF。待查：严格稳态输入误差包络是否会使六状态物理候选输入域为空？对应日志 `docs/research/model_selection/background_run_20261102_1747_didier_eschmann_actuator_gap.md`。

## 背景第23轮 — Eschmann等(2024) 单向四旋翼电机动态辨识（非MPC论文；新增去重）
- **书目**：Jonas Eschmann, Dario Albani, Giuseppe Loianno, *Data-Driven System Identification of Quadrotors Subject to Motor Delays*, *2024 IEEE/RSJ IROS*, pp.8095–8102，DOI https://doi.org/10.1109/IROS58592.2024.10801441；作者稿 arXiv:2404.07837v2 https://arxiv.org/pdf/2404.07837；代码 https://github.com/arplaboratory/data-driven-system-identification。
- **阅读状态/日期**：2026-11-02，**公开作者8页PDF全文p.1–8已读**，§III式(1)–(16)、§IV/图表；未逐页核对IEEE终版，未运行开源代码。
- **问题/模型/输入/量测**：标准四旋翼6DOF、位置/速度/四元数/机体系角速、逐桨真实RPM状态，目标RPM为输入；`dot ω_m=(ω_sp−ω_m)/T_m`、二次推力曲线`f_i=Σ_{j=0}^2K_{f,ij}ω_{m,i}^j`。IMU加速度、陀螺、电机命令、已知质量与桨臂；MAP/最小二乘辨识**参数**，非状态SMF/CZ。
- **证据**：真实27g Crazyflie 2.1辨识标称`T_m=0.072s`，3.35kg四旋翼标称`T_m=0.065s`，约一分钟飞行日志，公开复现工具；真实户外控制演示是RL，**不是MPC**。未报告可移植到本仓库1kg平台的确定性逐桨上升/下降速率、时间常数置信外包、ESC误差最坏界或硬安全定理。
- **可复用/局限/待查**：可作为辨识真实`T_m,K_f`的原始方法，不能把标称时间常数当`r_i^±`或把RPM一阶响应当推力一阶响应。20ms名义离散时转速指令差每拍缩小`1−exp(−0.02/T_m)≈0.242535/0.264859`，仅为独立模型推算。待查：开源日志是否足以构造**确定性**辨识残差和可靠`U_common`输入域？对应背景第23轮日志。



---

## 背景第25轮 — Bouffard/Aswani/Tomlin(2012) 机载四旋翼LBMPC：上层虚拟输入与低层ESC执行权限（2026-11-02；新增去重）

- **真实书目**：Patrick Bouffard; Anil Aswani; Claire Tomlin, *Learning-Based Model Predictive Control on a Quadrotor: Onboard Implementation and Experimental Results*, *2012 IEEE International Conference on Robotics and Automation (ICRA)*, pp.279–284, DOI https://doi.org/10.1109/ICRA.2012.6225035；作者公开PDF https://aswani.ieor.berkeley.edu/papers/icra_lbmpc_2012.pdf 。arXiv独立编号**未确认**。同作者2012技术报告 *On-board Model Predictive Control of a Quadrotor Helicopter* 为**不同文献**，本条不冒充其已读。
- **实际阅读日期/状态**：2026-11-02；作者公开6页PDF **正文分节已读**，§III模型(1)–(3)、§IV估计与QP(4)–(8)、§V硬件、§VI实飞A–D、§VII结论；双栏文本提取中数值矩阵排版不完整，**未逐式核对完整数值矩阵、未复现代码、未逐页比对IEEE终版**。
- **研究问题/真实模型与假设**：1.3kg健康单向四旋翼真实机载学习型MPC轨迹/悬停与接球；物理平台6自由度。控制器使用偏航固定、水平两轴解耦、姿态内环经验二阶响应的**10状态**离散仿射模型 `x=(x_N, vx_N, θ, θdot, x_E, vx_E, φ, φdot, x_D, vx_D)`；`A∈R10×10,B∈R10×3`，25ms离散。小范围悬停近似/固定偏航；非全6DOF刚体统一MPC，未建逐桨RPM或电机推力状态。质量、姿态内环模型由实验获得；电机具体物理参数/桨臂/逐桨推力系数**未从全文确认**。
- **控制输入与执行器**：MPC的3个输入是**虚拟** `u=(θ_s,φ_s,T_s)`（期望俯仰、横滚、总推力命令），不是四桨转速、逐桨推力或推力变化率；施加首项 `u_m=K xhat_m+c_m^*`。AscTec专有飞控底层1kHz闭环姿态、开环推力，40Hz串口上层命令。逐桨混控、ESC命令后饱和、变化率、执行误差及其确定性界**未报告/无法从全文确认**；不能由`u∈U`推出实际逐桨硬安全。
- **传感器/估计/不确定性**：Vicon MX 120Hz位姿，`y=(x_N,θ,x_E,φ,x_D)+ε`，`C∈R5×10`，速度与角速由改进EKF估计；同时学习12维动态修正参数，使用协方差/参数截断。噪声为有界随机量；没有确定性有噪位置success/miss自动机、状态SMF/CZ可靠后验、延迟位置观测或传感器故障恢复证明。**EKF联合状态与参数估计不等于集员状态滤波**。
- **MPC实现/约束**：Learning-Based MPC；名义模型 `F_N` 管约束，学习oracle `F_O` 改善代价，凸QP二次阶段/终端代价、`X,U`多面体、`X⊖D`扰动收紧、近似最大允许扰动不变集 `ω`，LSSOL求解；`N=15`、40Hz，即25ms采样、0.375s预测域；板载Intel Atom N270 1.6GHz、ROS/C++＋FORTRAN QP。具体状态/输入盒数值、终端`ω`多面体参数、单次求解最坏时间和20ms WCET**未从所读全文确认**。该终端集合不是有丢包模式/后验集合的终端信息RCI。
- **理论/仿真/实飞证据边界**：论文引用LBMPC先前理论，使用名义约束和扰动集合；本篇**未证明本仓库位置丢包、隐藏速度、执行器误差下递归硬安全**。真实四旋翼实验：近地有效推力增益约6%；一组水平阶跃超调相对线性MPC减少62%；恶意错误学习时高度显著下降但未触地，QP保持可行；人工抛球接球作者报告>90%但未做可控重复实验。以上是**实验观察**，不能写成严格零违约或全扰动保证。无已核验HIL/SITL、GPS失测试验、完整开源复现工件。
- **可复用技术/局限/与课题关联**：可借鉴名义约束与学习性能模型分离、扰动集合收紧、低算力QP与内外环架构；但真实底层执行器/混控和内环误差缺少可靠集合合同，不能直接移植到六状态平面 `(T,τ)` 或SMF/CZ终端。**已有四旋翼输出反馈、在线模型学习、约束MPC真实机载先例**，创新性不能凭这些关键词声称首次。待查：专有飞控/开源替代是否公开最终逐桨命令和饱和/速率/ESC误差；如何在同一间歇位置观测纤维下定义可执行`(T,τ)`共同域。详细日志 `docs/research/model_selection/background_run_20261102_1936_bouffard2012_virtual_interface.md`。

---

## 背景第33轮 — Alexis/Nikolakopoulos/Tzes (2012) 六自由度四旋翼12状态PWA切换MPC实飞核验（2026-11-03 UTC）

- **书目与原始全文**：Kostas Alexis, George Nikolakopoulos, Anthony Tzes, *Model predictive quadrotor control: attitude, altitude and position experimental studies*, *IET Control Theory & Applications* **6**(12):1812–1827 (2012), DOI https://doi.org/10.1049/iet-cta.2011.0348。开放全文PDF：https://www.diva-portal.org/smash/get/diva2%3A980101/FULLTEXT01.pdf 。DiVA记录：https://ltu.diva-portal.org/smash/record.jsf?pid=diva2%3A980101 。
- **阅读范围**：2026-11-03；开放16页PDF正文§1–6、式(1)–(27)、表1–3、主要飞行结果与结论已分节阅读；未运行作者代码或复现实验。状态：原始期刊公开全文正文分节已读。
- **控制任务与真实物理模型**：室内位置保持、水平轨迹跟踪、悬停、姿态机动和强制风阵；真实6物理自由度。式(3)的12状态plant为 X=(φ,φdot,θ,θdot,ψ,ψdot,z,zdot,x,xdot,y,ydot)，即三轴位置/速度与三轴Euler角/Euler角速度。刚体对称、重心与机体坐标原点重合，桨推力和阻力矩与转速平方成比例；地固系位置/速度，姿态运动学另用式(1)将Euler角速映射为机体系p,q,r。模型包含转子陀螺项 J_r Ω_r 和加性扰动；小速度假设用于姿态/平移动力学解耦。
- **与本课题状态定义的区别**：原文用Euler角速度；本课题拟用 x=(p_I[3],v_I[3],η_ZYX[3],ω_B[3])，其中ω_B为机体系角速度。两者物理自由度相同，但坐标不同；必须保留 dot(η)=E(η)ω_B，不能把ω_B直接当Euler角速度。
- **实际控制输入与电机权限**：式(4)定义 U=(U1,U2,U3,U4,Ω_r)，U1总推力，U2/U3滚转/俯仰力矩通道，U4偏航力矩通道，Ω_r为四个旋翼转速的残余组合量；它由四个物理电机转速Ω1…Ω4计算，不是第五个独立电机。U1=bΣΩ_i²，U2=b(−Ω2²+Ω4²)，U3=b(Ω1²−Ω3²)，U4=d(−Ω1²+Ω2²−Ω3²+Ω4²)，Ω_r=−Ω1+Ω2−Ω3+Ω4。姿态MPC输入包含(δU1,δU2,δU3,δU4,δΩ_r)，高度MPC输入δU1，水平位置MPC使用虚拟量(ux,uy)。论文给各分量输入区间和变化率约束；本轮未找到五维派生输入完整保留四个非负电机转速共同生成关系的精确联合可行集表达。
- **MPC结构与线性化**：作者称 Switching MPC（SMPC，此处是switching MPC，不是stochastic MPC）。12状态非线性plant拆成姿态、垂直高度、水平平移三个PWA离散子系统：姿态10维积分增广、9个PWA工作区；高度3状态、2个PWA工作区；水平位置6状态线性模型。工作点按估计状态与线性化点距离切换；不是统一12状态LTI MPC，也不是Tube MPC。代价含跟踪误差、控制增量和输入偏差二次项；状态、输入、控制变化率为多面体约束；风阵影响作为加性扰动界。
- **采样和参数**：Np=5、Nc=2；姿态采样0.0083s（120Hz），高度/水平采样0.03s（约33Hz）。原型m=1.1kg，臂长0.21m，Jxx=Jyy=0.0196、Jzz=0.0264 kg·m²，J_r=8.5×10⁻⁴ kg·m²，b=9.29×10⁻⁵、d=1.1×10⁻⁶。输入约束U1∈[0,36.63]、|U2|≤18.319、|U3|≤18.319、|U4|≤0.22；控制变化率限制为各通道最大值的±40%。未报告每次QP最坏求解时间、统一终端不变集或Tube终端集合。
- **传感器与估计**：Xsens MTi-G IMU、Maxbotix EZ1 sonar、Tam2 16×16 optic-flow视觉芯片；采用EKF/坐标修正EKF融合。无GPS和外部定位相机，室内定位由sonar+optic flow实现。没有位置success/miss自动机、最长连续失测合同或SMF/CZ状态集合；扰动状态估计也是EKF。
- **理论与实验边界**：论文明确指出，多个PWA局部控制器切换不能保证原非线性系统在切换过程中的稳定性，只报告试验中未观察到稳定性问题。真实UPATcopter约1.1kg，Atom Z530 1.6GHz/2GB板载计算；实飞包括位置保持、轨迹、悬停、风阵和激进姿态。作者报告水平位置保持通常在半径0.15m以内；悬停姿态MSE在无风/风阵下分别约为φ:1.5924e−4/0.0013、θ:2.2372e−4/5.0558e−4、ψ:4.3998e−4/0.0011。属于实飞观察，不是确定性硬安全、递归可行或稳定性定理。
- **对本课题的意义**：该期刊实飞论文直接证明12状态六自由度四旋翼plant与MPC有真实研究先例，支持将12状态非线性plant用于硕士仿真主对象；但其控制架构是三个PWA切换MPC，不支持单个12状态局部线性Tube MPC已被实飞验证。论文没有SMF/CZ、位置间歇测量或终端信息RCI。
- **待查问题**：标准单向四旋翼上，四个电机推力f映射到wrench w=(T,τx,τy,τz)时，应使用耦合可行集 W={Gf | f_min≤f≤f_max}，而不是四个互不相关的wrench区间。若G可逆，可施加 f_min≤G^{-1}w≤f_max；若优化逐桨推力，则四输入直接受电机盒约束。下一轮优先推导本课题12状态Euler/body-rate悬停线性化A、B和有限姿态包线内的非线性离散残差集合。

---

## 背景第34轮新增论文 — Parsi/Iannelli/Smith (2022 online; 2025 issue) 椭球Tube MPC四旋翼算例

- **书目信息/原始全文**：Anilkumar Parsi, Andrea Iannelli, Roy S. Smith, *Scalable tube model predictive control of uncertain linear systems using ellipsoidal sets*, *International Journal of Robust and Nonlinear Control*, **35(7), 2499–2520 (2025 issue)**；first published online **21 November 2022**；DOI https://doi.org/10.1002/rnc.6485 。作者公开PDF https://andreaian.github.io/pub/IJRNC22_RMPC.pdf ，出版社全文 https://onlinelibrary.wiley.com/doi/10.1002/rnc.6485 。**2026-11-03实际阅读范围**：PDF/出版社全文§2问题建模、§3.1状态管束与控制参数化、§3.4终端设计相关部分、§4.1 Theorem 1、§5.2 Quadrotor example、Appendix A.4 Proposition 6证明；**部分阅读，不声称全篇逐式读完**。
- **控制任务/物理模型/状态输入**：Crazyflie悬停附近位置设定值调节。6物理自由度四旋翼，12状态线性化离散模型，状态按论文记号为 x=[Δs, Δdot s, ψ, dotψ]，其中位置偏差3、速度3、roll/pitch/yaw 3及其角速度/角速率3；**4个输入为四个旋翼各自推力**，不是总推力加三轴力矩。连续非线性刚体模型仅用于导出局部平衡点离散线性模型；采样 Ts=0.1 s，预测时域 N=15。
- **不确定性/约束**：质量区间[27g,37g]，以LFT/乘性参数不确定性描述；另有有界风扰动，界限按x/y方向最大相对速度2m/s假设构造。每桨推力约束[0,0.157]N；位置被限制在以目标平衡位置为中心的超立方体，姿态/角速度也进入状态多面体约束。代价矩阵 Qx=diag(3,2,3,1,1,1,0.1,0.1,0.1,0.1,0.1,0.1)，Qu=I4；目标在10s仿真中于5s切换。
- **量测与估计**：在线问题每拍使用可用状态测量 xhat_k 初始化管束；论文没有给出实际IMU/Vicon/GPS传感器配置，也没有输出方程、观测器、测量噪声或丢包模型。这里的state measurement是状态可用假设，不能写成已实现的输出反馈。没有状态SMF/CZ后验或参数在线估计器。
- **MPC/终端/证明**：ETMPC用固定形状椭球的平移与缩放参数化状态管束，反馈输入为仿射形式 u=K(x-z)+v，在线求解凸SDP；离线通过SDP及标量线搜索设计椭球形状、反馈增益和终端集。终端椭球在u=Kx下满足鲁棒不变性及收缩条件，并落在状态/输入约束内。**Theorem 1**：离线设计问题(45)可行，且初始状态属于可行域 X_N(X_T)，真实系统满足论文式(1)–(5)的LFT不确定线性模型、扰动集合和状态/输入约束，则闭环轨迹留在该可行域、在线问题对所有后续时刻递归可行，并对外扰具有区域输入到状态实用稳定性（regional ISpS）。**Proposition 6**另在扰动最终变为零的附加条件下给出终端收缩后的指数收敛。作者指出Theorem 1给出的轨迹界在仿真中偏保守。该定理不是原始非线性六自由度模型、间歇观测或SMF输出反馈定理。
- **结果/计算时间**：仅数值仿真，不是真实飞行/HIL/SITL。ETMPC与多面体PTMPC均以N=15比较：在目标xy偏移0.55m时闭环成本109.3与121.4、均未违约；ETMPC最大可行目标偏移0.68m，PTMPC在0.68m不可行。**平均在线求解时间ETMPC=0.16s、PTMPC=0.04s**；相对100ms采样，ETMPC平均已超周期，PTMPC平均低于周期但仍超过仓库20ms预算。正文§5.1明确说明该节SDP使用YALMIP+MOSEK，并在Intel i7-8550 1.8GHz笔记本上运行；但该段对应mass-spring-damper算例。§5.2四旋翼例报告0.16s/0.04s平均在线时间，却未再次明确是否使用相同硬件/求解器，因此不能无条件把四旋翼计时归因于该设备/软件栈。论文未报告四旋翼最坏执行时间或百分位数。没有可核验的实飞数据。
- **复现状态/局限/可迁移性**：出版社数据声明给出补充材料DOI https://doi.org/10.3929/ethz-b-000559871；2026-11-03后续核验：可访问的ETH bitstream下载路径实际返回的是论文正文副本（其ETH存档DOI为10.3929/ethz-b-000582916），并非补充材料DOI 10.3929/ethz-b-000559871；补充材料DOI/元数据入口仍返回403。检查作者公开GitHub主页及可见仓库未找到该补充代码镜像。故补充材料仍未取得、未运行，不能声称已复现。可复用的是LFT参数不确定性、椭球管束参数化、终端椭球RPI与递归可行性证明结构；但它假设状态可用，且在线反馈使用状态误差，不能直接将SMF/CZ后验点估计代入。若实际仅有估计值xhat=x+epsilon，必须将估计误差集合及其经反馈产生的-BK epsilon项纳入误差管束，并证明后验到初始椭球管束的可靠包含关系。

## 背景第34轮新增论文 — Michel等(2019) AR.Drone 2.0水平Tube MPC实飞

- **书目信息/原始全文**：Nathan Michel, Sylvain Bertrand, Sorin Olaru, Giorgio Valmorbida, Didier Dumur, *Design and flight experiments of a Tube-Based Model Predictive Controller for the AR.Drone 2.0 quadrotor*, *IFAC-PapersOnLine*, **52(22), 112–117 (2019)**；1st IFAC Workshop on Robot Control；DOI https://doi.org/10.1016/j.ifacol.2019.11.058 。ONERA作者公开PDF https://w3.onera.fr/copernic/sites/default/files/2019_ifac_workshoprobotcontrol_design_flight_tube_mpc_ardrone.pdf 。**2026-11-03实际阅读：完整6页PDF pp.1–6，正文§1–6、模型、Tube约束、辨识、终端集与飞行结果；全文已读**。
- **控制任务/模型/输入**：Parrot AR.Drone 2.0水平位置稳定与连续waypoint调节。作者假设yaw角和垂直速度为零、小roll/pitch、x/y水平运动解耦；每个水平轴单独建模为3状态 Xx=[x,vx,φ] 与1个虚拟输入 Ux=φr（另一轴对应 Xy=[y,vy,θ], Uy=θr）。这是依赖机载内环的降阶模型，不是完整12状态MPC，也不是直接四桨推力/力矩输入。AR.Drone内部控制器负责roll/pitch、yaw-rate和垂直速度调节，MPC输出归一化姿态参考。
- **量测/扰动**：OptiTrack动捕测量位置、速度和姿态；地面ROS PC经Wi-Fi向无人机发送命令。离散扰动集合包含模型误差、外部气动力、离散化误差、动捕测量误差和通信延迟；通过辨识飞行数据计算一步预测残差，并取其凸包作为W。该集合的可信度依赖后续飞行扰动确实不超出辨识包络；无间歇测量/丢包状态SMF/CZ。
- **MPC/约束/终端**：Ts=0.05s，N=30（1.5s horizon）；Q=diag(0.8,1.2,1), R=5；状态约束含水平位置、速度和姿态界，输入姿态参考|U|≤0.56，名义输入收紧至|Ubar|≤0.332。用K=−[0.5,0.4,1]构造误差闭环Z+=(A+BK)Z⊕W的RPI集合Z，名义状态/输入分别使用X⊖Z、U⊖KZ收紧；终端代价来自离散Riccati方程，终端集采用MOAS并按waypoint作在线线性优化调整。QP由CVXGEN生成。
- **实验/保证边界**：真实AR.Drone 2.0飞行验证x/y两个方向，论文报告每轴最大计算时间4ms（含waypoint切换时终端集计算）。状态和输入约束满足的结论以实际扰动落在辨识得到的W内为前提；航点距离刻意选得较近以保证优化可行。该RPI tube与名义约束收紧是明确的线性系统条件保证，但不自动覆盖完整非线性六自由度、逐桨饱和/速率或任意未见扰动。
- **可迁移内容/局限**：这是本轮三篇中最强的Tube MPC真实四旋翼飞行证据，但控制权限是φr/θr虚拟姿态指令，低层飞控封装电机，不能作为12状态四电机直接MPC的实飞证据。它说明低维分层接口、数据驱动扰动包络、RPI误差管与QP可以在约20Hz水平控制周期内运行；没有全状态SMF/CZ、输出反馈后验包含或信息终端RCI。

---


---

## 背景第35轮新增论文 — Ji/Geng/Driggs-Campbell (2022) 四旋翼椭球SMF＋输出反馈鲁棒MPC

- **书目信息/版本**：Tianchen Ji, Junyi Geng, Katherine Driggs-Campbell, *Robust Output Feedback MPC with Reduced Conservatism under Ellipsoidal Uncertainty*, 2022 IEEE 61st Conference on Decision and Control (CDC), pp. 1782–1789, DOI https://doi.org/10.1109/CDC51059.2022.9992704；arXiv预印本 https://arxiv.org/abs/2008.04980。作者代码：https://github.com/tianchenji/Robust-SM-MPC。**2026-11-03实际阅读**：arXiv HTML全文§II–VI、§III-B状态SMF与误差传播、§IV Assumption 1/Theorem 1、§V-B四旋翼算例、Appendix A–C；全文已读。另静态检查代码sm_mpc_qr.py、SSE.py、sm_mpc.py、README与MIT LICENSE；未执行代码。
- **控制任务/模型/状态输入**：四旋翼悬停附近位置调节。论文先给6-DOF刚体模型 p_dot=v、m v_dot=mg e3−TR e3、R_dot=Rω^、Jω_dot=M−ω×Jω，再在Ωe=0、Te=mg附近线性化并以dt=0.2s离散。12状态，代码矩阵结构可识别为位置3、Euler角3、平移速度3、机体角速度3；**4个输入是总推力偏差ΔT与三轴力矩(Mx,My,Mz)**，不是四个电机推力/转速。没有电机分配矩阵、逐桨饱和或电机动态。
- **量测/SMF**：C=I12，12个状态全部作为带有界噪声的输出测量；状态扰动和输出扰动均为椭球集合。代码中Q=0.03²I12、R=0.03²I12。使用经典ellipsoidal set-membership state estimator，在线更新中心xhat、形状矩阵P及残差半径δ；β、ρ通过离线网格搜索选取以减小稳态trace(P∞)。测量更新每拍执行；**没有部分传感器、位置单独量测、间歇测量/丢包或延迟模型**。
- **MPC/约束/终端**：Tube-based robust output-feedback MPC，分解真实状态x=xbar+s，控制误差满足s⁺=(A+BK)s+w−BK e；分别传播控制误差集S和SMF估计误差集E，并直接从椭球集合计算约束收紧。代码N=15；状态约束是三个Euler角分别在[−π/9,π/9]，输入约束仅有总推力偏差T∈[−5,5]；力矩输入通道没有明确硬界，位置/速度也未作为硬约束。代码stage cost Q=I12、R=0.01I4，终端P由离散Lyapunov方程计算。
- **定理条件与结论**：Theorem 1：若Assumption 1中的终端代价下降与终端集合正向不变条件成立，且k=0时优化问题可行，则对任意允许初始误差、状态扰动和输出扰动，在线优化递归可行，原状态/输入约束逐拍满足，名义状态指数稳定，真实状态收敛到误差闭环的最小RPI集合S∞。该定理针对论文给定的线性离散系统及有界椭球不确定性，不是原始非线性六自由度/间歇位置量测/逐桨执行器定理。
- **求解器/复现/结果**：作者仓库为MIT License，README指定Python 3.7与CasADi 3.5；sm_mpc.py用CasADi构造NLP并调用IPOPT，椭球支持函数与MRPI相关计算也通过IPOPT优化。论文未给四旋翼算例的求解硬件、平均/最坏在线时间或实飞数据；仅数值仿真。代码静态审计完成，未运行，不能声称复现。
- **本课题价值/边界**：这是目前核验到的**直接12状态四旋翼“状态SMF＋输出反馈鲁棒MPC”原始论文先例**，因此不能宣称首次把SMF与MPC结合用于四旋翼。其关键缺口是C=I12全状态逐拍测量、wrench虚拟输入、输入约束不完整、无电机映射、无间歇位置观测、无真实飞行/WCET；本课题若主张创新，应限定在部分/间歇位置量测下的可靠状态集合、共享因果物理输入和硬安全终端递归可行，而不是一般SMF＋MPC。

## 背景第35轮新增论文 — Ping等(2020) LPV系统zonotope SMF＋输出反馈RMPC（部分阅读）

- **书目信息**：Xubin Ping, Sen Yang, Baocang Ding, Tarek Raïssi, Zhiwu Li, *Observer-based output feedback robust MPC via zonotopic set-membership state estimation for LPV systems with bounded disturbances and noises*, *Journal of the Franklin Institute*, 357(11), pp. 7368–7398, July 2020, DOI https://doi.org/10.1016/j.jfranklin.2020.05.014。ScienceDirect页面：https://www.sciencedirect.com/science/article/pii/S0016003220303549。
- **阅读等级/范围**：**部分全文阅读**；2026-11-03核验ScienceDirect可见预览的摘要、引言、LPV问题定义、后验观测器/估计误差集、算法与CSTR算例片段。出版社全文请求返回403，未取得完整PDF，故不声称全文已读。
- **方法与数学对象**：离散LPV系统(A(θ),B(θ),D(θ))属于顶点多面体；过程扰动w与量测噪声v均未知但有界。后验观测器增益按LPV顶点离线设计；估计误差采用随时间变化的zonotope生成元矩阵传播，再用缩放的最小椭球RPI集外包未来误差集。在线准min-max输出反馈RMPC分别处理不同预测时刻的估计误差界和闭环误差界，优化控制器增益与约束收紧。
- **保证/例子/局限**：论文摘要明确声称在相应LMI和初始可行条件下保证优化递归可行；名义估计误差系统与名义闭环观测器系统收敛到原点，实际有界扰动/噪声下分别进入时变RPI/RCI邻域。数值例为2状态CSTR，C=[0,1]，不是UAV。未找到测量丢包/间歇观测机制，未见四旋翼算例或实时硬件数据。
- **可迁移性**：可作为“zonotope后验误差集＋椭球RPI外包＋输出反馈RMPC”的一般理论基线；但它不是Constrained Zonotope，且CSTR验证不能直接证明12状态四旋翼可实时运行。该文与已登记的Ping/Sun 2015动态输出反馈zonotope MPC、Qiu等椭球SMF-MPC共同构成一般系统方法对照，避免重复登记旧论文。

## 背景第35轮新增论文 — Delansnay/Dewasme/Vande Wouwer (2025) 六旋翼CZ Tube-MPC实飞

- **书目信息/版本**：Gilles Delansnay, Laurent Dewasme, Alain Vande Wouwer, *Experimental Validation of Zonotopic Tube-MPC Applied to a Hexacopter*, 2025 7th International Conference on Control, Decision and Information Technologies (CoDIT 2025), DOI https://doi.org/10.1109/CoDIT66093.2025.11321702。会议公开6页PDF：https://www.codit2025-virtual-event.com/web/content/1364?download=true&unique=38ac7e7f7fb54cda0d6a9efdec7a04e7817a09c7。**2026-11-03实际阅读**：作者会议PDF pp.1–6全文已读。
- **平台/模型/输入**：DJI F550六旋翼，Pixhawk 4、Raspberry Pi 5；闭环对象是Pixhawk内部姿态/电机控制器。由实验数据辨识4状态模型(vx,vy,vz,ψ)，4个控制输入是北东地坐标三轴期望速度和期望yaw角；名义MPC另增3个位置积分状态以跟踪x/y/z/yaw，辅助状态反馈则回到4状态速度/yaw模型（作者称GPS位置估计精度不足）。因此它不是6-DOF或电机级MPC。
- **传感器/估计**：Pixhawk IMU/GPS，Raspberry Pi另接LiDAR和stereo camera；模型输出是三轴速度与yaw。文章没有构造SMF状态后验、没有明确量测噪声/丢包模型，未说明Pixhawk内部状态估计器误差的确定性集合。
- **Tube/CZ实现**：名义线性MPC＋LQR辅助反馈；误差动态e⁺=(A+BK)e+w；通过CORA/Constrained Zonotopes做可达集传播并近似RPI集合Γ，收紧名义状态/输入约束X⊖Γ、U⊖KΓ。do-mpc＋IPOPT；采样时间0.2s、预测时域10步。
- **实验/实时结果**：户外风扰条件下重复4次实验；Raspberry Pi 5整个控制环平均计算52ms、观察到的上限77ms，均低于200ms采样周期。它是真实六旋翼飞行的CZ Tube-MPC证据，但论文未提供与一般学术定理同等完整的递归可行性证明，也未实现状态SMF。
- **迁移边界**：支持“低维速度/yaw接口＋Pixhawk内环＋CZ RPI tube”可实飞；不支持12状态四旋翼、四电机独立命令、间歇位置SMF或20ms周期。六旋翼结果不能替代四旋翼直接证据。

---

## 非期刊研究来源（不计入原始论文数量）

Jinaykumar Nitinkumar Patel, *Set-theoretic Reachability-informed Model Predictive Control for Mechanical and Aerospace Systems*, Ph.D. dissertation, The University of Texas at Arlington, May 2026, DOI https://doi.org/10.13140/RG.2.2.27141.51681。2026-11-03定向阅读Chapter 6.1–6.2.5及Chapter 8.3.1–8.3.4；2026-11-03后续完整阅读Chapter 7 pp.141–168。Chapter 7重印Patel与Subbarao的AIAA SciTech 2026论文（DOI 10.2514/6.2026-0111），全文通过博士论文重印章节核验，AIAA proceedings独立PDF未单独取得；Chapter 7的hybrid ZSM-KF与Chapter 6的LTV SMF-MPC、Chapter 8.3的quadrotor reachable-set MPC是不同工作，不得合并其证明结论。Chapter 6是LTV航天器相对运动中的椭球/zonotope SMF＋MPC，Chapter 8.3是独立的Crazyflie 2.1 12状态四旋翼、四桨转速输入与zonotopic reachable-set MPC；两者不是同一个四旋翼SMF/CZ闭环案例。Chapter 6明确不主张渐近稳定；Chapter 8.3无SMF后验、无间歇量测、电机动态假设为瞬时转速变化。全文：https://www.researchgate.net/publication/406045114_Set-theoretic_Reachability-informed_Model_Predictive_Control_for_Mechanical_and_Aerospace_Systems。

---

## 待全文核验候选（不计入已读论文数量）

J. Patel, U. C. Kaya, K. Subbarao, *Real-Time Reachable Set-Based Model Predictive Control for Safe Trajectory Tracking of Quadrotors*, AIAA Science and Technology Forum and Exposition / AIAA SciTech Forum 2026, ISBN 9781624107658。当前仅核验二次数据库书目信息/概要，未取得AIAA出版方全文、页码或DOI；其与Patel 2026博士论文Chapter 8.3的重合程度未核实。来源：https://eurekamag.com/research/103/962/103962467.php。


---

## 背景第36轮新增论文 — Patel & Subbarao (2026) 航天器混合ZSM-KF＋时变MPC

- **书目信息**：Jinaykumar Patel, Kamesh Subbarao, *Robust 6-DOF State Estimation for Spacecraft Proximity Operations Using Zonotopic Set Membership based Kalman Filtering*, AIAA SCITECH 2026 Forum, 2026, vol. 48, no. 1, paper 0111, Orlando, Florida, January 2026, DOI https://doi.org/10.2514/6.2026-0111。**全文核验路径**：Patel博士论文 *Set-theoretic Reachability-informed Model Predictive Control for Mechanical and Aerospace Systems*（University of Texas at Arlington, May 2026, DOI https://doi.org/10.13140/RG.2.2.27141.51681）Chapter 7 pp.141–168明确注明本章经许可重印该AIAA论文；本轮完整阅读Chapter 7 §§7.1–7.6。AIAA proceedings独立PDF未单独取得，故阅读等级写作“全文经学位论文重印本核验”，不声称直接读过独立会议PDF。
- **任务/物理模型/状态输入**：航天器相对接近与交会。13个坐标状态：LVLH相对位置3、相对速度3、姿态四元数4、相对角速度3；物理自由度为6。平移采用Tschauner–Hempel时变相对轨道模型，旋转采用四元数/角速度动力学；组合矩阵采用分块对角形式A=diag(A_T,A_R)、B=diag(B_T,B_R)，未建模平移—姿态耦合。6个虚拟输入：3个LVLH平移推力/加速度通道＋3轴控制力矩；没有电机/推进器几何分配、执行器动态或速率状态。正文将平移输入称为加速度通道，而Table 7.1将其界限标为力(N)，单位需在迁移前澄清。
- **量测与估计**：平移输出为相对位置，C_T=[I_3 0]，速度由模型/滤波估计；仿真噪声结构另含四元数和角速度通道。没有给出真实相机、GPS、IMU等硬件映射。filter update固定每0.025s执行，算法没有测量丢失/随机间歇更新分支；因此是周期性多速率估计，不是间歇观测滤波。
- **混合ZSM-KF**：过程/测量不确定性分别拆为Gaussian与unknown-but-bounded (UBB)部分。非线性f、g在先验估计处一阶线性化；通过先验zonotope内Hessian范数构造二阶Lagrange remainder界，形成G_δ、G_ε；与UBB过程/测量生成矩阵G_w、G_v作zonotope精确Minkowski合并。后验集合误差生成矩阵为Ω_k=[(K_kH_k−I)G_δ,(K_kH_k−I)G_w,K_kG_ε,K_kG_v]。Kalman增益通过最小化Tr(P_k)+Tr(Ω_kΩ_k^T)选取。**边界**：Ω_k只界定UBB与线性化余项；Gaussian噪声进入协方差P_k，Gaussian分布本身无有限硬支撑。因此这不是一个对全部随机噪声实现都保证包含真实状态的纯确定性后验集合，除非另加置信水平或有界化假设。该方法用普通zonotope，不是constrained zonotope。
- **MPC结构/约束**：离散线性时变MPC；滤波步长0.025s，MPC步长0.5s（2Hz），预测时域30步、控制时域5步，基础仿真步长0.025s、仿真60s。Table 7.1给出平移力和力矩输入界限（分别标为±1N、±1Nm）及输入变化率惩罚；未给出硬速率约束。终端部分描述为最终时刻的速度边界条件并纳入代价，没有构造终端RPI/RCI集合。Algorithm 6将状态估计点xhat作为MPC预测初值；没有把Ω_k直接用于状态约束收紧、Tube初始化或终端集合。未见递归可行性/渐近稳定性定理；本章明确不主张渐近稳定性。
- **仿真与实时证据**：仅60s六自由度航天器仿真，50次Monte Carlo；不是四旋翼、不是HIL/实飞。平均RMSE：位置0.0763m（EKF 0.0764m）、速度0.0478m/s（0.0559m/s）、姿态0.1268°（0.1268°）、角速度0.0013rad/s（0.0068rad/s）；主要改善体现在非线性旋转角速度估计，线性Tschauner–Hempel平移估计与EKF几乎相同。ZSM-KF平均更新0.56ms，EKF 0.49ms；没有硬件说明、WCET/百分位数或MPC求解时间，不能据此宣称整个闭环满足20ms预算。
- **可迁移内容/限制**：可迁移的是“非线性Taylor余项→zonotope外包→与UBB过程/量测误差合并→混合协方差/集合误差准则选增益”的估计结构。不能直接迁移其分块对角航天器模型、虚拟平移/力矩输入或终端条件到四旋翼。对本课题最关键的缺口是：部分/间歇位置量测的后验集合、同一后验集合上的共同因果输入、将集合误差并入Tube/约束收紧、四桨分配及电机速率、硬终端RCI/递归可行性。



## 背景第31轮 — Ru/Subbarao (2017) SDC-NMPC四旋翼执行器预测缺口（2026-11-03 UTC；期刊正文部分核验）

- **书目**：Pengkai Ru; Kamesh Subbarao, *Nonlinear Model Predictive Control for Unmanned Aerial Vehicles*, *Aerospace* **4**(2), Article 31 (2017), 26页，DOI https://doi.org/10.3390/aerospace4020031 。出版社开放原文 https://www.mdpi.com/2226-4310/4/2/31 ；本轮MDPI访问429，实际阅读作者在ResearchGate提供的开放全文文本 https://www.researchgate.net/publication/317686529_Nonlinear_Model_Predictive_Control_for_Unmanned_Aerial_Vehicles 。**实际阅读**：2026-11-03，§2式(3)–(7)、§3式(8)–(11)、§4式(41)–(44)、§6实验描述、§7和附录A；**部分全文阅读**，其余公式及稳定性证明未逐式检查。
- **任务、模型、输入**：标准6物理自由度四旋翼，12状态 x=[惯性位置p(3),机体系速度V_B(3),Euler姿态Θ(3),机体系角速度Ω(3)]，不是12自由度；优化输入 u=[F1,F2,F3,F4] 四桨推力(N)，式(3)线性映射总推力及三轴力矩。悬停平衡每桨mg/4；LTI MPC在悬停点线性化，NMPC使用SDC伪线性状态依赖矩阵及零阶保持离散。采样Δt=0.05s，预测/控制时域均25步，即1.25s。仿真m=0.8kg，J=diag(0.0224,0.0224,0.0436) kg m²，桨臂L=0.165m。
- **执行器关键边界**：式(7)假定逐桨一阶推力动态 dFi/dt=λF(Fci−Fi)，λF=50 s⁻¹（附录A）；原文明确**执行器动态不进入MPC预测，仅用于真实系统数值状态传播**。故优化的逐桨推力盒不是自动的实际逐桨硬执行证书。0.05s采样对应一阶时间常数0.02s，采样/时间常数=2.5；若按零阶保持命令计算，该一阶模型在50ms内完成91.8%阶跃、仍残留8.2%；若改为20ms采样，单步完成63.2%、仍残留36.8%。这些仅是λ_F=50 s⁻¹假设下的模型推导，不是目标机实测或ESC最坏误差证书。输入仿真盒Fi∈[0,mg]；逐桨速率约束、实际电机RPM标定、分配残差可靠上界均未报告/未从本轮已读章节确认。
- **MPC与量测**：SDC状态依赖系数NMPC以SQP处理状态/输入/输出约束，另给悬停线性MPC对照（QP）；Q=I12、R=I4。全部仿真在Fujitsu America i7笔记本（8GB RAM、2.8GHz）运行MATLAB R2016a；论文未报告逐次求解时间或WCET。§3依赖当前状态；真实IMU/Vicon/GPS、Kalman/SMF/CZ、位置间歇测量及失测策略：**未报告/本轮已读范围无法确认**。终端集合、20ms最坏求解时间、所有扰动路径硬安全和递归可行证明：**本轮未核验，不得推断**。文中有采样数据跟踪误差有界性分析，但不能转写为本仓库有噪失测下的安全定理。
- **结果**：螺旋、球面螺旋、分段直线轨迹的MATLAB数值仿真；对比LMPC/NMPC及扰动情形，非四旋翼实飞。可复用：12状态真实坐标定义、逐桨推力混控及执行器模型/预测模型不一致的审计范例。局限：未把一阶执行器动态放入预测；与本课题的确定性SMF+Tube MPC信息状态、共同可执行物理输入、终端信息不变集均不等价。
- **本课题意义**：六状态平面(T,τ)仍条件性首选，四状态冻结推力仍仅数学基线。若采用逐桨/总推力预测，必须把执行器动态加入扩展状态或以实验有依据的误差集合外包；不能把论文的仿真追踪当作硬安全。**下一查**：从该文一阶执行器式(7)推导采样实际推力可达集，并与目标机体可测的ESC/RPM/推力辨识合同比较；由主研究任务实现验证，背景任务不开发控制器。

---


## 2026-11-03 Hu primary-source follow-up (targeted rereading)

See [scoped reading record](../research/model_selection/background_run_20261103_hu_primary_followup.md) for author-PDF page/section provenance, limitations and comparison. Three targeted body reads (Hu, Didier, Falanga), plus Alexis metadata/abstract only; no new unique-paper count asserted. Existing full-reading history is preserved; this entry records only this run's partial rereading. Current model priorities remain unchanged. No controller, experiment or safety certificate added.


## 2026-11-03 Hu model/proof-chain continuation — partial primary-source audit

[Detailed provenance and reading positions](../research/model_selection/background_run_20261103_hu_printed_model_proof_chain.md). Four body sources partially verified (Hu, Didier, Bouffard technical report, Villanueva theory); Alexis remains abstract-only. No full-read or new unique-paper count asserted. Visual inspection resolves the previous OCR uncertainty: the problematic indices are printed in the author PDF. Canonical attitude coordinates require transformation before physical interpretation; author-intended correction remains unverified. Hu is not a copy-ready simulation plant. Terminal containment and observation-history compatibility require separate checks. Preserve existing model priorities and all previous evidence; this is a reproducibility qualification, not a controller result.

### Hu author-version check, 2026-11-03

[Version/presentation audit](../research/model_selection/background_run_20261103_hu_printed_model_proof_chain.md#author-copy-and-presentation-continuation): coauthor-hosted PDF is byte-identical, not a corrected edition; author slide 29 repeats the disputed drift indices and rate labels. Slide 31 separates 81.6 ms optimization from 20 microsecond feedback. Zero new unique papers and no full-read upgrade. Actual implementation remains unverified; model priorities and safety gates unchanged. Next: trace the acknowledged Mo Chen model provenance, rather than repeat mirror downloads.


## 2026-11-03 02:34 PT — provenance cross-check (no new unique papers or full-read upgrades)

[Scoped background run](../research/model_selection/background_run_20261103_0234_provenance_crosspaper.md). **Three previously known direct quadrotor MPC original sources checked**: Bouffard (2012) UC Berkeley report UCB/EECS-2012-241, institution metadata/abstract reverified (partial primary PDF model reading inherited from preceding same-day continuation); Bouffard/Aswani/Tomlin ICRA 2012 DOI 10.1109/ICRA.2012.6225035, IEEE publisher abstract/metadata reverified (earlier author-PDF §III–VII findings inherited); Hu/Feng/Quirynen/Villanueva/Houska ACC 2018 DOI 10.23919/ACC.2018.8431112, author and IEEE abstract/metadata reverified (earlier same-day Hu PDF equation inspection inherited). **This run's accounting: 0 newly full-read; 1 ongoing partially read primary PDF; 2 metadata/abstract checks; zero newly unique works.** Mo Chen 2017 thesis §4.1.5.2 is a provenance lead from earlier same-day reading, **not a fourth independently reread source this run**. Findings: Bouffard's near-hover attitude transfer parameter fit is not Mo/Hu's; observable companion attitude second state need not equal physical angular rate; virtual pitch/roll/thrust commands do not prove four-rotor actuator feasibility; Hu printed equation index mismatch and optimizer timing remain unresolved. Next read: original thesis and Hu printed equations side by side, with explicit coordinate and actuator mapping. No model selection or Gate A promotion.


---

## 2026-11-03 — Bouffard report and Mo Chen 2018 model-provenance sources

### Patrick Bouffard (2012), UCB/EECS-2012-241 technical report

- **Bibliography**: Patrick Bouffard, *On-board Model Predictive Control of a Quadrotor Helicopter: Design, Implementation, and Experiments*, University of California, Berkeley, Technical Report UCB/EECS-2012-241, 13 December 2012. Institutional record: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-241.html ; 81-page PDF: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/Archive/EECS-2012-241.pdf . No DOI located. Distinct from Bouffard/Aswani/Tomlin, ICRA 2012, DOI 10.1109/ICRA.2012.6225035.
- **Reading status/date**: 2026-11-03, **partial primary-source reading**. Targeted Chapter 2 §§2.3.2–2.3.6 and §§2.4.1–2.4.3; equations (2.14)–(2.17), printed pp.16–19; combined 10-state model/output equation, pp.18–19; Appendix A.2–A.3, pp.53–54. Not read cover-to-cover; no code run.
- **Model/task/input**: 10-state discrete LTI near-hover model at Ts=0.025 s, two lateral 4-state channels plus a vertical 2-state channel. Three upper-level commands: desired pitch, desired roll and collective thrust, not four rotor thrusts/RPM. Identified attitude coefficients d0=80,d1=8,n0=40; Pelican mass 1.3 kg; KT=0.91.
- **Sensors/implementation**: five-output measurement y=[x1,theta1,x2,theta2,x3]+bounded i.i.d. noise. AscTec Pelican with Vicon MX at 120 Hz; proprietary AutoPilot inner controller at 1 kHz; setpoints sent at 40 Hz. Real onboard explicit MPC/LBMPC hover and ball-catching, but no deterministic per-rotor saturation/rate or motor-lag guarantee.
- **Coordinate caveat**: attitude companion block A_theta=[[-d1,1],[-d0,0]], B_theta=[0,n0]^T implies the second coordinate chi=physical_theta_rate+d1*theta. The report's global theta-dot label is not consistent with this matrix if read literally. This is an algebraic inference; the report does not explicitly state the transform.

### Mo Chen et al. (2018), model-provenance paper (not an MPC paper)

- **Bibliography**: Mo Chen, Sylvia L. Herbert, Mahesh S. Vashishtha, Somil Bansal, Claire J. Tomlin, *Decomposition of Reachable Sets and Tubes for a Class of Nonlinear Systems*, IEEE Transactions on Automatic Control, 63(11), 3675–3688 (2018), DOI https://doi.org/10.1109/TAC.2018.2797194 ; author preprint https://arxiv.org/abs/1611.00122 .
- **Reading status/date**: 2026-11-03, **partial full-text reading** of §VII-B, equations (61)–(64), and §VIII; not read cover-to-cover.
- **Classification/model**: Hamilton–Jacobi reachability/decomposition paper, not a quadrotor MPC controller. §VII-B gives a 10D near-hover quadrotor used for experiments involving learning-based MPC and cites Bouffard's 2012 report. State order (px,vx,theta_x,omega_x,py,vy,theta_y,omega_y,pz,vz). Dynamics: px_dot=vx+dx; vx_dot=g tan(theta_x); theta_x_dot=-d1 theta_x+omega_x; omega_x_dot=-d0 theta_x+n0 Sx; analogous y equations; pz_dot=vz+dz; vz_dot=kT Tz-g. Inputs Sx/Sy are desired pitch/roll, Tz vertical thrust; wind terms enter position derivatives, so they act as velocity disturbances.
- **Parameters/bounds**: d0=10,d1=8,n0=10,kT=.91; angle bounds ±10 degrees; Tz in [0,2g]; disturbances 0.5/0.5/1 m/s. The system decomposes into 4D+4D+2D reachability subsystems.
- **Supporting dissertation, not counted as a separate MPC paper**: Mo Chen, *High Dimensional Reachability Analysis: Addressing the Curse of Dimensionality in Formal Verification*, Ph.D. dissertation, UC Berkeley, UCB/EECS-2017-132, 26 July 2017; targeted Chapter 4 §4.1.5.2, equations (4.58)–(4.61), pp.90–92 and bibliography [25] (Bouffard report).
- **Coordinate caveat**: the text labels omega as pitch/roll rate, but theta_dot=-d1*theta+omega implies omega=physical_theta_rate+d1*theta. A physical-rate realization instead has theta_dot=rate and rate_dot=-d1*rate-d0*theta+n0*S. Gyro measurement maps, constraints and terminal sets must respect this transform.
- **Provenance limit**: Hu acknowledges Mo Chen and cites Bouffard's report. This supports structural lineage Bouffard -> Mo Chen -> Hu, not identical numerical calibration or uncertainty bounds.

### 2026-11-03 source-reading accounting

Four paper/report sources received targeted body reading this run: Hu (2018), Bouffard (2012) report, Didier (2021), and Mo Chen et al. (2018). **0 full-text-complete upgrades, 4 partial body reads, 0 abstract-only reads**. The Mo Chen 2017 dissertation was an additional partial supporting-document cross-check, not counted as a separate MPC paper. Three sources are direct quadrotor MPC sources (Hu, Bouffard report, Didier); the Mo Chen TAC paper is model-provenance/reachability evidence only.


---

## 2026-11-03 — actuator-state and physical command-interface audit

### Parakh M. Gupta, Ondřej Procházka, Jan Hřebec, Matej Novosad, Robert Pěnička, Martin Saska (2025), LoL-NMPC

- **Bibliography**: “LoL-NMPC: Low-Level Dynamics Integration in Nonlinear Model Predictive Control for Unmanned Aerial Vehicles,” 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2025), pp. 1186–1193. DOI: https://doi.org/10.1109/IROS60139.2025.11246583 . Author preprint: https://arxiv.org/abs/2506.02169 . Public implementation: https://github.com/ctu-mrs/lol_nmpc .
- **Reading status/date**: 2026-11-03, **partial primary-source body reading**, Sections III–V and conclusion, including the low-level controller/motor model, actuator constraints, implementation and experiments. Also inspected the public Acados model and configuration at repository commit 4526fe9443464bf7f33f942577e18ed3f6b78cee; files packages/controller_module/src/nmpc_acados/quadrotor_model.py and base_config.yaml. Not read cover-to-cover.
- **Model/state**: 20 coordinates: position (3), unit quaternion (4), translational velocity (3), body angular velocity (3), low-level rate-controller integral state (3), and four normalized motor-speed/throttle states (4). The quaternion is constrained to unit norm; 20 coordinates are not 20 independent physical degrees of freedom.
- **OCP input/interface**: four high-level inputs, collective throttle plus three desired body rates, not four independent motor commands. The low-level controller converts rate error and integral state into torque; the mixer maps collective throttle and torque to four motor commands. Linear constraints are imposed on the mixed per-motor commands.
- **Actuator model**: normalized motor-speed state follows a first-order lag, \(\dot r=(r_c-r)/\tau_m\). The public configuration sets \(\tau_m=0.05\) s, controller step 0.01 s, and prediction horizon 1.0 s. Thus the model explicitly carries motor lag and mixer feasibility, but it is a cascade-integrated high-level interface rather than direct rotor-command optimization.
- **Code/model consistency note**: the paper describes the low-level block as PID-type. In the inspected public Acados model, the predicted torque is \(\tau_c=K_p(\omega_c-\omega)+K_i z\); the derivative term is commented out. The released prediction model is therefore PI in this expression. This is a code observation, not a claim about every component of the PX4 firmware.
- **Platform/measurements/results**: real custom quadrotor, approximately 1.2 kg, Cube Orange+/PX4, Khadas VIM3 Pro ARM computer, GNSS RTK and IMU state estimation, ESC RPM feedback reported around 65 Hz. The paper reports real-time operation at 100 Hz, flight speeds up to 98.57 km/h and accelerations up to 3.5 g, with average trajectory-error reduction of 21.97% relative to the standard NMPC formulation.
- **Limitations/reuse**: this is the strongest recent real-flight example of including low-level controller, mixer and motor dynamics together in the prediction. It does not optimize four independent rotor commands at the OCP interface; the interface is collective throttle/body-rate references. Its 20-coordinate model is hardware-stack-specific and materially more complex than a 12-state rigid-body plant. It does not provide the SMF/CZ intermittent-measurement or robust Tube-MPC recursive-feasibility guarantee sought here.

### Bin Wang, Chuixu Kong, Mutian Yu, Chang Liu (2026), abstract-only candidate

- **Bibliography**: “Meta-Learning Augmented Model Predictive Control for Quadrotor UAV Flight in Strong Wind,” Drones, 10(10), 731 (2026), DOI: https://doi.org/10.3390/drones10100731 .
- **Reading status/date**: 2026-11-03, **metadata/abstract only**. The publisher full-text route returned an access/rate-limit error during this run; search-index excerpts are not treated as full-text evidence.
- **Reproducibility check**: inspected https://github.com/BW-AerialRobotics/ML-MPC at main commit 14ecd14c489324034088a092bf73920d7bf5bb8f. The visible tree contains baseline controllers, rotor-model test data, PX4 parameters and plotting utilities, but no clearly identifiable core implementation of the paper's meta-learning MPC. Do not use its model/input details in the evidence matrix until the author PDF or implementation is independently inspected.
- **Status**: retain as an abstract-only candidate for a later full-text retrieval; not counted among this run's body-read papers and not used to change model selection.

### 2026-11-03 targeted re-reading accounting (existing ledger records, no duplicate entries)

- **Ru & Subbarao (2017)**, DOI 10.3390/aerospace4020031: re-read the rigid-body equations, rotor allocation, actuator equation (7), prediction statement and Appendix A. The paper explicitly says the first-order actuator dynamics are ignored in prediction and used only for state propagation.
- **Bicego et al. (2020)**, DOI 10.1007/s10846-020-01250-9: re-read the actuator-force state/input definition, OCP constraints, state-dependent force-rate limits, approximation used to keep those constraints linear, stability/recursive-feasibility remarks and quadrotor implementation.
- **Nan, Sun, Foehn & Scaramuzza (2022)**, DOI 10.1109/LRA.2022.3154033: re-read the quaternion rigid-body model, first-order rotor-thrust lag, four-command OCP, INDI post-processing and real-flight instrumentation.
- **Wehbeh & Sharf (2024)**, DOI 10.1002/rnc.7627: re-read the SO(3) local error model, bidirectional thrust/rate constraints, scenario uncertainty treatment, sensor assumptions and simulation/timing tables.
- **Gupta et al. (2025)**, DOI 10.1109/IROS60139.2025.11246583: new partial body-read record above, plus public model-code review.
- **Count**: 5 original quadrotor/multirotor MPC papers received targeted body reading from primary full-text sources; 0 were read cover-to-cover; 5 are partial body reads; 1 additional 2026 candidate is metadata/abstract-only. Existing Ru/Bicego/Nan/Wehbeh entries are cross-referenced, not duplicated. The 2026 candidate is not used as evidence until full text is obtained.

## 2026-11-04 — 有限记忆输出反馈课题方案的定向核验

见 [本轮证据补充](../research/proposal/LITERATURE_UPDATE.md) 与 [完整课题方案](../research/proposal/RESEARCH_PROPOSAL.md)。本轮0篇新增完整全文精读；Scott2016、Hassaan2021和Ji2022为既有来源相关正文定向复核；Rego2020为摘要/书目复核。新增候选：Andrade等2024（DOI 10.1109/ACCESS.2024.3381622，Crossref书目及作者学校目录，独立正文未取得）；Robbins等ACC2026（作者单位摘要，pp.585–592）；Krsmanovic等arXiv:2609.03699和Baranowski arXiv:2610.26326（作者摘要，未升级同行评审状态）。后三项只做摘要核验。各原始链接、实际范围与迁移限制见专题，不重复增加既有来源数量。

Ji2022 §V-B的四旋翼示例采用12状态平衡点线性化、输出矩阵C=I和0.2s离散，不可表述为位置-only间歇观测或成熟飞控外环验证。CZ Tube MPC与在线CZ约束收紧已有直接先例，故本题贡献需限于时间戳、有限记忆、因果准入与模式收紧的可检验差异。本轮独立数学基线有解析证明、Fraction代数证书与本地闭环运行，不是原论文完整实验R3。

## 2026-11-04 — 丛一睿集员论文与 MPC 选题分析

入口为 [丛一睿论文清单](CONG_YIRUI_SET_MEMBERSHIP_PAPERS.md)，详细证据及五个课题见 [专题报告](../research/proposal/CONG_MPC_RESEARCH_TOPICS.md)，文件版本、SHA256、页数及逐篇阅读范围见 [manifest](sources/cong_mpc_20261104/manifest.json)。本条统计整个本次文献任务，不与上一条已有 MPC 核验重复计数。

- **阅读数量：** 主清单第1–8、10–13篇，共12篇定向正文阅读；0篇升级为全部证明/全文逐行精读，0篇完成实验复现。第9篇未取得本地全文，按用户要求不再获取，不用于推断具体控制结构。
- **全文版本：** 7篇arXiv作者稿、4篇正式出版PDF（含中文期刊）、1篇IEEE接收稿。第6篇所用作者稿称COIT，正式摘要称DOIT，具体结果按版本区分。
- **SPIN-SMF：** 新取得第3篇并读取§II–IV、Proposition 1、Theorems 1–2、Algorithms 1–3及结论。结构不变性、离线预计算、参数差异界和热启动均已有；新方向应转向控制约束方向、模式切换和有限迭代外包证书。未把论文仿真加速比当作本地测量结果。
- **中文ASMF：** 核实《导航定位与授时》13(3)，2026年5月，25–34；模型的过程噪声界已知，测量噪声界未知。正文目标为式(8)–(10)的非空与渐近有界；没有据此推断每拍真实包含。由于文本乱码，视觉核对PDF第3、4、6页（印刷页27、28、30）。
- **单信标与多机定位：** 第11篇已有凸松弛、半空间修正和滑窗；第13篇采用绝对观测与相对测距，Algorithm 2第15行取区间外包，几何假设限制需保留。不能把它们称为尚无估计理论或完全无绝对定位信息。
- **INS/GNSS：** 九维导航误差模型、位置差观测、截断离散化及滑窗；作者将INS线性化误差处理列为未来工作。未经残差外包不能用于宣称真实非线性飞行硬安全。
- **已有理论边界：** OIT最终恢复包含不代替启动期安全；有界扰动观测误差不代替输入饱和下的可控性；平滑不使用未到达数据，同一信息下也不凭空优于精确当前后验。撤回的arXiv:2305.15797未作为理论依据。
- **额外竞争检索：** Qiu2020（出版社摘要/引言）、Hung等2020（机构全文摘要/引言）、Wang–Manzie arXiv:2005.04006（作者摘要）、Ding等PLOS One2026（出版社摘要/引言）；与此前Hassaan、Ji、Andrade、Robbins、Parsi及预测降阶线索共同约束创新表述。完整新增检索返回见 [trace](sources/cong_mpc_20261104/novelty_search_trace.json)。此为定向检索，不是穷尽综述。
- **产出与限制：** 推荐优先比较联合状态—扰动抗扰MPC（B）与现有项目延续方案（A）；计算证书（C）、主动单信标（D）、相对安全分布式MPC（E）作为另外三个候选。均为待验证方案；未改变当前算法/接口选择，未执行新的闭环测试。

## 2026-11-04 — 硕士两项创新点：理论与机制仿真重评

用户明确两个创新点服务于硕士论文，抗扰不再是首要排序。详见 [评估报告](../research/proposal/CONG_MPC_MASTERS_EVALUATION.md)、[冻结试验计划](../research/proposal/CONG_MPC_MASTERS_PROBE_PLAN.md)及 [本轮检索记录](sources/cong_mpc_20261104/masters_search_trace.json)。原12篇阅读数量不变；没有追加原论文实验复现。

- **新增/深化的竞争阅读：** Zhang–Liu–Shi自触发自适应MPC作者稿（摘要、模型及算法入口）；Cai等2026 anytime原始—对偶MPC证书（摘要及模型相关部分）；Badalamenti等CDC2025模板选择（摘要、模型与控制构造）；Krsmanovic等2026预测zonotope降阶由摘要升级为§II–III定向正文阅读。Brunner等2018有限窗集员OFMPC为作者机构摘要级，具体全文差异仍未核对。2020有界误差目标跟踪为出版社摘要级。各阅读层级在报告中逐项标明，不把摘要作全文证据。
- **推导：** 标准支持保持、固定有限时域共同输入可行集等价、常值终端RPI假设下的每拍压缩移位可行性；另给条件化信息损失反例及预算上界/观测调度证明框架。这些不等于已证明新的学术贡献或一般输出反馈稳定性。
- **实际实验：** 新独立脚本experiments/cong_mpc_screen.py完成A/B/C/D/E机制筛选；C为稳定二维系统2700网格案例和48条闭环、1440步。方向模板/同规模均匀模板可行数1198/1178；闭环成对代价改善中位仅0.00757%，不支持显著控制收益。B相关性半宽改善中位1.123%，D/E仅分别为离散动作与联合顶点机制。保留负结果和同规模强基线。
- **审计：** experiments/cong_mpc_audit.py核对主脚本和10个CSV哈希，补报对偶最大间隙而非只用零中位数。无本轮PX4/Gazebo运行，无src控制算法修改，无Git提交。
- **修订建议：** 优先验证“控制相关集合压缩→观测资源调度”，两点须分别有新命题和独立基线；单信标“全假设安全→主动消歧”为探索备选。当前固定模板原型尚不足以直接定为创新点，第二点完整算法及闭环未实现。

## 2026-11-05 — 阶段 3 候选假设的定向核查

问题是已交付的位置历史能支持什么恢复与控制保证。阶段 2 的 37 项是已交付的系统库快照。本节按 DOI 引用补查与重读。八项材料的作者、题名、年份、出处、原文链接与检索式见[阶段 3 创新性证据表](../research/innovation_analysis.md)。

- **误差下界。** Haimovich 等的 Thm. 1 已给出规则采样下最佳因果微分的最坏情形精度。Wang 等 §4.3 研究椭球 SMF 的缺测持续时间与缺测率。Garulli、Vicino、Zappa（1997）已有信息复杂性与集员状态估计框架，后者仅核题录和摘要。[最优微分](https://arxiv.org/pdf/2106.05320) · [不完整观测](https://lab.bciml.cn/wp-content/uploads/2020/08/Set-Membership-Filtering-with-Incomplete-Observations.pdf) · [IFAC 书目](https://www.sciencedirect.com/science/article/pii/S1474667017428321)
- **历史与首步。** Nouwens 等作者稿 Def. 1、Thm. 1 给出删约束保持控制解的条件，Bemporad 等 Thm. 2 给出固定活动集上的参数解。候选 B 须额外说明哪些可达历史能改变相应约束右端。Brunner 2018 的期刊定理细节仍待核。[删约束作者稿](https://arxiv.org/pdf/2303.16581) · [参数 QP 出版正文](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf)
- **交付期限。** 重读原总账 Yang–Ozay 2021 的 Props. 4–5，补查同作者 CDC 2020 的 Thm. 1 与 Chen 等的有限图增时延算法。成功时观测状态、有噪状态、仅位置带戳交付分别对待。论文实验复现数本轮为零。[缺测安全博弈](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) · [有噪状态](https://web.eecs.umich.edu/~necmiye/pubs/YangO_cdc20.pdf) · [延迟博弈](https://link.springer.com/article/10.1007/s00236-020-00374-7)

## 2026-11-05 — 阶段 4 定题核对：哪一拍算跨块

重读已登记的 M1、M8、M9 作者稿第 2 页的延迟数据模型。三份 PDF 均以作者或 arXiv 版本取得，使用 pdftotext 定页读数。M1 与 M9 的文字分别以 \(i+\omega(i)>T_d\)、\(i+\omega(i)>T\) 描述超出时域并视同缺测。M8 的文字以 \(i+\tau(i)\ge T\) 描述与缺测相似的情况。这里记录作者稿的端点写法；跨版本复现还须对齐“观测何时可供状态估计及输入决策使用”。本项目将边界拍到达和严格越界到达分列，并只从实际交付拍起使用旧信息。[M1 作者稿 §2.2](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf#page=2) · [M8 作者稿](https://arxiv.org/pdf/2101.03389#page=2) · [M9 作者稿 §2.1](https://qiangs.github.io/Papers/Conf_HSCC2021Hassaan.pdf#page=2)

| 已登记的论文 | DOI | 本次获取的作者稿 SHA-256 |
|---|---|---|
| Syed M. Hassaan, Tarun Pati, Qiang Shen, Sze Zheng Yong，*Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*，IFAC-PapersOnLine，2021 | 10.1016/j.ifacol.2021.08.482 | c62443c17324b63bb40a60808ed010a125f03a2f15d9dd97088d2fd0af0313c2 |
| Syed M. Hassaan, Qiang Shen, Sze Zheng Yong，*Equalized Recovery State Estimators for Linear Systems With Delayed and Missing Observations*，IEEE Control Systems Letters，2022 | 10.1109/LCSYS.2021.3050300 | f964ebc69a0c6acc4cd18fd7a1afd3d0516609a43b20c7493c73d49966550a66 |
| Syed M. Hassaan, Qiang Shen, Sze Zheng Yong，*Path-Dependent Controller and Estimator Synthesis with Robustness to Delayed and Missing Data*，HSCC，2021 | 10.1145/3447928.3456655 | 7f80d95bf6e44b3c9068576351c47e0dbe0c46738b8cf40f2926fd0f972ffea7 |

另重查 Haimovich 等 Thm. 1 的规则采样最优微分精度，以及 Köhler 等 Thm. 4 对一步预算、移位与终端的要求。上述重读不增加阶段 2 书目数；本次论文实验复现数为零。与本地端点、对象及估计器的对应关系见[阶段 4 定题建议](../research/final_research_topic.md)。[最优微分作者稿](https://arxiv.org/pdf/2106.05320) · [在线估计界作者稿](https://arxiv.org/pdf/2105.03427)

## 2026-11-05 — 已选 A 的专项反方评审

从 M8 的前向引文定向核查 Syed M. Hassaan、Sze Zheng Yong，*System-Level Recurrent State Estimators for Affine Systems Subject to Data Losses Modeled by Automata*，IEEE CDC，2022，DOI 10.1109/CDC51059.2022.9992499。已阅读原文 Assumption 1、Definitions 4–5 与 Theorem 2 的问题和保证。其对有界仿射系统的缺测自动机构造路径和回返节点的恢复界，要求研究 A 明确延迟状态增广后究竟多得到什么。原文的缺测语义和估计器类别需对齐；用它否定一般的“首次重复恢复”有依据，用它否定 A 的所有窄命题仍证据不足。[CDC 原文](https://par.nsf.gov/servlets/purl/10411809)

六份主来源 PDF 的实际获取与 SHA-256、双库查询、引文边和限流记录见[原文指纹](../research/stage4_critique_A/primary_sources.json)与[检索记录](../research/stage4_critique_A/search.json)。本轮新增的是针对 A 的适用条件比对和本地信息价值算例；论文实验复现数为零，阶段 2 的固定书目快照沿用原计数。[审稿意见与数学核验](../research/stage4_critique_A/REVIEW.md)

## 2026-11-05 — Hassaan–Yong CDC 2022 可归约性补证

对照式 (1)、Definitions 1–5、Assumption 1、式 (2)–(5) 与定理 2 式 (18)–(19)，核查了整组观测有/无、已知观测矩阵、当拍残差用于下一估计、从直接路径起点误差球重新准入等条件。PDF 排版第 4118 页给出无穷范数。与前次记录一致的原文 SHA-256 为 023e728b05be57abe5053f8a6687912d5295c0065335594902f72afbc7be416a。ACC 2019 中的观察器误差增广与保存延迟位置的状态寄存器应分别理解。[CDC 原文](https://par.nsf.gov/servlets/purl/10411809) · [ACC 原文](https://bpb-us-e1.wpmucdn.com/sites/northeastern.edu/dist/e/2626/files/2020/04/Hassaan_ACC19.pdf)

本地有理数反例仅排除按物理拍合并成“有包/无包”的直接代换。统一缓冲至截止拍后可得到原文二值观测形式；本地紧恢复界来自独立的滑窗证明和极值证书，未声称复现 IEEE 仿射综合。查新状态保持未决，本文为已有论文复读。[逐项映射、数值及证据边界](../research/stage4_critique_A/CDC22_REDUCTION.md)

## 2026-11-05 — 选题 A 的控制侧信息增量

Florian D. Brunner、Matthias A. Müller、Frank Allgöwer，*Enhancing Output-Feedback MPC With Set-Valued Moving Horizon Estimation*，IEEE Transactions on Automatic Control 63(9)，2018，2976–2986，DOI 10.1109/TAC.2018.2791899。作者机构摘要明确将所用量测数量与预测步关联，并以此建立递归可行；本轮没有获得可核查的期刊逐定理文本。Köhler 等既有作者稿 Thm. 4 则明确需要新预算不超过此前一步预测预算，再作移位。本次重查不增加系统库条数。以上来源支持选择强基线，未据此认定本地条件检查具有新颖性。[Brunner 机构摘要](https://research.uni-hannover.de/en/publications/enhancing-output-feedback-mpc-with-set-valued-moving-horizon-esti/) · [Köhler 作者稿](https://arxiv.org/pdf/2105.03427)

本地新证书区分了原始速度约束、名义收紧行及最优首步。在所选可达记录上，提前一拍的数据改变了唯一最优首步；同信息精确增广得到相同结论。这里检验的是本地构造，论文实验复现数为零。[控制侧补证](../research/stage4_critique_A/CONTROL_PREFIX_SHIFT.md)

## 2026-11-05 — A 的固定窗口下界、条件删包与强基线

- Brunner 等，IEEE TAC 2018，DOI 10.1109/TAC.2018.2791899，2976–2986。复核作者机构摘要中逐预测步选择量测历史、递归可行及事前有界复杂度的原述。IEEE 正文入口返回验证页，OpenAlex DOI 记录与 Semantic Scholar 均未指向开放正文。CDC 2016（10.1109/CDC.2016.7798675）单列为会议版；Brunner 2017 年专著（ISBN 978-3-8325-4622-9）核至目录 §6.1，未将章节标题当作定理假设。[期刊机构记录](https://research.uni-hannover.de/en/publications/enhancing-output-feedback-mpc-with-set-valued-moving-horizon-esti/) · [作者机构会议版题录](https://www.irt.uni-hannover.de/en/forschung/publikationen/publikation-detail?tx_t3luhpublications_publications%5Baction%5D=show&tx_t3luhpublications_publications%5Bcontroller%5D=Publication&tx_t3luhpublications_publications%5Bpublication%5D=281) · [专著目录](https://www.logos-verlag.de/tocs/9783832546229toc.pdf)
- 复查 Köhler 等（arXiv:2105.03427）Thm. 4 的误差预算与移位条件、Nouwens 等（DOI 10.1016/j.automatica.2023.111243）作者稿 Thm. 1 中 C1/C2 的等价删约束条件，以及 Bemporad 等（DOI 10.1016/S0005-1098(01)00174-1）出版正文 Thm. 2 的参数 QP 分区。本地七格下界、删量测后的中点反馈反例为独立推导。本次未增加系统综述已读篇数。[Köhler 作者稿](https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf) · [Nouwens 作者稿](https://arxiv.org/pdf/2303.16581) · [Bemporad 出版正文](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf) · [本地逐项对照](../research/stage4_critique_A/PACKET_MEMORY_RESULT.md)

## 2026-11-05 — 阶段 5 冻结数学合同的两项原文依据

- J. K. Scott、D. M. Raimondo、G. R. Marseglia、R. D. Braatz，Automatica 69 (2016), 126–136，DOI 10.1016/j.automatica.2016.02.036。复核出版正文第 3 页 Prop. 1、式 (11)–(13) 的线性像、Minkowski 和与广义交集。阶段 5 仅借用其集表示；生成戳、启动时钟和六状态可观测秩由本地模型决定。[MIT 托管出版正文](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) · [数学模型](../research/mathematical_model.md)
- S. M. Hassaan、T. Pati、Q. Shen、S. Z. Yong，ADHS 2021，DOI 10.1016/j.ifacol.2021.08.482。复核作者稿第 5 页 Assumptions 1–3 及其引用的式 (12)、(18)，区分估计与跟踪误差要求、终端不变与下降条件。阶段 5 固定的是本项目的可见信息及比较目标。两项均为既有条目定向复读，保留原文献计数。[作者稿](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf) · [系统假设](../research/system_assumptions.md)

## 2026-11-05 — M2 取得 IEEE 期刊版，核对观测时钟、移位与复杂度

Florian D. Brunner、Matthias A. Müller、Frank Allgöwer，*Enhancing Output-Feedback MPC With Set-Valued Moving Horizon Estimation*，IEEE Transactions on Automatic Control，63(9)，2018，2976–2986。机构授权下载的出版版共 11 页，首页 DOI 为 10.1109/TAC.2018.2791899，文件 SHA-256 为 `913ea9eff1bdbd763f348863533a27a599d9fcd860b6a8eec30024d6ff3ffe29`。M2 从机构摘要升级为期刊正文定向核验，去重篇数沿用原计数。[IEEE 论文页](https://ieeexplore.ieee.org/document/8253530/) · [本地授权副本](sources/ieee_local/10.1109_tac.2018.2791899.pdf)

- **原文的可用信息。** 第 2979 页 Algorithm 1 每拍取得当拍输出并更新点估计。第 2980 页 §IV-A1、式 (18) 与 Remark 2 以窗口起点误差界及最近创新构造集合。即使集合估计省去较早的创新，点估计仍携带过去量测的信息。项目的固定原始时间窗下界限定了可用记忆；与本文比较时，点估计和误差界的存储也要计入。
- **移位条件。** 第 2979 页 Assumption 1、Theorem 1 把当前可行与下一拍可行联系起来。第 2980–2981 页 §IV-A2、Lemma 3 式 (22) 按预测步缩短所用创新历史，再接先验不确定性界，明确满足 Assumption 1 的前两项；终端另由 §IV-A3 处理。要迁移到本项目，还须对同一可见前缀下的乱序、空到达、同拍多包及每组相容读数重建这项移位包含关系。
- **复杂度的口径。** 第 2982 页 §IV-C 计数优化问题 (11) 的变量和约束，显式列出估计/预测时域、系统维度与多面体面数假设。本文给出了可实际核对的强基线；本项目能否在相同信息、相同保证下减少峰值存储，仍待证明。以上为原文定向比对，未复现论文数值实验。

<a id="b26-v1"></a>

## 2026-11-05 — B26 的采样数、最坏重构误差与阶段 5 的固定时间窗

Jerzy Baranowski，*Beyond Observability: Sharp Sample Bounds for Minimax State Reconstruction*。核对 arXiv 版本记录、PDF 首页版戳和本地文件：2610.26326v1 [eess.SY]，2026-10-19，28 页，586104 字节，SHA-256 为 `d1daa8eb6a9663825595eaa8249e897d734b20b7e720539b9e32f12d60d04c19`。登记的是公开预印本，DOI 10.48550/arXiv.2610.26326；提交页注明已投 *International Journal of Control*。本次将既有 B26 从摘要更新为指定页定向核读，保留原篇数。[版本记录](https://arxiv.org/abs/2610.26326v1) · [预印本 DOI](https://doi.org/10.48550/arXiv.2610.26326) · [本地 PDF](sources/arxiv/2610.26326v1.pdf)

| 原文定位（PDF 页码与印刷页码一致） | 已核结论及条件 |
|---|---|
| 第 3 页 §2.1，式 (2)–(8) | 在给定当前时刻 \(t\) 和回看时长内，用已知输入校正标量输出，得到关于**当前** \(x(t)\) 的观测矩阵 \(D\)。动力学无未知过程输入，量测误差逐样本满足绝对值界 \(\delta\)。作者在页末区分每次重构使用的样本数和滑窗维持样本可用所需的存储。 |
| 第 4 页命题 1，式 (9)–(12)；第 5 页首段 | 对满列秩 \(D\)，在无界状态空间、固定坐标和 \(\ell_\infty\) 误差下，所有估计器的全局最小最坏半径为 \(R^\star=\delta/\mu_\infty(D)\)，其中 \(\mu_\infty(D)=\min_{\lVert x\rVert_\infty=1}\lVert Dx\rVert_\infty\)。最优左逆达界，产生同一零观测的两状态给出下界。式 (7) 要求左逆，未对每组读数另加“估计点属于相容后验”的约束。不同物理单位可先按预定正对角尺度归一化。 |
| 第 5–6 页式 (13)–(18)、定理 1；第 22 页附录 A.1 式 (72) | 连续窗口内标量观测行张成 \(n\) 维空间。在给定 \(t\) 可选采样时刻时，无噪精确重构所需最少样本 \(m_{\rm obs}=n\)；达到完整连续历史同一最坏半径所需最少样本满足 \(n\le m_{\rm sat}\le n^2\)。上界对该系统类紧，由特构解析系统取到。第 6 页末明确取样时刻可随 \(t\) 改变。 |
| 第 11–12 页式 (55)–(60)、命题 3、表 1；第 27–28 页附录 B.4 式 (106)–(110) | 三层无阻尼楼体有六个状态，只测第一层位移。在 \([0,10]\) 内，六次标量采样可精确重构无噪状态，达到连续历史最优精度至少要七次。作者以区间证书排除六次并构造七个时刻；本文记录原文结论，未复跑其区间计算。 |

**阶段 5 对照。** 已知实际输入的补偿、确定性有界读数及满秩与误差半径的区分有正文依据。项目另设三轴共戳的三维位置包、每拍未知匹配加速度、紧先验、外生生成/延迟和合法历史。两戳保证在拍 5 才成立、六格/七格的紧速度半宽和四拍块末预算来自项目自己的时序与证书。比较精度时分别报告 m 与 m/s，若合并成一个范数须指明尺度。对给定历史要求同一可行代表点，还需在相容后验内验证其各坐标预算。G99 的期刊定义保留待核。[系统假设 §1–3](../research/system_assumptions.md) · [可观测性分析 §4 与单轴反例](../research/observability_analysis.md) · [固定时间窗证书](../research/stage4_critique_A/PACKET_MEMORY_RESULT.md)

**收件与物理依据。** 本次递归清点收件夹为 0 个文件。G99 仍为期刊题录与摘要，D4 仍为机构摘要；D4 所用的外环命令、实际可见量、平移扰动界来源及终端条件四项均待正文核对。把真实内环残差纳入匹配硬界仍是独立验证义务。[收件清单](FULLTEXT_DOWNLOAD_LIST.md) · [数学模型 §4](../research/mathematical_model.md)
