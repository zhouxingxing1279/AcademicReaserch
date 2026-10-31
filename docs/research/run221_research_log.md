# Run221 — 姿态通道SMF＋终端Tube MPC最小递归可行闭环（2026-10-31）

**基准远端main：** `df66453b7dc0565905c3d366c77f1ee0f27f2141`。**唯一瓶颈：** Run220在第193拍继续堆叠历史条带没有产生新增可认证收益，且现有四状态有限Backup不具备终端不变性。先在仓库真实Euler姿态子通道建立有完整量词的正向安全/递归可行基线，再讨论扩展到横向/垂向及缺测。

## 模型、信息权限及边界

取`configs/planar_baseline.json`中姿态子系统：`x=(phi,omega)`，`h=J=1/50`，`x^+=(phi+h*omega,omega+h*tau/J)`，`|phi|<=9/20`、`|omega|<=2`、`|tau|<=2/25`。每拍测量`y=x+n`，`|n_phi|<=1/200`、`|n_omega|<=1/100`；每拍姿态/角速度均可见（仓库`sensing.always_observed_indices=[4,5]`），姿态过程扰动为零。**位置传感丢包、横向/垂向残差、推力跳变及六状态约束均不在本证书内。**

使用区间SMF：`S_{k|k}=((A S_{k-1|k-1}+B tau_{k-1})∩[y_k-sigma,y_k+sigma])`（实现中每维分别外包），控制器只读取SMF中点`hat{x}_k`及名义`z_k`，不读取仿真真值。由于真值属于后验且每维后验宽度至多`2 sigma`，有`|hat{x}_k-x_k|<=sigma`；若该半宽预算不成立则拒绝认证（fail closed）。

## 可独立检查的严格代数证书

选择`K=(-8/25,-4/25)`，真实控制`tau=v+K(hat{x}-z)`，名义`z^+=Az+Bv`，误差`e=x-z`。令`r=23/25`、`s=e_omega+4e_phi`。误差满足

```
e_phi^+ = r e_phi + h s
s^+     = r s + K (hat{x}-x)
```

测量中点误差导致`|K(hat{x}-x)|<=2/625`。因此

- 误差RPI：`E={|e_phi|<=1/100, |e_omega+4e_phi|<=1/25}`；两个严格上界分别为`r/100+h/25=1/100`和`r/25+2/625=1/25`（均精确取等）。
- 真值硬约束收紧：名义`|z_phi|<=11/25`、`|z_omega|<=48/25`；`sup_E |Ke|=6/625`，再加测量中点误差`2/625`，得到`|v|<=42/625`。因此对任意允许真值与测量噪声，真实`|tau|<=2/25`、`|phi|<=9/20`、`|omega|<=2`。
- 名义终端集合：`Z_f={|z_phi|<=1/20, |z_omega+4z_phi|<=1/5}`；终端律`v_f=Kz`。变换后`|z_phi^+|<=r/20+h/5=1/20`、`|s_z^+|<=r/5<1/5`，且`sup_{Z_f}|Kz|=6/125<42/625`，故`Z_f`在收紧状态与输入约束内正不变。

有限预测时域`N=3`，每轮枚举`{-0.06,-0.03,0,0.03,0.06}^3`中所有满足收紧状态/输入与终端集合的计划，以有理数代价选择较优者，并始终把上轮可行尾计划作为候选。执行首拍`v_0`后，下一拍候选为`(v_1,v_2,K z_N)`；由`Z_f`不变性、固定名义状态更新及`E`不变性，此尾计划对**所有**允许测量噪声序列保持可行。初态`z_0=0`、`x_0`在配置的姿态初始盒内，零计划满足终端约束。因此**对上述孤立姿态模型，任意时间的递归可行性、SMF真值包含、姿态/角速度/力矩硬约束满足具有数学保证**；并不依赖下述有限重放统计。

**特别声明：** 这不是连续QP最优解，也没有终端Lyapunov下降/目标收敛证明。`check_terminal_polytope.py`已有同一K与误差变换的RPI证书；本轮的增量是把仓库的真实姿态测量、SMF中点、名义有限网格优化、移位尾计划、物理硬约束连接成可执行闭环，不能将既有RPI理论当作新颖贡献。

## 实验、对照与证据级别

本地`Linux, Python 3.13.5`，无第三方依赖。命令：

