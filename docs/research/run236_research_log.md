# Run236 — 四状态终端RPI的观测纤维共享力矩障碍（2026-11-01）

**基准main：** 9442a873d89c270204fa32b4562334e1d0a07d1b。**唯一瓶颈：** Run235有限4000生成元集合F已经严格RPI，但终端反馈 \(\tau=-Kx\) 使用未观测的横向速度；须先检验它能否在相同SMF观测纤维上实现，不能将状态反馈不变性冒充输出反馈安全。

## 1. 冻结模型、信息及严格证据

继承Run235的固定推力 \(T=9.81\,N\)、Euler四状态 \(x=(p,v,\phi,\omega)\)、\(h=0.02\,s\)、\(J=0.02\,kg\,m^2\)、\(B=(0,h,0,0)^T\)、\(D=1742383/800000\,m/s^2\)、\(K=(-0.123,-0.494,2.341,0.933)\)、力矩限幅 \(|\tau|\le0.08\,Nm\)。有限RPI为 \(F=P_{800}\oplus Q\)，其中 \(P_{800}\) 的第一个生成元是 \(DB\)。

令 \(x_\pm=\pm DB=(0,\pm1742383/40000000,0,0)\)。两个状态均在F内（第一个生成元系数取±1，其余取0），且满足配置初始先验 \(|v|\le0.1\)、\(p=\phi=\omega=0\)。根据 configs/planar_baseline.json，每拍可观测 \(\phi,\omega\)，位置在有包时可观测，**速度从未直接观测**。在初始成功位置包 \(y_p=y_\phi=y_\omega=0\) 和零合法噪声下，两状态产生完全相同的控制器可见信息；因此它们可以同时属于同一后验SMF纤维。即使在成功位置包时，也不能通过本拍观测区分两者。

Run235状态反馈给出的合法力矩为
\[
\tau_\pm=-Kx_\pm=\pm\frac{430368601}{20000000000}\ {\rm Nm}
=\pm0.02151843005\ {\rm Nm}.
\]
对**任意**共享观测力矩 \(\tau(y)\)，由三角不等式严格得到
\[
\max\{|\tau(y)-\tau_+|,|\tau(y)-\tau_-|\}
\ge \frac{|\tau_+-\tau_-|}{2}
=0.02151843005\ {\rm Nm}.
\]
由于 \(h/J=1\)，在相同当前 \(\omega\) 下，至少一个真实状态的下一拍角速度相对其原全状态反馈后继产生不小于 \(0.02151843005\,rad/s\) 的误差。**这是对Run235特定反馈律的实现障碍，不是“所有共享控制无法保持F不变”的反例。** 两个全状态反馈力矩本身均未超出执行器限制。

还通过100项精确有理数支持函数和得到
\[
\sup_{x\in F}|Kx|\ge D\sum_{j=0}^{99}|KA^jB|>\frac3{50}=0.06\ {\rm Nm}.
\]
因此任何用统一加性误差预算 \(\epsilon\ge0.02151843005\) 且直接施加全局三角不等式 \(\sup_F|Kx|+\epsilon\le0.08\) 的**朴素收紧充分条件**必然失败，因为 \(0.06+0.02151843005>0.08\)。这只排除了该保守的充分认证路径，**不意味着物理力矩约束一定被违反**，也不意味着不存在更好控制器、联合误差管或SMF条件化收紧。

## 2. 文献与证据边界

- Mayne、Raković、Findeisen、Allgöwer (2006), *Robust output feedback model predictive control of constrained linear systems*, *Automatica* 42(7):1217–1222, DOI https://doi.org/10.1016/j.automatica.2006.03.005 。本轮重新核对DBLP书目/公开摘要及Run221已读笔记；未重新获取全文。文中估计误差RPI、tube收紧、终端条件提供必要的方法背景，不能直接证明本冻结非线性失测模型。
- Lucia、Ernesto、Castelan (2023), *Set-theoretic output feedback control: A bilinear programming approach*, *Automatica* **153:111004**, DOI https://doi.org/10.1016/j.automatica.2023.111004 。DBLP与交叉书目核实；纠正统一阅读日志旧记的151:110861及错误DOI。Run141已有分节阅读，本轮仅书目复核，不重复计入已读。
- docs/literature/PAPER_READING_LOG.md去重已读仍**91篇**；上述严格纤维结论来自本项目的有理数代数，不冒称文献定理。

## 3. 实现、测试、失败信息

新增验证器 verification/check_four_state_shared_torque.py（Fraction同观测双状态、两个力矩、最小共享误差及100项支持下界）；8项测试 verification/test_four_state_shared_torque.py；归档 results/four_state_shared_torque_20261101/checks.json；完整checkout工作流 .github/workflows/run236-shared-torque.yml。

本地Linux Python 3.13隔离目录使用Run235公开常数和动力学的等价最小模块镜像执行：

    PYTHONPATH=/mnt/data/run236/verification python -m unittest discover -s /mnt/data/run236/verification -p 'test_four_state_shared_torque.py' -v
    PYTHONPATH=/mnt/data/run236/verification python /mnt/data/run236/verification/check_four_state_shared_torque.py --output /mnt/data/run236/results/four_state_shared_torque_20261101/checks.json

结果：**8项中7通过，1项真实配置检查因本地缺完整checkout跳过**；源码编译及JSON生成通过。首次执行缺少Run235模块，触发 ModuleNotFoundError: check_four_state_finite_rpi；添加与远端公开源码参数/矩阵一致的本地最小镜像后重测通过。**该本地镜像不等于完整仓库测试**，GitHub Actions完成前不得宣称真实配置及全部聚焦回归通过。

## 4. 闭环与课题判断

四状态固定推力、**全状态**反馈F仍有Run235严格无限时域RPI证明，本轮没有推翻它。四状态**输出反馈**终端律尚未实现；缺测位置下的SMF共享力矩、联合估计/跟踪误差RPI、MPC递归可行性、稳定性、六状态安全和20ms最坏时延均未建立。

**Gate A=blocked。** 可行性：F可作为全状态数学基线；创新性：信息权限反例本身不是硕士论文创新，可能的创新必须来自可实现的模式条件化SMF+MPC及同等安全/预算下的保守性改善；难度：高，但比盲目搜索终端核更聚焦。

**下一轮唯一优先任务：** 在Run235 F上建立共享控制的**真正后继包含**测试 \(\exists\tau(y)\,\forall x\in S(y)\,\forall d:\ f(x,\tau,d)\in F\)，先针对本轮双状态纤维做精确或可认证外包的单步可行性判定；若可行，再推广到15模式SMF误差管及终端移位，避免将“反馈律不同”误写成“无共享控制”。

## 5. 合并状态

PR #41 https://github.com/zhouxingxing1279/AcademicReaserch/pull/41 已安全Squash合并。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41279295891 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41279361402 均为 completed/success。GitHub Actions Python 3.13.17完整checkout执行Run224–236共 **94/94项聚焦测试通过、无跳过**，真实配置、源码编译、精确分数证书、JSON逐字比对及工件上传均成功；main CI日志报告Ran 94 tests in 23.894s / OK。合并落地main SHA **7afc3a60e663fd7640fc7e6eb60bb7d8c4643744**，已重新读取远端main及新增源码/测试/JSON的Git Blob，与本地验证文件一致。研究代码合并后的CI已成功；本次仅文档证据补记未单独触发CI。仍未执行全仓库历史回归、在线LP 20ms最坏时间、输出反馈终端递归可行或六状态安全证明。
