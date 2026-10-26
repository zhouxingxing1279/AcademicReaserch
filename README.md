# AcademicReaserch

最新研究检查点：[Run184 box information-ensemble graph obstruction](docs/learning/118_houska_box_ensemble_graph_lp.md)：
构造完整`Y/G/Lambda`与6参数`Z/H/Omega`后，时序正确的15-mode/17-edge LP含498变量、2772约束。
axis-aligned position measurement不能收缩velocity radius；最短五边环的21行exact Farkas
证书把全部变量消去并得到`0<=-572143/800000`。因此纯box terminal family被否定，下一步只
研究最小position--velocity相关facet模板。

最新研究检查点：[Run183 Houska vertical baseline adapter](docs/learning/117_houska_vertical_adapter_contract.md)：
式(29)的固定 `A,B,C,W,V` 假设不能原样接入实际推力相关 residual；本轮对真实竖直 tracking
error 冻结执行器全域 residual 包络，并保留15-mode packet边、miss/success测量语义和分叉前
共享控制，得到 exact 可执行适配合同。它不是 invariant terminal ensemble；下一步才选择
`Y/G/Lambda`与`Z/H/Omega`模板并综合极端信息集控制。

最新研究检查点：[Run182 lifted-cell composability gap](docs/learning/116_lifted_cell_composability_gap.md)：
Run180/181 的 local estimator/tracking 证书不能直接连成 cell graph；两条 miss 边的位置支持已
越出共同 `d`-cell，mode-4 success 的位置/速度支持越界更大。该结果不否定其他 partition，
但终止手工 cell 枚举；下一步转向 Houska 式固定模板 information-ensemble terminal 强基线。

最新研究检查点：[Run181 mode-4 unknown-branch lifted-cell oracle](docs/learning/115_mode4_unknown_branch_lifted_cell.md)：
同一正体积 source cell 与同一可见零修正策略，在当前输入后才揭示的 `4->5 miss`、`4->0 success`
两支共 26 个 target normals 上 exact 闭合，并保留实际推力相关 residual 与 success 噪声语义。
该结果仍只是双边一步实现证书，不是 terminal RCI 或递归可行性证明；下一步检验有限 cell 覆盖
和重叠策略一致性。

最新研究检查点：[Run180 mode-0 miss lifted-cell oracle](docs/learning/114_mode0_miss_lifted_cell.md)：
固定正体积 `(eta,d)` source cell、仿射可见策略和 10 个 target normals，在保留
actual-thrust-dependent 共享竖直 residual 的 `0->1 miss` 上得到 exact 一步闭合。该结果只是
接口实现引理，不是 terminal RCI 或递归可行性证明；下一步转向 mode 4 的未知 success/miss 分叉。

**当前主线：传统集员滤波（SMF）与输出反馈 Tube MPC，暂停学习算法与在线参数辨识。最新入口：[36 执行器权限与 scheduling-conditioned residual 审计](docs/learning/36_actuator_authority_and_scheduled_residual.md)。第33–35章的 static-K 失败不能升级为执行器物理不可能：移除固定反馈结构后，在低推力、全部硬状态/力矩约束下，单一 global residual 的首个数值 torque-feasible horizon 为 381 tick，而按已知 thrust 条件化同一解析 residual 后降为 160 tick（约 58%）。这些 horizon 是 HiGHS 数值边界，不是形式化最短性证明。下一步只做 certificate-based ancillary/RCI synthesis，并以 scheduling-consistent W(T) 作为强基线；该基线闭合前不恢复 CZ 几何收益讨论。**

## 当前研究与历史边界

当前理论链条为 [15 联合误差与控制方向](docs/learning/15_cz_output_feedback_tube.md) → [16 递归可行性](docs/learning/16_recursive_feasibility_direction_template.md) → [17 近似支持与候选证书](docs/learning/17_certified_caps_for_inexact_support.md) → [18 多维优化与下降验证](docs/learning/18_multidim_cz_qp_and_descent.md) → [19 同时刻性能损失证书](docs/learning/19_compression_performance_certificate.md) → [20 实际多步查询证书](docs/learning/20_certified_multistep_queries.md) → [21 通用多等式 CZ 认证查询](docs/learning/21_generic_cz_support_certificate.md)。候选贡献是可行性与性能双证书驱动的控制相关集合计算，不把 SMF、CZ 与 Tube MPC 的组合宣称为新方法；首次性仍待近邻全文排重。

