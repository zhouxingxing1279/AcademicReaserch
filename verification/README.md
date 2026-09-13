# 理论核对与历史数值检查

本目录区分解析证明的精确算术核对和历史浮点检查，均不运行新的 MPC 闭环实验。

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
