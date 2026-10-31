# Run225 — 四状态二步鲁棒前驱的严格包含与排除（2026-10-31）

**基准 main：** b4b8d6beeaabf0e25d53fef4dad9289a2e822716。**唯一问题：** Run224 只证明 Pre(X) 非空；本轮检验 Pre(Pre(X))，不预设终端不变核非空。

## 冻结模型、信息权限和量词

沿用 Run224 的冻结四状态 Euler 模型，状态 (p,v,phi,omega)，步长 h=1/50，T∈[981/200,2943/200]，tau∈[-2/25,2/25]，|p|≤5、|v|≤3、|phi|≤9/20、|omega|≤2；每拍横向残差 |r|≤R(T)=47/25+(243/16000)T。角度过程扰动为零。正确二步量词是 exists u0 forall r0 exists u1(x1) forall r1；要求每个中间状态都在 X 中。此处控制器拥有完整真实状态；并非 SMF 输出反馈结论。

## 严格正见证：二步前驱非空

初始 x=(0,±3,±3/20,0)，固定两拍 T=2943/200、tau=0。利用 Run224 的有理数交错 Taylor 上下界 s7≤sin≤s5，将所有残差引起的位置/速度二步区间外包；姿态保持 ±3/20，角速度保持 0。二步全部状态区间严格位于 X 内，因此这两个初态属于 Pre²(X)。固定开环策略本身满足更强的 forall r0 forall r1 量词。

## 严格负见证：Pre(X) 与 Pre²(X) 确实不同

初始 x=(0,3,3/20,-2) 以及符号对称 x=(0,-3,-3/20,2)；第一拍 T=2943/200、tau=±2/25 能保证对所有残差下一状态仍在 X，故两点都属于 Pre(X)。

但正向状态的第一拍后角度必为 phi1=3/20-(1/50)·2=11/100，独立于任何 tau0。扰动对手选择每拍 r_i=+R(T_i)。由于 s7(3/20)>RT、s7(11/100)>RT，任意合法 T0、T1 的最小两拍速度增量发生于 TMAX。由 s5 上界严格推出：

v2-3 ≥ h[2R0+2TMAX·RT-TMAX(s5(3/20)+s5(11/100))]
= 15703932131047/2000000000000000 > 0。

所以任意因果控制都不能保证两拍速度硬约束；负向状态由奇对称得到同样严格排除。这不是求解器超时或统计反例，而是基于指定残差合同的解析排除证书。

## 复现、文献与边界

本地 Python 3.13 标准库 Fraction；命令：PYTHONPATH=verification python -m unittest -v verification.test_four_state_two_step_predecessor；python -m py_compile verification/check_four_state_two_step_predecessor.py verification/test_four_state_two_step_predecessor.py；python verification/check_four_state_two_step_predecessor.py --output results/two_step_predecessor_20261031/checks.json。本地镜像（Run224 关键函数逐式复制）6项中5通过、1项完整 checkout 配置核对跳过。GitHub Actions 工作流负责完整 checkout、旧新测试及结果逐字比较；CI 未成功前不得宣称通过。

文献：Kolmanovsky & Gilbert (1998), *Theory and computation of disturbance invariant sets for discrete-time linear systems*, Mathematical Problems in Engineering 4(4):317–367, DOI https://doi.org/10.1155/S1024123X98000866；本轮复核出版商摘要和书目，未阅读全文、不新增已读计数。原文讨论 LTI 最大扰动不变集及算法，不能将其定理直接用于本非线性推力调度模型。本轮证书独立推导。

**课题评价：** 可行性：Pre²(X) 有非空见证，但不能推出无限时域 RCI；创新性：二步前驱是成熟集合控制理论，暂属基线/阻塞定位；难度：高，必须处理角速度导致的预测安全损失、部分观测、失测和在线复杂度。**Gate A=blocked**。无四状态 Tube MPC、终端不变集、递归可行性、Lyapunov 稳定性、六状态安全或20ms最坏执行时间保证。

**下一轮唯一优先任务：** 在同一冻结模型上计算第三轮鲁棒前驱的严格局部包含/排除，优先检查本轮二步正见证能否继续，以及角速度约束引起的前驱边界收缩；只有形成非空不变终端集合后才接入输出反馈 MPC。


## 合并后核验（2026-10-31）

PR #18 https://github.com/zhouxingxing1279/AcademicReaserch/pull/18 通过非强制 Squash 合并，落地 main SHA 6c1a574c6c742c1335bd5b3592eea486b2d2171b。PR 聚焦 CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41232818700 和合并后 main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41232866432 均为 success；均核验旧新两组测试、真实配置、语法编译与归档 JSON 逐字一致。已再次读取 main SHA 与源码/测试/结果 Blob 确认落地。CI 为聚焦测试，不代表全仓库回归、完整四状态闭环或实时安全证明。