以下学习框架、物理模型障碍与旧实验是历史记录；其“暂停控制实现”等阶段指令不再约束当前两状态线性基准，但旧四旋翼合同的未解决问题依然存在。[研究总框架](docs/research_framework.md) 保留供追溯。

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

优先读 [36 执行器权限与 scheduling-conditioned residual 审计](docs/learning/36_actuator_authority_and_scheduled_residual.md)。下一步唯一优先任务是在 scheduling-consistent `W(T)` 下建立 certificate-based ancillary/RCI baseline：必须对全部允许 thrust scheduling 与 disturbance sequences 成立，并联合通过 `|px|<=5, |vx|<=3, |phi|<=0.45, |omega|<=2, |tau|<=0.08`。若固定 `K` 的可认证 controller/RCI class 不可行，只能否定该证书类；不能升级为物理 actuator impossibility。该基线闭合后再恢复 CZ-SMF tightening 比较。

前置结果 [17 近似支持下的证书上界](docs/learning/17_certified_caps_for_inexact_support.md)：由旧可行计划构造方向上界，允许新的后验支持查询近似或缺失，保持线性每步测量基准的递归可行性。4096 步合成查询压力重放通过；仍需精确噪声支持及可靠上界算术，尚无高维计算优势或四旋翼保证。

精确支持基准见 [16 方向保护压缩的线性递归可行性基准](docs/learning/16_recursive_feasibility_direction_template.md)：固定模型、每步测量、精确支持方向更新与终端条件下的递归可行性证明；含非空标量终端证书及 1024 步可行移位候选重放。尚无四旋翼/缺测保证，当时尚未实施多维压缩或 MPC 目标优化；两状态实现现见18，高维与四旋翼仍未完成。

按最新研究决策，暂停学习算法与在线参数辨识。当前主线见 [15 CZ 集员滤波与输出反馈 Tube MPC](docs/learning/15_cz_output_feedback_tube.md)：联合误差传播、测量条件化和整个预测时域的控制方向保护。该章完成线性接口定理及精确反例；跨时刻压缩兼容与终端追加的每步测量线性基准见16，四旋翼闭环仍未完成。下述 13–14 作为历史研究与基础工具保留。

前一阶段结果见 [14 有限预算集员学习与控制价值](docs/learning/14_anytime_set_learning_and_control_value.md)：已给出完整覆盖下的中断安全更新证明、精确有理数对照，以及集合体积不等于控制收益的反例。两条候选贡献收敛为联合信息压缩的控制兼容性和同预算下控制相关计算分配；未宣称已有闭环递归可行性或学习优越性。

前置模型合同见 [13 集合值数据学习合同](docs/learning/13_set_valued_learning_contract.md)：核查带状态估计误差的残差学习与集员更新，建立安全中心条带基线，再研究保留联合状态—参数关系的固定复杂度方法。创新性须以近邻文献、一般性证明与同预算对照共同确认，不能仅凭学习、SMF、MPC和四旋翼的组合。另一候选是有限预算下学习选择认证收紧任务，是否采用RL取决于相对简单策略的真实收益。

[12 控制权限与输入结构](docs/learning/12_feedback_authority_and_input_structure.md) 的外包改进与不可行性结论保留为控制基础：不为已否定的旧独立全域盒继续搜索覆盖初始中心的终端证书；完整输出反馈、终端条件和递归可行性仍未闭合。

初版方案：2026-09-08；理论优先重置：2026-09-10。AI 辅助文献分析与推导，作者需复核理论及实验；没有代替作者实施人类阅读确认。仓库原有项目名保留。

## 单步共享气动因子图审计（2026-10-12）

```bash
PYTHONPATH=verification python verification/check_vertical_shared_factor_graph.py \
  --output results/theory_vertical_shared_factor_graph_20261012/exact_checks.json
pytest -q verification/test_vertical_shared_factor_graph.py
```

精确证书表明Run169点满足真实单步共享气动因子图，因此可靠的单步CZ/SPZ外包不能排除其像；这不证明该点可由初始集跨时刻到达。详见[106 单步共享气动因子图](docs/learning/106_vertical_shared_factor_graph.md)及归档`results/theory_vertical_shared_factor_graph_20261012/exact_checks.json`。

