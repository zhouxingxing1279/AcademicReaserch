# 外环 MPC、12 状态物理 plant 与 SMF/CZ 文献证据

> 目的：为“成熟飞控负责底层稳定控制、外环 MPC 负责任务/轨迹指令、12 状态四旋翼作为仿真物理对象”的研究背景建立可追溯证据。本文区分全文/正文分节、摘要、书目核验；摘要不能支持未公开的模型矩阵、定理假设或实时性能结论。

## 1. 先分清三个维度

- **物理仿真对象**：12 状态六自由度四旋翼刚体模型（位置 3、速度 3、姿态 3、角速度 3），由成熟飞控在仿真闭环中控制底层姿态、角速度、分配和电机。
- **外环预测状态**：可先从 6 状态平移状态 \([p^T,v^T]^T\) 起步；若姿态/角速度、飞控瞬态或参考跟踪滞后对约束有实质影响，必须增广预测状态或采用经验证的 12 状态闭环模型。
- **外环优化输入**：position/velocity/acceleration setpoint 之一，依实际飞控接口选择；不能把“12 状态物理 plant”误读为“外环优化器直接输出四个桨推力”。

因此，完整 12 状态物理仿真与 6 状态外环预测并不矛盾。降阶是否合法取决于闭环残差和约束影响能否被可靠外包，而不是为了减小维数而先验删掉姿态动态。

## 2. 直接四旋翼外环 MPC 证据

