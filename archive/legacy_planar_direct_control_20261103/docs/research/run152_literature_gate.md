# Run152 文献准入卡：有限信息抽象充分性

日期：2026-10-11。起点为 Run151 `df10a61`；本地 `main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容与边界 |
|---|---|---|
| Baras--Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, TAC 1998, DOI `10.1109/9.654887`，[作者全文](https://user.eng.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf) | **重读 §IV-A 的 Information State Formulation、Lemma 4 证明、Remarks 8--10、Theorems 9--11 与 Corollary 4** | 完整可见历史诱导的信息状态递归是输出反馈问题的充分统计量，且一般为无限维。有限标签若要替代它，必须证明递归模拟/包含；不能仅凭 mode 和点估计宣称等价。 |
| Kjellqvist, *Minimax Dual Control with Finite-Dimensional Information State*, L4DC 2024，[全文](https://proceedings.mlr.press/v242/kjellqvist24a/kjellqvist24a.pdf) | 复核 Run143 对 §2.1--2.2、Assumption 2、Proposition 4 的全文笔记；本轮未重复全文阅读 | 有限测量逆像基数给出有限维信息状态；当前连续有界测量噪声不满足该条件。 |
| Houska, *Intrinsic Separation Principles*, 2023/Automatica 2025，[预印本](https://arxiv.org/pdf/2307.04146) | 复核 Run151 对 §4.4、§5.5、§6.4--6.5、Theorem 3 的全文阅读 | 一般 information ensemble、极端信息集控制与终端 ensemble 已覆盖方法框架；有限历史模板本身不是创新。 |

## 差异、强基线与准入

最强概念基线是 Baras--Patel 的完整信息状态；最强可计算近邻是 Houska 的多面体
information ensemble。当前问题只是在冻结的 15-mode packet/observer 合同中，判断一个
有限 automaton memory 加连续可见变量能否形成**保守模拟**。充分性判据是已有信息状态
原理的直接特化，不作创新声明。

审计发现：现有 `mode=0,...,14` 已等于当前 miss age，三条 success return 都重置为 mode 0。
若 `return-age` 与 mode 同义，则它不增加信息；若指上一 return 周期，必须显式保存
`last_return in {5,10,15}` 并逐边更新。Run148 的三个不同 return seed说明现有标签不唯一
决定形状，但其凸包可共同外包，所以这不是一般不可行反例。

**准入通过：只允许写出有限抽象的初始化覆盖、历史一致性、逐边模拟、硬约束和终端闭合
五项合同；不准入求解器、RCI 存在性、递归可行性或算法创新声明。** 推翻候选类需要证明
同索引全部历史不存在满足硬约束和共享控制的共同外包，不能只展示两条历史形状不同。
