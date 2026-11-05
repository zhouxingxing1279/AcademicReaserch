# 外环模型与输入权限复核｜2026-11-03 07:34 PST

## 任务与证据等级
本轮唯一主问题：原始四旋翼外环 MPC 文献中的虚拟输入、模型阶次与“成熟飞控内环”是否真正一致？实际新核验两篇四旋翼外环 MPC 原始论文：Andriën et al. (2024) **公开正式PDF部分正文核验**（§I、III、IV开头，印刷页5216–5220，式(7)–(16)、(22)及图2；未通读全文）；Santos & Lagoa (2022) **作者单位/期刊摘要核验**（未取得完整方程）。另复核仓库既有论文总账中 Xue et al. (2024) 的**历史正文记录**，不计本轮新阅读全文。分布：全文0、部分1、摘要1；第三篇为既有记录复核。严禁称已满足逐式全文要求。

## 原始论文 1：Andriën, Lefeber, Antunes, Heemels (2024)
*Model Predictive Control for Quadcopters With Almost Global Trajectory Tracking Guarantees*, IEEE TAC 69(8):5216–5230, DOI 10.1109/TAC.2023.3349098，正式PDF https://pure.tue.nl/ws/files/336894291/Model_Predictive_Control_for_Quadcopters_With_Almost_Global_Trajectory_Tracking_Guarantees.pdf 。
- **真正控制结构**：图2外环MPC输出三维虚拟加速度误差 `a_d`，再生成所需推力与姿态参考；专门设计的非线性姿态内环输出力矩 `tau`。不是 PX4 位置参考黑盒，更不是逐桨MPC。
- **物理/数学**：式(7a–d)含 `p∈R³,v∈R³,R∈SO(3),omega∈R³`，物理输入总推力 `T` 和力矩 `tau`；式(8)约束 `0≤T≤Tmax`，正文明确忽略电机动态和桨叶气动；式(15)误差平移 `dot(p_tilde)=v_tilde; dot(v_tilde)=-D v_tilde+a_d`，在旋转相关阻力可忽略假设下成立。外环是6维平移误差，但作者另称**四阶外环参考模型**以保证加速度参考二次可微；“四阶”是动态链阶数，不等于仅4个状态，更不能直接称6状态二重积分就是其完整MPC优化状态。
- **关键边界**：文中连续时间几乎全局渐近跟踪保证依赖其特定姿态控制律、参考可微性、推力裕度、阻力近似与可行参考；**不能转述为 PX4 内环、失测SMF、随机风和Tube硬安全的现成证明**。采样周期、时域、求解器、终端集合、仿真量化数据尚未在本轮核验，后续读§VI–VIII。
- **对选型影响**：支持加速度虚拟输入与姿态内环分离；同时暴露“加速度命令接口存在”不等于其设计中的可微参考、姿态闭环性能和稳定性保证可直接在 PX4 实现。

## 原始论文 2：Santos & Lagoa (2022)
Davi A. Santos; Constantino M. Lagoa, *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, ISA Transactions 128:123–135, DOI 10.1016/j.isatra.2021.12.002；作者单位页面 https://pure.psu.edu/en/publications/wayset-based-guidance-of-multirotor-aerial-vehicles-using-robust-/ 。
- **已核验（摘要）**：外层为wayset supervisory guidance、固定预测时域Tube鲁棒MPC；**下层既有姿态和位置稳定控制器**，外环使用考虑闭环平移与转动时间尺度分离的降阶闭环平移模型，离散LTI+有界加性随机扰动及测量噪声；论文摘要声称递归可行、鲁棒稳定和数值仿真。
- **不可断言**：摘要并未给出确切外环优化变量到底是位置参考、速度参考或其他wayset指令；不应仅因“lower-level position controller”就断言是 `p_ref`。矩阵、采样、终端条件、量测C、证明量词、PX4适配均**未核验**。本轮无法完成逐式核验，下一轮继续同一主问题。

## 仓库控制权限差异
仓库 `docs/research/01_model_and_bounds.md` 与 `configs/planar_baseline.json`：`x=[px,pz,vx,vz,phi,omega]`, `u=[T,tau]`，离散Euler真值、`dt=0.02s`，位置每5拍有机会观测、姿态/角速每拍；它属于**直接总推力/俯仰力矩控制的平面模型**，不是成熟PX4内环上的位置参考外环。原Run246/260/261证明/反例均不可直接迁移。唯一矩阵旧节称此模型“首选”属于**历史任务范围**，与当前新任务首选的成熟飞控级联架构存在范围冲突；须在矩阵中明确标注。

## 迁移合同与 SMF/CZ
候选A：`x=[p;v]∈R⁶`、MPC输出`p_ref`，用固定版本PX4 SITL辨识 `x[k+1]=Acl x[k]+Bcl p_ref[k]+w[k]`；状态是3D平移位置和速度，非6物理DOF。候选B：同状态、MPC输出`a_ref`，`dot(p)=v, dot(v)=a_ref+e_a+d`，但必须标定加速度跟踪误差集合 `e_a`、接口优先级、命令速率/jerk、延迟及饱和。候选C速度参考作为对照，需辨识速度闭环。以上都是**拟验证模型**，不是文献已证明PX4精确模型。
在所有合法失测序列上：`X^-_{k+1}=A X_k⊕B U_k⊕W`，成功量测时与带界测量条带相交，失测时不交；若PX4 EKF输出已融合原始传感器，必须建立联合误差界，不能假定其与GNSS/VIO独立。若控制器只接收估计值而非原始位置，需核实估计值可用性及安全接口。Tube约束必须包括闭环残差和命令饱和；`X_k`真值包含、硬约束与终端递归可行均待证明。

## 决策与未完成
当前级联外环为唯一优先研究架构。三维6状态+位置参考暂定首选，三维6状态+加速度参考为备选，速度参考待辨识；12状态刚体/电机增强暂缓。**没有证明首选优于备选**。未运行SITL/HIL、未开发控制器、未做CI、未获得Santos全文、未完成PX4版本锁定。
**下一轮唯一优先问题**：逐式获取 Santos–Lagoa 的外环优化变量、状态空间方程、终端约束与证明假设；若全文持续不可得，转为核验另一篇可获取全文的预稳定位置闭环外环Tube MPC论文，不重复摘要打卡。
