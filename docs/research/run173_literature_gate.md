# Run173 文献准入卡：首个15步窗口的联合气动支持

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Jafarpour, Harapanahalli, Coogan, *Interval Reachability of Nonlinear Dynamical Systems with Neural Network Controllers* (L4DC 2023) | **开放全文新增精读** §5 Theorems 2--3、Remark 4，§6 Algorithm 1 | inclusion/decomposition embedding给出可靠可达盒；每步重分割并取并集可提高紧度，且外包必须持续包含真实轨迹。连续时间NN闭环设定不直接覆盖本仓库。 |
| Rego等, *Reachability Analysis of Nonlinear Discrete-Time Systems Using Polyhedral Relaxations and Constrained Zonotopes* (CDC 2024) | 重读§§II--III | 离散非线性图的factorable CZ递推是同条件强基线。 |
| Hu等, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model* (ACC 2018) | 复核Run168--172记录 | 局部余项界必须覆盖整个预测tube；首窗口界不能自动升级成递归tube。 |

## 差异、强基线与推翻条件

本轮不提出新区间或CZ算法。针对仓库解析Euler模型，以依赖顺序
`torque -> phi -> horizontal acceleration -> vx -> aerodynamic support`构造首个15步窗口的可靠盒投影，
并与Run168门槛比较。强基线仍为Rego的factorable CZ递推；本轮盒界若已低于门槛，则无需为
该首窗口实现更复杂表示。

若姿态归纳、横向加速度绝对界、Run172竖直速度下界或最终气动支持上界任一不覆盖全部允许
输入/风历史，或者支持上界不低于门槛，则候选命题被推翻。

## 判断

**通过首个15步窗口的解析支持证书；不通过递归tube或算法创新声明。** 只允许实现精确有理数
检查器。测量成功后的任意posterior reset是否重新落入同一小盒，仍须另证。
