# 理论核对与历史数值检查

本目录区分解析证明的精确算术核对和历史浮点检查，均不运行新的 MPC 闭环实验。

## 跨时刻可达集包含

[check_shifted_reachable_inclusion.py](check_shifted_reachable_inclusion.py) 核对 [学习 09](../docs/learning/09_shifted_reachable_inclusion.md) 的绝对集合中心位移、旧控制尾部平移、扰动集合嵌套与缺测恒等更新，并保存改变控制、扩大扰动和忽略中心位移的负对照。

```bash
python -m unittest discover -s verification -p test_shifted_reachable_inclusion.py -v
python verification/check_shifted_reachable_inclusion.py --output /tmp/shifted_reachable.json
```

输出路径须不存在。该核查只通过声明的六维仿射合同；结果中的完整 MPC 递归可行性门保持 blocked，直到控制侧 tube 与终端证书完成。

## 竖直硬约束的精确可达支持

[check_vertical_hard_constraints.py](check_vertical_hard_constraints.py) 核对 [09](../docs/theory/09_vertical_input_certificate.md) 的完整生成元传播、固定序列第 30 步首次输入支持越限及达到该值的 39 个原始参数；另核对任意实际共同输入从误差方程消去。

```bash
python verification/check_vertical_hard_constraints.py --output /tmp/vertical_constraints.json
```

输出路径须不存在。归档见 [checks.json](../results/theory_vertical_constraints_20260913/checks.json)。没有认证受限输入下的状态安全，也没有证明反例可由原气动风场实现。

## 新增益筛选与任意缺测观测界

[check_gain_screen.py](check_gain_screen.py) 核对 [08](../docs/theory/08_gain_screen_and_switched_observer.md) 的提升误差映射全部系数、任意间隔统一界、启动期、恒定扰动必要条件与 Jury 余量，并拒绝遗漏绝对值的负对照。

```bash
python verification/check_gain_screen.py --output /tmp/gain_screen.json
```

输出路径须不存在。结果见 [checks.json](../results/theory_gain_screen_20260913/checks.json)。没有原硬约束或六维终端安全认证，不改写 06 的旧矩阵。

## 终端候选否证的精确核对

[check_terminal_obstruction.py](check_terminal_obstruction.py) 核对 [07](../docs/theory/07_terminal_candidate_obstruction.md) 的周期误差均值、增益必要条件，以及独立盒模型第 88 步首次越界的有理数见证。它复用 06 映射，不调用气动真值或运行经验控制试验。

```bash
python verification/check_terminal_obstruction.py --output /tmp/terminal_counterexample.json
```

输出路径须不存在。归档见 [counterexample.json](../results/theory_obstruction_20260913/counterexample.json)。结论只否定当前候选与独立盒的组合，不能推断原解析气动世界可实现该反例。

## 因果增广模型的精确核对

[check_causal_model.py](check_causal_model.py) 生成 [06](../docs/theory/06_causal_augmented_model.md) 的成功/缺测两组 14 维有理数矩阵，核对全部线性误差系数、输入对未知真值的零直接依赖、遗漏校正负对照和最长 15 步包间隔。

```bash
python verification/check_causal_model.py --output /tmp/causal_matrices.json
```

输出路径须不存在。仅需标准库；复用前序证书核对。结果见 [matrices.json](../results/theory_causal_model_20260913/matrices.json)。解析余项界须结合正文证明；没有验证候选增益稳定性、全系统不变性或学习优势。

## 有限姿态多面体证书的精确核对

[check_terminal_polytope.py](check_terminal_polytope.py) 使用标准库 Fraction 核对 [理论 05](../docs/theory/05_finite_terminal_polytope.md)：坐标变换、四面非负乘子、初始包含、参考严格见证和改进后的 40 步界。错误乘子与过小矩形必须被拒绝。

```bash
python verification/check_terminal_polytope.py --output /tmp/terminal_polytope_certificate.json
python verification/plot_terminal_polytope.py --output /tmp/polytope_and_reference.svg
```

输出路径须不存在。绘图另需 NumPy/Matplotlib，浮点图形不参与包含验证。归档见 [certificate.json](../results/theory_terminal_polytope_20260911/certificate.json) 与 [manifest.json](../results/theory_terminal_polytope_20260911/manifest.json)。通用 `exact_inclusion` 只检查给定仿射映射的充分包含条件，不自动验证真实非线性外包、控制因果性或六维终端闭合。类内最小性及核包含仍需结合正文证明。

## 六维有限时域证明的精确核对

