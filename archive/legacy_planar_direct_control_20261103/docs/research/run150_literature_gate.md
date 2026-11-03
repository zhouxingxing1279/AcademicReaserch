# Run 150 文献准入卡：translated fixed-shape return containment

日期：2026-10-03。仓库起点为本地 Run149 提交 `f333cdf`；远端
`main=1c49659`，远端最新实际成果分支为 Run147 `18a2b61`。Run148--149 尚未由命令行
同步，因为 HTTPS remote 没有凭据；其基线已用仓库根入口复验为 `verification/` 201/201、
`tests/` 39/39。

## 本轮问题

在 Run136 固定 global residual envelope 下，Run149 已证明 correction 只平移联合
`(eta,e)` 信息集，不改变 intrinsic shape。本轮检查 Run148 的

`C0 = conv(J4 union J9 union J14)`

能否作为 translated fixed-shape mode-0 target。具体地，从 `C0` 沿 miss 动力学生成
mode-indexed 零中心 shapes `C_j`，并对三条 return edge `4->0`、`9->0`、`14->0`
验证是否存在任意 source/target centers 与同一当前 correction，使完整 success image
包含于 `C0+c0`。mode 4/9 的 correction 必须同时服务未知 miss/success successor。

## 最近邻原始文献与本轮实际阅读

| 工作 | 本轮阅读层级 | 已解决内容 | 对本轮的严格边界 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, 2023, arXiv:2307.04146 | **重新精读作者全文 pp.14--17 的 Sections 4.1--4.3、Definition 4--6、Theorem 1及证明，pp.23--25 的式(18)--(19)/Theorem 2，pp.29--32 的 Definition 7、Theorem 3及证明** | 固定 `A,B,W,V` 时，tight information tubes 的 intrinsic equivalence class 与控制策略无关；控制自由度可写成 information-set-dependent translations；极端信息多面体各自配置一个共享控制并用凸权重插值。 | 直接覆盖 fixed-shape/translation 思路和极端集合共享输入量词。本轮只能核查当前 packet graph 的实例可行性，不能把集合参数化或算法称为新贡献。其 Theorem 1 还要求固定 `W`，所以这里只使用 Run136 global envelope。 |
| Hempel--Kominek--Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901` | 本轮复核 Run149 已精读的 Section III-A--C、Definition 2、Theorem 1 与式(3)--(12)记录；**不计作本轮新增全文精读** | 给定 OFCI polytope 的验证和 PWA input computation；同一 noisy-output fiber 及未知 successor 必须共享当前输入。 | 支持 mode 4/9 的共享输入量词，但不给当前 correlated convex-hull template，也不能读取隐藏 `eta`。 |
| Wehbeh--Kerrigan--Scaccia, *Generalized Semi-Infinite Programming for Robust Optimal Control with Decision-Dependent Uncertainty*, 2026, arXiv:2609.01538v1 | 复核作者全文中 Run149 已读的 Introduction、Section II Assumption 1/Theorem 1、Section IV Assumption 2/Theorem 3；并核对 2026-09-01 v1 元数据；**本轮不重复算法实现** | 决策相关不确定性形成 GSIP，可在正则条件下改写为 existence-constrained SIP 并用 adaptive discretization。 | 只有 fixed-envelope translated class 失败且 scheduled residual 的潜在 tightening 足以改变结论时，才值得支付 GSIP 成本；其框架不提供当前信息 ensemble、terminal 或递归可行性证书。 |
| Rungger--Tabuada, *Computing Robust Controlled Invariant Sets of Linear Systems*, 2017, TAC 62(7), DOI `10.1109/TAC.2017.2672859` | 复核 Run142/145--146 已精读的 pp.1--7、式(4)--(10)、Theorems 1--2；**不计作本轮新增全文精读** | predecessor 递减迭代、投影以及有限层与 RCI/停止证书的区别。 | 本轮只做候选类的一步 return containment；即使三条边通过也不是 fixed point 或 RCI。 |

本轮满足“至少精读一篇正文”的硬门槛：Houska 全文相关章节及证明已重新逐页核对。搜索还
发现 Ning 2026 data-driven output-feedback RPI，但它综合 observer-based augmented RPI，
不处理 noisy-output fibers、packet automaton 或 translated information ensembles，因此不列为
本轮同条件强基线。

## 差异、证明义务、强基线与推翻条件

1. **候选类。** `C0` 是 Run148 三条固定零修正 return images 的最小凸容器；`C_j`
   定义为从 `C0` 经 `j` 次固定-envelope miss shape propagation 得到的零中心凸 shape。
   source/target centers 任意，当前 correction 只能通过 Run149 的已证平移接口进入。
2. **必要条件。** 若 `S+t subset T+c`，则所有方向的 width 必须满足
   `width_S(a)<=width_T(a)`；平移与 current correction 均不能改变 width。对中心对称
   shapes 可用 exact support 半宽比较。
3. **共享输入。** mode 4/9 的 miss 与 success 必须使用相同 correction。miss target
   `C_{j+1}` 由传播定义，shape containment 可由中心递推吸收；若 success 单边已违反 width，
   则 shared-input branch 更不可能成立，无需虚构读取 packet outcome 的两套输入。
4. **最强同条件基线。** Houska 的固定 `W` translated information tube 是一般方法基线；
   本轮比较的是其在当前 exact low-rank `C0` shape 上的实例，而不是与 box/ellipsoid 作
   不同信息或不同预算的弱比较。
5. **推翻条件。** 若三条 success image 的所有必要 width 均不超过 `C0`，本轮不能给出
   否证，必须进入完整 lifted convex-hull containment；若任一 exact width 严格超出，
   只否定该 translated fixed-shape family，不否定 history-conditioned shapes、一般
   information ensembles 或 scheduled GSIP。

## 课题作用与准入判断

该检查直接决定是否值得继续在单一 `C0` 上优化 centers/affine visible policy。若最早 return
已存在控制不可改变的 shape-width obstruction，继续枚举 centers、法向或启动 GSIP 都不会
闭合该候选的控制可行性证据链，应转向 mode/history-conditioned intrinsic shapes。

**准入通过：实现三条 return edge 的 exact support-width obstruction verifier，并保留
mode 4/9 shared-input 语义；不准入一般 RCI、完整信息 ensemble、六状态、terminal、MPC
递归可行性或算法创新声明。**
