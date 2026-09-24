# 36 执行器权限与扰动合同审计：静态反馈失败不等于系统物理不可行

日期：2026-09-24。承接第 35 章。

## 1. 本轮核心问题

第 33 章已经严格否定一个具体 hover-DARE ancillary feedback；第 34–35 章进一步做了约束感知 static-K 搜索，并在 vertex-consistent residual 下仍没有找到同时通过 state+torque finite necessary checks 的样本。

但这些结果都只否定具体反馈或搜索到的 controller class，不能推出 plant-level actuator impossibility。如果继续写成“执行器权限不足，因此不存在可行 Tube MPC”，会把 controller-synthesis failure 错写成物理不可能。

本轮暂时移除静态 K，检查：在低推力 T=4.905、全部硬状态约束和 |tau|<=0.08 下，面对允许的恒定最坏水平 residual，是否连任意可行控制序列都无法到达扰动平衡状态？同时核查单一 global residual box 是否本身造成显著保守性。

## 2. 模型与两个合法扰动合同

沿用横向—姿态模型

\[
x=[p_x,v_x,\phi,\omega]^\top,
\]

\[
p_x^+=p_x+h v_x,\quad
v_x^+=v_x-hT\phi+h r_x,
\]

\[
\phi^+=\phi+h\omega,\quad
\omega^+=\omega+\frac hJ\tau,
\]

其中 h=0.02, J=0.02。硬约束是

\[
|p_x|\le5,\ |v_x|\le3,\ |\phi|\le0.45,\ |\omega|\le2,\ |\tau|\le0.08.
\]

继续把 -T phi 保留在已知 LPV 动力学内。水平 residual 使用已有解析合同

\[
|r_x(T)|\le1.880+\frac{T(0.45)^3}{6}.
\]

单一全域盒取

\[
\bar r_G
=
1.880+\frac{14.715(0.45)^3}{6}
=
2.1034840625.
\]

如果利用当前已知推力，低推力顶点可合法使用

\[
\bar r_L
=
1.880+\frac{4.905(0.45)^3}{6}
=
1.9544946875.
\]

这不是学习缩界或修改物理假设，只是没有把高推力时的 Taylor remainder 强行复制到低推力时刻。

## 3. 扰动平衡揭示 global box 的保守性

固定 T 和恒定 r_x=d>0 时，静止平衡满足

\[
v_x^\star=0,\quad
\omega^\star=0,\quad
\phi^\star=d/T,\quad
\tau^\star=0.
\]

低推力下，global box 要求

\[
\phi_G^\star=2.1034840625/4.905=0.4288448649.
\]

距离硬角度边界只剩 0.0211551351 rad。即使姿态推到 0.45，最大水平制动能力也只有

\[
4.905(0.45)-2.1034840625=0.1037659375\ {\rm m/s^2}.
\]

推力条件化 residual 则给出

\[
\phi_L^\star=1.9544946875/4.905=0.3984698649,
\]

角度余量增至 0.0515301351 rad，最大水平制动能力增至

\[
0.2527553125\ {\rm m/s^2}.
\]

因此这里的保守性直接消耗真实姿态和制动权限，不只是集合体积差异。

## 4. 去掉反馈结构后的 LP

给定 horizon N，优化变量为 x_0,...,x_N、tau_0,...,tau_{N-1} 和 peak variable t，最小化 t，满足：

1. x_0=0；
2. 每步满足上述线性动力学，且 r_x=d 为恒定最坏正 residual；
3. 全时域满足全部硬状态约束；
4. -t<=tau_k<=t；
5. 终端满足
   \[
   v_N=0,\quad \omega_N=0,\quad \phi_N=d/T_L,
   \]
   p_{x,N} 只需仍在硬约束内。

到达该状态后，tau=0 可永久保持，因此若 N 可行，则 N+1 也可行。代码据此二分搜索第一个数值满足 t_N^*<=0.08 的 horizon。

该 LP 使用比任意固定 K 更宽的控制策略类，因此适合区分“反馈结构失败”和“系统物理不可行”。

## 5. 实际代码结果

新增：

- verification/check_actuator_authority_and_scheduled_residual.py
- results/actuator_authority_scheduled_residual_20260924/checks.json

