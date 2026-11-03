**Run269 PR/main落地独立复核（2026-11-02 UTC）：** PR #129 https://github.com/zhouxingxing1279/AcademicReaserch/pull/129 基于main `7d0006ab2521d94150131100e8e8e339c97b10d6`，compare ahead=7/behind=0、仅7个预期文件、mergeable=true。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41478868445 completed/success，Python3.13完整checkout Run26x聚焦**83/83通过**，源码编译、冻结真实配置核验及Fraction JSON归档逐字比较成功。以expected head `31cc2155a4e831c12411b975bfa61b5610bf0442` 非强制squash合并main `b2905c03022b1f46705e56a48d7aa425aeb8ec3d`；重新读取main SHA、PR merged、证书Blob `950723a20551b8749870c2f5b99be20afe5a8215` 及日志Blob确认落地。合并后main push CI尚未独立确认，全仓库历史回归未执行；**Gate A=blocked**。

---

# Run269 — 两次连续位置丢包造成的不可消除速度后验直径（2026-11-02）

## 1. 基准与唯一问题

起始远端 `main` SHA：`7d0006ab2521d94150131100e8e8e339c97b10d6`。已读取 `docs/research/CURRENT_CHECKPOINT.md`、`docs/literature/PAPER_READING_LOG.md`、`docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md`、Run260/261/267/268日志、Run268源码/精确证书、`configs/planar_baseline.json`和背景第21轮Jacquet逐桨执行器证据。Run268的11种读数条件化条带为可靠**外包**，并非真实后验或终端RCI；Run267必要守卫通过不等于反馈终端安全。背景任务提出的逐桨共同输入域尚无平台辨识值。本轮只推进一个瓶颈：**合法位置丢包间隙内，即使使用最优SMF/CZ，真实后验速度是否存在不可消除的最小宽度？**

## 2. 严格两轨迹不可区分性结论（研究者独立推导，非论文定理）

仅针对冻结Run260四状态**定义离散Euler真值**：
`p+=h*v, v+=h*(-T*sin(phi)+r), phi+=h*omega, omega+=h*tau/J`，`h=J=1/50, T=981/100, |r|<=R=3246383/1600000, |tau|<=2/25`。位置仅在每5拍有一次机会，最多连续2个**位置包**miss；姿态角/角速度每拍观测且测量噪声有界。选择Run261已构造的第45拍真实零状态见证，位置第45拍成功、50/55拍丢失、60拍成功；第46–59拍**没有任何位置读数**，但有姿态/角速度读数。

固定任意基于已见观测的因果合法力矩策略。构造两条过程扰动历史：第45–58拍分别每拍 `r=+R` 与 `r=-R`，两条历史采用同一角传感器噪声（例如零）。由于横向扰动不进入角动力学，且此间没有位置读数，两条历史具有**完全相同的控制器可见信息**，故策略必给相同力矩；于是 `phi,omega` 在两条轨迹上相同，任意非线性 `-T sin(phi)` 项相消。逐拍相减可得，对 `1<=q<=14`：

`Delta v_q=2*q*h*R`，`Delta p_q=q*(q-1)*h*h*R`。

在第59拍 `q=14`，任意包含这两条轨迹的同一观测纤维可靠后验**速度投影直径至少**
`22724681/20000000=1.13623405 m/s`；位置投影直径至少
`295420853/2000000000=0.1477104265 m`。这是在该特定非空历史、这对极端合法扰动下的**必要信息宽度下界**，并非全部后验宽度的精确值或每条历史的统一下界。

**独立真实状态见证：** 取共同合法 `tau=0`、初态零，`q=14` 两条末状态分别为
`(p,v,phi,omega)=(±295420853/4000000000, ±22724681/40000000,0,0)`。每拍 `|p|<=5,|v|<=3,|phi|<=0.45,|omega|<=2` 均满足，所有可见姿态/角速度读数均可取零，因此不是不安全轨迹或外包虚假角点造成的伪反例。对任意其他合法因果力矩，差分公式仍成立；若该策略声称对两条合法扰动均鲁棒安全，其后验必须包含二者。

