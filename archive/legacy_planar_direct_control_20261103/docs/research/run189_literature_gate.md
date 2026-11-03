# Run189 文献准入卡：物理有界 direct-offset ensemble 门槛

日期：2026-10-27。远端基线为 Run188 `b5253cbb`（tree `6a786415`），远端
`main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026), 112661；arXiv:2307.04146 | **重读 §3.1--3.2、§6.2--6.7、式(25)--(30)、Definition 7** | information ensemble向下闭合，极端集合给出最小表示；`P(z)={y:Gy<=0,Zy<=z}`，`H/Omega`只保留真正extreme vertex polytopes。 | 参数多面体有很多几何极点，不代表information ensemble有同样多的极端集合；必须先做包含极大性过滤。 |
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, Automatica 163 (2024), 111543；arXiv:2208.12554 | **重读 §3.4--3.5、Definition 6、Lemma 1、Theorems 1--2及证明接口** | 固定法向的configuration domain是多面锥，锥内vertex maps线性有效。 | 物理状态约束可逐vertex线性施加，但这只给出有界参数域，不保证多个不可比较的最大集合。 |
| Badalamenti et al., *Efficient CCTMPC via Variables Restriction and Template Selection*, CDC 2025；arXiv:2505.14440 | **重读 §3.5--3.6、§4.1、Algorithm 1及复杂度讨论** | 同伦限制、自由参数化及template refinement已有系统复杂度/保守性折中。 | 随意加offset caps或shape constraints不是创新；约束必须由information结构和闭环证书驱动。 |
| Badalamenti et al., *CCTMPC for Difference-of-Convex Nonlinear Systems* (2026), arXiv:2609.07809 | **仅核对摘要、Introduction与问题概述** | 将configuration-constrained tubes推广到DC非线性系统并给出隐式终端条件。 | 与本轮线性information ensemble不直接同条件；不据此作首次性判断。 |

## 候选与证伪条件

1. **仅物理包含（本轮审计）**：`Q_X={y in G:P(y) subseteq X}`，不引入调参；
2. **独立offset上下界**：可制造多个参数极点，但界值没有仓库合同依据，本轮拒绝；
3. **mode/history-conditioned shape约束**：可能保留多个不可比较的极端集合，留作下一问题。

若`Q_X`包含一个`P(y_X)=X`且所有`P(y)`都包含于它，则诱导ensemble的极端边界只有`X`；此时
即便`Q_X`有多个参数极点，也不能提供在线information-dependent controls。

## 准入判断

**通过“物理有界参数域是否保留intrinsic information的精确停止证书”；不通过“物理bounds已给出
有用`H/Omega`”或“参数极点数等于extreme information-set数”。** 允许实现最小有理数checker；
不进入15-mode/17-edge LP。
