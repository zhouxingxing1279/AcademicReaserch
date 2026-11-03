# AcademicReaserch — 四旋翼外环 MPC 与 SMF/CZ

**当前主线（2026-11-04）：** 先完成间歇/异步位置量测下的 CZ 集员估计、Equalized Recovery、因果输出反馈 Tube MPC 和终端递归可行性理论；具体 PX4/ArduPilot 指令接口与 SITL 暂缓。

## 当前状态

- 仓库主体整理已提交 PR #191：旧平面直接控制方案和历史实验归档到 archive/legacy_planar_direct_control_20261103/，保留当前研究所需文档与通用数值工具。
- 高保真物理对象仍是 12 状态六自由度四旋翼刚体 plant，成熟飞控承担姿态、角速度、控制分配和电机执行。
- 外环理论先用抽象离散模型 \(x^+=Ax+Bu+Gw\)，位置-only 量测 \(y=C_px+v\)，有限 success/miss/delay 语言；具体命令接口不冻结。
- 理论研究重点：可靠 CZ 后验 → 相位相关估计误差界 → Equalized Recovery → 共同因果输出反馈 → Tube 约束收紧 → 共同终端集合与递归可行性。
- 目前尚未实现新外环控制器或 CZ-SMF，也未运行新 SITL/HIL；理论框架文档给出的是条件定理模板和待证明 Gate，不是已完成的项目级安全证明。

## 控制边界

\[
\text{间歇位置量测}\rightarrow\text{CZ-SMF}\rightarrow
\text{因果输出反馈 Tube MPC}\rightarrow
\text{成熟飞控}\rightarrow\text{四旋翼}
\]

外环优化器不直接输出电机转速、四桨推力或姿态稳定命令。

## 从这里开始

1. [当前研究检查点](docs/research/CURRENT_CHECKPOINT.md)
2. [理论框架与条件定理模板](docs/research/THEORY_FRAMEWORK.md)
3. [抽象模型与理论合同](docs/research/MODEL_CONTRACT.md)
4. [研究路线图](docs/research/RESEARCH_MAP.md)
5. [外环 MPC、12 状态物理 plant 与 SMF/CZ 文献证据](docs/research/model_selection/OUTER_LOOP_MPC_LITERATURE.md)
6. [模型选型证据矩阵与历史论文审计](docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md)
7. [唯一论文阅读总账](docs/literature/PAPER_READING_LOG.md)

## 关键理论锚点

- Hassaan et al. (2021), finite-length missing/delayed-data language、Equalized Recovery、time-varying output-feedback Tube MPC 与递归可行性：[DOI](https://doi.org/10.1016/j.ifacol.2021.08.482)。
- Rego et al. (2020), nonlinear constrained-zonotope set-membership prediction/update：[DOI](https://doi.org/10.1016/j.automatica.2019.108614)。
- Scott et al. (2016), constrained zonotope exact set operations：[DOI](https://doi.org/10.1016/j.automatica.2016.02.036)。
- Ji et al. (2022), direct 12-state quadrotor ellipsoidal SMF + output-feedback Tube RMPC precedent：[DOI](https://doi.org/10.1109/CDC51059.2022.9992704)。

这些先例已经覆盖通用 SMF-MPC、CZ set estimation 和 intermittent-data Tube MPC 的不同部分；本项目必须证明它们在位置-only、有限测量语言和四旋翼外环抽象模型下的接口闭合，不能用“首次结合 SMF 与 MPC”作为创新主张。

## 活动代码边界

目前活动源码只保留通用数值集合工具 [numerical_sets.py](src/common/numerical_sets.py)。它实现 float64 Box/Zonotope 运算，不是 Constrained Zonotope，也不是向外舍入的形式化证书。旧平面 plant、滤波器、脚本、测试和实验已完整移入归档。

## 暂缓资料

PX4 外环接口和 v1.17.0 源码审计继续保留在 docs/research/model_selection/ 下，供理论 Gate 完成后做具体接口映射；当前阶段不推进接口 A/B 或 SITL。
