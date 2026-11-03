# 当前研究检查点 — 外环 MPC + SMF/CZ 理论主线（2026-11-04）

> **当前优先级：先完成理论闭合，再处理具体 PX4/ArduPilot 指令接口。** PX4 v1.17.0 源码审计和 Offboard 接口记录保留为背景资料，本阶段不继续做位置/速度/加速度接口 A/B，也不启动 SITL 接口辨识。

## 唯一研究目标

研究间歇/异步位置量测和有界模型残差下，如何构造可靠包含真实位置—速度状态的 SMF/CZ 后验；如何从有限测量模式中得到估计误差界；以及如何把估计误差、跟踪误差和有界扰动共同纳入因果输出反馈 Tube MPC，使同一观测历史下的所有可能真实状态共享一个可执行命令，并证明原状态/输入硬约束和递归可行性。

## 控制架构边界

- 高保真物理对象：12 状态六自由度四旋翼刚体模型。
- 成熟飞控承担姿态、角速度、控制分配、执行器与电机闭环。
- 外环理论先使用抽象高层命令变量，不预设它是位置、速度或加速度接口。
- 不把电机推力、总推力/力矩 wrench 或姿态稳定输入作为当前外环优化变量。
- 具体飞控接口、消息字段、固件参数和 SITL/HIL 辨识均延后到理论 Gate 完成后。

## 抽象外环模型（理论候选）

\[
x_{k+1}=Ax_k+Bu_k+Gw_k,\quad w_k\in\mathcal W
\]

\[
y_k=C_px_k+v_k,\quad v_k\in\mathcal V
\]

首个外环状态候选为 \(x=[p^\mathsf T,v^\mathsf T]^\mathsf T\in\mathbb R^6\)，位置量测矩阵候选为 \(C_p=[I_3\;0]\)。这只是用于理论推导的抽象离散模型，不是已冻结的 PX4 闭环方程。飞控跟踪误差、风扰、命令保持/延迟、模型失配和离散化余项必须有依据地进入 \(\mathcal W\)。

## 当前理论架构

1. 用有限状态自动机/有限长度语言描述 success、miss、delay、最大连续失测和时间戳。
2. 用 CZ 做集合预测、位置量测一致性更新、空集检测和可靠外包降阶。
3. 从 CZ 后验构造相位相关估计误差集合 \(\mathcal E_i\)，证明有限语言下的 Equalized Recovery。
4. 合成只依赖已收到观测历史的因果输出反馈控制器，并构造跟踪误差管 \(\mathcal S_i^c\)。
5. 按 \(\mathcal X\ominus\mathcal S_i^c\) 和 \(\mathcal U\ominus\mathcal U_{\mathrm{err},i}\) 收紧名义约束。
6. 构造跨所有测量相位有效的共同终端集合/终端反馈，用移位论证证明递归可行；持续有界扰动下目标是鲁棒实用稳定，而非无条件收敛到原点。

完整推导、条件定理模板、证明分工与文献边界见 [理论框架](THEORY_FRAMEWORK.md)。

## 当前缺口

- 有限测量语言下，CZ 后验是否能获得有限、相位相关且保包含的估计误差界。
- 位置-only 观测在有界过程扰动和最大连续失测约束下的统一可观测/误差恢复条件。
- CZ 后验到估计误差管、估计误差管到跟踪 Tube 的严格包含关系。
- 对同一观测历史中所有可能真实状态都有效的共同因果控制输入。
- 非空共同终端集合、终端 Lyapunov 下降条件和初始可行域。
- 12 状态非线性物理 plant 到抽象外环模型的残差包含证明。
- 最坏分支计算复杂度和后续实时预算。

## 暂缓资料

- [PX4 外环接口证据](model_selection/PX4_INTERFACE_EVIDENCE.md)
- [PX4 v1.17.0 源码审计](model_selection/PX4_V1_17_SOURCE_AUDIT.md)

以上仅保留供后续接口映射时查阅；不属于当前理论阶段的待办事项。

## 历史证据边界

旧四/六状态平面直接控制模型、Run246、Run260/261、Run278 及旧实验/测试见 [历史归档索引](../../archive/legacy_planar_direct_control_20261103/ARCHIVE_INDEX.md)。它们只对各自冻结的旧模型、观测与控制量词成立，不能直接推出当前成熟飞控外环模型的安全结论。

## 当前规范化文档

- [理论框架](THEORY_FRAMEWORK.md)：CZ-SMF、有限测量语言、Equalized Recovery、共同因果 Tube 和终端递归可行性。
- [抽象模型合同](MODEL_CONTRACT.md)：理论状态、输入、扰动和量测边界。
- [研究路线图](RESEARCH_MAP.md)：理论 Gate 顺序。
- [外环 MPC 与 SMF/CZ 文献证据](model_selection/OUTER_LOOP_MPC_LITERATURE.md)。
- [模型选型证据矩阵](model_selection/MODEL_SELECTION_EVIDENCE.md)。
- [唯一论文阅读总账](../literature/PAPER_READING_LOG.md)。

## 下一唯一优先问题

**Gate T3：** 在 \(x=[p;v]\)、\(C_p=[I_3\;0]\) 的抽象离散平移模型下，给定明确的最大连续失测数、有限测量语言、有界加速度/模型残差和有界位置噪声，推导并验证位置-only CZ-SMF 的相位相关误差界；比较精确 CZ 后验与路径相关 observer + CZ 误差外包两条路线，证明至少一条路线满足 Equalized Recovery。未完成该 Gate 前不推进 PX4 接口 A/B 或具体飞控 SITL。
