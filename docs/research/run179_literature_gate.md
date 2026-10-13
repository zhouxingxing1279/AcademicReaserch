# Run179 文献准入卡：参数化 `Gamma` 类型审计

| 最近邻 | 本轮实际阅读 | 已解决内容 | 当前严格缺口 |
|---|---|---|---|
| Rego--Raffo--Scott--Raimondo, *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, Automatica 111 (2020) 108614，DOI `10.1016/j.automatica.2019.108614`，[作者预印本](https://arxiv.org/pdf/1908.09950) | **全文精读 §2、§3.1、§§4.1--4.5，Theorems 1--3、Lemma 1、Corollaries 1--2、Remarks 8--10及式(22)** | 已知输入和已实现测量下，单个CZ的可靠非线性 mean-value/Taylor prediction、精确 generalized-intersection update、外包降阶和复杂度分析。 | 不表示连续 `d` fibers 上的集合值策略图，也不证明压缩新增 fibers 的共享输入闭合。 |
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026) 112661 | 复核 Run154/178 对 information ensemble、extreme information sets 和同一 ensemble policy 的全文记录 | 正确控制对象是 information sets 的集合，策略对每个 information set 定义。 | 不直接给出本项目 nonlinear packet graph 的固定分片 graph 和可靠 oracle。 |
| Hempel--Kominek--Werner, *Output-Feedback Controlled-Invariant Sets for Systems with LPV State Transition Matrix*, CDC-ECC 2011 | 复核 Run140--155 对 Definition 2、Theorem 1 和 fiber-shared input 的全文记录 | noisy-output fiber 共用输入及给定多面体 OFCI 的验证已有直接基线。 | 当前 plant 非线性且输入参与余项，不能直接套用LPV顶点条件。 |

## 准入判断

**不通过“单个固定阶 CZ 就是 `Gamma`”的实现；通过 family 类型纠正。** Rego 的算法可作为
单-fiber传播原语，但把连续 fibers 合并成一个CZ会迫使不必要的单一输入，逐fiber保存则复杂度
不固定。正确候选至少要表示 lifted graph `(d,s)`，并同时冻结 fiber partition、集合法向和策略
参数化。

最强同条件基线是 Houska information ensemble + Rego nonlinear CZ propagation + Hempel
fiber-shared robust control 的组合。该组合本身不是创新。本轮问题只有在形成完整逐边、硬约束、
45-state终端和MPC移位证书，并在同预算基线上取得严格优势时才具论文价值。

推翻候选表示的条件：任一 source cell 没有共享可行输入；一条合法 success/miss 后继不能由
target cells覆盖；Taylor/CZ外包越出余项source domain；或固定cell/normal预算下只能靠无限细分
保持包含。准入未达到写求解器的门槛。
