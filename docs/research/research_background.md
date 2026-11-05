# 阶段 1 · 四旋翼外环 MPC 与集员估计的研究背景

在位置包迟到的那一拍，外环必须先决定给飞控什么命令。此时同一段已收位置记录可能对应多个速度。已有研究分别给出了有界误差下的状态估计、有限量测语言下的恢复控制，以及多旋翼上的 Tube MPC。比较这些结果，首先要问控制器当时收到了什么、其输入作用在哪一层、保证对哪些扰动和时间序列成立。[外环模型合同](MODEL_CONTRACT.md) · [技术路线](research_technology_map.md) · [待判定问题](research_questions.md)

本阶段于 2026-11-05 完成定向背景阅读。项目事实取自本地已提交文件与未提交研究材料，文献取自本地原文、在线论文和标明范围的既有笔记。下文的 D、M、F 分别索引直接相关工作、可迁移方法和基础理论。末表给出 21 项文献及本轮使用的证据层级，编号只用于这三份阶段文档。

## 1. 四旋翼 MPC 的问题分工

跟踪、感知与抗扰约束解决的是不同任务。Falanga 等在机载视觉跟踪中把特征可见性写入优化代价。Elokda 等在真实四旋翼上比较由历史输入输出驱动的预测控制与模型式 MPC。Xue 等把风扰与跟踪放进外环随机 MPC。Ji 等则问有界状态和量测扰动下怎样收紧硬约束。四者的实验即使都报告跟踪误差，也不能仅凭这一指标比较间歇量测下的硬约束保证。参见 D1–D3、D5。

## 2. 外环位置与速度的建模

本课题物理对象有三维位置、速度、姿态及角速度。成熟飞控闭合姿态、角速度与执行链。外环预测使用六状态 \(x=[p^\top,v^\top]^\top\)，位置输出 \(C_p=[I_3\ 0]\)。Elokda 的物理仿真用十二状态，实际外部控制器向内环给参考量。Xue 的外环则将六维平移量增广三维风状态，并在每拍量测中同时使用位置和速度。两例说明，物理维数、优化器状态和传感器输出必须分别记录。具体应用到本课题，还要给出从内环跟踪偏差到 \(G\mathcal W\) 的覆盖条件。一般模型的 \(u\) 保持抽象，仅在注明的 ZOH 算例中具有加速度量纲。参见 D1、D2、D4。[模型合同](MODEL_CONTRACT.md)

## 3. 无人机上的 Tube MPC

