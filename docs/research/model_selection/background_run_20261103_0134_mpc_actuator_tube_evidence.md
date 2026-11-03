# 背景调研 2026-11-03 01:34 PST：执行器权限与终端鲁棒性证据（进行中）

## 检查点与主问题
读取main的 CURRENT_CHECKPOINT、PAPER_READING_LOG、MODEL_SELECTION_EVIDENCE（2026-11-03）。主任务Run278给出真实MMS观测纤维速度直径下界0.713044490909 m/s，并排除该纤维66拍共同开环硬安全；不排除未来因果反馈。Gate A blocked。本任务仅研究论文证据，不开发控制器。

**本轮主问题：四旋翼MPC论文的实际优化输入与执行器权限，能否支持有界扰动下的硬约束与递归可行性迁移？**

## 实际核验范围
本轮独立核验原始研究**4篇**，均仅出版社/机构书目与摘要（**全文0、部分0、仅摘要4**）；没有获取并阅读完整论文，不应将下述未公开细节写成事实。另对照既有总账中Falanga(2018)、Elokda(2021)、Mendez(2023)等已读记录，**不计本轮新读**。

|原始论文及来源|直接对象、MPC结构|已核验内容|尚不能确认|
|---|---|---|---|
|Alexis, Nikolakopoulos, Tzes, *On Trajectory Tracking Model Predictive Control of an Unmanned Quadrotor Helicopter Subject to Aerodynamic Disturbances*, Asian Journal of Control 16(1):209–224 (2014), DOI 10.1002/asjc.587，2012在线|四旋翼平移积分MPC+姿态MPC，分段仿射PWA，多工作点，风扰仿真|双层控制、仿真验证、推力约束的摘要陈述|逐项状态、内外环输入映射、硬终端集、鲁棒递归可行证明|
|Hu, Feng, Quirynen, Villanueva, Houska, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model*, ACC 2018 pp.3135–3140, DOI 10.23919/ACC.2018.8431112|10状态四旋翼示例，非线性输入仿射Tube MPC、ACADO实时迭代|数值实验、毫秒量级计算的摘要陈述|10状态逐项定义、量测、逐桨输入、终端条件、是否实飞；**10状态不等于真实执行器闭合**|
|Zanelli, Horn, Frison, Diehl, *Nonlinear Model Predictive Control of a Human-sized Quadrotor*, ECC 2018|真实大型四旋翼姿态内环NMPC，嵌入式Cortex A9 800MHz、partially tightened RTI|摘要报告实机实验与约3倍加速|姿态状态/力矩或速率输入、传感器、执行器饱和、终端证明、真实最坏耗时|
|Didier, Parsi, Coulson, Smith, *Robust Adaptive Model Predictive Control of Quadrotors*, arXiv:2102.13544 (2021)|四旋翼RAMPC，质量未知/有界风、旋翼效率下降，直接与解耦架构比较|摘要报告实飞及鲁棒自适应设计，提及lambda收缩多面体与量测噪声挑战|已发表终版、具体状态输入、噪声集合、实飞约束违约、递归可行条件|

来源： https://doi.org/10.1002/asjc.587 ; https://doi.org/10.23919/ACC.2018.8431112 ; https://awesco.eu/publication/zanelli-2018-a/ ; https://arxiv.org/abs/2102.13544 。

## 横向结论与模型决策
1. **姿态内环**（Zanelli）可以在嵌入式实现，但不能据此推论平面位置硬约束；**平移/姿态级联**（Alexis）必须审计虚拟推力与姿态指令的共同可实现域；**10状态Tube**（Hu）提供鲁棒管束的研究入口，但状态数不构成硬执行器保证；**RAMPC**（Didier）研究有界参数不确定性，必须区分参数集更新与本项目的状态SMF后验。
2. 既有已读Falanga使用(p3,v3,q4)及(c,omega3)虚拟输入；Elokda真实DeePC使用(f_total,omega_ref,x,omega_ref,y)，两者均不能未经分配器认证替代逐桨硬约束。Mendez的12状态增量MPC经姿态需求/PID/混控，仍需辨识实际电机速率与饱和。
3. **模型矩阵决策暂不变**：条件性首选平面6状态(T,tau)，4状态只作有限证书基线，2状态姿态内环保底；完整12状态和分层模型保留对照。Run278反例要求优先审计观测条件化安全前驱，而不是简单增加维数。不存在可直接移植的已核验SMF/CZ+Tube无限时域证明。

## 证据缺口、续读精确位置与下一轮唯一问题
- **专题进行中**，未达阶段性完成。依次取得Hu全文§model/tube/terminal/experiments、Didier全文§problem/assumptions/constraints/experiments、Alexis全文§PWA/dual-MPC/constraints、Zanelli全文§model/solver/experiments，逐式提取x/u、采样、终端条件、硬界和计算量。当前均停在出版社/机构摘要，**无可声称的正文页码**。
- 逐一核验是否有确定性全扰动硬安全、终端RCI、位置机会丢包及真实逐桨分配误差；目前四项均未被本轮正文验证。
- 主任务接口建议：要求提供(T,tau)到真实电机的共同可实现域、推力调度残差上界、采样周期和位置失测自动机；由主任务负责控制器和证书。
- **下一轮唯一优先问题**：Hu(2018)的10状态Tube MPC全文中状态/控制权限/管束终端条件是否足以对照Run278的因果信息安全问题，并以Didier和Alexis全文作交叉验证。

## 提交范围
本轮仅独立背景日志；唯一论文总账不增加“已读”条目，模型证据矩阵不做未经全文支持的修改。CI与合并状态另行验证。