[check_coupled_theory.py](check_coupled_theory.py) 使用 Python 标准库 Fraction，核对 [理论 04](../docs/theory/04_coupled_predecessor_and_finite_horizon.md) 的参考多项式、41 个先验时刻的六维包络、域内余量、结构比较和终端反例。配置与解析基准公式的文件哈希必须匹配；它只读取公式文件哈希，不导入真值生成器。

```bash
python verification/check_coupled_theory.py --output /tmp/coupled_exact_checks.json
```

输出文件须不存在。该脚本复用下述姿态代数检查，不能只把六维数值表从旧报告复制过来。完整归档见 [exact_checks.json](../results/theory_coupling_20260910/exact_checks.json)。结论覆盖 0..40 tick，尚未证明六维无限时域不变性或学习优势。

安装有 NumPy/Matplotlib 的原科学绘图环境可运行：

```bash
python verification/plot_coupled_bounds.py --output /tmp/finite_horizon_bounds.svg
```

图中显示解析集合上界，不是真实状态轨迹；浮点绘图不参与证书核对。

## 姿态子系统证明的精确核对

[check_invariance_theory.py](check_invariance_theory.py) 使用 Python 标准库 `fractions.Fraction`，读取当前配置并核对姿态闭环矩阵、幂零恒等式、级数外包界、输入余量、时变参考收紧界、非零参考见证与不可恢复反例。

```bash
python verification/check_invariance_theory.py --output /tmp/invariance_exact_checks.json
```

输出文件须不存在。无穷时域与集合包含的证明见 [理论 03](../docs/theory/03_invariant_domain_analysis.md)，脚本仅复核有限算术，不能自动证明全系统安全。归档结果见 [exact_checks.json](../results/theory_invariance_20260910/exact_checks.json)。

[plot_attitude_kernel.py](plot_attitude_kernel.py) 需要 NumPy、Matplotlib；按解析公式绘制示意图，浮点绘图不用于验证包含关系：

```bash
python verification/plot_attitude_kernel.py --output /tmp/attitude_kernel.svg
```

## 历史浮点检查的范围

下文仅描述 `run_checks.py` 的代数 smoke checks，没有由该脚本完成安全证明。固定随机种子为 `20260908`；同一数值环境下可重复，跨 BLAS/平台允许浮点尾数差异。

## 运行

需要 Python 3、NumPy、SciPy（`scipy.optimize.linprog` 使用 HiGHS）。不依赖 GPU、SymPy 或商业求解器。运行前按项目依赖说明建立环境；首次运行结果会记录实际版本。

```bash
python verification/run_checks.py
python verification/run_checks.py --output verification/algebra_checks.json
```

全部通过时退出码为 0；检查失败时退出码为 1。JSON 包含源码 SHA-256、环境版本、随机种子、样本量和误差阈值，不包含不可复现的时间戳。`algebra_checks.json` 是本脚本实际执行结果，不能作为论文控制实验表格。

## 检查对象与解释

| 检查 | 方法与成功条件 | 不能说明什么 |
|---|---|---|
| 平面四旋翼模型 | 悬停点不漂移；Euler 离散状态/输入解析 Jacobian 对中心差分误差小于 `1e-8` | 不验证 Euler 精度、真实动力学或非悬停 Jacobian |
| 输出反馈增广误差 | 100 组随机矩阵，直接真值/观测器更新对误差递推误差小于 `1e-11`；漏掉 `-BK eta` 的负对照必须失败 | 不证明观测器收敛、闭环稳定、鲁棒不变性 |
| 测量条带外包络 | 500 个可行状态及噪声，显式有界生成系数重构误差小于 `1e-11` | 不表示得到精确交集，也不证明任意代码路径正确 |
| 支持函数 | 30 个方向的 HiGHS LP 对普通 zonotope 解析支持函数误差小于 `1e-10`；检查随机点及 box hull 的大小关系 | 不检查 constrained zonotope 的等式约束 LP |
| tanh MLP 区间 | 两层网络的 1000 个输入样本位于区间传播结果内 | 样本通过不是全域认证；不是物理残差包络 |
| Lipschitz 网格补偿 | 已知 `sin` 玩具真值和小网络，解析导数界构造网格覆盖余量，对 2000 个随机点检查 | 玩具模型的导数界不能移植到真实无人机 |
| 测量调度 | 基础周期 0.02 s、每 5 tick 测量、连续丢 2 次机会：14 个无校正 tick、15 个传播步、到达间隔 0.30 s | 不证明控制器能容忍该丢测时长 |

状态顺序固定为 `[px,pz,vx,vz,phi,omega]`，输入 `[T,tau]`，质量 1 kg、惯量 0.02 kg m²、重力 9.81 m/s²。姿态为零时推力沿正 z；正俯仰使水平推力沿负 x。网络检查使用独立玩具参数，不是训练所得模型。

