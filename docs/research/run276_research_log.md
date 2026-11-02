**Run276 PR #149 CI与安全合并独立复核（2026-11-02 UTC）：** 研究PR https://github.com/zhouxingxing1279/AcademicReaserch/pull/149 基于main `fb8a8675e5dea7175d0e7e0be134201be72f3824`，合并前compare ahead=7/behind=0，仅7个预期文件且无删除；mergeable=true，expected head `3ce055763ca21a57ce0418c63f34efa1c8bc9fbe`。GitHub Actions https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41534362938 **completed/success**，Python3.13.17完整checkout、源码编译、Run276聚焦**6/6通过**、冻结配置检查和Fraction归档JSON逐字比较成功，已独立读取job日志。使用expected-head非强制squash合并至main `fb349a5e7c2f60dc3ada5c91d6b96eb682e40e88`；重新读取main SHA、PR merged及脚本/证书/日志/检查点/唯一论文总账Blob确认落地。**合并后main push CI及全仓库历史回归未独立确认**。真实SMM后验见证仅否定第三块速度门槛自动普遍通过，不证明硬约束违约、MPC不可行或无限时域不安全；**Gate A=blocked**。

---

# Run276 — Run260真实SMM观测历史下第90拍速度门槛的严格反例（2026-11-02）

## 基准与唯一问题
基于远端main fb8a8675e5dea7175d0e7e0be134201be72f3824；读取CURRENT_CHECKPOINT、PAPER_READING_LOG、Run260/271/274/275日志、Run260精确证书、Run271/275源码与冻结configs/planar_baseline.json。背景第27轮PR #148已进入main，不修改背景任务文件。本轮唯一问题：Run275的G=187678479/80000000=2.3459809875m/s第三15拍充分准入门槛，是否对Run260固定真实SMM前缀之后所有非空读数后验自动成立？

## 冻结模型及构造
四状态Euler真值 x=(p,v,phi,omega)，h=J=1/50，T=981/100，R=3246383/1600000；p+=h*v，v+=h*(-T*sin(phi)+r)，phi+=h*omega，omega+=h*tau/J。约束 |p|<=5,|v|<=3,|phi|<=0.45,|omega|<=2, |tau|<=0.08, |r|<=R；每5拍位置机会，最多连续2次丢包，成功位置噪声±0.02，姿态/角速每拍有噪观测。

继承Run254在tick30可行零状态与Run255 tick30..34共同非零力矩脉冲 tau=(1/25,-1/25,-1/25,1/25,0)，姿态phi最大1/1250、tick35后phi=omega=0。tick30..34选合法扰动 r=(4/5)R+T*sin(phi)，其幅值<=4R/5+T/1250<R，横向真实净加速度精确为4R/5；tick35..89取r=R，因phi=0，净加速度精确为R。tick0..30零状态、零输入、零扰动；tick35成功位置读数0、噪声=-3246383/500000000=-0.006492766m，合法。其余成功位置读数取真实p、噪声0；每拍姿态/角速读数取真实值、噪声0（30..34的姿态/角速读数不是强行设零）。成功包拍号5,10,15,30,35,50,60,65,70,75,80,85,90；20,25,40,45,55丢包，完整字符串SSSMMSSMMSMSSSSSSS。35/40/45为SMM，50/55/60为SMS，均合法。tick35及之前成功位置读数均为0，符合Run260固定前缀；45与60真值也落在Run260 SMM可靠外包内。

## 严格有理数结论
- tick45: p=301913619/4000000000=0.07547840475m, v=22724681/40000000=0.568117025m/s；
- tick60: p=165565533/500000000=0.331131066m, v=94145107/80000000=1.1768138375m/s；
- tick90: p=5561054079/4000000000=1.39026351975m, v=191536597/80000000=2.3942074625m/s；
- 速度超过Run275第三块充分门槛 **1929059/40000000=0.048226475m/s**，但仍小于3m/s硬约束；
- 85与90均成功：|y90-y85|=22724681/100000000=0.22724681m，大于Run275针对(85,90)的D=363255181/2000000000=0.1816275905m。

对这条合法完整真实轨迹，所有0..90拍硬状态盒、所有施加输入、所有成功读数噪声和丢包自动机均合法。故任何可靠的SMF后验在对应非空观测纤维的tick90必须包含这个v90>G的真值，**Run275速度门槛不可能对所有Run260真实历史后验自动成立**。这是存在性反例；不能把门槛失败解释为硬约束已经违反，也不能推出不存在其他观测条件化反馈策略。Run275的D充分引理本身依然正确，否定的是“所有真实后验均满足D/G”的可能普遍断言。

## 论文核验与迁移边界
2026-11-02重读Qiu, Yang, Zhu, Mousavinejad (2020), *Output feedback model predictive control based on set-membership state estimation*, IET Control Theory & Applications 14(4):558–567, DOI https://doi.org/10.1049/iet-cta.2019.0881，出版社开放HTML §2 Assumptions1–2、§3.1 Theorem1、§3.2–3.4与Algorithm1、§4终端鲁棒正不变集条件及§5案例。该文离散LTV有界过程/测量噪声、椭球状态SMF、minimax MPC、LMI硬约束和附加终端RPI假设；§4局部终端控制还明确采用状态已知假设。它不是四旋翼、不是间歇位置量测，也没有本仓库共享因果控制与失测自动机。论文已在唯一总账登记，按DOI去重不新增篇数；未独立重算全部LMI或论文数值案例。可复用的是“状态真值包含、MPC预测约束、终端信息状态回返”必须分别论证，不能从有限安全轨迹推出无限递归安全。

## 工件与测试
- verification/check_run276_actual_posterior_gate.py：Fraction精确轨迹、观测、门槛及状态硬盒见证；三角函数仅通过全局|sin(phi)|<=|phi|认证扰动合法。
- verification/test_run276_actual_posterior_gate.py：6项独立断言，含脉冲、离散运动学求和、历史自动机、Run260外包成员、门槛失败、测量噪声。
- results/run276_actual_posterior_gate_20261102/checks.json：逐项精确分数归档。
- .github/workflows/run276-actual-posterior-gate.yml：PR完整checkout测试、源码编译、冻结配置、归档JSON字节比较。

本地Linux Python3执行：cd /mnt/data/run276 && python -m unittest -v test_run276_actual_posterior_gate.py，**6/6通过**；python -m py_compile check_run276_actual_posterior_gate.py test_run276_actual_posterior_gate.py通过；python check_run276_actual_posterior_gate.py --output checks.json生成归档。最初测试将tick35位移误写成4R*h²导致1/6失败，修正为8R*h²后6/6通过；保留负面记录。GitHub CI与main合并状态以实际复核为准，不预先声称成功。

## 课题评价与下一轮唯一任务
可行性：真实历史反例明确了零力矩终端门槛不能自动通过；创新性：这不是新MPC算法，是安全量词与观测纤维的必要校验；难度：全纤维反馈前驱、SMF/CZ关联传播、20ms预算和六状态执行器接口仍中高。没有新增MPC优化器、完整CZ后验、所有分支因果安全回返、终端信息RCI、无限递归可行/稳定或六状态物理安全；Gate A=blocked。

**唯一下一步**：针对本轮合法SMM第60拍观测纤维，构造包含全部一致真值的可靠SMF后验，并研究第60–90拍允许非零力矩的观测条件化安全前驱；先验证全部成员/全部丢包后继，不以单条见证轨迹替代终端信息集合证明。
