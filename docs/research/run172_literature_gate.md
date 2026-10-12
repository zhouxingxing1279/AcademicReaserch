# Run172 文献准入卡：跨时刻竖直速度可达性

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Jafarpour, Harapanahalli, Coogan, *Interval Reachability of Nonlinear Dynamical Systems with Neural Network Controllers* (L4DC 2023) | **开放全文精读** §2（可达集、decomposition/inclusion function）、§5 Theorem 2 | 从初始区间和扰动区间出发，用嵌入系统给出非线性闭环可达集的可靠盒外包；分割用于收紧外包。本文是连续时间与NN闭环，不能直接替代本仓库的离散Euler证明。 |
| Rego, Raffo, Terra, Scott, *Reachability Analysis of Nonlinear Discrete-Time Systems Using Polyhedral Relaxations and Constrained Zonotopes* (CDC 2024) | 重读Run170--171已核查的§§II--III | 离散非线性像必须从输入集合递归外包；factorable CZ保留共享图因子。 |
| Kochdumper, Althoff, *Sparse Polynomial Zonotopes* (TAC 2020) | 重读Run171的Definition 1、Propositions 1--4 | dependent factors减少依赖丢失，但仍必须从真实初始集传播。 |

## 差异、强基线和推翻条件

本轮不提出新可达集算法。只针对配置中的离散Euler真值模型，利用硬状态域、输入域、风域和
初始竖直速度区间，推导一个逐步成立的竖直加速度下界。它比实现通用CZ/SPZ传播器弱，但足以
回答Run171指定的单点问题，且是任何可靠跨时刻外包必须满足的投影界。

强基线仍是Rego的factorable CZ递推以及Jafarpour等的区间嵌入外包。若余弦下界、相对竖直
速度域、气动项下界或Euler归纳任一不成立，或者Run169速度没有落在所得下界之外，本轮命题
即被推翻。

## 判断

**通过项目特定的跨时刻投影排除证书；不通过通用非线性可达实现或创新声明。** 允许实现纯
有理数归纳检查器；结论仅排除Run169这一末端速度，不自动证明全部气动支持低于Run168门槛。
