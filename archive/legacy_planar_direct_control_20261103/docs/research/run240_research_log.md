# Run240 — 5/10/15拍全部成功观测值的精确SMF速度区间包络（2026-11-01）

**基准main：** e8e2516146b9390a8c5b7d9166a581ff45f7e922。**唯一瓶颈：** Run239仅对成功观测y=0精确计算后验，并指出某极端y不降低速度绝对上界；必须区分“绝对速度上界”和“后验区间半宽”，检验全部可达y及5/10/15拍失测模式。

## 1. 数学方法与全量词

沿用Run236两个初始状态x±=(0,±hD,0,0)，冻结四状态Euler、固定T=9.81N、tau=0、h=1/50s、逐拍独立r∈[-3246383/1600000,+3246383/1600000]，成功位置包|y-p|≤1/50m。对于n∈{5,10,15}，每个初始符号s的p_n,v_n均为n个扰动系数的仿射函数；给定任意实数成功观测y，按位置生成元p_j和速度生成元v_j的v_j/p_j排序，构造分数背包原始见证及候选对偶斜率λ∈{0,v_j/p_j}，精确Fraction验证原始值=对偶值，得到各分支速度上支持U_s(y)。两分支并集的U(y)=max_s U_s(y)，由中心对称性L(y)=-U(-y)，故区间外包半径r(y)=[U(y)+U(-y)]/2。此区间是后验并集的最小一维区间外包，**不等于后验非凸集合本身**。

对每支，U_s(y)仅在有限个由位置可达端点和贪心扰动系数翻转产生的y断点处改变仿射表达式；其可行区间外不参与上包络。在相邻断点的开区间上，U(y)及U(-y)分别为若干仿射函数的最大值，故r(y)为凸分段仿射函数，其最大值不超过相邻端点的较大值；在支路可行性端点亦逐一直接评价。因此枚举**20/40/60个精确有理数断点**即可认证全部连续可达实数y，而非网格采样。每个支路原始—对偶等式由程序逐点检验。

| 成功观测间隔 | 观测前速度半宽(m/s) | 全部y中最大后验区间半宽(m/s) | 最坏半宽缩减 |
|---|---:|---:|---:|
| 5拍 | 0.2464585125 | 0.2464585125 | 0% |
| 10拍 | 0.4493574500 | 0.3188500014 | 29.04% |
| 15拍 | 0.6522563875 | 0.3681367927 | 43.56% |

三种模式的最坏区间半宽均可由y=0达到。**严格负面结果：** 5拍时噪声条带足够宽，y=0对速度区间无任何收缩；故“所有5/10/15成功包都统一严格收缩”是假命题。即使10/15拍有统一半宽收缩，对y等于先验正向极端位置的观测，后验速度**绝对上界**仍可等于先验上界；这不矛盾，因为区间中心随观测移动。最后一拍扰动对位置无影响，故仅靠本拍位置观测无法消除至少hR≈0.04058m/s的隐藏速度半宽。

在该指定初始纤维下，无论成功观测y如何，继续忽略该观测、执行同一个零力矩15拍，其0到n+15的状态绝对值被未条件化zonotope外包。n=15最坏末端|p|≤303343917/800000000≈0.379180m、|v|≤3152383/2500000≈1.260953m/s，仍严格低于冻结硬约束。**只是有限时域安全，不是可重复闭合、MPC、或无限时域RCI。**

## 2. 文献核验（已读去重91篇不变）

- Yang, Liren; Ozay, Necmiye (2021), *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 54(5):97–102, DOI https://doi.org/10.1016/j.ifacol.2021.08.481，作者全文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。本轮实际重读§3 Problem Statement、Assumption 1、§4.1–4.2 String Automaton/Causality、Proposition 2。研究问题是受自动机约束的丢包序列下的无限时域硬安全；以字符串自动机和因果输入承诺构造product safety game。关键假设包括成功包给出**无噪完整状态**、初始包成功和有界连续丢包；这些不同于本仓库有噪位置+每拍姿态量测。论文的安全游戏需覆盖全部允许丢包串，不能由本轮固定零力矩有限管替代。其结构与方法属于已有成果，不是本轮创新。
- Scott, J. K.; Raimondo, D. M.; Marseglia, G. R.; Braatz, R. D. (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69:126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036，作者全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。本轮复核摘要、Proposition 1的集合交框架和历史Run239阅读笔记；后验各分支精确线性条带交可用CZ表示，但本轮一维支持计算是项目实现，未使用论文定理直接证明递归控制。未阅读全文，不新增去重已读篇数。

## 3. 可复现工件、证据与下一轮

- 验证器：verification/check_four_state_all_observations.py；13项测试：verification/test_four_state_all_observations.py；归档：results/four_state_all_observations_20261101/checks.json；CI：.github/workflows/run240-all-observations.yml。
- 命令：PYTHONPATH=verification python -m unittest -v verification.test_four_state_all_observations；python -m py_compile verification/check_four_state_all_observations.py verification/test_four_state_all_observations.py；python verification/check_four_state_all_observations.py --root . --output /tmp/run240_certificate.json；diff -u results/four_state_all_observations_20261101/checks.json /tmp/run240_certificate.json。
- 本地隔离Python3执行13项测试：12通过、1项因缺完整仓库配置跳过；语法编译、JSON生成通过。完整checkout CI需真实运行并读取结果，不能预先宣称成功。严格证据限于指定两点纤维、固定零力矩与有界残差的精确一维后验区间和有限安全管。没有一般初始SMF后验、可调共享恢复律、四状态输出反馈MPC、递归可行、六状态耦合安全、稳定性或20ms最坏时延认证。
- 可行性：后验条件化计算可行；创新性：分数背包和CZ条带均为已知基础运算，尚不足独立支撑硕士论文；研究难度：在每个y与每种丢包模式上构造shift-compatible共享备份/终端集合仍高。
- **下一轮唯一优先任务：** 基于本轮全部y的速度区间，构造**依赖可见后验而非隐藏真实状态**的非零力矩恢复控制准入判据，首先检验15拍最坏观测后的共享控制是否能使信息状态严格回到一个可重复闭合的候选域；失败时保留对抗反例。


## 4. 完整checkout CI、PR与main落地核验（2026-11-01）

研究PR #49 https://github.com/zhouxingxing1279/AcademicReaserch/pull/49 基于main e8e2516146b9390a8c5b7d9166a581ff45f7e922，ahead=1/behind=0、mergeable=true、预期head 8780c7ed819fede385a75b1fad37497d41956039；完整checkout PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41301543344 为completed/success。Python 3.13完整仓库执行Run224–240共**134/134项聚焦测试通过、无跳过**（21.819s），真实配置合同、精确Fraction原始—对偶断言、归档JSON逐字diff、代码编译与工件上传均成功。通过非强制Squash合并至main SHA **af072cccf1cee23a711c1d0d756d32623f38d3d0**，随后重新读取远端main与源码/测试/JSON/论文记录/检查点Blob，均已落地。main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41301632613 亦为completed/success，134/134通过、无跳过（22.382s），JSON一致并上传工件。**未执行全仓库历史回归**；这些测试不证明一般输出反馈递归可行或20ms最坏时延。
