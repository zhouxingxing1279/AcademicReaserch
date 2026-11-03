# Run 123 文献准入卡：两时刻因果更新与候选移位

日期：2026-09-28。仓库基线：`main` 1c49659c；研究基线：`research/run122-reproduce-run119` 90acb9a。

## 本轮阅读与最近邻

| 文献 | 阅读层级与本轮定位 | 已解决内容及与本轮的差异 |
|---|---|---|
| Dey, Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026，[arXiv:2605.23661](https://arxiv.org/abs/2605.23661)，[全文](https://arxiv.org/pdf/2605.23661) | **全文定向精读** Section IV（pp. 4–7）、Algorithm 1（p. 7）、Theorem 2 及 Appendix IV（pp. 10–11），特别是 (51)–(55)。 | 已对 LTI 参数/加性不确定系统建立自适应观测器、随估计更新的 tube/收紧/终端，并用备份集合和旧解移位证明递归可行；(52e)、(52g) 正是跨时刻误差集合嵌套。故“在线集合收缩 + 输出反馈 adaptive tube + shift proof”不是创新。本轮仅把仓库的高维状态后验和冻结控制器实例化到其固定模型/固定点估计的子情形。 |
| Köhler, Müller, Allgöwer, *Robust output feedback model predictive control using online estimation bounds*, 2021，[arXiv:2105.03427](https://arxiv.org/abs/2105.03427)，[全文](https://arxiv.org/pdf/2105.03427) | 本轮复核原始论文页面、摘要及仓库既有阅读记录；**本轮未重读全文**。 | 已将在线验证的估计误差界并入非线性 homothetic tube MPC，并在 10 状态四旋翼数值例中展示减保守性。其标量/度量误差界与本轮 602 潜变量 CZ 风格后验不同，但宽泛主张已被覆盖。 |
| Köhler, Kötting, Soloperto, Allgöwer, Müller, *A robust adaptive model predictive control framework for nonlinear uncertain systems*, IJ Robust Nonlinear Control 31 (2021)，[DOI](https://doi.org/10.1002/rnc.5147) | 继承 Run 121–122 对 Section II–III、Theorem 1–2 及候选移位证明的全文核查；本轮只用于比较。 | 参数集合非扩张、传播单调性和终端条件已被用于在线更新下的递归可行；状态后验测量求交不能与模型参数集合混同。 |
| Robbins, Glunt, Thompson, Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*, ACC 2026, pp. 585–592 | 仍只取得机构摘要与书目信息，**未取得全文**。 | 摘要已覆盖 CZ 在线可达收紧和免优化 zonotope 外包；因此固定复杂度比较必须把该方法列为强基线，不能据摘要判断其是否覆盖本项目的余量准入。 |

## 问题、证明义务与最强基线

问题不是提出新的 adaptive tube，而是验证仓库中 Run 122 的 601 潜变量后验能否经过一次真实的“控制—预测—新测量—旧计划移位—终端追加”。固定模型、反馈和扰动集合时，若新 nominal 初值取旧 nominal 后继，测量交集给出

\[
C_{t+1}\subseteq F C_t\oplus W=E_{1|t},\qquad
E_{i|t+1}\subseteq E_{i+1|t}.
\]

于是旧计划的第 1 至第 29 阶段约束可直接转移；最后一拍必须另用 Run 121 的固定 RPI 终端证书和零输入追加。这个结论是 Dey–Bhasin Theorem 2/Appendix IV 固定模型子情形的直接实例化，不是独立贡献。最强同条件基线就是“不改点估计/模型时的旧解移位 + RPI 终端策略”。

推翻条件：新测量交集为空；新误差坐标没有锚定旧 nominal 后继；任一控制相关支持超过旧 tube 下一阶段；移位名义动态不一致；终端零状态/零输入不满足；或 Run 121 RPI 条件失效。

## 准入结论

**通过基线实例化，不通过新算法或首次性声明。** 允许实现一个可执行的两时刻验证器，用于封闭仓库证据链和暴露下一阻塞；不允许把固定对齐中心的集合嵌套称为创新。真正未覆盖的候选问题仍是：在非零重定心和固定复杂度压缩同时发生时，能否以有限控制方向证书保留同一移位候选，并在同预算下优于固定 tube/常规外包。
