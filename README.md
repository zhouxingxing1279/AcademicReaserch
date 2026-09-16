# AcademicReaserch

**主方案已确定（2026-09-15）：[强化学习调度集合验证的输出反馈 MPC](docs/learning/03_selected_plan.md)。[04 控制接口](docs/learning/04_control_interface_and_finite_scheduler.md) 与 [05 C1 间歇测量误差接口](docs/learning/05_intermittent_error_interface.md) 已完成。C1 证明固定二次 metric 不能逐 tick 严格收缩，但构造了覆盖 15 模式/17 条边的 mode-dependent 二次 metric，并得到统一鲁棒标量递推。当前唯一下一任务是 C2：把 mode-dependent 估计集合接入 set-membership 与 MPC nestedness/constraint tightening；C2 前不训练 Double DQN，也不宣称完整闭环安全。**

## 当前研究：有限计算预算下强化学习辅助的集员输出反馈 MPC

**当前入口：[研究总框架](docs/research_framework.md)。先固定研究主问题、模块接口和证明依赖，再推进具体算法。**

主问题：在相同物理信息、独立验证器和在线总计算预算下，学习调度能否比强非学习调度更有效地降低控制器实际使用的可靠估计误差界，同时保持证书正确性与既定鲁棒控制接口？

用户随后授权的 [方向选择机制核查](docs/learning/01_direction_selection_probe.md) 已完成：八个精确几何实例显示相关方向可减少冗余，但单目标准确支持时，直接查询约束法向的非学习规则已最优。[04 控制接口](docs/learning/04_control_interface_and_finite_scheduler.md) 进一步把候选库限制为观测误差度量分解得到的成对方向，并给出两步预算下的严格序列价值见证：一步贪心最终证书为 5，精确最优为 5/2。随后 [05 C1](docs/learning/05_intermittent_error_interface.md) 给出 mode-dependent metric：齐次收缩系数 19/20，Young 扩展后的统一鲁棒系数 99/100。以上仍只建立理论接口，不证明 Double DQN 优于有限前瞻。

此前框架的基础任务是 F1：核查并选定控制基础合同。暂停逐组增益搜索、限幅不变集分支扩展、网络训练及新的控制实现。以下保留历史理论进展，其“下一步”建议以总框架为准。

最新 [竖直硬约束核查](docs/theory/09_vertical_input_certificate.md) 对 08 新候选给出准确可达支持证书：每 5 步成功测量时，第 30 步输入偏移可达 5.347934 N，超过原 4.905 N 限制。未限幅候选因此被否定；同时证明实际受限输入进入观测器时，08 的观测误差界仍保留。下一步转向带限幅分支或共同动作区间的竖直不变族，不再为此未限幅候选搜索安全证书。

[增益筛选与切换观测误差界](docs/theory/08_gain_screen_and_switched_observer.md) 给出新竖直候选 kp=5、kd=3、观测速度增益 4.5：通过完整外包的恒定扰动平均必要条件，并证明任意允许包间隔切换的统一观测误差界。同一合同下，成功包速度误差界由 1.3297 降至 1.0516 m/s。仅认证误差界与无约束竖直有界性，原硬约束及六维终端仍未通过。

[终端候选否证与必要条件](docs/theory/07_terminal_candidate_obstruction.md) 证明 06 的固定高度反馈与独立扰动盒组合无法保持原高度约束：解析平均高度与安全界矛盾，且有第 88 步越界的精确有理数见证。停止为该已否定组合搜索终端证书；先按一般高度增益必要条件修改候选结构。这不否定真实气动模型或其他反馈。

[因果增广模型与非线性外包](docs/theory/06_causal_augmented_model.md) 明确了八维控制器内部状态、14 维增广后继、15 个观测模式与 17 条允许边，并归档成功/缺测两组有理数矩阵。全域余项具有解析界；候选增益仍待不变集证书验证，不代表已通过六维安全门。

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
python verification/check_terminal_obstruction.py --output /tmp/terminal_counterexample.json
python verification/check_gain_screen.py --output /tmp/gain_screen.json
python verification/check_vertical_hard_constraints.py --output /tmp/vertical_constraints.json
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

按 [05 C1](docs/learning/05_intermittent_error_interface.md) 执行 C2：正式实例化六维 mode-dependent 误差集合，计算统一扰动增益，并证明 future-mode uncertainty 下的集合 nestedness 与 MPC constraint tightening 接口。优先比较 future-mode union envelope 与 mode-conditioned tube；C2 未通过前不训练 RL，也不继续扩展新的控制器分支。

初版方案：2026-09-08；理论优先重置：2026-09-10。AI 辅助文献分析与推导，作者需复核理论及实验；没有代替作者实施人类阅读确认。仓库原有项目名保留。
