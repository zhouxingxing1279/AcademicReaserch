# Run171 文献准入卡：单步共享因子图能否排除Run169点

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Kochdumper, Althoff, *Sparse Polynomial Zonotopes: A Novel Set Representation for Reachability Analysis* (IEEE TAC 2020), DOI `10.1109/TAC.2020.3024348` | **开放全文精读** §1.1--1.2、Definition 1、Propositions 1--4 | 用dependent factors和全局identifier保留重复不确定因子的依赖；非凸表示减少非线性reachability wrapping。独立因子运算快但会外包。 |
| Rego, Raffo, Terra, Scott, *Reachability Analysis of Nonlinear Discrete-Time Systems Using Polyhedral Relaxations and Constrained Zonotopes* (CDC 2024) | 重读Run170全文范围：§II--III、式(1)--(11) | 从输入集合递归外包非线性像；factorable lifted graph的polyhedral enclosure必须包含每个真实图点。 |
| Hu等, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model* (ACC 2018) | 复核Run168--170精读记录 | tube-dependent remainder bound仍量化其输入tube；单步图外包不能替代从初始集得到该tube的可达性证明。 |

## 差异、强基线与推翻条件

本轮不提出新的集合表示。问题仅是：把Run169点代入真实`plant.py`气动计算图后，共享
`r_x,r_z,phi,T`因子是否自洽。若自洽，则任何可靠单步graph outer approximation都必须包含
其像；单步CZ/SPZ因子化本身不能排除该点，下一步必须处理从benchmark初始集到J14的跨时刻
联合非线性可达性。

强基线是Rego的factorable CZ外包和Kochdumper--Althoff的dependent-factor SPZ，而不是独立
残差盒。若Run169点违反任一共享因子等式、真实输入域或原始气动公式，本轮命题即被推翻。

## 判断

**通过精确单点图一致性证书；不通过单步CZ传播器或创新声明。** 实现只允许证明“可靠单步
外包不能排除该点”以及明确剩余跨时刻义务，不把单点成员检查误称为可达性证明。
