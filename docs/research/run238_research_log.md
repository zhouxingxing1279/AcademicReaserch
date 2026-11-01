# Run238 — 指定隐藏速度后验纤维的15拍共享控制安全管（2026-11-01）

**基准远端 main：** `be3596f98686c7bde600bcade8269ca66be8616f`。本轮唯一瓶颈：Run237严格排除指定两状态纤维在原4000生成元终端F上的任何共享一步力矩，但尚未给出更大安全集合中的正向可行见证。本轮不改写Run235全状态F的RCI结论，而是提供一个在**15拍位置观测最长间隔**内可执行的、精确有理数鲁棒安全备份，并明确说明它**不是递归不变终端**。

## 1. 冻结模型、信息及控制量词

冻结横向四状态 `x=(p,v,phi,omega)`，定义离散Euler：`p+=p+h*v`，`v+=v-h*T*sin(phi)+h*r`，`phi+=phi+h*omega`，`omega+=omega+(h/J)*tau`。`h=1/50 s`、`J=1/50 kg m²`、`T=981/100 N`、`|r_k|<=R=3246383/1600000 m/s²`，状态硬约束 `(|p|,|v|,|phi|,|omega|)<=(5,3,.45,2)`，`|tau|<=.08`。只考察Run236/237中已证实位于F及初始先验、在本拍观测不可区分的两个状态 `x±=(0,±hD,0,0)`，其中 `D=1742383/800000`。

对这两个隐藏状态，**所有时刻选择同一控制** `T=9.81 N, tau=0 Nm`，不读取真实速度、未来测量或扰动。由于初始 `phi=omega=0`，在该备份策略下严格保持 `phi=omega=0`，所以 `sin(phi)=0` **精确成立**（不是对一般状态做小角度近似）。位置/速度递推是精确线性的，允许扰动对手在每个控制后独立选择任意 `r_k∈[-R,R]`。

## 2. 可计算集合、证明与边界

令 `A0(p,v,phi,omega)=(p+h*v,v,phi+h*omega,omega)`，`B=(0,h,0,0)`。用zonotope表示两个初态的凸包（保守但可靠），定义

`Z_n = [g_init(n)] [-1,1] ⊕ sum_{j=0}^{n-1} [g_j(n)] [-1,1]`，其中

- `g_init(n)=(n*h²*D,h*D,0,0)`；
- `g_j(n)=(h²*R*(n-1-j),h*R,0,0)`，`j=0,...,n-1`。

初始两点均属于 `Z_0`。对每个 `n>=0`，逐项精确代数验证 `A0 Z_n ⊕ B[-R,R] = Z_{n+1}`，因此对任何隐藏初态与任意逐拍扰动，真实状态都包含于相应 `Z_n`。该等式是**有限时间的精确凸包传播**，不包含测量更新，也不构成 `Z_n` 对所有n不变。

所有 `n=0,...,15` 的状态/输入硬约束严格通过。第1拍 `|p_1|<=1742383/2000000000 = 0.0008711915 m`、`|v_1|<=6731149/80000000 = 0.0841393625 m/s`。第15拍 `|p_15|<=78628341/800000000 = 0.09828542625 m`、`|v_15|<=52180511/80000000 = 0.6522563875 m/s`，姿态与角速度恒零，力矩恒零。 `Z_15`有16个生成元，保留了位置—速度的扰动相关性，不能将它称为已证实的终端RCI。

负面边界：在初态 `+hD`、对手每拍 `r=+R`、始终零力矩时，第73拍 `v_73=3.0058840625>3m/s`，故此备份**不能无限持续**。15拍是配置中5 tick位置周期、最多连续丢2个包的最大成功间隔；即使15拍后收到位置数据，也**尚未证明**可从 `Z_15` 通过一个共同控制恢复到安全递归终端集合。不能把“15拍安全”重复应用到任意新后验。

## 3. 文献复核（不虚增已读篇数）

核对Bemporad & Garulli (2000), *Output-feedback predictive control of constrained linear systems via set-membership state estimation*, *International Journal of Control* 73(8):655–665, DOI https://doi.org/10.1080/002071700403420 ，出版社摘要与作者书目 https://old.control.ee.ethz.ch/publications/2000/407.html 。摘要强调在可用信息一致的所有状态与全部允许扰动上施加约束；本轮未取得全文，**只标记书目及摘要核验，不记作新增已读**。重新查阅Qiu et al. (2020) https://doi.org/10.1049/iet-cta.2019.0881 出版社开放正文§3.1–3.2与§4关于SMF预测/更新、终端约束和初始可行性的论述；其椭球/LMI定理不能直接应用到本模型。统一阅读记录去重仍91篇。

## 4. 复现、测试、证据等级

- 源码：`verification/check_four_state_fiber_recovery.py`；测试：`verification/test_four_state_fiber_recovery.py`（9项）；归档：`results/four_state_fiber_recovery_20261101/checks.json`；CI：`.github/workflows/run238-fiber-recovery.yml`。
- Linux本地Python标准库Fraction：`PYTHONPATH=verification python -m unittest -v verification.test_four_state_fiber_recovery`；`python -m py_compile verification/check_four_state_fiber_recovery.py verification/test_four_state_fiber_recovery.py`；`python verification/check_four_state_fiber_recovery.py --output /tmp/run238_certificate.json`。在无完整checkout的隔离目录运行：**8项通过，1项真实配置核验跳过，编译和JSON生成通过**；实际配置合同由GitHub Actions完整checkout检查，CI未完成前不得声称111项通过。
- **证明等级：** 对冻结Euler模型、指定两个初态、固定推力/零力矩和任意有界残差，15拍状态安全与信息因果性为精确有理数归纳证明。不是整个先验的输出反馈安全保证，也不是SMF后验更新、MPC优化、递归可行性、ISS/稳定性、六状态控制或20ms最坏时延。
- **课题评估：** 有限时间共享控制可行性得到正向见证；长期可行性仍被Gate A阻塞。该初等备份无独立创新性，技术难点是从`Z_15`设计模式依赖的估计误差/信息状态递归恢复；不应将本轮结果包装成完整硕士创新。

**下一轮唯一优先任务：** 在15拍观测间隔末端，针对包含位置—速度相关性的 `Z_15` 和有噪位置/姿态观测，构造并验证一个不读取隐藏速度的恢复/收缩策略及可重复闭合的信息状态终端候选；若无法闭合，给出可验证反例并收缩课题安全主张。


## 5. 完整checkout、PR与main的实际验证（2026-11-01）

研究PR #45 https://github.com/zhouxingxing1279/AcademicReaserch/pull/45 已在main未并发变化、compare ahead=1/behind=0、mergeable=true及expected head SHA `4c92e4f16bbc4ff825ebeac03d81aaf8a6205501` 校验后通过**非强制Squash合并**。合并代码main SHA `973460fe93a05e7a00a6b1c24a4c2dbd580e3740`，已重新读取远端main及源码/JSON Blob核验落地。

PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41287562924 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41287634108 均为completed/success。GitHub Actions Python 3.13.17完整checkout执行Run224–238共**111/111项聚焦测试通过、无跳过**，真实配置合同、精确Fraction归纳、归档JSON逐字比对和工件上传成功。PR日志报告Ran 111 tests in 28.600s / OK，main日志报告Ran 111 tests in 19.271s / OK。**不是全仓库历史回归**，没有SMF-MPC递归可行性或20ms最坏时延认证。后续此文档补记不单独触发CI。
