**Run263 PR/main CI与安全合并复核（2026-11-02 UTC）：** 研究PR #111 https://github.com/zhouxingxing1279/AcademicReaserch/pull/111 以main 84937248548b4c4f1a1d48650ed03dc6559e84a0 为基准，合并前compare ahead=3/behind=0、仅7个预期文件、mergeable_state=clean、expected head b27c101e12a796c67e700931fa5847c83e61df3b。首轮PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41427063681 **失败**：35/35单元测试成功，但JSON精确逐字比较在第80行失败，原因是JavaScript JSON格式化将数字字符串键“5/10/15”排序，与Python sort_keys=True顺序不一致；保留此负面记录。修正归档键序后，PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41427264817 **completed/success**，完整Python3.13.17 checkout聚焦Run260–263 **35/35通过、无跳过**，源码编译、真实配置核验、精确JSON逐字比较、artifact上传均通过。expected-head非强制squash合并至main 3b5f9921a360fc7f30ddef46c6d4953eecda8777，重新读取main SHA、PR merged及源码/证书Blob确认落地。main push CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41427340573 **completed/success**，35/35、配置/JSON比较及工件上传再次通过。**全仓库历史回归未执行**。本轮仅证明第60拍全部非空有噪后验的速度投影宽度上界，不证明绝对状态安全终端RCI、无限递归可行、稳定或20ms WCET；Gate A=blocked。

---

# Run263 — 全有噪读数下第60拍速度宽度上界（2026-11-02 UTC）

## 1. 基准与唯一问题
基于远端 main 84937248548b4c4f1a1d48650ed03dc6559e84a0；核对 CURRENT_CHECKPOINT、Run259–262、真实配置与统一论文记录。Run260只证明第45–60拍 SMM/MMS 固定历史的共享零力矩有限安全，Run261否定无限重复，Run262给出三拍力矩响应时滞。**本轮唯一问题**：不假设未来位置读数为零、不枚举连续读数空间，能否给第60拍所有非空有噪后验一个与11条合法包模式一致的速度投影宽度上界？本轮不构造终端信息RCI。

## 2. 冻结合同、全读数宽度定理
四状态定义离散Euler：x=(p,v,phi,omega)，p+=h*v，v+=h*(-T*sin(phi)+r)，phi+=h*omega，omega+=h*tau/J。h=J=0.02，固定T=9.81，|r|<=3246383/1600000，位置噪声半宽eps_p=0.02m，姿态噪声半宽eps_phi=0.005rad；位置每5拍有一次机会，最多连续2次miss；姿态每拍成功测量，允许任意与真实轨迹一致的读数。实际力矩可取任意合法已知序列，宽度推导不需要未来力矩固定零，但**状态硬安全仍只继承Run260的固定零力矩桥**。

对任意两次成功位置包间隔 n=5,10,15，锚点与当前成功位置条带宽各不超过2eps_p。Euler精确运动学恒等式：
v_(k+n)=(p_(k+n)-p_k)/(n*h)+h*sum_{i=0}^{n-1}((i+1)/n)*a_(k+i)，a=-T*sin(phi)+r。
每拍有噪姿态条带宽<=2eps_phi，且 |sin(a)-sin(b)|<=|a-b|，故加速度可靠外包宽<=2(R+T*eps_phi)。从而任意非空成功后验速度投影宽
W_s(n)<=4eps_p/(n*h)+h*(n+1)*(R+T*eps_phi)。
精确Fraction结果：C5=41974589/40000000=1.049364725；C10=68573493/80000000=0.8571686625；C15=13974589/15000000≈0.9316392667 m/s。未成功位置更新的每拍宽度增加至多 Delta=2h(R+T*eps_phi)=3324863/40000000=0.083121575 m/s。旧锚点丢弃只降低紧度、不影响真值包含。

Run260第45拍历史：SMM上次成功位置在35，40/45连续miss，因此50必须成功；MMS上次成功在45，因此50/55/60不能全部miss。枚举50/55/60包，分别4和7条合法分支。每个分支至少在60之前或当拍发生一次距上一成功不超过15拍的成功位置更新，因此在成功时应用C(n)，后续失测以Delta传播。**对所有与冻结模型和有界噪声一致的非空连续读数（不只是零读数）**，严格得
- SMM起点：W_v(60)<=105771301/60000000≈1.7628550167 m/s（最不利未来SMM）；
- MMS起点：W_v(60)<=75223219/40000000=1.880580475 m/s（最不利未来SMM）；
- 两者共同W_v(60)<=1.880580475 m/s。

这也是完成后脉冲期首次有效位置锚点重置后、在每拍姿态成功且最多2次位置miss下**测量机会时刻的宽度不变上界**：成功时宽<=max C(n)=C5，最多10步失测传播再增加10Delta。注意首次从30到35/45的姿态未完全测量，不能把该一般界套用于那段历史；本轮第60拍证明仅依赖35或45之后的锚点。宽度不变不是位置/速度绝对值约束、全状态集合不变、终端RCI或递归可行性。

## 3. 文献阅读及创新性界限
Zhexian Li, Ketan Savla, *Output-feedback adaptive model predictive control for ramp metering: a set-membership approach*, arXiv:2308.05265 (2023初稿，2025修订)，https://arxiv.org/abs/2308.05265；作者网站将其列为2026年Automatica在线发表，DOI https://doi.org/10.1016/j.automatica.2026.113290（期刊终版未逐页核验）。2026-11-02实际阅读arXiv开放HTML全文§3.1/3.3、§4.1–4.4、§5.1–5.3及§6关键实验，核对Lemma 1、Propositions 1–3、Theorem 1和附录证明片段。其对象是道路Cell Transmission Model，状态为I个主线单元和I个匝道队列车辆数共2I维，输入I个匝道流量；输出为部分主线状态和完整匝道状态的**无噪直接量测**，非四旋翼、非位置丢包。混合单调嵌入同时更新状态/需求/参数上下界，MPC为MILP；Proposition 3的递归可行依赖嵌入终端正不变集合和初始可行。Theorem 1在恒定需求、无限匝道储存等条件下给有界队列而非四旋翼硬安全。论文报告较高计算耗时（如T=300时约209.6秒），不适合直接迁移20ms控制器。说明SMF+MPC与集合嵌入终端集合**已有先例**；本课题需要明确有噪位置失测自动机和真实T/tau控制权限的新增贡献。

## 4. 工件、测试、证据等级
新增 verification/check_run263_epoch_velocity_width.py、verification/test_run263_epoch_velocity_width.py、results/run263_epoch_velocity_width_20261102/checks.json 和 .github/workflows/run263-epoch-velocity-width.yml。隔离Python标准库9/9单元测试通过，py_compile通过，exact Fraction JSON生成成功；用等价冻结配置字段进行--root交叉核验与JSON逐字比较通过。完整GitHub checkout中真实配置核验、Run260–262回归及PR/main CI由workflow进一步验证；未经CI成功不得宣称已完成。代码对11条离散包模式逐项计算**上界**，连续测量值由数学Lipschitz证明覆盖，而不是逐一数值采样。无新增MPC求解器、真实SMF/CZ递推、反馈控制、无限递归可行或飞行实验。Gate A=blocked。

## 5. 下一轮唯一优先任务
以第60拍11条合法分支的全部非空后验为起点，结合本轮统一速度宽度上界、绝对p/v/phi/omega位置及Run262三拍力矩响应，检验一个有反馈的共享因果15拍安全前驱是否非空。**先验证绝对状态/控制权限充分条件，不得把宽度收缩冒充终端安全。**
