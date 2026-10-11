# Run164 文献准入卡：测量条件化后的 `J14` 方向半宽

## 最近邻核查

| 工作 | 本轮阅读范围 | 对本轮问题的覆盖 |
|---|---|---|
| Scott et al., *Constrained zonotopes* (Automatica 2016) | **全文定向重读** Sections 2.2、3.1--3.2 | generalized intersection、线性像及多面体/CZ精确表示已覆盖“给定观测后取等式切片”；本轮只是对冻结 `J14` 的精确实例。 |
| Alamo et al., *Guaranteed state estimation by zonotopes* (Automatica 2005) | 正式摘要、问题设定与可访问正文片段；非全文精读 | 预测集与实际测量一致条带求交后再外包；说明SMF后验按已实现测量条件化。 |
| Goulart & Kerrigan, *Output feedback receding horizon control of constrained systems* (2007) | 复核既有全文记录的 Sections 4.2--4.3、6.4--6.5、Theorem 3 | 同一 information set/fiber 内共享控制；不同已观测 information set 可选不同控制。一般方法已知。 |
| Le et al., *Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation* (CDC 2011) | 复核既有正文记录与本轮题录 | zonotopic SMF与tube MPC组合已有，不能把条件化support查询本身当作创新。 |

## 差异、最强基线与推翻条件

本轮不提出新的集合表示或SMF算法，只审计Run161必要门槛的量词。最强同条件基线是：测量成功后，
控制器以实际可见偏差 `d=e-eta` 为信息，针对对应 `J14(d)` fiber重新规划；同一fiber内仍必须共用
因果输入。若精确求得的最坏fiber方向半直径仍大于1，则Run161的seed阻塞保留；若小于1，则整体
`J14`无条件support把不同观测混在一起，不能继续作为条件化策略的必要门槛。

## 判断

**通过量词纠错与精确验证，不通过新算法声明。** 该问题直接决定是否应继续缩小seed合同；若旧门槛
不是必要条件，就必须停止错误的初始化不可能性支线，转而验证每个fiber的完整15-tick安全与跨时刻
移位。Scott/Goulart已覆盖一般集合与信息结构，本轮贡献仅是当前四状态冻结合同的可复现证书。
