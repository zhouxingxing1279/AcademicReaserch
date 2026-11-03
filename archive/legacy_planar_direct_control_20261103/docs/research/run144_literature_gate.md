# Run 144 文献准入卡：竖直联合信息集的一步因果 predecessor

日期：2026-10-02。仓库起点为 Run 143 本地提交 `bb48593`；远端
`research/run143-joint-information-semantics=3fcaeab`，两者 tree 均为
`3893f404fc78ba81993bb37c9c4ed9dd2b14348c`；远端 `main=1c49659`。

## 本轮问题

在竖直坐标
`s=(eta_pz,eta_vz,e_pz,e_vz)` 中定义不人为限制 `d=e-eta` 的最小约束导出候选，
并按可见 `d` 固定 observation fiber。先判断 forced `14->0` success 与 mode 4/9
success/miss 分叉是否各有非空、因果的一步 predecessor。只有这三处通过，后续才允许做
15 模态固定点迭代。

## 最近邻原始文献

| 工作 | 本轮实际阅读 | 已解决内容 | 与本轮边界 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, arXiv:2307.04146, 2023，[全文](https://arxiv.org/pdf/2307.04146) | **全文定向精读 Sections 4.4、6.1--6.7，Definition 4、Lemma 2、Theorem 3、Problems (24)、(27)、(29)** | 把未来可能的信息集表示成 information ensemble；configuration-constrained polytope 与 extreme vertex polytope 给出有限维凸近似，每个 extreme information set 共享一个控制，(29) 可计算不变 polytopic information ensemble。 | “联合信息集”“极端纤维控制”及其有限维多面体近似都已有一般方法，不能作为本项目创新。本轮只核查带 packet graph、observer split、actual-thrust 相关共享余项的一个精确实例；不实现该文的完整 meta-information 优化。 |
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901`，[全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **重读 Sections III-A--C、Definition 2、Theorem 1、式 (3)--(10)** | 给定 noisy output 后，对全部相容隐藏状态及扰动使用同一输入，并用 Farkas 条件验证给定 OFCI 多面体。 | 本轮 predecessor 的正确量词直接来自该框架；差异仅在 15 模态未知后继分叉和同一 actual thrust 同时决定控制平移及余项宽度。 |
| Kumar, Kothyari, *Set-Theoretic Output Feedback Tracking Control via Linear Programming*, MTNS 2026，[作者公开全文](https://www.researchgate.net/publication/407040373_Set-Theoretic_Output_Feedback_Tracking_Control_via_Linear_Programming) | **全文定向精读 Sections 2.3--3、Definition 4、Theorem 5、式 (14)--(29)** | 对 `y=Cx`、静态 `u=Ky+Lr` 和加性过程扰动，用 zonotope containment 线性条件联合求反馈增益与状态 RCI。 | 该文没有测量噪声、丢包、observer 信息状态或控制相关扰动；其 state-fiber OFCI 定义是近邻，但不能替代本轮 `d=e-eta` 信息纤维。其 2026 zonotope-LP 结果也排除了“zonotope + LP”本身的首次性。 |

## 严格差异、候选与证明义务

本轮不提出新的 output-feedback invariance 算法。只实例化 Run 143 已冻结的合同：

1. 令 `E_j` 为 Run 136 六维估计误差 zonotope 的竖直精确投影，令
   `B_e={|e_pz|<=1, |e_vz|<=11/4}` 为真实状态域与 nominal hover box 的精确差集。
   采用无额外模板参数的候选
   `S_j={ (eta,e) | eta in E_j, e in B_e }`。它不独立约束 `d=e-eta`。
2. 对固定可见 `d`，真实 fiber 为
   `Q_j(d)={eta | eta in E_j, eta+d in B_e}`。一个 correction 必须同时服务
   `Q_j(d)` 中全部隐藏 `eta`、同一 mode 的全部未知后继边，以及共享 physical/noise
   primitives。
3. 一步 predecessor 量词为
   `Pre_j(S)={s in S_j | exists deltaT=kappa_j(d), forall eta_tilde in Q_j(d),
   forall outgoing edges and primitives, s+ in S_target}`。本轮只接受一个具有正体积的
   fiber 区域及同一可执行输入作为非空证书；单个采样点或允许输入读取 `eta` 不算。
4. residual 半宽必须按同一实际推力
   `T=barT+deltaT` 计算；不得把 `eta+` 与 `e+` 的 residual 分裂采样。状态约束施加在
   `e`，Run 136 投影约束施加在 `eta`。

最强同条件基线是 Houska 的 polytopic information ensemble；本轮的零输入内证书只是其
非常受限的可复核特例。Hempel/Kumar 的单一 plant-state polytope 不保留当前 observer split。

## 作用、推翻条件与准入判断

若三类关键 predecessor 连正体积 observation-fiber 区域都为空，则当前冻结输入预算或候选
必须在启动 15 模态固定点前修正。若非空，只能排除“第一步已死”的阻塞，不能推出 RCI、
terminal set 或 MPC 递归可行性。

下列任一结果会推翻拟用证书：fiber 不是由 `d=e-eta` 精确定义；mode 4/9 为不同后继选择
不同输入；actual thrust 的余项宽度未联动；Run 136 目标投影不包含估计误差后继；或
所谓非空集合只有零维见证。

**准入通过：只实现精确有理数的一步非空内证书及负对照，不进行固定点迭代，不作算法
创新、完整 RCI 或降低保守性声明。**
