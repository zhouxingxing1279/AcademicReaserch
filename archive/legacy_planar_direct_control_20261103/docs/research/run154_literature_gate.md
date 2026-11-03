# Run154 文献准入卡：历史完备共同外包算子

日期：2026-10-11。起点为 Run153 `a95da0a`；本地 `main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容与边界 |
|---|---|---|
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026) 112661，DOI `10.1016/j.automatica.2025.112661`，[预印本](https://arxiv.org/pdf/2307.04146) | **定向精读 §4.2--4.3 的 Definitions 5--6/Theorem 1，以及 §6.3--6.5 的 Definition 7、Theorem 3 与证明** | information ensemble 的一步算子、tight tube、极端信息集控制和多面体外包已有一般方法。Theorem 3 的量词是“存在同一个 ensemble policy 使整个下一 ensemble 被外包”；不是逐点另选策略。 |
| Baras--Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, TAC 1998，[作者全文](https://user.eng.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf) | 复核 Run152 对 §IV-A、Lemma 4、Theorems 9--11 的全文记录 | 完整历史信息状态是一般输出反馈充分统计量；有限压缩必须证明递归模拟。 |
| Yang--Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 2021，[作者全文](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) | 复核 Run153 对 §4.1--4.4、Propositions 2--5 的全文记录 | string automaton 处理缺测语言和输入串因果性；产品不变性仍需对所有允许 return string 与扰动闭合。 |

## 差异、强基线与准入

最强方法基线是 Houska 的 information-ensemble 外包。当前问题不是提出新的集合算子，而是
把仓库的 60-state packet refinement、可见 `d=e-eta`、共享物理原语和执行器约束嵌入该
一般框架，避免错误地把不同历史或不同策略混成一张正证书。

本轮得到两个准入边界：

1. 对**预先固定的同一因果策略** `kappa(q,d,z,ubar)`，前向历史包络算子是单调的，可以从
   真实 `(0,init)` 初始集取 Kleene 可达闭包；
2. 若每次迭代在 `exists kappa` 下重新选不同策略，所得集合并不对应一张可执行控制器，也无
   一般的“跨策略最小闭包”。共同外包若再做凸化，会产生新的 observation fibers；只有策略
   在这些新增 fibers 上也定义、满足输入约束并使凸化后集合逐边闭合，凸包才是安全外包。

**准入通过：只允许形式化历史完备、固定策略的单调外包合同及 terminal/init 两层接口；不准入
数值迭代。** 该算子是已有 information-state/ensemble 理论的项目特化，不作创新声明。最强
同条件基线是完整 history-indexed information ensemble；候选有限压缩若不能在相同共享输入、
共享原语和硬约束下闭合，应退回该基线。推翻有限压缩所需的是任一允许策略类均无法闭合的
证书，而不是某个固定策略或单次凸包失败。
