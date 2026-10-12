# Run169 文献准入卡：J14 首步局部气动界

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Hu, Feng, Quirynen, Villanueva, Houska, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model* (ACC 2018), DOI `10.23919/ACC.2018.8431112` | **开放全文重读** §II-A、Theorem 1、式(8)、Lemma 1及证明 | RFIT包含所有允许不确定实现；非线性外包必须对tube内每个状态和扰动成立。局部界可以随tube变化，但不能删除tube中的极值。 |
| Do, Prodan, *Tube MPC via flatness for multicopter trajectory tracking* (ECC 2024) | 复核Run168全文精读记录 | 固定扰动集进入mRPI及约束收紧；若扰动过大导致收紧为空，必须改变可靠合同，而不是运行时忽略极值。 |
| Scott等, *Constrained zonotopes* (2016) | 复核Run167全文精读记录 | 精确CZ线性像与相交保留相关性；本轮直接使用J14生成元相关性判断横、竖速度端点能否同时达到。 |

## 差异、强基线与推翻条件

本轮不是设计新的reachability算法，而是按Hu等式(8)的全tube量词审计项目特定的首个预测边。
强基线是保留J14生成元相关性的精确线性像，而不是把各坐标盒化后拼接极值。

命题若满足任一条件即被推翻：(i) J14横、竖速度极值依赖同一生成元且符号冲突；(ii) 构造的
nominal velocity、实际状态或风超出配置域；(iii) 在`phi=0`时真实竖直气动余项未超过Run168门槛；
(iv) 该J14 return不是要求覆盖的初始化族成员。

## 判断

**通过精确首步反例；不通过局部tube实现。** 若J14中存在合法状态/风使第一个未来边的真实竖直
气动余项已超过`D_star`，则任何覆盖完整初始化族的15-tick局部界都不能满足Run166必要门槛。
本轮只允许实现相关性与有理数下界检查器，不声称一般非线性tube或六自由度不可行。
