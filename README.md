# AcademicReaserch

## 当前研究：间歇位置测量下的神经动力学建模与集员输出反馈 MPC

本仓库从零建立一条可证伪的研究路线：在物理状态上学习未建模加速度，研究测量更新与丢测模式是否改变模型训练的最优选择，并验证这种变化是否减少集合外包络冗余、改善控制可行性。

**当前阶段已调整为理论优先设计。新的控制实现、分区加密和训练暂停，先完成域内保持与优势条件的证明。**

最新 [因果增广模型与非线性外包](docs/theory/06_causal_augmented_model.md) 明确了八维控制器内部状态、14 维增广后继、15 个观测模式与 17 条允许边，并归档成功/缺测两组有理数矩阵。全域余项具有解析界；候选增益仍待不变集证书验证，不代表已通过六维安全门。

[有限姿态多面体与终端闭合接口](docs/theory/05_finite_terminal_polytope.md) 给出四面鲁棒不变集，并证明它在固定坐标变换的对称矩形类中最小。同一模型、噪声和反馈增益下，力矩校正界从 0.0296 降至 0.0128 N·m，参考力矩预算从 0.0504 增至 0.0672 N·m；参考核与动作证书均有严格扩张见证。这是证书保守性的改进，尚不证明实际控制性能或神经网络优势。六维终端闭合的有限乘子接口已写明，但完整实例尚未求出。

[共同控制前驱与六维有限时域证书](docs/theory/04_coupled_predecessor_and_finite_horizon.md) 证明固定信息与目标多面体时，一步鲁棒可行动作集对共同推力/参考扭矩为凸集；并给出从原初始集合出发、覆盖全部允许扰动和角测量误差的 40 步（0.8 s）六维域内先验管。这是解析包含证明，尚未构成无限时域不变族。

该文还证明独立大盒抽象确实会丢失部分一步可行状态，并反证固定倾角延续不能作为终端策略。结构比较属于离线基准诊断，不计为神经网络优势。

[不变域分析与姿态证书](docs/theory/03_invariant_domain_analysis.md) 证明固定厚盒及原任务域的结构性限制，并构造包含当前初始姿态集合的输出反馈鲁棒不变集：角度、角速度、扭矩的已证上界分别为 0.0225 rad、0.12 rad/s、0.0296 N·m。结论仅适用于文中的固定零姿态反馈及精确离散角模型；完整六维无限时域保持仍未证明。

该文 3.5 进一步证明受约束时变倾角参考的跟踪不变族，给出从零参考到 0.2 rad 的解析可行见证。参考生成规则、力矩收紧与初始误差条件必须同时满足，尚未证明它与平移控制需求相容。

[理论设计](docs/theory/01_proof_first_design.md) 给出窗口误差显式界、相对物理基线的集合包含保证、严格改进见证，以及输出反馈 MPC 的证明接口；[审查与准入条件](docs/theory/02_review_and_gates.md) 明确尚未通过的不变族、学习独立优势与控制闭合条件。

历史实现保留：模型 A、仿射传播、联合差函数界及局部包络查询；39 项历史测试通过，正常测量完成 20 秒，缺测仍超域。详见 [12](docs/research/12_joint_local_envelope.md)。这些结果不构成新理论的证明。

此前 [09 非线性 zonotope 结果](docs/research/09_nonlinear_zonotope_implementation.md) 保留：27 条轨迹完成 20 秒，27,027 次数值成员检查通过；实时门未通过。

### 文档导航（建议按顺序阅读）

