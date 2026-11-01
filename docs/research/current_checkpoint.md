# 当前研究检查点 — Run243（2026-11-01）

**基准远端main：** 8a795a5575bf787313ba23ad299007ee4f7be420。Run242的原位置脉冲固定重复局部不稳定。本轮构造从两次成功有噪位置包及已知力矩历史恢复速度的SMF区间；在**精确已知初始零姿态**的特殊冻结四状态模型下，对20/25/30拍包间隔给出全部残差/位置噪声下速度包含半宽0.526088/0.607537/0.695653m/s。该估计界有效但过宽。

**正向理论：** 采用饱和的u=0.5y+0.5vhat力矩幅值，承诺15拍角度复位脉冲。无噪无扰、局部不饱和时三个**固定**n=5/10/15宏周期的精确Jacobian行列式均0.9099442，全部Jury条件严格成立，故各固定模式局部渐近稳定；单宏周期局部盒可认证输入/状态安全但**未自映射**。75个混合模式宏周期的无扰浮点闭环终点p≈-0.003033m、v≈0.000511m/s，只是单轨迹现象，非任意切换稳定证明。

**核心缺口/负面结果：** 实际两包速度区间半宽至少0.526m/s，大于无饱和局部设计的0.1m/s速度盒，无法认证全扰动下力矩裕度、递归信息状态不变、完整四状态SMF+Tube MPC、六状态安全或20ms最坏时延。Gate A仍blocked。源码、13项测试、JSON证书、CI和详细边界见[Run243研究日志](run243_research_log.md)。本地隔离12通过/1跳过；完整checkout CI及main合并须以实际结果核验。

**文献：** Köhler/Müller/Allgöwer (2021) arXiv:2105.03427分节重读；Mayne等(2006) DOI 10.1016/j.automatica.2006.03.005仅书目/摘要复核。唯一论文日志去重仍91篇。

**下一轮唯一优先任务：** 将两包速度区间与Run240关联CZ后验交集，在实际残差/噪声和任意5/10/15成功模式下检验阻尼律共享输入裕度与信息状态递归闭合，保留失败证书。

---

**Run242完整checkout与main核验（2026-11-01）：** PR #53 https://github.com/zhouxingxing1279/AcademicReaserch/pull/53 已非强制Squash合并至代码main `4a63fa5eb64e8b49b9337853a3eac385e32aee27`，再次读取main SHA核验。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41309752362 和main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41309850659 均completed/success；Python 3.13.17完整checkout Run224–242聚焦测试**154/154通过、无跳过**，精确Fraction、真实配置、归档JSON与artifact上传成功。全仓库历史回归、一般SMF+MPC递归安全和20ms最坏时延仍未认证。该段为验证记录，不改变算法。

---

# 当前研究检查点 — Run242（2026-11-01）

**基准远端main：** 475cbf3598286ce4d57068dd876191ad88329684。Run241单次共享非零力矩脉冲严格保证指定两点后验纤维的15拍安全及10/15拍模式微小可靠上界收益；Run242检查原脉冲原样重复是否可作终端稳定策略。对固定n∈{5,10,15}零力矩等待+15拍脉冲的宏周期，允许的无噪无扰特例下，精确Fraction得到Jacobian det=1276487/1250000=1.0211896>1、判别式严格小于0，故两特征值模长均>1，非线性sin系统悬停平衡点局部不稳定。**严格排除的仅是此固定重复策略的局部稳定性，不排除其他有界RCI、模式切换或基于SMF后验速度的阻尼控制。**

**工件：** verification/check_four_state_repeated_pulse.py、verification/test_four_state_repeated_pulse.py、results/four_state_repeated_pulse_20261101/checks.json、.github/workflows/run242-repeated-pulse.yml、docs/research/run242_research_log.md。本地Python3 9项中8通过、1项因缺完整checkout跳过；真实配置与完整聚焦CI待运行验证。论文日志定向重读Yang/Ozay(2021)与Köhler/Müller/Allgöwer(2021)，去重91篇不变。

**Gate A=blocked：** 仍无一般SMF后验、四状态输出反馈Tube MPC递归可行/稳定、六状态安全及20ms最坏时延保证。**下一轮唯一任务：** 合成基于SMF后验速度信息的阻尼型共享恢复律，先证明固定宏周期Schur稳定，再认证模式相关误差管与信息状态递归闭合。