环境：Python 3.13.5、NumPy 2.3.5、SciPy 1.17.0，求解器为 scipy.optimize.linprog 的 HiGHS。

### 5.1 单一 global residual

第一个数值满足 |tau|<=0.08 的 horizon 为

\[
N=381=7.62\ {\rm s}.
\]

对应

\[
t_{381}^\star=0.07994631095.
\]

前一时域

\[
t_{380}^\star=0.08039911778>0.08.
\]

N=381 的最大绝对状态是

\[
(2.80994,\ 0.72049,\ 0.45,\ 1.32353),
\]

终端为

\[
(2.80994,\ 0,\ 0.4288449,\ 0).
\]

因此至少在数值优化层面，global residual contract 下也存在满足全部硬约束的控制序列。

### 5.2 推力条件化 residual

只把 residual 换成同一解析公式在当前 T_L 上的值。第一个数值满足 torque limit 的 horizon 降为

\[
N=160=3.20\ {\rm s},
\]

其中

\[
t_{160}^\star=0.07996782686,
\]

而

\[
t_{159}^\star=0.08104047747>0.08.
\]

N=160 的最大状态为

\[
(1.05907,\ 0.63733,\ 0.45,\ 1.32353),
\]

终端为

\[
(1.05907,\ 0,\ 0.3984699,\ 0).
\]

首个数值可行 horizon 从 381 tick 降到 160 tick，减少 221 tick，约 58.0%。

## 6. 结论等级

### 已严格推导

- residual 上界 \(\bar r(T)=1.880+T(0.45)^3/6\)；
- 低推力扰动平衡角度 d/T_L；
- global box 与 T-conditioned bound 的姿态余量和制动权限差异；
- 达到 terminal equilibrium 后可以零 torque 延长，因此 horizon feasibility 关于 N 单调。

### 仅数值证据

N=381 与 N=160 是 HiGHS 浮点 LP 的优化结果。本轮没有有理化对偶解或 Farkas certificate，所以不能把“380 必不可行、381 严格最短”写成精确数学定理。

### 被否定

第 33 章特定 K 的失败不能升级为“当前模型在 |tau|<=0.08 下不存在任何可行鲁棒控制”。本轮已经在更宽控制策略类中找到可行序列。

### 仍未完成

这不是 causal feedback synthesis、任意时变 disturbance 的 RCI、arbitrary thrust scheduling tube、output-feedback SMF、terminal append 或 recursive-feasibility proof。

## 7. 文献边界

Kothare、Balakrishnan、Morari 的 robust constrained MPC 已经用 LMI 在模型不确定性下联合处理 worst-case objective、输入/输出约束和 state-feedback synthesis，所以“把约束直接放进反馈设计”本身是经典问题。

Lorenzen、Cannon、Allgöwer 2019 将在线 set-membership model update 与 homothetic robust prediction tubes 结合，目标之一就是在保持约束保证时减少保守性；因此“不确定集合条件化后更小可以降低 MPC 保守性”也不是新概念。

Bujarbaruah、Nair、Borrelli 2020 进一步直接处理 state-dependent uncertainty，并使用 set-membership refinement 得到随状态变化的 uncertainty envelope。

因此本轮的价值不是声称 parameter-dependent disturbance set 新颖，而是建立一个当前仓库必须遵守的强基线：

> 后续如果要证明 CZ-SMF 或学习降低了保守性，必须先与语义一致、按已知 scheduling T 条件化后的 residual/tube 比较，不能只和单一全域 worst-case box 比较。

否则会把本可由已知物理变量消除的保守性错误归因于 SMF、CZ 或学习。

## 8. 下一轮唯一优先问题

只解决：

> 能否在 W(T) 而不是单一 W_G 下，构造一个对全部允许 thrust scheduling 和扰动序列都成立的 ancillary/RCI tube，并同时通过 |tau|<=0.08 与状态硬约束？

优先先检查固定 K + parameter-dependent disturbance tube。若仍失败，再考虑 gain-scheduled K(T)，但必须接已有 LPV tube 理论补递归可行性。

在这个强控制基线通过以前，不重新讨论 CZ 几何收益。