| 文献 | 论文中实际架构/证据等级 | 对本课题支持什么 | 不能直接推出什么 |
|---|---|---|---|
| Santos & Lagoa (2022), *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, ISA Transactions 128:123–135, [DOI](https://doi.org/10.1016/j.isatra.2021.12.002) | 本轮为机构/出版社摘要和书目信息核验；摘要描述 supervisory outer wayset guidance，假设已有稳定姿态/位置内环，使用降阶闭环平移离散模型、有界加性扰动和测量噪声 | 直接支持“成熟内环之上做外环 Tube MPC”的研究架构 | 不证明 PX4/ArduPilot 的具体 setpoint 模型；不提供本项目所需 A/B、采样/时域、位置丢包自动机或内环误差界 |
| Andriën et al. (2024), *Model Predictive Control for Quadcopters With Almost Global Trajectory Tracking Guarantees*, IEEE TAC 69(8):5216–5230, [DOI](https://doi.org/10.1109/TAC.2023.3349098) | 机构摘要/既有正文摘录交叉核验；外环产生平滑加速度参考，作者设计的非线性姿态/角速度内环跟踪 | 支持加速度参考型级联外环是有真实论文先例的 | 几乎全局跟踪结论属于论文特定非线性内环，不可直接迁移为 PX4 黑盒的保证 |
| Izadi et al. (2024 preprint; later 2026 publication record), *High-Performance Model Predictive Control for Quadcopters with Formal Stability Guarantees*, [arXiv:2412.20277](https://arxiv.org/abs/2412.20277) | 本轮仅核验预印本摘要；外环加速度参考经姿态/角速度参考传给非线性内环。正式 Automatica 终版与预印本差异尚未逐项核验 | 作为加速度参考级联结构的补充线索 | 不应把预印本摘要当成正式终版全文，也不能移植其定理到现成飞控 |
| Xue et al. (2024), *Output feedback stochastic MPC for tracking control of quadrotors with disturbances*, IET Control Theory & Applications 18(5):566–580, [DOI](https://doi.org/10.1049/cth2.12588) | 仓库已有公开正文分节摘录；外环 6 维位置/速度 + 3 维风增广状态，虚拟三轴加速度输入，姿态 ADRC/ESO 内环；每拍获得带噪位置和速度 | 证明“外环输出反馈 MPC + 内环姿态控制”在四旋翼研究中有文献先例 | 不是位置-only 间歇量测；其机会约束/随机保证不等于确定性硬安全；虚拟加速度不是 PX4 实际加速度跟踪保证 |

## 3. 12 状态物理模型与控制权限证据

### Elokda et al. (2021)：物理状态维数与优化器输入维数不同

E. Elokda, J. Coulson, P. N. Beuchat, J. Lygeros, F. Dörfler, *Data-enabled predictive control for quadcopters*, International Journal of Robust and Nonlinear Control 31(18):8916–8936 (2021), [DOI](https://doi.org/10.1002/rnc.5686), [开放全文](https://onlinelibrary.wiley.com/doi/full/10.1002/rnc.5686).

- 本轮在期刊 HTML 中阅读 §1、§2.1–2.3，属于**部分正文阅读**，不是全文通读。
- §2.1 的物理四旋翼刚体模型是 12 状态：惯性位置 3、惯性速度 3、ZYX Euler 姿态 3、机体系角速度 3。裸物理模型的原始执行输入是四个桨的推力。
- 论文的实际商用四旋翼架构保留厂商 IMU 内环，外部优化器不能直接命令四个桨；外部优化器使用三个参考输入：两个机体角速度参考和总推力参考。反馈由外部 motion-capture 提供位置与姿态五个输出，偏航内环由厂商实现。
- 若把厂商内环和电机电流动态视为未知，外环黑盒状态可能不止 12 维。论文主要方法为 DeePC，并有 model-based MPC 比较；不是 Tube MPC，也不是 SMF/CZ。
- 该论文是“12 状态物理对象与外部优化器输入权限可分离”的重要架构证据，但其三个参考输入不是本课题当前优先考虑的位置/速度/加速度接口，不能把它误写成 PX4 Offboard 直接证据。

### Bezerra & Santos (2022)：完全驱动旋翼的分配证明不能照搬

J. A. Bezerra & D. A. Santos, *On the guidance of fully-actuated multirotor aerial vehicles under control allocation constraints using the receding-horizon strategy*, ISA Transactions 126 (2022):21–35, [DOI](https://doi.org/10.1016/j.isatra.2021.07.019).

PR #170 的核验等级为摘要/书目。摘要所述对象为具有双自由度可转向旋翼的 fully-actuated multirotor，内层逆动力学与凸优化分配；其分配可行性证明不能直接移植到标准固定轴、单向推力四旋翼。

### Recalde et al. (2022)：商用飞控速度命令的补充证据

L. Recalde et al., *Constrained Visual Servoing of Quadrotors Based on Model Predictive Control*, IFAC-PapersOnLine 55(37) (2022):353–360, [公开记录](https://repositorio.uti.edu.ec/items/04944da2-e8b0-46b4-b8e3-b7c65493dc25).

PR #170 仅核验摘要。论文摘要描述基于图像的视觉伺服 MPC，以商业 Mavic Pro 2 的速度命令简化模型为对象，并通过 Webots 仿真比较；精确状态维数、速度命令动态与求解细节未从全文核实。它支持速度命令型外环存在工程先例，不等于 PX4 的同一闭环合同。

## 4. SMF/CZ 输出反馈理论证据

| 文献 | 核验范围 | 可借鉴点 | 迁移限制 |
|---|---|---|---|
| Reis de Souza, Efimov & Raïssi (2022), *Robust Output Feedback MPC for LPV Systems Using Interval Observers*, IEEE TAC 67(6):3188–3195, [DOI](https://doi.org/10.1109/TAC.2021.3099449) | 出版社摘要/书目信息 | LPV 区间观测器与输出反馈 MPC 的集合约束、递归可行框架 | 通用 LPV，不是四旋翼，也未覆盖本项目实际丢包自动机 |
| Qiu et al. (2020), *Output feedback model predictive control based on set-membership state estimation*, IET Control Theory & Applications 14(4):558–567, [DOI](https://doi.org/10.1049/iet-cta.2019.0881) | 公开正文 §2–5 文字/定理叙述分节核验；图片公式未全部逐式检查 | SMF 状态集合到输出反馈 MPC 约束/终端条件的理论接口 | 非四旋翼；其测量假设不等于本项目异步位置失测合同 |

## 5. 证据综合与当前模型决策

1. 选择**12 状态六自由度刚体作为仿真物理对象**，由成熟飞控在 SITL/HIL 中负责姿态/角速度、分配和电机，是合理且有 12 状态真实四旋翼模型论文先例的研究背景。
2. 外环 MPC 不因此获得四桨推力或 wrench 权限。优先比较位置参考、速度参考和加速度参考三种高层接口；其中 PX4 ROS 2 position setpoint 暂为首要辨识候选，而不是已冻结的闭环 plant。
3. 外环预测模型可先使用六维 \([p,v]\) 平移状态；但必须用 12 状态物理仿真验证其在姿态瞬态、限幅、延迟和扰动下的残差覆盖。若不成立，增广预测状态，不能将姿态动态当作零。
4. 位置/速度/加速度 setpoint 都只是请求命令。Tube 扰动集合必须覆盖真实闭环跟踪误差与饱和；没有确定性残差外包时，不得宣称硬安全。
5. Xue 的每拍位置+速度随机输出反馈、通用 LPV/椭球 SMF 文献、以及 Elokda 的厂商内环架构，都不能单独证明本项目的“间歇位置测量 + CZ 状态包含 + Tube MPC 递归硬安全”。

## 6. 来源 PR 与整合边界

- [PR #184](https://github.com/zhouxingxing1279/AcademicReaserch/pull/184)：四旋翼外环 MPC 与 SMF/CZ 文献交叉核验。
- [PR #162](https://github.com/zhouxingxing1279/AcademicReaserch/pull/162)：Elokda 12 状态物理 plant 与真实优化器输入权限审计。
- [PR #170](https://github.com/zhouxingxing1279/AcademicReaserch/pull/170)：Wayset 外环、完全驱动可转向旋翼与商用速度命令文献比较。
- PR #162 与 #170 的分支相对当前 main 已分别落后 11 和 9 个提交且发生 diverged；本文按已审查内容移植其可用证据，不合并或改写原分支。
- 本文不新增“已读全文”记录，不声称实现 SMF/CZ、Tube MPC、SITL/HIL 或递归可行性证明。
