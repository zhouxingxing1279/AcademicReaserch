# Run153 文献准入卡：`last_return` 自动机的语义边界

日期：2026-10-11。起点为 Run152 `07ac10f`；本地 `main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容与边界 |
|---|---|---|
| Yang--Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 2021, DOI `10.1016/j.ifacol.2021.08.481`，[作者全文](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) | **精读 §4.1--4.4、Algorithm 1、Propositions 2--5 及式 (8)--(11)** | string automaton 在成功测量时采样决策状态；控制器须在未知下一 return length 时预先给出最坏长度的开环输入串。产品系统上的不变集在紧性/连续性条件下给出安全问题的 sound/complete 解。有限缺测自动机并不自动压缩连续信息集合。 |
| Baras--Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, TAC 1998，[作者全文](https://user.eng.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf) | 复核 Run152 对 §IV-A、Lemma 4、Theorems 9--11 的全文笔记 | 完整可见历史诱导的信息状态才是一般输出反馈充分统计量；有限标签须另证递归模拟。 |
| Houska, *Intrinsic Separation Principles*, arXiv:2307.04146 | 复核 Run151 对 §6.4--6.5、Theorem 3 的全文笔记 | information ensemble/极端信息集已经提供一般集合层；本轮只能核查离散记忆语义，不能把标签扩展宣称为集合算法创新。 |

## 差异、强基线与准入

最强缺测调度基线是 Yang--Ozay 的 string-automaton 产品系统，最强连续信息基线仍是
Baras--Patel/Houska。当前 `mode=0,...,14` 是逐 tick 的 current miss age，而 Yang--Ozay
在成功测量时使用的是 return string；两者的采样时刻不同。新增 `last_return` 只保存上一
完整周期长度，不代表连续信息状态。

审计推翻 Run152 下一步中“直接以三 return seed 为初始化像”的表述：原合同初始化于
`mode=0,d=0`，首次成功之前没有上一周期，故必须加入瞬态哨兵 `init`。扩展状态应为
`(mode,r)`，`r in {init,5,10,15}`；miss 保持 `r`，从源 mode `4/9/14` 的 success 分别令
下一记忆为 `5/10/15`。若直接只保留三个 seed，会丢失真实初始集合与首次 return 前的 15 个可达
状态，初始化覆盖条件失败。

**准入通过：只允许给出离散自动机的确定性、可实现性和初始化修正；不准入共同外包求解器。**
文献已覆盖有限缺测语言/产品系统思想；Run148 三 seed 仅是固定零修正的首次 return 像，不能
初始化所有循环历史。进入集合求解前必须先定义每个扩展状态覆盖的全部历史语言，并证明候选
外包对 shared control/primitive 的逐边映射闭合。若 `last_return` 下的共同外包违反硬约束，
则构成该压缩的反例；仅观察不同 shape 不能推翻它。
