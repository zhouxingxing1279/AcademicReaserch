# Run156 文献准入卡：第二周期零策略硬约束门槛

日期：2026-10-11。起点为远端 Run155 `1a7d413`，tree `3b950c06`；远端
`main=1c49659`，起点工作树干净。

| 最近邻 | 本轮实际阅读 | 已解决内容与边界 |
|---|---|---|
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026) 112661，DOI `10.1016/j.automatica.2025.112661`，[正文](https://www.sciencedirect.com/science/article/pii/S0005109825005576) | **重新精读 §6.5、Theorem 3 及完整证明，并复核 §4.2 Definitions 4--6** | 极端信息集各配一个控制，再按依赖当前信息集的凸权重构造 `mu(X)`；凸输入集保证插值输入可行，逐步 information-tube inclusion 已有一般方法。固定零策略只是最弱可执行基线，不是该方法的代表。 |
| Yang--Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 54(5), 2021，DOI `10.1016/j.ifacol.2021.08.481`，[作者全文](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) | **重读正文 Introduction 关于 string automaton、因果输入承诺和 product safety game；§4.1--4.4 的详细结论沿用 Run153 已核查记录** | 缺测模式必须在产品系统上逐步满足安全约束；控制器运行时不知道未来连续缺测长度。只检查 return 时刻而忽略中间 miss tick 不构成安全证书。 |
| Hempel--Kominek--Werner, CDC-ECC 2011，DOI `10.1109/CDC.2011.6160901` | 复核 Run155 对 §III-A--C、Definition 2、Theorem 1 的全文阅读记录；**本轮未重新读正文** | 同一观测纤维共享输入；支持本轮对零策略的因果解释，但不把零策略失败推广为一般 output-feedback 失败。 |

## 差异、强基线与准入

最强一般基线是 Houska 的 extreme-information-set feedback；最强缺测语义基线是 Yang--Ozay
的 product safety game。本轮只验证 Run155 指定的固定 global residual、三类首次 return seed、
零修正策略下九条第二周期 histories 是否在**每个中间 tick**满足当前竖直硬约束。

**准入通过：允许做精确有理数的零策略/标签开环基线反证；不准入非零 affine policy 综合、
RCI 或创新声明。** 若九条路径全部满足 estimator、true-error 和 actuator 约束，则下一步才是
同标签 target convex hull；若任一路径中间时刻的集合半宽严格超过硬约束，则零策略基线立即
终止，而且凸化不能修复 constituent-set 已经不安全的问题。

该反证也覆盖任何在每个标签上对整个集合施加常数 correction 的 open-loop/label-only 序列：
固定 global residual 下常数输入只平移 `e_v`，不能改变方向宽度。它不覆盖依赖可见 `d` 的
仿射/分片策略，因为反馈增益会改变闭环集合形状。