```
PYTHONPATH=verification python -m unittest -v verification.test_attitude_terminal_smf_mpc
PYTHONPATH=verification python verification/check_attitude_terminal_smf_mpc.py --output results/attitude_terminal_smf_mpc_20261031/checks.json
python -m py_compile verification/check_attitude_terminal_smf_mpc.py verification/test_attitude_terminal_smf_mpc.py
```

本地**6项测试中5项通过、1项因无完整仓库checkout显式跳过**；另完成完整的代码编译。验证包括：`E/Z_f`解析不变性、16个误差/测量噪声极端角点、所有可行3拍网格计划的移位可行性、SMF真值包含、错误测量拒绝及确定性闭环。

与同样SMF及K、但名义仅执行终端律的`terminal_only`对照，采用4个初始姿态角点×4种合法测量噪声序列×2策略，共32条48拍轨迹（1536拍）。有限样本中：SMF覆盖1536/1536个后续状态（另有32个初态包含），硬约束违约0，MPC优化器相对尾计划变更624次；平均角度跟踪RMSE：MPC **0.0132953553 rad**，terminal_only **0.0400187357 rad**。最大实际角度约0.04996154 rad、角速度约0.25498360 rad、力矩0.0632 N·m。**跟踪收益仅为这16对确定性样本，不是最优性或统计显著性结论**。

本地100次固定原点优化的耗时中位数约5.49ms、p95约6.70ms、最大约7.68ms；8次48拍MPC重放的平均每拍墙钟约4.47ms（本地单机、非WCET）。没有证明20ms实时上界，也不能将此速度外推到四/六状态问题。由于本地github.com DNS解析失败，配置核验测试须在GitHub Actions完整checkout执行；本轮新增工作流负责完整配置断言、6项测试、结果文件再生成逐字比对。

## 文献阅读与定位（2026-10-31）

1. **Mayne、Raković、Findeisen、Allgöwer (2006)**, *Robust output feedback model predictive control of constrained linear systems*, *Automatica* 42(7):1217–1222，DOI https://doi.org/10.1016/j.automatica.2006.03.005；作者公开PDF https://www2.ee.ic.ac.uk/publications/p5346.pdf 。本轮直接阅读§2–4、Propositions 1–3、Theorems 1–2与终端条件A1–A3。该文采用Luenberger观测器、估计误差与名义误差RPI、Pontryagin收紧和终端代价，证明相应假设下鲁棒约束满足与稳定性。本轮改用区间SMF中点与固定名义状态，并**只证明终端不变/递归可行，不援引其稳定性定理**；需另证A3式终端下降与扩展信息合同。
2. **Lorenzetti、Pavone (2020)**, *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, ECC 2020，DOI https://doi.org/10.23919/ECC51009.2020.9143979，arXiv https://arxiv.org/abs/1911.07360，作者稿 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。本轮直接核对§II–IV-D式(7)–(11)：固定截面Tube、收紧的名义MPC及终端控制/下降条件。其固定截面方法不是本项目创新；本轮缺少终端下降和高维实时综合。

统一`docs/literature/PAPER_READING_LOG.md`保持87篇去重，不把已存在的两篇重复计数。

## 课题可行性/创新性/难度及下轮唯一任务

- **可行性：** 孤立姿态通道已具备严格正向递归可行基线；四状态/六状态Gate A依然blocked，不能宣称无人机整体安全。
- **创新性：** 本轮是可靠工程基线，不构成新理论；后续创新性需在同等终端保证和预算下证实测量条件化SMF/CZ减少保守性。
- **难度：** 将此正向终端证书扩展到`(p_x,v_x,phi,omega)`时，位置缺测、推力跳变与横向扰动会破坏简单固定截面RPI；需要全量词的可行性/安全证书。

**下一轮唯一优先任务：** 在四状态冻结横向—姿态系统中检验本轮姿态终端集合能否与横向状态/速度硬约束组成一个**充分的、因果的受控不变终端集合**；若不能，构造精确阻塞证书，不把姿态子通道的递归可行性误推广到四状态。


## 完整仓库GitHub Actions补充验证（2026-10-31 15:09 UTC）

[Run221 CI #41213452861](https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41213452861) 在GitHub-hosted Ubuntu、Python 3.13.17、**完整checkout**中执行：6/6项测试通过（包含对真实`configs/planar_baseline.json`的严格合同断言），`py_compile`通过，脚本使用`--root .`重新生成`checks.json`并与提交工件`diff -u`逐字相等。CI结论`success`，无跳过、无失败。此结果验证的是本轮两状态模块与配置的一致性及可复现性；不等于全仓库历史回归、四/六状态闭环或20ms最坏执行时间。