| 文件 | 解决的问题 |
|---|---|
| [00 研究总纲与验收](docs/research/00_research_contract.md) | 研究问题、创新边界、交付物、继续/终止条件 |
| [01 模型与误差界](docs/research/01_model_and_bounds.md) | 坐标、单位、连续/离散方程、Jacobian、网络、残差包络 |
| [02 集员滤波与训练算法](docs/research/02_filter_and_training.md) | 区间与 zonotope 递推、测量修正、A/B/C/D 训练、伪代码 |
| [03 输出反馈 MPC 与证明义务](docs/research/03_mpc_and_proof_obligations.md) | 误差耦合、约束收紧、可行性、安全候选验证、待证定理 |
| [04 验证协议](docs/research/04_validation_protocol.md) | 工具、数据划分、实验矩阵、统计、时延与失败分类 |
| [05 后续执行路线](docs/research/05_execution_roadmap.md) | 模块接口、阶段任务、时间预算、模块验收与论文推进 |
| [06 文献与工具依据](docs/research/06_sources_and_tools.md) | 最近邻文献、证据等级、工具能力边界与复现依据 |
| [07 本次交付核查](docs/research/07_delivery_audit.md) | 实际执行了什么、没有执行什么、审查结论 |

默认物理参数、归一化、传感器时序和实验种子见 [planar_baseline.json](configs/planar_baseline.json)。其中控制增益与终端证书留空，表示后续需要求解的对象。

### 现在可以运行什么

姿态证明与本轮六维有限时域证明的有理数恒等式、约束余量和反例可用 Python 标准库精确核对：

```bash
python verification/check_invariance_theory.py --output /tmp/invariance_exact_checks.json
python verification/check_coupled_theory.py --output /tmp/coupled_exact_checks.json
python verification/check_terminal_polytope.py --output /tmp/terminal_polytope_certificate.json
python verification/check_causal_model.py --output /tmp/causal_matrices.json
```

输出路径须不存在。[姿态核对](results/theory_invariance_20260910/exact_checks.json) 与 [六维有限时域核对](results/theory_coupling_20260910/exact_checks.json) 均含脚本和配置哈希。论证与适用时域见理论文档，脚本不是自动定理证明器。以下命令属于历史实现复现，不代表已获新的控制实施准入。

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell 使用 .venv\Scripts\Activate.ps1
python -m pip install -r verification/requirements.txt
python verification/run_checks.py --output /tmp/academic_checks.json
```

输出路径可按系统修改。详见 [verification/README.md](verification/README.md)。脚本只核查基础代数和数值实现关系，不能据此宣称完成 SMF、神经训练、MPC 闭环或实机验证。

### G1 原型运行

```bash
python -m unittest discover -s tests -v
python scripts/run_g1.py --output results/my_g1_run
```

依赖沿用上面的 NumPy/SciPy。输出目录须为空；结果带源码、配置和数据哈希。已归档的 [实际结果](results/g1_20260909/summary.json) 与 [科研图](results/g1_20260909/g1_findings.svg) 均为数值 pilot，不是训练或控制性能。

### 非线性 zonotope 重放

```bash
python scripts/run_zonotope.py --output results/my_zonotope_run
```

默认比较 30/60/120 个生成元预算；完整日志、公式和计时范围见 09。

### 模型 A 训练与重放

```bash
python scripts/train_model_a.py --output results/my_model_a
python scripts/evaluate_model_a.py results/my_model_a --output results/my_model_a_replay
```

当前 NumPy/SciPy 实现不依赖 PyTorch；默认单初始化、120/40 条训练/验证轨迹，属于 pilot。

### 后续工作的第一条指令

按 [理论准入表](docs/theory/02_review_and_gates.md)，基于 [06 的明确候选映射](docs/theory/06_causal_augmented_model.md)，求解并验证具有平移反馈的终端信息状态族及逐模式非负乘子证书，证明原初始信息状态包含以及全部观测/缺测后继闭合。不能把 40 步先验管重复拼接成无限时域结论。完整不变性与学习独立优势尚未通过，不启动新的控制实现或训练消融。

初版方案：2026-09-08；理论优先重置：2026-09-10。AI 辅助文献分析与推导，作者需复核理论及实验；没有代替作者实施人类阅读确认。仓库原有项目名保留。