**关键时间边界：** `q=14` 指第59拍、下一次强制成功位置包**之前**。第60拍位置成功后，两条历史可由不同位置读数区分，**不得**把1.13623405m/s当作第60拍成功更新后仍成立的下界。这里的“最多两次丢包”是**每5拍一次机会的包丢失**，绝非只缺少两拍量测。结果只适用于四状态冻结模型与上述特定观测历史，不是六状态高度/执行器模型证书。

## 3. 对终端信息状态与硕士课题的影响

Run268的第60拍仿射条带不能自动消除第59拍的真实信息直径。任何以`|v-\hat v|<0.568117025`（严格小于半直径）定义第59拍信息终端的方案，若要求包含该历史的所有可能真值，必然失败；这只是**必要条件**，不证明宽信息集合不能安全，也不证明第60拍后验或15拍反馈终端RCI不存在。应在信息终端族中显式保留距离上次位置成功的age/位置包自动机状态；控制设计必须接受失测期间的不可消除误差，而不能假设每拍位置校正。将来若改变物理模型、引入速度直接传感器或扰动相关的角输出，需重新证明不可区分性。

可行性：Fraction精确计算与证书成本极低；创新性：不可区分性本身是基础观测信息事实，**不主张新理论创新**；研究难度：若希望对所有未来观测纤维证明终端RCI，仍属高难度。当前主方向六状态平面四旋翼条件性首选、四状态数学基线不变；**Gate A=blocked**。

## 4. 真实论文重读与保证边界

Johannes Köhler, Matthias A. Müller, Frank Allgöwer (2021), *Robust output feedback model predictive control using online estimation bounds*, arXiv:2105.03427，作者全文 https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf ，arXiv https://arxiv.org/abs/2105.03427 。**2026-11-02重新分节核验作者全文** §II Assumption 1/Definitions 1–4，§III-C Theorem 2，§IV-B Assumption 7/Theorem 4与§IV-C Assumption 9/Theorem 5，§V十状态四旋翼数值案例；附录和全文逐式未完全复核。论文在有界扰动、δ-IOSS/δ-ISS、可靠在线估计误差界、可行初始MPC与终端假设下证明鲁棒约束与递归可行。§V模型为10状态 `(z1,z2,z3,phi1,phi2,v1,v2,v3,omega1,omega2)`，输入3维虚拟姿态/推力；采样0.05s、输出5维位置/角度，每拍带噪，**无本项目每5拍位置机会/最多2包miss合同，也无逐桨动态与20ms WCET**。本轮为既有已读论文的范围补充，不增加唯一总账去重数。论文理论与本轮独立下界不能相互替代。

## 5. 工件、实际测试与负面结果

新增 `verification/check_run269_unobserved_gap.py`、`verification/test_run269_unobserved_gap.py`、`results/run269_unobserved_gap_20261102/checks.json`、`.github/workflows/run269-unobserved-gap.yml`。本地Linux Python3执行 `cd /mnt/data/run269 && python -m unittest -v test_run269_unobserved_gap.py`：**7/7通过**；`python -m py_compile check_run269_unobserved_gap.py test_run269_unobserved_gap.py`：通过；`python check_run269_unobserved_gap.py --output checks.json`：生成精确Fraction证书；正负两条零力矩真实轨迹每拍硬约束验证通过。GitHub Actions将以Python3.13完整checkout运行Run26x聚焦回归、真实配置交叉核验和归档JSON逐字比较；**CI成功与否必须以PR实际结果为准**。本地容器无法解析github.com，无法本地完整checkout或执行历史回归。代码及文档的GitHub PR合并状态以独立验证为准。

**未完成**：没有真实后验CZ、15拍共享因果终端回返、MPC控制器、完整闭环仿真、无限递归可行/稳定、六状态安全或20ms WCET；该必要信息宽度下界不解决Gate A。

## 6. 下一轮唯一优先任务

以第59拍此特定不可区分的双状态纤维为起点，在第60拍**强制位置成功**且存在±0.02m位置噪声时，构造真实读数分支的后验集合，检查是否存在一条读数条件化、同纤维共享、可执行的15拍安全回返策略；若不行，给出可复核阻碍，而不是继续仅收紧无条件盒。
