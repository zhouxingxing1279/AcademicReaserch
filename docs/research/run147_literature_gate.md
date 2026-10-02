# Run 147 文献准入卡：初始化路径的相关 return seed

日期：2026-10-03。仓库起点为远端 Run 146 提交 `160952c`，tree
`5f039e1db09b01af209bf15db8ea7bd73ea88728`；远端 `main=1c49659`。

## 本轮问题与排重

Run 146 的下一问题要求在 mode 14 构造非乘积条件纤维，使固定可见 `d` 下的
`q=eta_p+h eta_v` 半宽低于 product target 门槛，并同时保留初始化 miss-chain。
这与 Run 143 已证明的事实冲突：合同初始化为 `mode=0,d=0`，14 条 miss 上 `d` 的更新
不含隐藏 `eta` 或 residual；因此同一 observation history 必须保留完整 mode-14
`eta` reachable zonotope，其 `q` 半宽为 `23312147/48000000`，不能靠条件化缩小。

本轮不重复该否证，改查真正的证明义务：把这条必经初始化路径经强制
`14->0 success` 的**完整联合像**写成 `(eta_p,eta_v,e_p,e_v)` 四维相关 zonotope。
检查它是否同时满足 Run 136 mode-0 estimator set 和真实 tracking-error 硬约束，并量化
其 `d=e-eta` 投影为何可以超过 Run 146 的 product `D_0^0` 限幅。该集合是任何包含初始
切片的 joint RCI 必须容纳的 return seed，而不是一个 RCI 证书。

## 最近邻原始文献与本轮实际阅读

| 工作 | 本轮阅读层级 | 已解决内容 | 本轮严格边界 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, 2023, arXiv:2307.04146 | **精读全文 HTML 的 Sections 4.4、6.2、6.4--6.5、Lemma 2、Definition 7、Theorem 3 及证明** | 一般 information ensemble、极端信息集、每个极端集合的共享控制和多面体 information tube 已给出系统框架。 | 本轮只实例化当前 packet graph 上一个必要 reachable information set；集合相关性与 extreme-set control 均不是创新。Houska 假设固定线性系统、凸输入和外生多面体噪声，本项目还需处理 observer split、共享原语和 actual-thrust residual。 |
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901` | **重读全文 Sections III-A--C、Definition 2、Theorem 1、式 (3)--(11)** | 对同一 noisy output 相容的全部状态共享一个输入；给定 OFCI polytope 的验证和在线/显式 PWA 控制已有结果。 | 初始化 miss-chain 的全部隐藏 `eta` 不能按真值拆分；本轮 zero correction 只用于形成必要 return image，不是综合控制律。 |
| Kumar, Kothyari, *Set-Theoretic Output Feedback Tracking Control via Linear Programming*, MTNS 2026 | **复核作者公开全文的 Sections 2.3--3、Definition 4、Theorem 5（此前 Run 144 已精读）** | 用 zonotope containment 线性条件联合综合静态 output gain、state RCI 和 admissible reference set。 | 其输出无测量噪声、无 packet automaton/observer information state；不能替代当前 correlated return seed。也排除“zonotope + output-feedback LP”作为首次性。 |
| Baras, Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, TAC 1998 | **复核 Run 143 的全文笔记：Section IV-A、Lemma 4、Theorems 9--11** | observation history 诱导的信息状态是一般输出反馈鲁棒控制的充分统计量。 | 本轮四维 zonotope只是一个可执行有限维必要种子，不声称等价于一般信息状态。 |

稳定全文链接见 `docs/literature/READ_PAPERS.md`。本轮 Web 检索还核对了 2025--2026
output-feedback/RPI 近邻；未发现把有界丢包 observer split、共享 residual/measurement
primitive 和本合同初始化切片一起处理的直接结果。该检索不足以支持首次性声明，故不作声明。

## 差异、证明义务、基线与推翻条件

最强方法基线是 Houska 的 polytopic information ensemble；最强静态 zonotope 基线是
Kumar--Kothyari。当前只做这两类方法之前都需要的实例一致性检查。

对 Run 136 mode-14 zonotope `E_14`，初始化 miss-chain 给出 `d=0,e=eta`。令下一步
垂向 residual 和位置噪声与 estimator update 使用同一原语。必须：

1. 由源生成元直接生成四维 `J_0^ret`，不得把 `eta+`、`e+` 或 `d+` 独立装箱；
2. 精确证明 `proj_eta J_0^ret subset E_0`，且 `proj_e J_0^ret` 位于
   `|e_p|<=1, |e_v|<=11/4`；
3. 精确确定其 affine-hull 维数，并给出独立生成元见证；若低于四维，必须标成低维
   reachable seed，不能把它冒充正体积 joint candidate；
4. 精确计算 `d` 速度支持，并与 Run 146 `D_0^0` 限幅比较；
5. 把结论限制为“初始化路径的必要 correlated seed”。它不证明 controlled invariance、
   输入可行、终端/移位或递归可行性。

若完整联合像违反 `eta` 或 `e` 的硬约束，则当前 hover 合同已在第一次强制 return 上失败，
应停止 joint-RCI 综合并修改域/输入预算。若通过，则它推翻“必须先压缩 mode-14 `q|d`”
这一错误前置条件，并给下一轮 correlated template 提供不可省略的 seed。

## 准入判断

**通过必要 return-seed 的精确实例验证；不通过算法创新、RCI、完整六状态或 MPC 递归
可行性声明。** 本轮价值是纠正 Run 146 的下一问题并把单点相关见证升级为完整可达集合
证书，而不是新增一种集合算法。
