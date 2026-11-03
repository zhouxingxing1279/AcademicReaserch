# AcademicReaserch — 四旋翼外环 MPC 与 SMF/CZ

**当前主线（2026-11-03）：** 成熟飞控承担姿态、角速度、控制分配和电机执行；研究其上的四旋翼位置/速度/航点/轨迹外环 MPC，并探索间歇/异步测量下的 SMF/CZ 与 Tube MPC 安全保证。

## 当前状态
- 研究方向已从底层电机/力矩直接控制切换为成熟飞控之上的外环控制。
- 主仿真对象为 12 状态六自由度四旋翼刚体 plant，成熟飞控负责底层闭环；外环预测可先检验六维平移状态 \\(x_{out}=[p^\\mathsf T,v^\\mathsf T]^\\mathsf T\\)，但必须由 12 状态 SITL 验证其残差覆盖。它不是旧仓库的平面六状态 \\([p_x,p_z,v_x,v_z,\\phi,\\omega]\\)。
- 位置、速度、加速度三种飞控接口仍需通过文献与 SITL 辨识比较；位置指令型闭环模型暂作首要候选，不视为已冻结。
- 尚无新的外环控制器、SITL 闭环实验、SMF/CZ 外环实现或递归安全证明。

## 控制边界
\[
\text{异步传感器}\rightarrow\text{SMF/CZ}\rightarrow\text{外环 Tube MPC}
\rightarrow\text{成熟飞控}\rightarrow\text{四旋翼}
\]
外环 MPC 只输出高层参考指令。成熟飞控保留姿态/角速度稳定、控制分配、执行器限幅和电机控制。风扰、飞控跟踪误差、延迟、饱和及模型失配必须以有依据的集合/界进入外环模型。

## 从这里开始
1. [当前研究检查点](docs/research/CURRENT_CHECKPOINT.md)
2. [临时模型与接口合同](docs/research/MODEL_CONTRACT.md)
3. [研究路线图](docs/research/RESEARCH_MAP.md)
4. [模型选型证据矩阵](docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md)
5. [PX4 外环接口证据](docs/research/model_selection/PX4_INTERFACE_EVIDENCE.md)
6. [外环 MPC 与 SMF/CZ 文献证据](docs/research/model_selection/OUTER_LOOP_MPC_LITERATURE.md)
7. [模型选型文档导航](docs/research/model_selection/README.md)
8. [唯一论文登记总账](docs/literature/PAPER_READING_LOG.md)
9. [历史归档索引](archive/legacy_planar_direct_control_20261103/ARCHIVE_INDEX.md)
10. [开放 PR 分类与依赖图](docs/research/PR_TRIAGE_20261103.md)

## 关键文献锚点
- Santos & Lagoa (2022), ISA Transactions：位置指令型外环 Tube MPC。[DOI](https://doi.org/10.1016/j.isatra.2021.12.002)
- Andriën et al. (2024), IEEE TAC：加速度参考型外环 MPC 与姿态内环。[DOI](https://doi.org/10.1109/TAC.2023.3349098)
- Izadi et al. (2026), Automatica：时变/耦合约束下的级联外环 MPC。[DOI](https://doi.org/10.1016/j.automatica.2026.113141)

这些论文支持研究架构，不意味着其自定义内环和稳定性证明可直接移植到 PX4/ArduPilot。

## 活动代码边界
目前活动源码只保留通用数值集合工具 [numerical_sets.py](src/common/numerical_sets.py)。它实现 float64 Box/Zonotope 运算，不是 Constrained Zonotope，也不是向外舍入的形式化证书。旧平面 plant、滤波器、脚本、测试和实验已完整移入归档。
