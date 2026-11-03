# Run239 — 15拍有噪位置观测下的精确SMF后验支持（2026-11-01）

**基准main：** f40c17e4833f6186c4e44b67b552c1a1e70f9e5e。**唯一瓶颈：** Run238仅证明指定两点隐藏速度纤维在零力矩下15拍安全，没有将成功位置观测转化为集合后验。此次保持冻结四状态Euler、固定T=9.81N、tau=0、h=.02s、r∈[-3246383/1600000,+3246383/1600000]，且只考虑Run236/238两个初始状态及其15拍可达集合。

## 1. 精确SMF预测、更新与证据

设初始速度符号s∈{-1,+1}，15个扰动系数ξ_j∈[-1,1]。每个分支的第15拍位置、速度均为系数的仿射映射，使用Run238精确生成元g_j。成功位置测量y=p+n，|n|≤1/50 m。给定y，后验为两个分支的并集，分支内引入测量噪声松弛ζ∈[-1,1]和一条等式p(ξ)+ζ/50=y，得到**每支16个变量的精确CZ**。两个初始点的并集不可默认为单个CZ，除非明确取凸外包。

对于y=0，通过Fraction枚举一维对偶折点λ∈{0,v_j/p_j}，结合固定初态符号的原始扰动分数背包构造，实现逐支原始/对偶最优值**精确相等**。后验速度半宽为353411321/960000000≈0.368136792708 m/s；Run238先验为52180511/80000000≈0.6522563875 m/s，减少约43.56%。取得上界的实际初态s=-1、测量相容位置p=+0.02，扰动系数详见JSON证书。无噪y=0的精确速度半宽为281453/1000000=0.281453 m/s；最后一拍扰动的生成元位置分量为零，故即使无噪位置观测，速度仍不能唯一确定。

**重要负面结果：** 取另一个合法成功观测y=+78628341/800000000 m，先验最大速度的轨迹仍与观测相容，因此后验速度上界仍为0.6522563875 m/s。**不能声称对所有观测存在统一收缩率**。独立位置/速度盒过滤会遗漏y=0下的速度相关性收益。

在**条件y=0**下，即使后续再用相同零力矩15拍，保守区间传播也得|p_30|≤690107493/3200000000≈0.215659m、|v_30|≤937760261/960000000≈0.976834m；姿态和角速度仍为零，故满足冻结硬约束。此为条件有限时域安全，不是可重复无限闭合。

## 2. 文献（分节阅读，不虚增计数）

Scott, Raimondo, Marseglia, Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, *Automatica* 69:126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036 ，作者公开PDF https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。本轮重新阅读Definition 3、Proposition 1的广义交式(13)、Proposition 2、§5估计递推式(31)–(33)。论文提供线性集合预测/交运算的理论背景，但本轮两分支支持函数/分数背包证书为项目独立推导。原文已有历史阅读记录，去重已读91篇不变。未阅读全文其余部分，不将原论文CZ算子视为本课题创新。

## 3. 复现、限制与课题评价

- 源码：verification/check_four_state_posterior_strip.py；测试：verification/test_four_state_posterior_strip.py（10项）；JSON：results/four_state_posterior_strip_20261101/checks.json；CI：.github/workflows/run239-posterior-strip.yml。
- 命令：PYTHONPATH=verification python -m unittest -v verification.test_four_state_posterior_strip；python -m py_compile verification/check_four_state_posterior_strip.py verification/test_four_state_posterior_strip.py；python verification/check_four_state_posterior_strip.py --root . --output /tmp/run239_certificate.json；diff -u results/four_state_posterior_strip_20261101/checks.json /tmp/run239_certificate.json。
- 本地隔离Python 3：10项中9通过、1项因缺完整checkout配置跳过，编译及JSON生成成功。完整checkout CI结果须单独核验，不提前宣称通过。
- 证明级别：指定两点初始纤维、固定零角动力学、单个y=0位置包条件下，15拍预测及有噪测量后验的速度支持为精确有理数结果；后续15拍为保守但严格有限安全上界。**不覆盖一般后验、任意观测统一收缩、完整四状态输出反馈Tube MPC递归可行、六状态耦合、稳定性或20ms最坏时延**。
- 可行性：历史相关的SMF更新已有可复核增量；创新性仍需一般观测与闭环控制收益对比；难度主要在递归信息状态不变性。

**下一轮唯一优先任务：** 对所有可达成功观测y（而非只y=0）和允许的5/10/15拍观测模式，构造统一可计算的SMF后验与因果恢复控制准入判据，先验证最坏观测分支是否存在可重复的安全后继。


## 4. 完整checkout与main落地核验（2026-11-01）

研究PR #47 https://github.com/zhouxingxing1279/AcademicReaserch/pull/47 在基准main未变、ahead=1/behind=0、mergeable=true、PR head SHA eb2d5270ee08a8436725cd20082ae1a81bcdd0b1 与预期一致后，经**非强制Squash**合并至main 60905d7f00c0da013e1d8995fa0da64af47fe8eb。重新读取main与源码、测试、归档JSON、论文阅读日志的Git Blob，全部与提交工件一致。

PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41296087821 和代码合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41296187607 均为completed/success。GitHub Actions Python 3.13.17完整checkout执行Run224–239共**121/121项聚焦测试通过、无跳过**（PR 28.623s，main 33.288s），真实配置核验、源码编译、精确Fraction原始—对偶证书、JSON逐字比对及artifact上传均成功。**尚未执行全仓库历史回归**；不证明一般后验递归可行或20ms最坏耗时。本段为证据补记，未改变算法。