## 跨时刻竖直速度排除证书（2026-10-12）

```bash
PYTHONPATH=verification python verification/check_vertical_cross_time_velocity_exclusion.py \
  --output results/theory_vertical_cross_time_velocity_exclusion_20261012/exact_checks.json
python -m unittest -q verification.test_vertical_cross_time_velocity_exclusion
```

从配置初始集出发的精确15步投影界排除了Run169竖直速度端点；仍需联合传播横向速度与姿态以核查全部可达气动支持。详见[107 跨时刻竖直速度投影](docs/learning/107_vertical_cross_time_velocity_exclusion.md)。

## 首个15步窗口气动支持（2026-10-12）

```bash
PYTHONPATH=verification python verification/check_vertical_initial_window_aero_support.py \
  --output results/theory_vertical_initial_window_aero_support_20261012/exact_checks.json
python -m unittest -q verification.test_vertical_initial_window_aero_support
```

分层有理数外包认证配置初始集首个15步窗口的竖直气动核心支持不超过`1.23048791`，低于Run168门槛；该结论尚未覆盖测量reset后的重复周期。详见[108 首窗口气动支持](docs/learning/108_vertical_initial_window_aero_support.md)。

## 成功测量不等于物理reset（2026-10-12，Run175量词纠错）

```bash
PYTHONPATH=verification python verification/check_vertical_measurement_reset_obstruction.py \
  --output results/theory_vertical_measurement_reset_obstruction_20261012/exact_checks.json
python -m unittest -q verification.test_vertical_measurement_reset_obstruction
```

五步精确plant轨迹仍表明成功位置测量本身不会把真实竖直速度重置到配置初始盒；但该轨迹使用最大推力，而推力属于控制器选择，因此不能据此否定存在因果策略实现受控回返。Run173首窗口证书不能仅凭测量成功直接逐周期复用；受控回返是否成立仍须按“存在同一观测fiber策略、对全部扰动与缺测路径”验证。详见[109 测量reset反例](docs/learning/109_vertical_measurement_reset_obstruction.md)和[Run175量词纠错](docs/research/run175_research_log.md)。

Run176进一步确认仓库已有线性product-fiber前驱与固定J14策略无关反证，重复实现策略类没有价值；当前未决对象收敛为配置初始posterior上的五步非线性information-state predecessor。详见[110 受控回返前驱排重](docs/learning/110_controlled_return_predecessor_dedup.md)。

Run177进一步纠正该对象：配置产生的是随tick-0测量变化的posterior族，不是单个盒；第五个输入先于tick-5位置包，且success/miss后继进入不同mode。故暂不实现会混淆物理回返与测量收缩的单盒检查器；当轮曾把下一步记为定义mode-indexed terminal information-family，已由Run178排重纠正。详见[111 五步information-state合同](docs/learning/111_five_step_information_state_contract.md)。

Run178排重纠正Run177的下一步：`T0/T1`只是一对局部success/miss边，仓库第88、89章和Run154已定义更完整的60-state扩展、15个首次返回瞬态标签与45个循环terminal标签。故停止重复的两族checker；下一步应先为真实非线性plant冻结fixed-complexity `Gamma`及可靠逐边包含oracle。详见[112 terminal information-family排重](docs/learning/112_terminal_information_family_dedup.md)。

Run179进一步纠正`Gamma`的类型：普通CZ/SPZ降阶只压缩一条已实现history的posterior，不能直接表示连续可见`d`上的集合值策略图。下一步必须先冻结lifted `(d,s)` cell、fixed normals和cell内仿射fiber policy，再验证一条真实非线性miss边。详见[113 参数化Gamma类型审计](docs/learning/113_parameterized_gamma_obstruction.md)。

最新传统基线进展见[119 固定单斜向形状阻断](docs/learning/119_single_slant_shape_cycle.md)：独立复审纠正`q=p-(1/10)v`坐标变换后，固定`(p,q)` parallelogram的15步`q->q`增益严格大于1，不能周期闭合。该结果不否定保留原active velocity facets的六边形；完整configuration/meta LP仍待构造。