观测器检查约定为：先以实际输入预测 `hat x^- = A hat x + B u`，再使用 **下一时刻** 测量 `y[k+1]` 校正。控制量由当前后验估计给出。改变更新顺序或时间索引时必须重新推导，不能沿用公式。

## 后续验证门槛

以下为历史实现顺序；当前推进顺序以 [理论准入表](../docs/theory/02_review_and_gates.md) 为准，完整不变性及学习独立优势未通过前，不恢复新的训练或控制实现。

1. 主文档中的符号推导和假设先经人工/独立复核；本脚本不替代推导。
2. 实现带单位约束、真实测量时序的滤波器和控制器；加入非悬停线性化及数值积分收敛验证。
3. 单独建立每个训练模型的残差包络、工作域覆盖条件，以及状态/输入误差处理。
4. 按主文档的 A/B/C/D 对照开展完整闭环实验，日志与本目录代数检查结果分开。
5. 在满足安全与模型有效性条件前，不从有限仿真声称确定性约束保证或实飞可用。

## 学习方向选择的机制核查

[check_direction_selection.py](check_direction_selection.py) 使用 Fraction 核对八个二维集合的四类单查询规则、可靠包含与冗余负对照，见 [报告](../docs/learning/01_direction_selection_probe.md)。这是无量纲几何探针，不是网络或四旋翼性能实验。

```bash
python verification/check_direction_selection.py --output /tmp/direction_probe.json
```

输出须不存在。结果见 [checks.json](../results/direction_probe_20260915/checks.json)。


## C2：六维模式集合与控制接口否证（2026-09-16）

```bash
python verification/check_mode_nestedness.py --output /tmp/mode_nestedness.json
```

标准库 Fraction；路径须不存在。核查15个六维度量、17条模式边、2176个盒顶点与442个模式移位关系，并验证统一 Young 椭球收紧在第3步违反原速度区间宽度必要条件。`status=pass` 表示代数和否证核查通过，`mpc_ellipsoid_only_gate.status=blocked` 表示该控制接口不通过；不等同于物理系统不可控。来源哈希及精确分数见 `results/theory_mode_nestedness_20260916/exact_checks.json`，解析证明及 C2-R 任务见 `docs/learning/06_mode_dependent_nestedness.md`。


## C2-R：模式条件半径与方向集合对照（2026-09-16）

```bash
python -m unittest discover -s verification -p test_mode_radius.py -v
python verification/check_mode_radius.py --output /tmp/mode_radius.json
```

使用 Fraction 与整数平方根向外舍入，核查模式条件半径、442项移位关系，以及全允许路径生成元坐标支持的312项后向方向复核。结果将 `radius_control_gate=blocked` 与 `geometry_coordinate_width_gate=pass_finite_horizon_only` 分开报告。原初始盒下的25步坐标宽度通过不代表 MPC、终端、任意滚动窗口、实时性或完整闭环通过。精确值、峰值路径及哈希见 `results/theory_mode_radius_20260916/exact_checks.json`，论证见 `docs/learning/07_mode_radius_and_geometry.md`。


## C2-G/CZ：约束 zonotope 有界试验（2026-09-16）

```bash
python -m unittest discover -s verification -p test_constrained_zonotope.py -v
python verification/check_constrained_zonotope.py --output /tmp/cz_certificates.json
```

输出路径须不存在。SciPy 仅提议 LP 对偶乘子，Fraction 复算可靠支持上界；三项解析回归覆盖非零条带、中心变换、任意乘子和删除等式反例。两条指定观测记录另生成36项证书，见 results/constrained_zonotope_20260916/certificates.json 与 docs/learning/08_constrained_zonotope_interface.md。physical_domain_gate 若为 blocked，则不得解释为完整25步物理外包证书。此比较不证明 MPC、固定复杂度、实时性、任意未来观测或学习优势。


## C2-G/T：固定模板CZ与滚动夹逼（2026-09-17）

```bash
python -m unittest discover -s verification -p test_cz_template.py -v
python verification/check_cz_template.py --output /tmp/cz_template_checks.json
python verification/check_template_reference.py --template-result /tmp/cz_template_checks.json --output /tmp/cz_reference.json
```

输出文件须不存在。六个解析回归、60次移位更新、28,548项有理支持/舍入核查、27,000项移位方向界比较与1,586个成员见证。发布表示12/6，临时测量最多16/10；位长与运行时间不因此固定。模板精度未通过，tick9第25层发布坐标界不能认证原域，60步末端后验发布速度半宽也超3；不压缩离线参考明显更紧，但不是同预算性能对照。结果见 results/cz_template_20260917，条件证明和范围见 docs/learning/10_fixed_template_cz.md。
