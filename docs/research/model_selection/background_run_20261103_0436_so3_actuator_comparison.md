# 背景深度调研：12状态刚体与MPC真实输入权限的跨论文对照（2026-11-03 UTC）

## 基线和研究范围
- 读取 main 基准 SHA：`9375b7d32de20233574e602ba762d889eeab8d98`；核验 CURRENT_CHECKPOINT、PAPER_READING_LOG、MODEL_SELECTION_EVIDENCE。
- 主任务仍为 Gate A blocked；12状态完整6DOF非线性 plant 是毕业仿真主对象，四状态和六状态平面作为证明/对照平台。
- 本轮围绕“12状态物理模型是否意味着单个12状态MPC直接控制四个电机”继续研究。与主任务分工：仅文献与建模审计，不开发控制器/测试。
- 本轮原始论文来源3篇：2024 Wehbeh/Sharf 开放正文复核（§2.1–2.3、§3.1、§6.2–6.3）；2022 Wehbeh/Sharf IEEE RA-L 原始论文书目和摘要核验（未获取全文，**仅摘要**）；2012 Alexis/Nikolakopoulos/Tzes 依据main既有已读原文记录作跨论文对照（**本轮未重新阅读全文**）。另回顾2021 Elokda等现有PR #162的正文核验结论。新全文读完0，正文部分复核1，新增摘要核验1，既有证据交叉对照2。不得把历史阅读计入本轮新增全文。

## 文献A：Wehbeh & Sharf (2024) [开放正文分节复核，DOI已登记]
Jad Wehbeh, Inna Sharf, *Nonlinear scenario-based model predictive control for quadrotors with bidirectional thrust*, International Journal of Robust and Nonlinear Control 34(18):12450–12475, DOI https://doi.org/10.1002/rnc.7627 ，开放全文 https://onlinelibrary.wiley.com/doi/full/10.1002/rnc.7627 。
- §2.1式(1)–(5)：plant 为 `r_a(3),v_a(3),C_ab∈SO(3),ω_b(3)`，局部12维刚体自由坐标；控制优化变量为逐桨有符号推力 `u=(T1,T2,T3,T4)`，通过 `[T;m_b]=Γu` 映射总推力/三力矩。四桨支持反向推力，**不能套用标准单向桨的非负域**。
- §2.2：独立电机、推力状态依赖的非线性速率约束；不是简单4个wrench各自限幅。§2.3 SO(3)李代数小误差线性化并零阶保持离散。
- §3.1、§6：scenario MPC对估计状态与质量/惯量不确定性采样；MEKF概率估计而非有界状态SMF/CZ；未处理环境扰动的确定性最坏情况。50Hz控制、预测网格40ms、Np=8、MATLAB Monte Carlo仿真。悬停恢复最大平均步成本det.MPC 7.39、MDSMPC(M=200) 3.67，只是统计性能指标，不是硬约束递归安全证书。求解器名称和端到端20ms WCET本轮未确认。
- 本论文已有总账条目，本轮不重复登记。

## 文献B：Wehbeh & Sharf (2022) [仅出版社摘要核验；全文未读]
*An MPC Formulation on SO(3) for a Quadrotor With Bidirectional Thrust and Nonlinear Thrust Constraints*, IEEE Robotics and Automation Letters 7(2):4945–4952, published 2022-02-24, DOI https://doi.org/10.1109/LRA.2022.3154021 ，出版社摘要 https://ieeexplore.ieee.org/abstract/document/9720938/ 。
- 摘要明确：SO(3)李代数时间依赖线性化、以QP实现预测控制、显式考虑双向推力非线性电机约束；仅仿真半翻滚、急转与桶滚，和Euler角NMPC基线比较。
- **未从全文确认**：精确12维状态排列、完整输入/状态/终端约束、估计器/传感器、采样周期、求解器、终端定理、实飞、WCET。2024论文§2明确把2022方法作为确定性MPC基线；这属于后文的交叉引用，不代表本轮读过2022全文。
- 不把“有非线性推力约束”写成标准单向桨的硬安全证明，也不把双向桨负推力权限迁移至普通四旋翼。

## 文献C：Alexis, Nikolakopoulos & Tzes (2012) [main既有全文记录，本轮仅复核账目]
*Model predictive quadrotor control: attitude, altitude and position experimental studies*, IET Control Theory & Applications 6(12):1812–1827, DOI https://doi.org/10.1049/iet-cta.2011.0348 ；原文 https://www.diva-portal.org/smash/get/diva2%3A980101/FULLTEXT01.pdf 。
- 已有总账证明原文12状态刚体plant，实际控制采用姿态、高度、平移PWA切换MPC子系统；输入总推力/力矩相关通道以及从四电机转速派生的Ωr，Ωr**不是第五个独立执行器**。
- 真实IMU、声呐、光流＋EKF室内实飞；不是统一12状态Tube MPC；切换稳定性和全状态递归硬安全未证。当前轮不重复宣称读过全文。

## 文献D：Elokda et al. (2021) [已有PR #162，本轮仅横向对照]
*Data-enabled predictive control for quadcopters*, DOI https://doi.org/10.1002/rnc.5686 ；12状态plant但实际DeePC外环使用两个角速度参考与总推力参考，底层姿态控制器闭环。既有PR #162仍open，不能把它当已并入main的结果。

## 跨论文结论与选型
| 文献 | 物理plant | MPC实际输入权限 | 估计/反馈 | 硬安全证据 |
| --- | --- | --- | --- | --- |
| Wehbeh/Sharf 2024 | SO(3)局部12维 | 四桨**有符号**推力＋非线性速率约束 | MEKF随机估计 | Monte Carlo，非确定性终端RCI |
| Wehbeh/Sharf 2022 | SO(3)模型（摘要） | 双向桨约束，精确维度待全文 | 未核验 | 摘要未确认 |
| Alexis等2012 | 12状态6DOF | 姿态/高度/位置分层PWA，Ωr派生 | EKF＋实飞传感器 | 切换全局稳定未证 |
| Elokda等2021 | 12状态6DOF | 三参考输入外环＋现有内环 | 外部动作捕捉 | DeePC非Tube MPC |

**主仿真plant决策不变**：12状态 `x=(p_I,v_I,η_ZYX,ω_B)`，`dot(η)=E(η)ω_B`；候选MPC wrench `w=(T,τx,τy,τz)` 必须经标准单向桨 `f_i≥0` 和上界/速率/执行误差检查，满足 `w=Gf`、`f_min≤G^{-1}w≤f_max`（G可逆时）。2024论文双向桨 `f_i<0` 的可行域不能作为本项目物理许可。12状态plant并不等于12状态单环MPC，仍须单独证明线性化残差管束、量测SMF包含和终端信息RCI。

## 未完成和下一轮续读位置
1. 2022 Wehbeh/Sharf IEEE RA-L DOI 10.1109/LRA.2022.3154021：目前仅出版社摘要；下一轮获取作者全文，逐式核对§动力学、MPC输入/电机速率约束和求解时延。
2. 2024 Wehbeh/Sharf：补查附录推力速率模型和§5 MEKF误差分布；确定与标准单向桨的可迁移部分。
3. 找到至少一篇**标准单向桨、12状态刚体plant、直接四输入MPC**的全文原始论文，核对实际电机分配和非线性残差。
4. 仅文献审计，不产生新控制器/测试/终端证明；Gate A blocked。唯一优先研究问题：标准单向桨四输入MPC的真实可执行输入域是否有全文可核验证据。
