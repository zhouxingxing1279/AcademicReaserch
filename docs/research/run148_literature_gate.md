# Run 148 文献准入卡：固定零修正下三种 success return 的统一相关模板

日期：2026-10-03。仓库起点为远端 Run 147 提交 `038cacc`；本轮只处理短检查点指定的
5/10/15 tick 初始化 return，不扩展到完整六状态或 MPC terminal 层。

## 本轮问题

当前合同从 `mode=0,d=e-eta=0` 初始化。第一次成功测量可能发生在第5、10或15 tick，
分别对应 `4->0`、`9->0`、`14->0`。Run 147 只认证最后一种固定零修正 return。本轮先
回答：当先行 miss 的修正推力全部固定为零时，三种 seed 是否全部满足竖直 estimator/真值
约束，以及是否存在一个单一的、最小凸 mode-0 模板容纳它们。非零 correction 会平移
可见 offset，因此这些 seed 不是任意 RCI 控制策略必须容纳的 policy-independent target。

## 最近邻原始文献与实际阅读

| 工作 | 本轮阅读层级 | 已解决内容 | 与本轮的严格边界 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, 2023, arXiv:2307.04146 | **重读全文 Sections 6.4--6.7、Definition 7、Theorem 3及证明、Remark 6** | 极端信息多面体的凸合包编码 extrinsic information；对每个极端信息集分配控制并以同一组连续凸权重恢复可行控制；给出 invariant polytopic information ensemble 的直接框架。 | `conv(J4 union J9 union J14)` 及其 lifted convex-combination 表示是该框架的直接实例，不是 one-hot 路径选择，也不是新算法。本轮不综合 extreme controls。 |
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901` | **重读全文 Sections III-A--C、Definition 2、Theorem 1、式(3)--(14)** | 同一 noisy output 相容的全部状态必须共享输入；给定 OFCI polytope 可用LP验证并构造分段仿射输出反馈。 | 三条 return path 是互斥 observation histories；每条路径内部不能拆分 hidden `eta`，但不同路径不共享同一次噪声 realization。本轮只构造 target，不验证 OFCI。 |
| Dey, Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026, arXiv:2605.23661 | **重读全文 Sections IV-A--F、Assumptions 2--4、Criterion 1、Theorem 2及Appendix IV** | 用 set-membership 更新参数/初值集合，以 estimation-error 外包做 tightening，以 homothetic tube 与 backup/compatibility 条件保证 recursive feasibility。 | 其输出式无测量噪声，且把 estimation-error bound 与 observer-state tube 通过外包/收紧组合；不处理 bounded-dropout graph 中 `(eta,e)` 的路径相关联合像。本轮不能据此声称 adaptive tube 首次性。 |
| Artstein, Rakovic, *Set Invariance Under Output Feedback: A Set-Dynamics Approach*, 2011 | **复核 Run143/147 的全文阅读记录与本轮相关定义** | 用信息集动力学定义 output-feedback invariance，说明单一状态集合不能替代信息集合族。 | 本轮三条 seed 只是固定零修正的有限路径样本；其凸包不是一般 information ensemble 的等价表示。 |

稳定全文链接与既有系统假设对照见 `docs/literature/READ_PAPERS.md`。本轮还检索了2025--2026
output-feedback/adaptive-tube工作；Dey--Bhasin 2026仍是与在线收紧和递归可行性最接近的
公开全文，但不覆盖本轮 packet-path correlation。检索不足以支持首次性声明。

## 差异、证明义务与推翻条件

对 `m in {4,9,14}`，必须从同一 Run136 `E_m` 生成完整
`J_m subset (eta_p,eta_v,e_p,e_v)`，而不是独立装箱。每个 seed 必须精确核查：

1. 在显式 `deltaT=0` miss 序列下到达完整 `E_m` 形状与零可见偏移，且图中存在 `m->0 success`；
2. residual 与 measurement-noise 在同一路径内共享，affine-hull 秩和线性关系不被破坏；
3. 完整 `eta` 投影位于 mode-0 estimator box，完整 `e` 投影位于真值硬约束；
4. 单一模板取最小凸容器 `C0 = conv(J4 union J9 union J14)`，用连续 selector 的
   perspective lift 保留每个路径块内部的生成元列耦合；允许跨路径分数混合，但不能把
   多个路径块同时以单位尺度激活；其支持应为三者支持的最大值，而不是生成元拼接后的和；
5. 若任一 seed 违反约束，停止 joint-RCI；若凸包违反约束，则不存在满足同一凸硬约束的
   convex mode-0 模板；若仅 naive generator concatenation 失败，只否定该外包表示。

最强基线是 Houska 的 polytopic information ensemble。最强 MPC 闭环基线是 Dey--Bhasin
2026，但其假设/信息结构不同。本轮结果只有在三种 exact seed 全部通过且 convex-hull
template 的完整支持通过时，才允许进入 causal controlled predecessor。

## 准入判断

**通过固定零修正 exact multi-return seed 与最小凸容器核查；不通过 policy-independent
必要性、新算法、RCI、六状态、terminal、移位或递归可行性声明。** 若统一模板只在低维
仿射子空间中成立或触及 estimator 边界，必须显式报告，不得通过随意加厚或浮点容差掩盖。
