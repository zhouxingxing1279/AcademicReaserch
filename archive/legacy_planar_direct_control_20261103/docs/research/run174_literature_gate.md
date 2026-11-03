# Run174 文献准入卡：测量成功后的首窗口reset

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Scott等, *Constrained zonotopes* (2016) | **开放全文重读** §2 Definition 2、§3.1 Proposition 1及证明、§5估计递推 | generalized intersection精确表示预测集与有界观测的一致部分；更新保留一致真值，但不作用于物理plant。 |
| Mayne等, *Robust output feedback MPC of constrained linear systems* (2006) | 正式摘要、引言及控制器结构正文 | 用不变估计误差集与不变控制tube截面保证真实轨迹约束；不是把真实状态在每次观测后重置到初始盒。 |
| Hassaan等, *Time-Varying Tube-Based Output Feedback MPC...Intermittently Delayed Data* (2021) | 复核既有全文记录 §§2.2、3.1--3.2、Theorems 5--7 | 缺测语言由时变估计/控制tube和公共终端骨架闭合，是本轮后续强基线。 |

## 差异、推翻条件与判断

本轮不提出新的CZ更新或Tube MPC。只检验仓库特定的强命题：首次成功位置测量后，真实六状态
是否必然重新进入Run173使用的绝对初始盒。若存在一条满足初态、plant、输入、风、硬状态域和
成功观测合同的轨迹，其成功时刻`|v_z|>0.1`，该命题即被推翻。

**准入通过精确物理反例；不通过算法创新或递归不可行声明。** 反例失败时才需继续证明直接
reset；反例成立则停止复用首窗口盒，转向5/10/15相位周期information tube。
