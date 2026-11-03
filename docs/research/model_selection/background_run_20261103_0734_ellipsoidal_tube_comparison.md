# 背景深度调研：12状态椭球Tube MPC与降阶wayset Tube MPC对照（2026-11-03 UTC）

## 本轮证据等级
- 直接四旋翼论文正文分节阅读：1篇；摘要核验：1篇；非四旋翼理论迁移正文阅读：1篇。没有完整逐式读完任何新论文，不能宣称三篇全文。
- 主要原始论文：Parsi等，*Scalable tube model predictive control of uncertain linear systems using ellipsoidal sets*, *International Journal of Robust and Nonlinear Control*, DOI https://doi.org/10.1002/rnc.6485 ，出版社开放HTML https://onlinelibrary.wiley.com/doi/10.1002/rnc.6485 。本轮实际核验§3.4、§5.2及附录A.4中递归可行性/终端论证片段；其余章节和全部公式仍需续读。
- 对照：Davi A. Santos, Constantino M. Lagoa, *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, *ISA Transactions* 128 (2022) 123–135, DOI https://doi.org/10.1016/j.isatra.2021.12.002 ，PubMed及机构摘要核验，**未取得全文**。
- 方法学对照：Victor M. Cunha, Tito L. M. Santos, *Robust nonlinear model predictive control based on nominal predictions with piecewise constant references and bounded disturbances*, *International Journal of Robust and Nonlinear Control* 32(6) (2022) 3944–3968, DOI https://doi.org/10.1002/rnc.6004 ，出版社开放HTML摘要和方法说明核验；非四旋翼实验（反应釜、buck-boost），仅作可迁移理论。

## 关键直接证据：Parsi等椭球Tube MPC
- §5.2：Crazyflie微型四旋翼，27g，92×92×29mm；**12状态**为三维位置偏差、三维速度偏差、3欧拉角、3角速度；**4个输入是四个旋翼推力**。离散悬停线性化，Ts=0.1s；质量不确定27–37g，风扰动；各桨0–0.157N；状态盒与位置约束；预测N=15。采用椭球管束、LFT参数不确定性，在线半定规划，非逐桨ESC动态模型；**数值仿真，不是实飞**。
- §3.4式(44)–(45)离线设计终端椭球形状P和反馈K，使终端集合在扰动和参数不确定性下鲁棒正不变；附录A.4说明管束包含与终端不变性结合保证所述约束下的递归可行。注意这是**假设模型/不确定集合准确、控制状态可用于反馈**的线性系统结论；不能自动转化为间歇观测、可靠SMF后验及真实ESC约束下的12状态输出反馈安全。
- 论文是对之前“没有12状态四桨直接输入Tube MPC论文”的**重要纠正**：存在直接相关的12状态、逐桨推力、Tube MPC仿真原始研究。应将其列为主候选文献，但不代表已解决输出反馈问题。
- 待逐式核验：系统(1) LFT扰动定义、式(11)实际反馈策略、定理编号/初值可行条件、quadrotor所用P/K、质量不确定参数与控制输入偏置、求解时间/硬件WCET、测量状态来源、是否处理姿态角奇异域与非线性残差；没有从本轮可读节确认的内容一律未报告/待查。

## 与Santos/Lagoa的架构差异
| 比较维度 | Parsi等（正文分节） | Santos/Lagoa（摘要） |
|---|---|---|
| 预测模型 | 12状态悬停线性化四旋翼 | 假定内层姿态/位置控制器已稳定的降阶闭环平移模型 |
| MPC输入 | 四个逐桨推力 | 外层wayset导航控制，具体输入需全文确认 |
| 不确定性 | 质量参数不确定+风，椭球tube | 加性有界扰动及测量噪声 |
| 理论 | 在线SDP、离线终端不变集与递归可行 | 摘要宣称递归可行/鲁棒稳定，条件未全文核查 |
| 证据 | 四旋翼仿真 | 真实感模型数值仿真 |
| SMF/丢包 | 本轮未确认支持 | 摘要未报告间歇丢包SMF |

## 模型选型与主任务接口
12状态完整仿真主候选得到**更直接的论文支撑**，但其实现需核对物理单向桨推力域、采样周期与主任务20ms预算冲突（论文Ts=100ms并不能证明20ms可行）。6状态平面模型仍是降阶可证明性候选；2/4状态仅保底/反例基线。不可将状态维数直接等同于6DOF或声称全状态可测。
主任务应审查从逐桨f到请求wrench的物理映射、SMF集合下的反馈可实现性和失测分支的终端信息不变性；本背景任务不重复写控制器。
现有Run246/260/261与Gate A=blocked不变。

## 下轮续读位置（同一专题进行中）
1. Parsi等原文§2–3的动力学/LFT、tube递推与定理，§5.2全部数值参数/求解耗时及附录证明；先提取明确的状态反馈/初始集合合同。
2. Santos/Lagoa寻作者稿/机构存档全文，逐式核验终端条件、测量噪声处理和内环接口。
3. 追查Parsi等引用的quadrotor多面体Tube MPC原始研究（§5.2 Reference 26），核对是否已有更适合QP实时实现的四桨模型。