Santos–Lagoa 的上层导航假定位置和姿态稳定环可用，通过时间尺度分离得到平移预测模型。Parsi 等的四旋翼算例采用近悬停模型、四个旋翼推力输入与椭球管，控制器可使用状态测量。Delansnay 等在六旋翼上用闭环辨识得到的速度及偏航模型和辅助反馈进行室外试验。前者支撑分层建模，中者展示特定输入约束及不确定性下的 Tube，后者提供多旋翼闭环实验先例。把这些结果用于仅测位置的外环，需另提供辅助反馈实际能使用的状态信息。参见 D4、D6、M6。[多旋翼实验论文](https://doi.org/10.1109/CoDIT66093.2025.11321702)

## 4. SMF 的真值包含与最优后验

SMF 问哪些状态与已收观测、已施加输入及硬误差界同时相容。Cong 等的 Thm. 1 把最小相容集写成条件值域。已知边际界时，把扰动与历史状态分别取极值可给出包含真值的外包。若还要声称得到精确后验，Thm. 2 的“无关联”条件或对联合约束的显式保留才有依据。同一个物理扰动应在历史轨迹的不同方程中共享变量。非退化高斯误差有无界支持，用其有限分位数建立的集合只能提供相应概率解释。EnKF 用样本估计统计量，本文所需 SMF 则检验所有与硬界相容的真值。参见 F3、M3。[Cong 等，本地原文](../literature/sources/cong_mpc_20261104/2004.04524.pdf)

## 5. 盒、zonotope、CZ 与椭球

对单个约束面 \(a^\top x\le b\)，控制器需要方向支持值 \(h_S(a)=\sup_{s\in S}a^\top s\)。表示的选择取决于哪些方向约束会激活，以及测量更新会留下哪些相关性。

| 表示 | 方向支持或更新 | 在本研究中的用途 |
|---|---|---|
| 坐标盒，中心 \(c\)、半径 \(r\) | \(a^\top c+\lvert a\rvert^\top r\) | 预算便于复算。丢失位置–速度相关性时可能拒绝原本存在的共同输入 |
| Zonotope \(c+D[-1,1]^g\) | \(a^\top c+\|D^\top a\|_1\) | 线性像与 Minkowski 和保留生成元相关性。量测切片后的精确几何可能偏离中心对称 |
| CZ，另带 \(F\xi=f\) | 在线性等式及 \(\|\xi\|_\infty\le1\) 下求方向 LP | 可在共享历史生成元上叠加量测等式。比较代价时要计生成元、等式、LP 数及耗时。选取 \(\hat x\) 需有可行见证 |
| 椭球 \(c+D\mathbb B_2\) | \(a^\top c+\|D^\top a\|_2\) | Ji 等以椭球扰动直接算收紧，Parsi 等使用固定形状缩放管。与 CZ 的对照须固定原始噪声支撑或解释外包差别 |

Scott 的 Prop. 1 给出 CZ 线性像、和及广义交集的表示。Rego 的非线性预测还要包络余项。Qin 等的有限窗 CZ 一致有界性定理给出了窗长与可检测性条件。选较复杂的表示能否改善控制，仍取决于活跃约束面上的支持是否缩小。参见 F1、F2、M4、D3、D6。[Scott 等，Prop. 1](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) · [本地共同输入算例](cz_startup_predecessor.md)

## 6. 间歇、丢失与延迟量测

在决策时刻 \(k\)，可使用的是已经交付的包及其**生成时间戳**。迟到的 \(y_s\) 约束 \(x_s\)。历史更新要保留随后已经收到的量测约束，并沿已经施加的输入传播到 \(k\)。等价做法是在共享轨迹变量上加入该历史约束再投影。离线平滑允许以后获得的资料重估过去。在线重算则只使用截至当下收到的资料，先前实际发出的命令已确定。参见 M5、M8、F3。

三类论文的时间假设尤其值得区分。Meslem 等的式 (11) 在规定采样机会给出 \(Cx_{k-s}\) 的有噪读数，Assumption 1 针对给定稀疏指数检验可检测性。Hassaan 等以固定长度的允许词与可见事件前缀处理不同到达模式。Yan 等采用有成功概率的 Bernoulli 到达，约束折扣期望二阶矩。三者分别适合做周期延迟基线、全允许词恢复基线和随机性能对照。采用随机丢包率时，还须另立确定性条件才有最大陈旧年龄保证。参见 M7、M8、M3。[Meslem 等会议展示稿，式 (8)–(15)](https://css.paperplaza.net/images/temp/CDC/files/2323.pdf#page=1) · [Hassaan 等估计器论文](https://arxiv.org/pdf/2101.03389)

## 7. 从集员估计到输出反馈控制

用 \(z\) 表示名义状态，\(\varepsilon=x-\hat x\) 表示估计误差，\(e=x-z\) 表示跟踪误差。实际命令只能根据已收历史构造。在线性反馈 \(u=\bar u+K(\hat x-z)\) 下，控制修正取决于 \(e-\varepsilon\)。仅给出估计误差直径，还缺少跟踪误差如何传播以及修正项占用多少输入余量。Mayne 等给出固定误差管的输出反馈框架。Hassaan 的 HSCC 工作将可见前缀一致性纳入联合控制器／估计器综合，IFAC 工作进一步使用时变管收紧名义 MPC。Ji 的十二状态数值例采用 \(C=I_{12}\)，因此仍需单独解决本项目的位置包到达前隐藏速度的歧义。参见 F5、M9、M1、D3。[HSCC 论文，Thm. 3.2](https://qiangs.github.io/Papers/Conf_HSCC2021Hassaan.pdf) · [Ji 等，§V-B](https://arxiv.org/pdf/2008.04980)

## 8. 共同终端、递归可行与稳定性

递归可行要求在下一拍实际收到的**每一种相容量测历史**下还能构造可行计划。Hassaan 等先要求估计与跟踪误差满足相位界，再要求同一个终端集合与终端反馈适用于全部相关相位。对其名义问题，初始可行与终端条件使旧解能移位并在末端追加反馈。稳定性还使用终端代价下降条件。Brunner 等的摘要给出另一条线索，即越远的预测步使用越少的历史量测，以保持计划可移位。本地阶段 1 对照所需的下一层证据是两种时间结构是否兼容。持续有界扰动下，真实状态的结论应表述为相应集合附近的有界性或原文给出的集合稳定性。参见 M1、M2、F5、F6。[Hassaan 等，Assumptions 1–3、Thms. 5–7](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf) · [Brunner 等机构摘要](https://research.uni-hannover.de/en/publications/enhancing-output-feedback-mpc-with-set-valued-moving-horizon-esti/)

## 文献定位与阅读层级

“在线正文”和“本地原文”均为本轮定向核查指定部分。“既有笔记”保留仓库先前的阅读范围。摘要支持架构与研究目标，详细定理条件另列待查。DOI 对应出版版本，作者稿按下方链接定位。

| 编号 | 作者、题名与出处 | DOI | 本轮证据与定位 |
|---|---|---|---|
| D1 | Elokda, Coulson, Beuchat, Lygeros, Dörfler. *Data-enabled predictive control for quadcopters*. IJ Robust Nonlinear Control, 2021 | 10.1002/rnc.5686 | 既有笔记，§2.1–2.3、§3.4，物理模型与外部参考输入。[外环资料](model_selection/OUTER_LOOP_MPC_LITERATURE.md) |
| D2 | Xue, Dai, Wang, Sun, Xia. *Output feedback stochastic MPC for tracking control of quadrotors with disturbances*. IET CTA, 2024 | 10.1049/cth2.12588 | 既有笔记，式 (2.3)、(2.11)，每拍位置与速度、概率收紧。[分节笔记](model_selection/background_run_20261101_1136_xue_output.md) |
| D3 | Ji, Geng, Driggs-Campbell. *Robust Output Feedback MPC with Reduced Conservatism under Ellipsoidal Uncertainty*. CDC, 2022 | 10.1109/CDC51059.2022.9992704 | 在线正文，§V-B，近悬停线性化、采样 0.2 s、单位输出矩阵。[作者稿](https://arxiv.org/pdf/2008.04980) |
| D4 | Santos, Lagoa. *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*. ISA Transactions, 2022 | 10.1016/j.isatra.2021.12.002 | 在线机构摘要，稳定内环与时间尺度分离。具体输出矩阵、终端条件待正文。[培养单位记录](https://flavioluiz.github.io/pgeam/en/publicacoes/85122342732/) |
| D5 | Falanga, Foehn, Lu, Scaramuzza. *PAMPC: Perception-Aware Model Predictive Control for Quadrotors*. IROS, 2018 | 10.1109/IROS.2018.8593739 | 既有笔记，式 (1)–(13)、机载视觉实验，感知项为代价。[分节笔记](model_selection/background_run_20261102_2337_falanga_vio_data_access.md) |
| D6 | Parsi, Iannelli, Smith. *Scalable tube model predictive control of uncertain linear systems using ellipsoidal sets*. IJ Robust Nonlinear Control, 2025 卷期，2022 在线 | 10.1002/rnc.6485 | 既有笔记，Thm. 1 与 §5.2，椭球 Tube 和四旋翼算例。[模型笔记](model_selection/background_run_20261103_1240_threepaper_tube_mpc_audit.md) |
| M1 | Hassaan, Pati, Shen, Yong. *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*. IFAC-PapersOnLine, 2021 | 10.1016/j.ifacol.2021.08.482 | 在线正文，Def. 3、§3、Assumptions 1–3 与 Thm. 6，周期语言与共同终端。[作者稿](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf) |
| M2 | Brunner, Müller, Allgöwer. *Enhancing Output-Feedback MPC With Set-Valued Moving Horizon Estimation*. IEEE TAC, 2018 | 10.1109/TAC.2018.2791899 | 在线机构摘要。已核对预测步依赖的历史量测数与有界复杂度，精确移位条件待全文。[机构记录](https://research.uni-hannover.de/en/publications/enhancing-output-feedback-mpc-with-set-valued-moving-horizon-esti/) |
| M3 | Yan, Cannon, Goulart. *Stochastic output feedback MPC with intermittent observations*. Automatica, 2022 | 10.1016/j.automatica.2022.110282 | 既有笔记，式 (6)、Thms. 7、9，创新反馈与折扣期望约束。[分节笔记](model_selection/background_run_20261102_0634_yan_stochastic_contract.md) |
| M4 | Qin, Cong, Wang, Liu. *A Fast and Accurate Linear Constrained Zonotopic Set-membership Filter*. IEEE TAC, 2026，依本地题录 | 10.1109/TAC.2026.3712691 | 本地原文，Thms. 1–2，窗长、可检测性与参数化计算复用。[本地 PDF](../literature/sources/cong_mpc_20261104/A_Fast_and_Accurate_Linear_Constrained_Zonotopic_Set-membership_Filter.pdf) |
| M5 | Li, Cong, Zhou, Dong. *Optimal Set-Membership Smoothing*. IEEE TAC, 2026 卷期，2025 在线 | 10.1109/TAC.2025.3632158 | 本地作者稿，Thm. 1 式 (8)、Cor. 1，非随机 HMM 下给定全部已知资料的回溯条件集。[本地 PDF](../literature/sources/cong_mpc_20261104/2410.09857.pdf) |
| M6 | Delansnay, Dewasme, Vande Wouwer. *Experimental Validation of Zonotopic Tube-MPC Applied to a Hexacopter*. CoDIT, 2025 | 10.1109/CoDIT66093.2025.11321702 | 在线论文摘要及既有分节记录，六旋翼、外扰、名义 MPC 加辅助状态反馈。[会议原文](https://www.codit2025-virtual-event.com/web/content/1364?download=true&unique=38ac7e7f7fb54cda0d6a9efdec7a04e7817a09c7) |
| M7 | Meslem, Hably, Wang, Raïssi. *Set-Valued State Estimator With Sparse and Delayed Measurements for Uncertain Discrete-Time Linear Systems*. IEEE Control Systems Letters 8, 904–909, 2024 | 10.1109/LCSYS.2024.3405376 | 在线会议展示稿，式 (8)–(15)、Assumption 1、区间预测。期刊论文及 CDC 展示合计一项。[原文](https://css.paperplaza.net/images/temp/CDC/files/2323.pdf#page=1) · [作者 HAL 记录](https://cv.hal.science/nacim-meslem) |
| M8 | Hassaan, Shen, Yong. *Equalized Recovery State Estimators for Linear Systems with Delayed and Missing Observations*. IEEE Control Systems Letters, 2022 卷期 | 10.1109/LCSYS.2021.3050300 | 在线作者稿，§II-B、Defs. 2、6、Ex. 3，允许词到可见事件前缀的映射。[作者稿](https://arxiv.org/pdf/2101.03389) |
| M9 | Hassaan, Shen, Yong. *Path-Dependent Controller and Estimator Synthesis with Robustness to Delayed and Missing Data*. HSCC, 2021 | 10.1145/3447928.3456655 | 在线正文，Thm. 3.2、式 (26)，全允许事件词、共同前缀与鲁棒合成可行条件。[作者稿](https://qiangs.github.io/Papers/Conf_HSCC2021Hassaan.pdf) |
| F1 | Scott, Raimondo, Marseglia, Braatz. *Constrained zonotopes: A new tool for set-based estimation and fault detection*. Automatica, 2016 | 10.1016/j.automatica.2016.02.036 | 在线正文，Prop. 1 式 (11)–(13)，CZ 运算。[期刊 PDF](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) |
| F2 | Rego, Raffo, Scott, Raimondo. *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*. Automatica, 2020 | 10.1016/j.automatica.2019.108614 | 在线正文，§2 式 (1)，光滑非线性过程、线性量测、有界不确定性；§4 方法范围。[作者稿](https://arxiv.org/pdf/1908.09950) |
| F3 | Cong, Wang, Zhou. *Rethinking the Mathematical Framework and Optimality of Set-Membership Filtering*. IEEE TAC, 2022 | 10.1109/TAC.2021.3082508 | 本地作者稿，Thms. 1–2、式 (13)–(16)、Assumption 1，条件值域与无关联假设。[本地 PDF](../literature/sources/cong_mpc_20261104/2004.04524.pdf) |
| F4 | Cong, Wang, Zhou. *Stability of Linear Set-Membership Filters With Respect to Initial Conditions: An Observation-Information Perspective*. Automatica, 2025 | 10.1016/j.automatica.2024.111993 | 本地作者稿 v2，Thm. 1 式 (16)，可观测、A 非奇异、连续观测窗长度满足条件时的 OIT 直径界。[本地 PDF](../literature/sources/cong_mpc_20261104/2203.13966.pdf) |
| F5 | Mayne, Raković, Findeisen, Allgöwer. *Robust output feedback model predictive control of constrained linear systems*. Automatica, 2006 | 10.1016/j.automatica.2006.03.005 | 既有总账的 Run221 正文笔记，§§2–4，估计与控制误差管、初始准入及终端条件。[阅读总账](../literature/PAPER_READING_LOG.md) |
| F6 | Raković, Kerrigan, Kouramas, Mayne. *Invariant approximations of the minimal robust positively invariant set*. IEEE TAC, 2005 | 10.1109/TAC.2005.843854 | 既有总账及专项笔记，扰动集合与缩放包含的适用条件。对低维扰动像须检查尾项。[本地数学审计 §3](proposal/OIT_MRPI_THEORY_AUDIT.md) |

阶段 2 宜优先取得 M2 的期刊正文，核实预测步如何选择历史量测、哪些后继信息可使移位成立。D4 的采样与终端条件仍为全文待查项。阶段 1 据已核实材料确定比较问题，创新性判断留在系统对照之后。
