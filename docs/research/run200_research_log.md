# Run200：间歇测量 SMF—MPC 最小可运行闭环与可行性基线

日期：2026-10-30。接续 main=a5b7eeca04eb（Run199）。本轮不改变 Run199 冻结 SOCP 的数值不可行结论；Gate A 仍 blocked。研究目标从仅分析终端候选，补齐一个可逐步替换为无人机动力学的端到端闭环最小基线。

## 文献与重复性边界

- Köhler、Müller、Allgöwer，*Robust output feedback model predictive control using online estimation bounds*（2021，arXiv:2105.03427），Section IV-B、Algorithm 1、Assumption 7、Theorem 4：在线有效估计误差界、终端条件与旧计划移位共同保证递归可行性；其数值例已涉及10状态四旋翼。本项目不能把“SMF + MPC + 四旋翼”称为新方法。https://arxiv.org/pdf/2105.03427
- Scott、Raimondo、Marseglia、Braatz，*Constrained zonotopes*（2016，Automatica 69:126–136，DOI:10.1016/j.automatica.2016.02.036），Definition 3、Proposition 1，式(11)–(13)：测量一致集合的 generalized intersection 已有精确 CZ 运算；本轮仅用一维区间精确交集作为可审计基线。https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf
- Mulagaleti、Mejari、Bemporad，*Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate*（2025，IEEE TAC 70(2):1259–1266，DOI:10.1109/TAC.2024.3454528），Definition (4)–(6)：当前 scheduling 参数可见，后继参数未知且必须对所有允许值成立。本轮标量基线不含推力调度；其证明不得外推到原仓库四状态 LPV/六状态无人机。https://arxiv.org/pdf/2309.02384

## 可复现标量合同（刻意不是无人机模型）

x[k+1] = (1/2)x[k] + u[k] + w[k]，|w| ≤ 1/20；收到包时 y[k]=x[k]+v[k]、|v|≤1/10，缺包时不更新。硬约束 |x|≤2、|u|≤3/5。初始可信集合 [-1,1]，终端集合 S=[-1/2,1/2]。预测时区间按真实控制与扰动精确传播，收到测量时与 [y-1/10,y+1/10] 求交；测量不一致即拒绝，不允许默默修复。

有限时域 N=3，每步动作从 {-1/2,-1/4,0,1/4,1/2} 中选，枚举全部 5^3=125 个计划，以预测中心的二次和加输入正则为目标，只在逐步区间硬约束和终端约束均满足时接受。因此是精确有限动作优化，不是连续 QP 求解器。控制选择只依赖当前后验，下一次扰动/测量是否到达在控制后才揭示。

## 有限动作 MPC 的递归可行性证明（仅此标量合同）

1. u=0 下终端不变性：(1/2)(1/2)+1/20=3/10 ≤ 1/2。零计划从初始 [-1,1] 出发，第三步区间包含于 S，故初始可行。
2. 假设时刻 k 的计划 (u0,u1,u2) 对所有 w∈[-1/20,1/20] 逐步满足状态/输入约束且终端落在 S。实际施加 u0 后，预测区间为 R1，真实状态在 R1 内；无论收到何种一致测量或缺包，后验 B[k+1]⊆R1。
3. 在 k+1 取旧计划尾 (u1,u2) 并附加 0。线性区间映射对包含关系单调，故前两步预测包含于旧计划 R2,R3；附加零动作后的新终端包含于 (1/2)S⊕[-1/20,1/20]⊆S。输入仍在动作网格中，故该移位候选可行。
4. 枚举优化只选择已通过精确区间可行性检查的计划，所以存在的可行尾计划永不因优化而消失。归纳得到：对任意有界扰动、任意一致噪声及任意缺包序列，在该标量模型与初始集合下可递归保持硬约束。证明不依赖384步有限仿真；代码使用 Python fractions.Fraction 复核合同中的有理数运算。

## 实际运行

运行命令：
- PYTHONPATH=verification python -m unittest verification.test_intermit_smf_mpc_closed_loop -v
- python verification/check_intermit_smf_mpc_closed_loop.py --output results/intermit_smf_mpc_scalar_20261030/checks.json

本轮验证环境：Python 3.13.5 标准库，无 NumPy/SciPy 依赖。5/5 新测试通过。16条确定性闭环轨迹×24步=384步；164次收到测量、220次缺测；9次相对可行尾计划更换优化方案；状态/输入违约0。另对初始区间端点、扰动端点及成功/缺测观测分支逐一测试旧计划移位可行。完整结果在 results/intermit_smf_mpc_scalar_20261030/checks.json。

## 不得外推的结论与下轮唯一问题

本轮完成的是标量安全闭环基线，不是原四状态横向—姿态 Gate A 的 RCI，也不是六状态四旋翼的闭环安全证明；标量 a=1/2 自身稳定，即使无限缺测也能保持不变，因而避开了无人机位置积分器、推力调度、状态相关气动残差、姿态耦合、因果分叉和控制权限等核心难点。有限枚举计算量也不是实机实时保证。

下一轮唯一优先任务：把“当前后验⊆旧一步可达集 → 旧计划移位 → 终端后继不变”三个接口映射到仓库的四状态横向—姿态 scheduling-conditioned 合同，逐项检查何处失效；不得直接把标量证明移植到无人机。若无法找到共同后继控制/终端集，必须保留 Gate A blocked，并明确最小反例或缺失条件。
