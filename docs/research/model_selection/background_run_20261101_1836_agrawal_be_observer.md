# 背景第9轮：六状态有界误差观测器安全控制的可迁移性（2026-11-01 18:36 America/Los_Angeles）

## 基准与任务分工
读取远端main `3337f994e58e5882e73d57c286a9272772e12253`，`docs/research/CURRENT_CHECKPOINT.md`（Run255）、`docs/literature/PAPER_READING_LOG.md`（去重102）、`docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md`（背景第8轮）及`docs/research/run255_research_log.md`。本轮**只更新模型/文献论证**，不改主任务控制源码、检查点、验证工件；不将理论讨论当闭环证明。

## 论文及实际阅读
Agrawal, Devansh R.; Panagou, Dimitra (2023卷，2022-06-22在线), *Safe and Robust Observer-Controller Synthesis Using Control Barrier Functions*, IEEE Control Systems Letters 7:127–132, DOI https://doi.org/10.1109/LCSYS.2022.3185142，作者期刊PDF https://dev10110.github.io/pdfs/2022-observer-controller.pdf ，arXiv:2211.14364 https://arxiv.org/abs/2211.14364 。实际阅读期刊PDF pp.127–132，§II、§III-A/B (Theorems 1–3, Definition 5, Eq.16–18)、§IV-A/B/C；分节已读，未复现实验。IEEE期刊页的2023卷年与2022在线日期分别标记。

**具体模型**：§IV-B `x=(p1,p2,phi,v1,v2,omega)`、`u=(T,tau)`，惯性系位置/速度，m=1kg、J=0.25kg·m²；连续有噪输出 `(p1,p2,phi)`（5cm、5°），`v1,v2,omega`隐藏；有界动力学扰动≤2m/s²。DEKF有界误差椭球为**状态估计包含集**，不是未知质量的参数SMF；论文没有CZ实现、位置丢包或MPC。避碰圆障碍是安全目标；无本仓库状态/输入硬盒及20ms最坏计算保证。§IV-C Crazyflie实飞用IMU/气压计/Vicon、EKF 99.8%置信区间及内部PWM映射，不能转写为确定性全扰动硬安全实飞认证。

## 关键定理与本项目方程审计
Theorem 2 (17)：当BE observer保证`x∈P(t,xhat)`，且对**全部**`x∈P`存在一个共同`u`满足TRCBF安全输入条件时，可得到连续时间前向安全；这是充分条件，非所有安全策略的必要条件。Theorem 3 (18)以已知Lie导数上下界、同号、相对阶1和**无界输入U=R^m**构造QP，不能直接用于`T∈[4.905,14.715], |tau|≤0.08`。位置/速度硬约束通常对推力相对阶>1，必须另做高相对阶或离散前驱，不能把障碍CBF简单当成MPC终端不变性。

仓库6状态真值`v_z^+=v_z+0.02(Tcos(phi)-9.81+r_z)`、`|r_z|≤2.086+0.10125T`，J=0.02；论文J=0.25、扰动模型不同。第7轮已有同姿态隐藏`v_z=±3`无法共享推力的**候选纤维一拍**反例，第8轮有hover初始盒15拍共享固定输入正证；二者均不构成一般终端RCI。主任务Run255四状态特定历史后验39拍有限安全，Gate A仍blocked。新增文献强化了**信息集合与共享安全输入接口**的合理性，同时排除了“首次部分观测六状态安全控制”的创新主张。

## 模型选型与成熟度
首选仍为**条件性六状态平面(T,tau)**；四状态作为已有SMF+MPC有限闭环基线，2状态姿态保底，10/12状态和分层作为后续对照。可行性：有限安全内证非空但递归闭合未得；创新性：仅在有噪间歇位置、SMF/CZ状态集合、饱和输入与信息终端安全的结合上保留待验证空间；难度：高，特别是全观测分支、相对阶与离散输入约束。论文CBF-QP不是本轮新控制器，也未证明可取代MPC。

## 验证/负面结果
本轮对文献原文、仓库现有公式和模型配置做静态交叉核验；**未运行新六状态闭环/CI、未复现论文实飞**。已读新论文只增1条且查重DOI；保留作者实飞99.8%概率区间与确定性BE理论间的证据等级差异。计划仅提交本日志、专用矩阵和唯一论文阅读总账，不覆盖主任务文件。

**下一轮唯一优先问题：** 阅读具有物理输入饱和和采样/高相对阶处理的部分观测安全控制论文，逐式核对是否能给六状态失测信息状态提供可移位终端接口；若不能，明确建议将六状态限定为有限时域物理验证场景。