---
**Run241完整checkout与main核验（2026-11-01）：** 研究PR #51 https://github.com/zhouxingxing1279/AcademicReaserch/pull/51 已安全Squash合并至代码main `327adea4ed882bb236afde6b71ca40caacf10a88`，重新读取main SHA及源码/测试/JSON Blob确认落地。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41305256384 与main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41305374967 均completed/success；完整checkout Python 3.13.17聚焦测试**145/145通过、无跳过**，真实配置、精确Fraction、归档JSON和artifact上传成功。全仓库历史回归、SMF-MPC递归可行性及20ms最坏时延未认证。此补记不改变算法。

---

# 当前研究检查点 — Run241（2026-11-01）

**基准main：** `a61ed856bffe12058d4e8fc5cf9e15b7290c512b`。本轮在Run236两点隐藏速度纤维上，使用成功位置观测`y`设计共同可执行非零力矩脉冲`tau_j=(2/3)y[+1×3,-1×6,+1×3,0×3]_j`，对n=5/10/15全部合法成功观测、独立残差及噪声给出精确Fraction与sin Taylor余项的15拍可靠外包。全部中间硬约束认证通过，末端phi/omega精确归零。10/15拍模式相对零力矩基线的精确最坏终端位置/速度均有严格可靠上界改善；15拍分别至少0.0016587797m、0.0110585315m/s。5拍模式的证书上界反而更大，保留负面结果，不断言实际性能更差。详见[Run241日志](run241_research_log.md)及`verification/check_four_state_observation_pulse.py`。

**证据边界：** 仅指定两点初始纤维、冻结四状态固定推力、一次成功观测与一次15拍预承诺策略。没有一般SMF后验、重复信息状态终端闭合、MPC优化、递归可行、六状态安全、稳定性或20ms时延证明。Gate A仍blocked；论文去重91篇不变。本地隔离11项测试10通过、1项缺完整checkout配置跳过；完整CI及远端合并结果必须另行读取，不能提前宣称成功。

**下一轮唯一优先任务：** 对重复5/10/15成功/缺包模式的SMF信息状态建立非空递归闭合终端域，验证本轮一次性脉冲能否组合为可重复的共享因果策略。

---

**Run240完整checkout与main合并核验（2026-11-01）：** 研究PR #49 https://github.com/zhouxingxing1279/AcademicReaserch/pull/49 已非强制Squash合并，代码main SHA af072cccf1cee23a711c1d0d756d32623f38d3d0。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41301543344 和main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41301632613 均success；Python 3.13完整checkout Run224–240共**134/134聚焦测试通过、无跳过**，配置、精确证书、归档JSON与工件上传通过。尚未执行全仓库历史回归，Gate A仍blocked。

---

# 当前研究检查点 — Run240（2026-11-01）

**基准main：** e8e2516146b9390a8c5b7d9166a581ff45f7e922。Run240已对Run236两点初始纤维在零力矩下的5/10/15拍**全部连续可达成功位置观测**，用精确Fraction分支原始—对偶与有限断点包络计算后验速度区间。最坏后验半宽分别0.2464585125、0.3188500014、0.3681367927m/s；相对各自先验半宽的统一缩减分别0%、29.04%、43.56%。**5拍成功观测不保证任何速度区间半宽缩减**；10/15拍虽有半宽缩减，某些观测仍不降低绝对速度上界。继续共同零力矩15拍仅得到有限时域安全，不构成RCI或MPC。证据详见[Run240日志](run240_research_log.md)、验证器与JSON归档。Gate A仍blocked；全仓库CI与main合并结果需实际核验，不能提前宣称。已读去重91篇，Yang & Ozay 2021与Scott等2016为既有文献定向重读。下一轮唯一优先任务：构造全部后验观测分支上可执行的非零力矩共享恢复准入判据，寻找严格递归闭合的信息状态终端。

---

**Run238完整checkout与main合并核验（2026-11-01）：** PR #45 https://github.com/zhouxingxing1279/AcademicReaserch/pull/45 已经安全Squash合并，代码main SHA `973460fe93a05e7a00a6b1c24a4c2dbd580e3740`；PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41287562924 与main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41287634108 均success。Python 3.13.17完整checkout Run224–238共**111/111项聚焦测试通过、无跳过**，真实配置合同、精确Fraction、JSON归档及工件上传通过。**仍未实现SMF后验更新、递归输出反馈MPC或完整历史回归**。

