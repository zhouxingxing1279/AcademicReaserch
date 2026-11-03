# Run170 文献准入卡：非线性联合物理可达性

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Rego, Raffo, Terra, Scott, *Reachability Analysis of Nonlinear Discrete-Time Systems Using Polyhedral Relaxations and Constrained Zonotopes* (CDC 2024 / arXiv 2025), DOI `10.1109/CDC56724.2024.10886592` | **开放全文精读** §II 式(1)--(8)、§III Definition 3、式(10)--(11)及乘法包络 | 从`X0`和`W`递归外包真实非线性像；factorable graph把重复因子放在同一lifted space，并以相交的多面体包络保留约束。复杂度线性增长后仍需降阶。 |
| Hu等, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model* (ACC 2018) | 重读Run168--169全文记录：Theorem 1、式(8)、Lemma 1 | RFIT要求对tube内全部状态/扰动覆盖非线性余项；它不允许把未经真实可达性证明的外包成员反向称为plant可达。 |
| Robbins等, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations* (ACC 2026) | 本轮仅核查IEEE摘要；全文未取得 | 用CZ和非线性polyhedral envelope在线传播误差，并转为zonotope做收紧；是最强同主题线索，但不能凭摘要判断其是否处理本项目缺测联合信息状态。 |

## 差异、最强基线与推翻条件

Run169的cycle-lifted集合是可靠但保守的线性残差外包：每条边独立注入`rho_x,rho_z`，没有
证明选定极端状态、风和残差来自同一真实非线性历史。Rego等的方法说明可把状态、风及气动
因子置于同一factorable lifted graph递归传播；这不是本项目创新，而是修复证据链的直接基线。

候选项目问题严格多出的义务是：在有界丢包、测量求交和因果输入下，将联合物理可达外包接到
控制相关收紧与跨时刻移位证明。最强比较应是当前独立残差盒、常规CZ线性化，以及Rego式
factorable CZ外包在相同复杂度预算下的支持、可行率与运行时间。

若联合外包仍包含Run169极端组合，或虽排除它但Run166门槛仍失败，或固定预算压缩损失抹去
优势，则该路线被推翻。

## 判断

**通过方向纠错与下一证明义务；不通过新算法/创新声明。** 本轮只撤回过强结论、建立可执行
证据边界并记录最近邻。尚未实现非线性联合传播，也未证明它排除反例或降低收紧。
