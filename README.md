# AcademicReaserch — 四旋翼外环 MPC 与 SMF/CZ

> **2026-11-05 工作入口：** [统一检查点](docs/research/CURRENT_CHECKPOINT.md)是唯一阶段状态；[阶段 0 审查报告](docs/research/STAGE_0_AUDIT_20261105.md)区分 main、本地草稿与未合并 PR；[AGENTS.md](AGENTS.md)规定验收顺序。下方旧日期的优先级仅为历史背景。

**当前主线（2026-11-04）：** 间歇/异步位置量测下的CZ集员估计与因果输出反馈Tube MPC。限定数学基线已形成；按用户要求先行开展PX4/Gazebo验证，实际接入成功，但现有模型/误差界未通过验证，下一步修复执行动态与残差覆盖。

## 当前状态

- 仓库主体整理已提交 PR #191：旧平面直接控制方案和历史实验归档到 archive/legacy_planar_direct_control_20261103/，保留当前研究所需文档与通用数值工具。
- 高保真物理对象仍是 12 状态六自由度四旋翼刚体 plant，成熟飞控承担姿态、角速度、控制分配和电机执行。
- 外环理论先用抽象离散模型 \(x^+=Ax+Bu+Gw\)，位置-only 量测 \(y=C_px+v\)，有限 success/miss/delay 语言；具体命令接口不冻结。
- 理论研究重点：可靠 CZ 后验 → 相位相关估计误差界 → Equalized Recovery → 共同因果输出反馈 → Tube 约束收紧 → 共同终端集合与递归可行性。
- 已实现有限记忆 CZ 与输出反馈 Tube MPC 的 ZOH 六状态数学基线：有限窗包含、统一误差界、启动准入和显式终端的限定模型证明已形成，原26组本地闭环验证完成。一般模型、相位优化与12状态物理映射仍未完成；后续算法级SITL已运行但未通过，HIL未开展。

**最新交付：** [完整课题方案](docs/research/proposal/RESEARCH_PROPOSAL.md) · [理论证明](docs/research/proposal/FINITE_MEMORY_THEORY.md) · [验证与局限](docs/research/proposal/VALIDATION.md)。方案包含研究假设、文献差异、实验矩阵、已证基线与后续验收标准。

**抗扰验证更新：** 主要目标是扰动下的约束保持与鲁棒可行性，跟踪精度为辅助。新增226条压力/随机轨迹，136条合同内轨迹全部通过数值检查；合同外包含失败、空后验和输入越界均保留。16组解析预算及50组随机成对比较见[抗扰结果](docs/research/proposal/ROBUSTNESS_RESULTS.md)。当前CZ与pair共享统一Tube，尚未证明额外抗扰优势或相对普通MPC的提升。

**首次Gazebo结果：** 4次正式算法接入已实际运行。连续测量下出现空后验，失测组出现速度越界，均已正常降落上锁。原算法未调参，不能声称SITL通过。见[结果、残差图与ULog](docs/simulation/CZ_SITL_RESULTS.md)。

**接口诊断更新：** 四个旧场景已逐轴重放，连续测量的空后验定位到垂直轴；新增两次独立启动、9个分轴激励块完成。初步辨识水平有效滞后与垂直增益失配，留出短窗预测改善但长期漂移和原CZ失败仍在。见[辨识结果与下一步](docs/simulation/INTERFACE_IDENTIFICATION_RESULTS.md)。

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

活动源码包含通用数值工具、[精确有理数一步门](src/outerloop/startup_gate.py)、[有限记忆CZ估计](src/outerloop/finite_memory.py)和[输出反馈Tube MPC](src/outerloop/tube_mpc.py)。新增LP/QP原型使用float64，不是向外舍入认证；[独立证书](experiments/finite_memory_certificate.py)只检查其声明的代数恒等式和端点支持。旧平面控制器保留在归档中。

旧启动门证书仍可用Python标准库运行 `python -m experiments.cz_startup_predecessor --check`。新增基线先安装 [固定依赖](requirements-research.txt)，再用虚拟环境运行活动测试和实验；完整命令见[课题方案](docs/research/proposal/RESEARCH_PROPOSAL.md)。

## 暂缓资料

PX4 外环接口和 v1.17.0 源码审计继续保留在 docs/research/model_selection/ 下，供理论 Gate 完成后做具体接口映射；当前阶段不推进接口 A/B 或 SITL。