# 当前研究检查点 — Run238（2026-11-01）

**基准main：** `be3596f98686c7bde600bcade8269ca66be8616f`。Run237对原全状态RCI F的指定两状态观测纤维证明共享一步控制不可能；Run238构造**同一两状态纤维的15拍共同零力矩有限安全备份**：固定T=9.81N、tau=0，精确Fraction归纳Z_n有n+1个生成元，所有逐拍独立|r|<=2.028989375，15拍内|p|<=0.09828542625m、|v|<=0.6522563875m/s、phi=omega=0，硬约束成立；第73拍正向极端残差下速度越界，故**非无限时域终端RCI**。仅针对两点，不覆盖全先验、不进行SMF更新、无MPC或递归可行性证明。Gate A仍blocked。测试：隔离Linux本地9项中8通过、1项真实配置因无完整checkout跳过；完整checkout CI结果需实际读取后补记。去重已读91篇，Bemporad & Garulli (2000)仅摘要核验，Qiu等(2020)重读公开章节。唯一下一轮任务：在Z15与噪声观测后构造可重复闭合的共享因果恢复/收缩策略。详见 [Run238研究日志](run238_research_log.md)。

---

**Run235完整仓库验证与合并补记（2026-11-01 UTC）：** 研究PR #39 https://github.com/zhouxingxing1279/AcademicReaserch/pull/39 已通过非强制Squash安全合并至main SHA 995b5c49991870e80920caeb659eea17f81a5329。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41275719918 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41275783414 均success；Python 3.13.17完整checkout Run224–235共86/86项聚焦测试通过、无跳过，配置、编译、精确支撑/尾项、JSON归档及工件上传通过。main源码、测试、归档Blob与本地实测字节一致。**仍无SMF共享控制、MPC递归可行、全仓库回归、六状态安全或20ms最坏时限保证。**

# 当前研究检查点 — Run235（2026-11-01）

**基准main：** db23aaa410a67fc929100146e12a51d8b3ebf820。冻结四状态Euler、固定T=9.81N、完整真实状态反馈K=(-.123,-.494,2.341,.933)下，Run234无限zonotope S的有限外包F现已构造：F=P_800⊕Q，Q=(1-rho)^(-1)∑_{j=0}^{799}A^j W，W=eps[-1,1]^4，eps=D||A^800 B||∞，rho=||A^800||∞<0.044224501。严格有理数证明A F⊕B[-D,D]⊆F；F有4000生成元，可用4×4000 LP判定成员资格。可靠状态绝对上界(4.36189355,2.55727183,0.37147212,0.77413543)，力矩<0.06690522Nm，均低于冻结硬约束。原非线性sin余项在F姿态范围内被D包络覆盖，故F对固定推力**全状态反馈**非线性系统RCI。

**证据边界：** F有限维不等于在线高效；未实现成员资格LP求解时间评估。tau=-Kx读取真实隐藏状态，不能直接用于间歇量测SMF或输出反馈MPC，不能宣称共享因果控制、递归可行、六状态安全、稳定性或20ms保证。**Gate A仍blocked。**

**测试：** 本地Python3.13最小等价配置镜像9/9测试通过，包含4000生成元支撑复核与n=400不可认证负例；完整checkout CI结果待实际验证，不能预先报成功。唯一论文日志继续91篇，Raković等2005仅复核书目/摘要与历史记录，不新增“已读”。

**唯一下一轮任务：** 严格分析间歇量测同一SMF后验纤维上是否存在共享控制将后继送入F；如不可行保留反例，改用联合估计误差RPI/输出反馈终端。

详见 [Run235研究日志](run235_research_log.md)。

---

# 当前研究检查点 — Run234（2026-10-31）

**Run234合并验证补记（2026-11-01 UTC）：** 研究PR #37 https://github.com/zhouxingxing1279/AcademicReaserch/pull/37 已安全Squash合并，代码main SHA `0f4f61431b4ea226de4fe29080ba0c6009e68701`；PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41272122206 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41272164237 均success。完整checkout Python 3.13.17执行Run224–234共77/77项聚焦测试通过、无跳过，真实配置、编译、Fraction精确证书、JSON逐字对照与工件上传成功。重新读取远端main、源码/测试/结果Blob验证落地。**未执行全仓库历史回归；全状态固定推力四状态RCI证明不等于SMF+MPC输出反馈闭合。**



