# Run226 — 四状态三步鲁棒前驱严格内外证书（2026-10-31）

**基准 main：** `5ddca85294ecfd5a1693410c9cc9b0e0e70ef2bc`。**唯一研究问题：** Run225两个二步正见证能否延续到三步，以及角速度是否造成严格的 `Pre²(X)\Pre³(X)` 边界收缩。冻结Run224 Euler模型和Run208/210逐拍独立横向残差合同，不改模型或假设。

## 模型、信息结构与安全合同

`x=(p,v,phi,omega)`，`h=1/50`，`T∈[981/200,2943/200]` N，`tau∈[-2/25,2/25]`，`I=1/50`；`|p|≤5, |v|≤3, |phi|≤9/20, |omega|≤2`；`|r|≤R(T)=47/25+(243/16000)T`。状态更新为 `p+=hv, v+=h(-T sin(phi)+r), phi+=h omega, omega+=h tau/I`。姿态过程扰动为零。三步正确量词：`exists u0 forall r0 exists u1(x1) forall r1 exists u2(x2) forall r2`，各中间状态均须安全。这里控制器观察完整真实状态，**不是SMF输出反馈结论**。

## 正见证：Pre³(X)非空

初始 `(0,±3,±3/20,0)`，三拍固定 `T=2943/200, tau=0`。用 `s7(phi)≤sin(phi)≤s5(phi)` 有理数Taylor界对所有残差传播区间，三拍每个中间状态满足硬约束。正向第三拍速度包含在约 `[2.741852029,2.994270117]` m/s；负向严格镜像。因此两个初态属于 `Pre³(X)`。固定开环策略是充分见证，不是最优控制或终端不变性。

## 严格负见证：Pre²(X)不包含于Pre³(X)

初始 `(0,3,3/20,-2/5)` 和符号镜像 `(0,-3,-3/20,2/5)`。前两拍固定 `T=TMAX`，`tau0=±TAUMAX,tau1=0`，有理数区间验证全部合法残差下状态安全，故均属于 `Pre²(X)`。正向第二拍速度上界约 `2.998509423` m/s。

对任意合法因果控制，正向姿态 `phi0=3/20`、`phi1=71/500`，而 `phi2∈[331/2500,339/2500]`，不依赖第二拍力矩。三拍全部 `sin(phi)>RT`，对手可逐拍选 `r_i=+R(T_i)`；每拍速度增量关于推力严格递减，故所有控制中最有利的速度下界取 `TMAX`。再用正弦上界 `s5` 得到严格有理数证书：

`v3-3 >= h[3(R0+RT*TMAX)-TMAX(s5(3/20)+s5(71/500)+s5(339/2500))] = 31023794855816198031/39062500000000000000000 ≈ 0.0007942091483 > 0`。

因而不论控制器如何根据已发生扰动调整推力/力矩，第三拍必有合法对抗残差使 `v3>3`。负向由奇对称得到相同严格排除。此结论只针对冻结模型与允许独立选择的对抗残差，不等同真实气动必然持续极端。

## 复现与证据级别

本地Python 3.13.5、标准库 `fractions.Fraction`，源码兼容镜像运行：
```sh
PYTHONPATH=verification python -m unittest -v verification.test_four_state_three_step_predecessor
python -m py_compile verification/check_four_state_three_step_predecessor.py verification/test_four_state_three_step_predecessor.py
PYTHONPATH=verification python verification/check_four_state_three_step_predecessor.py --output results/three_step_predecessor_20261031/checks.json
```
7项测试6通过、1项因本地无法完整checkout而跳过；语法编译及归档JSON生成通过。新增GitHub Actions工作流将在完整checkout中执行Run224/225/226回归、真实配置合同、编译及归档逐字比较；**CI未返回成功前不声称通过**。源码和测试的本地Git Blob SHA分别为 `d120e52789f258adfbc6d455f7fc92702ecc3741`、`9d96e671bd6f33e3d804622cb3b6ebdcb98e5184`，归档Blob SHA为 `202c434afd1cf30912b236d5cdb586922f5f557e`。完整仓库历史回归、20ms最坏时间及四状态MPC闭环均未验证。

## 文献与硕士课题评价

本轮原文阅读Liu、Anevlavis、Ozay、Tabuada（2021），*Automaton-based Implicit Controlled Invariant Set Computation for Discrete-Time Linear Systems*，arXiv https://arxiv.org/abs/2109.12378，阅读§II–IV-A、Definition 2/3、Assumptions 1–3、Theorems 1–2。论文明确区分未观测扰动的 `forall x exists u forall d` 与已观测扰动的 `forall x forall d exists u`；使用有限自动机控制器和增广状态RPIS得到隐式RCIS，定理依赖线性系统、多面体等条件，不能直接推广到本非线性推力调度模型。本轮为**新增分节原文阅读**，非全文精读；唯一论文日志去重计数由87增至88。Kolmanovsky & Gilbert (1998) DOI https://doi.org/10.1155/S1024123X98000866 为既有摘要/书目核验，不新计数。

**可行性：** `Pre³(X)` 非空，但RCI核仍未知。**创新性：** 三步前驱属于已知控制不变集理论；本轮价值在严格排除有限步虚假终端保证，不作为独立创新声明。**难度：** 高，关键是从局部有限步见证转为非空不变终端策略并满足输出反馈量词、计算预算。**Gate A=blocked**；没有四状态终端RCI、完整SMF＋Tube MPC递归可行性、稳定性、六状态安全保证。

**下一轮唯一优先任务：** 停止机械逐拍扩展，围绕可允许双侧倾角切换的四状态联合终端候选，构造并检验真正的 `forall x in C exists u forall r: F(x,u,r) in C` 不变性条件；若无法构造，给出明确阻塞与课题范围调整建议。
