# Run 143 文献准入卡：联合信息集的坐标与 mode-14 门槛

日期：2026-10-02。仓库起点为 Run 142 本地提交 `799d730`；远端
`research/run142-vertical-causal-predecessor=be558f8`，两者 tree 均为
`d0056a3ed6627d69a0a5c29c8f8fd9687ec04679`；远端 `main=1c49659`。

## 本轮问题

Run 142 建议在竖直四维
`(eta_pz,eta_vz,d_pz,d_vz)` 上构造联合信息集，并先要求 mode 14 的条件纤维
`q=eta_pz+h eta_vz` 支持不超过 `57902137/162000000`。本轮先审计这个门槛是否仍是
**联合**信息集的必要条件；若门槛只来自 product target，则不得据此否定联合候选。

## 最近邻原始文献

| 工作 | 本轮实际阅读 | 已解决内容 | 与本轮边界 |
|---|---|---|---|
| Baras, Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, IEEE TAC 43(1), 1998, DOI `10.1109/9.654887`，[作者全文](https://user.eng.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf) | **全文定向精读 Section IV-A，尤其 Information State Formulation、Lemma 4、Remarks 8--10、Theorems 9--11** | 与观测和控制历史相容的可行状态信息通过递归 information state 演化；输出反馈问题等价为以该信息状态为全信息状态的动态博弈。 | 保持隐藏状态之间及其与可见量的相关性是已有一般理论。本轮不能把“使用 joint information set”或“历史相关集合”作为创新。 |
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901`，[公开全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **全文重读 Section III-A--C，Definition 2、Theorem 1、式 (3)--(10)** | 给定测量 `y` 后，对所有与之相容的隐藏状态使用同一输入；用鲁棒化支持和 Farkas 条件验证给定 OFCI 多面体并计算输入。 | 支持按 observation fiber 计算已有。其候选是 plant-state polytope，调度外生可测；不直接给出当前 packet graph、shared primitive 或 `eta+d` 坐标合同。 |
| Kjellqvist, *Minimax Dual Control with Finite-Dimensional Information State*, L4DC/PMLR 242, 2024，[全文](https://proceedings.mlr.press/v242/kjellqvist24a/kjellqvist24a.pdf) | **全文定向精读 Sections 2.1--2.2、Assumption 2、Proposition 4 与式 (11)--(18)** | 当每个测量逆像最多含有限个元素时，把 worst-case history 压成有限维递归 information state。 | 当前带界连续测量噪声的 observation fiber 含连续无穷多个状态，不满足 Assumption 2；不能据此宣称本项目已有有限维精确递归。它反而说明有限维压缩需要额外结构证明。 |

Artstein--Rakovic 2011 的出版页面与仓库既有全文阅读记录继续作为 set-dynamics 近邻，但本轮
未重新取得其正文，不引用新定理编号。

## 严格差异与证明义务

本轮不提出新的 information-state 算法。唯一可准入的问题是当前项目合同的实例化语义：

1. 沿初始化后的 14 条强制 miss 边，`d` 的竖直更新是否与隐藏 `eta` 和 residual 无关；若是，
   同一 observation fiber 必须包含完整 Run 136 mode-14 `eta` image，故条件 `q` 支持不能缩小。
2. forced success 后，测量项 `L(q+n)` 是否在 `eta_v^+ + d_v^+` 中精确抵消；若是，
   Run 142 从 product target 的独立 `d_v` 半宽导出的 `0.35742` 门槛不是 joint target 的必要条件。
3. 正确的 joint source constraint 应作用于 `e=eta+d=x-z`，同时保留 `eta` 投影和可见
   `d=e-eta` 的 policy 量词。任何四维求解器必须显式使用这三个接口，不能分别限幅 `eta,d`。

最强同条件基线是一般递归 information state；可实现的有限基线是 Hempel 型 observation-fiber
鲁棒化。二者都不提供本配置的自动联合集合综合。

## 对课题主线的作用与推翻条件

若上述两条代数事实成立，本轮会纠正一个会误杀联合候选的门槛，并把后续综合坐标改为
`(eta_pz,eta_vz,e_pz,e_vz)`。这直接影响控制可行性判断，而不是局部数值改善。

下列任一情况会推翻本轮方向：miss 更新中的 `d` 实际依赖 hidden `eta`/residual；success 中
`q+n` 未在 `e^+` 精确抵消；配置对 `d` 本身另有硬约束；或 Run 136 mode-14 image 不是
初始化切片沿 14 条 miss 边的精确 reachable image。

## 准入判断

**通过“语义纠正 + 精确反例”准入；不通过四维 RCI 求解、算法创新或一般可行性声明。**
先以精确有理数验证上述必要事实。只有确认 Run 142 门槛不适用于 joint target 后，才把下一轮
问题改写为在 `(eta,e)` 坐标中构造保持 observation fiber 的候选并检查 shared-input invariance。