**基准main：** `107d08ac91e71948d65f535b19c9fe06caf3cb5b`。本轮建立首个**非空、严格无限时域四状态RCI存在性证书**，仅针对固定推力9.81 N、冻结Euler横向模型、完整全状态反馈 `tau=-Kx`，`K=(-.123,-.494,2.341,.933)`，对所有逐拍独立有界横向残差成立。并非Run233的饱和LQR策略。

**证书：** `S=⊕_{j>=0} A_cl^j B[-D,D]`，`D=1742383/800000`；精确Fraction计算800步支撑与几何尾项，`||A_cl^800||∞<0.044224501`；可靠状态幅值上界(4.406855m,2.538442m/s,0.361233rad,0.742976rad/s)，力矩幅值<0.064424 Nm，均严格低于硬约束。用 `|phi-sin(phi)|<=|phi|^3/6` 证明真实非线性闭环每拍被线性扰动集合包含，故S严格不变。详见 [Run234研究日志](run234_research_log.md)及 `verification/check_four_state_rpi_zonotope.py`。

**证据级别：** 数学证明（固定模型和全状态反馈）；不是SMF后验共享控制、MPC递归可行、六状态安全或渐近点稳定性证明。S为隐式无限zonotope，尚无可在线使用的有限终端成员资格约束。**Gate A仍blocked，但四状态固定推力全状态终端RCI存在性子问题已证明可行。**

**本地测试：** Python标准库Fraction，8项中7通过1项因隔离镜像缺真实配置跳过；已修正一次测试预期分数约分问题并重测。完整checkout GitHub Actions须实际成功后才能归档，未执行全仓库历史回归或20ms在线时限认证。

**文献：** 复核Raković等(2005)，DOI https://doi.org/10.1109/TAC.2005.843854 既有mRPI记录；非新增全文阅读，唯一日志去重仍91篇。

**下一轮唯一优先任务：** 将隐式S转成可验证鲁棒后继闭合的有限终端集合表示，进一步研究间歇位置量测SMF后验集合上的同一因果控制律。

---

## 历史Run233检查点（保留）
# 当前研究检查点 — Run233（2026-10-31）


**Run233验证补记（2026-11-01 UTC）：** PR #35 https://github.com/zhouxingxing1279/AcademicReaserch/pull/35 已安全Squash合并，代码main SHA 52d4d02cce7d9f60fb11a25880cec714c12992f4；PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41268160006 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41268193922 均success。完整checkout Python 3.13.17，Run224–233聚焦测试69/69通过、无跳过；真实配置、编译、JSON归档核对及工件上传成功。已重新读取远端main及源码、测试Blob确认落地。**未执行全仓库历史回归，数值反馈种子仍非RCI/SMF+MPC安全证明。**


**基准main：** 8cee19a9a937f7037cf4ba1b28f2ede8ed82b98b。主方向：无人机MPC+SMF鲁棒输出反馈闭环；子课题允许证据驱动收敛。

**本轮实测增量：** 新增冻结四状态Euler的全状态饱和LQR反馈数值种子（固定T=9.81N，tau=clip(-Kx,±0.08)）。原点7种确定性/固定种子残差序列各1000拍未观察到违约；128组小初始扰动的1000拍随机残差实验0/128违约；相同持续正向极端残差下无反馈基线第74拍越界。**全部是有限轨迹数值证据，不是非空RCI、输出反馈MPC或安全证明。** 详见 [Run233研究日志](run233_research_log.md)。

**文献：** 新增Decardi-Nelson & Liu (2020) arXiv:2009.13581分节原文阅读§2.1、§3.1–3.4；统一论文日志去重90→91篇，未核实期刊DOI。

**测试：** 本地Python 3.13.5共8项测试7通过1项缺完整checkout跳过，源码编译及JSON输出成功；GitHub Actions完整仓库结果待实际运行后补记。尚未执行全仓库历史回归或20ms最坏耗时认证。

**Gate A=blocked：** 四状态非空终端RCI、SMF输出反馈Tube MPC递归可行性、稳定性和六状态安全均未证明。下一轮唯一优先任务：从数值反馈轨迹提取相关四维小单元，以严格区间外包认证闭合终端策略图，不能将数值无违约误作鲁棒安全。

