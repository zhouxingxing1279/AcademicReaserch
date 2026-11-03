# 外环MPC与SMF/CZ文献交叉核验（2026-11-03 UTC）

## 核验范围和状态
基准main eb18e857090b0babe531c13c61aea944793af428。本轮核验4篇原始期刊论文的出版社/大学公开摘要及书目，其中直接四旋翼外环MPC 2篇；1篇IET公开正文分节核验（但公式图片未全部逐式核对）；其余3篇仅摘要/书目核验。**不将摘要核验标记为全文已读**，不将本轮论文计作新全文阅读。Automatica 2026为额外书目线索，尚未全文核验。

## 论文及模型/接口证据
1. A.R.P. Andriën, E. Lefeber, D.J. Antunes, W.P.M.H. Heemels, *Model Predictive Control for Quadcopters With Almost Global Trajectory Tracking Guarantees*, IEEE TAC 69(8):5216–5230 (2024), DOI https://doi.org/10.1109/TAC.2023.3349098 。大学公开书目与摘要 https://research.tue.nl/en/publications/model-predictive-control-for-quadcopters-with-almost-global-traje/ 。外环MPC产生二阶可微加速度参考，转换为姿态/角速度/加速度参考，由**作者非线性内环**跟踪；推力上下界；闭环跟踪几乎全局渐近稳定；数值案例。不是PX4黑盒或直接电机MPC。状态向量/采样周期/求解器本轮未逐式核验。
2. D.A. Santos, C.M. Lagoa, *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, ISA Transactions 128:123–135 (2022), DOI https://doi.org/10.1016/j.isatra.2021.12.002 。作者/机构摘要 https://pure.psu.edu/en/publications/wayset-based-guidance-of-multirotor-aerial-vehicles-using-robust-/ 。外环为监督式wayset引导Tube MPC，低层姿态与位置稳定控制器**假定已存在**，采用闭环平移降阶线性模型、有界加性扰动和测量噪声；论文分析递归可行、鲁棒稳定，数值四旋翼仿真。**不能声称直接验证PX4**；实际位置命令与具体A/B矩阵本轮未核对原文。
3. A. Reis de Souza, D. Efimov, T. Raïssi, *Robust Output Feedback MPC for LPV Systems Using Interval Observers*, IEEE TAC 67(6):3188–3195 (2022), DOI https://doi.org/10.1109/TAC.2021.3099449 。出版社摘要 https://ieeexplore.ieee.org/document/9496205/ 。通用离散约束LPV，区间观测器更新SMF集合、区间预测器进入MPC，给出递归可行/约束/终端ISS条件；非四旋翼，未覆盖本课题具体失测自动机。
4. Q. Qiu, F. Yang, Y. Zhu, E. Mousavinejad, *Output feedback model predictive control based on set-membership state estimation*, IET Control Theory & Applications 14(4):558–567 (2020), DOI https://doi.org/10.1049/iet-cta.2019.0881 。公开正文 https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-cta.2019.0881 。§2–5文字与定理叙述核验，椭球SMF→输出反馈MPC→预测约束LMI/终端条件，仿真与DC-DC例；不是四旋翼，逐拍量测假设与失测条件不同，未逐式审计图片公式。

## 横向比较和决策
- **首选条件性架构**：成熟飞控预稳定内环 + 外环位置/速度闭环平移plant（可先以6状态[p,v]作候选），MPC位置参考输入与加速度参考输入必须分别建模，不能把加速度虚拟输入与飞控实际电机控制量混淆。
- Santos/Lagoa直接支撑“预稳定内环 + 外环Tube MPC”；Andriën直接支撑“外环加速度参考 + 非线性姿态内环”，但二者均**不直接证明PX4/ArduPilot黑盒的误差界**。
- IEEE TAC LPV区间观测器和Qiu椭球SMF提供状态集合→约束/终端安全的理论接口；**没有证明它们能直接迁移到四旋翼异步失测+PX4闭环模型**。
- 与main当前冻结平面6状态[p_x,p_z,v_x,v_z,phi,omega]、(T,tau)输入及4状态Euler证明模型的关系：这些属于直接刚体/姿态权限的模型，**不是**新的6状态三维[p,v]预稳定外环plant；既有Run246/260/261/278安全证据不可直接转移。主研究任务需要重新确定闭环接口和扰动界；本任务不改其代码。
- CZ vs椭球 vs区间的严格保守性与预算优劣仍无实证。SMF后验集合必须可靠外包；预测Tube与后验集合是不同对象。飞控EKF已融合输出不能与原始IMU重复当独立测量。

## 证据缺口与唯一优先问题
尚未核验原始论文的精确A/B矩阵、外环输入约束、采样/时域/求解器和传感器；未完成PX4接口代码与内环误差/延迟/饱和实证，未获得有界噪声标定、SMF失测后验、终端信息RCI或闭环MPC安全证书。**Gate A=blocked**。下一轮唯一优先问题：获取并逐式核验Santos/Lagoa全文中位置指令→闭环平移状态模型的控制权限、采样/时域、约束和扰动界，明确其迁移到PX4 Offboard接口所需验证的最小合同。
