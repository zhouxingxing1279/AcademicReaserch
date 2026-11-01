# Run233 — 四状态全状态反馈数值种子与RCI构造方向（2026-10-31）

**基准main：** 8cee19a9a937f7037cf4ba1b28f2ede8ed82b98b。**唯一研究瓶颈：** Run224–232持续得到有限步正/反证书但尚无非空终端RCI；本轮不继续扩大单一速度桥或机械延长前驱步数，而是建立可运行的四状态反馈候选与反例基线，为相关多单元RCI内核搜索提供可复现种子。此次不声称已获得终端闭合循环。

## 模型、控制与证据级别

使用 configs/planar_baseline.json 的冻结Euler横向四状态 x=(p,v,phi,omega)，h=0.02s、I=0.02kg m²，p+=p+h v，v+=v+h(-T sin(phi)+r)，phi+=phi+h omega，omega+=omega+h tau/I；约束 |p|<=5m、|v|<=3m/s、|phi|<=0.45rad、|omega|<=2rad/s、T∈[4.905,14.715]N、|tau|<=0.08Nm；控制后残差 |r|<=1.88+(243/16000)T。

固定T=9.81N、使用饱和全状态线性反馈 tau=clip(-Kx,-0.08,0.08)，K=(-0.58081592,-0.91373144,4.11224856,0.74135794)。K来自hover线性化离散系统的DARE/LQR数值解，Q=diag(1,1,10,1)、R=1；SciPy 1.17.0离线生成后冻结8位小数。它不是MPC，不使用SMF估计，不满足Run221的部分观测接口，亦无Lyapunov或RCI证明。**任何有限样本未越界仅为数值现象。**

## 可复现数值结果（本地Python 3.13.5）

每次1000拍=20秒。原点初始的7种残差序列：持续正极值、持续负极值、逐拍交替、40拍切换、80拍切换、根据位置符号向外推动、种子233的均匀随机残差，**均未观测到硬约束越界**。其中持续正极值下max(|p|,|v|,|phi|,|omega|)=(1.475019423m,0.843065081m/s,0.262841349rad,0.386475189rad/s)；80拍切换时速度最大1.477603441m/s、角速度最大0.85289411rad/s。固定T=9.81、tau=0的无反馈基线在同样持续正极值下**第74拍首次违约**。

另以种子233001生成128组小初始扰动：p,v∈[-0.05,0.05]、phi∈[-0.005,0.005]、omega∈[-0.01,0.01]，每组采用独立固定种子的1000拍均匀随机残差；观察到0/128违约，最大绝对状态分量=(0.259195888,0.451869508,0.090051287,0.320795279)，平均位置RMS=0.069574854m。以上**不是**对任意自适应扰动、任意初始集合或无限时域的安全保证；控制器调参及测试序列未作严格独立预注册，不据此宣称概率置信界。

新增验证器 verification/check_four_state_feedback_seed.py、8项unittest、完整checkout CI工作流、results/feedback_seed_20261031/checks.json。无运行时SciPy依赖，使用Python标准库。复现：

    PYTHONPATH=verification python -m unittest -v verification.test_four_state_feedback_seed
    python -m py_compile verification/check_four_state_feedback_seed.py verification/test_four_state_feedback_seed.py
    python verification/check_four_state_feedback_seed.py --root . --output /tmp/run233_summary.json

本地8项中7项通过，1项因隔离镜像没有完整仓库配置跳过；Python编译与JSON生成通过。完整checkout CI需运行后核验，不预先写为成功。尚无20ms最坏耗时保证。

## 文献与课题收敛

新增分节阅读Decardi-Nelson & Liu (2020), *Computing robust control invariant sets of constrained nonlinear systems: A graph algorithm approach*, arXiv:2009.13581，https://arxiv.org/abs/2009.13581；核对§2.1、§3.1–3.4、Theorems 2–3与Algorithm 1，未核实正式期刊DOI。该文图细分与内外近似区分支持本轮“先寻找候选、再做严格内核认证”的研究策略；论文并未替本项目证明任何安全性。唯一阅读日志去重90→91篇。

**Gate A=blocked。** 可行性：初步数值闭环轨迹提供可搜索的控制策略种子，但四状态非空RCI未知；创新性：LQR反馈和数值成功均属基线而非论文创新；难度：高。四状态输出反馈SMF+Tube MPC、递归可行、稳定性、六状态安全尚未建立。

**下一轮唯一优先任务：** 从本轮全状态反馈轨迹提取位置—速度—姿态—角速度相关的小单元，使用Run228严格Fraction外包及正确“先控制后扰动”的量词，验证候选终端集合的全部后继闭合；如认证失败，记录可归因于控制菜单、外包保守性或真实反例的不同证据，不将数值成功误称RCI。


## 完整checkout CI与安全合并的事后核验（2026-11-01 UTC）

研究PR #35 https://github.com/zhouxingxing1279/AcademicReaserch/pull/35 以基准main 8cee19a9a937f7037cf4ba1b28f2ede8ed82b98b 创建；合并前核验ahead=2、behind=0、mergeable=true、无冲突。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41268160006 与代码合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41268193922 均为**success**；完整checkout Python 3.13.17执行Run224–233共**69/69项聚焦测试通过，无跳过**，配置合同、源码编译、数值摘要与归档JSON对照及Actions工件上传均成功。PR #35以非强制Squash合并，首个main落地SHA 52d4d02cce7d9f60fb11a25880cec714c12992f4；重新读取远端main，源码与测试Git Blob SHA分别为 db9b5ac93c044af53af793341dc8007188ca7c4b、47bda39816624c5c4e19224f998cb636e6fa0cc7，与本地已测文件完全一致。

**边界不变：** 69项均为聚焦回归，未执行全仓库历史回归；7种固定扰动与128次随机实验未违约不等于RCI证明，也没有四状态输出反馈SMF+Tube MPC、递归可行、稳定性、六状态安全或20ms最坏耗时保证。本节仅补记CI证据，不修改算法。
