# Run180 文献准入卡：mode-0 lifted cell 的逐法向 oracle

| 最近邻 | 本轮实际阅读 | 已解决内容 | 与本轮严格差异 |
|---|---|---|---|
| Hempel--Kominek--Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011，DOI `10.1109/CDC.2011.6160901`，[全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **全文重读 §II、§III-A--C，Definitions 1--2、Theorem 1、式(3)--(14)与Algorithm 1** | 对每个 noisy output 的全部相容状态共用 output-dependent input；给定多面体的逐 facet/Farkas 验证及显式 PWA controller 已有直接结果。 | 当前 edge 是 packet-mode joint `(eta,e)` dynamics，且 residual bound 由所选 actual thrust 决定；本文的过程扰动集固定、scheduling 外生可见。 |
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026) 112661 | 复核既有全文笔记中 §4.2、§4.4、§6.1--6.7 | information ensemble、固定配置多面体与 extreme-information-set control 已给出一般框架。 | 不直接提供当前 15-mode nonlinear residual graph 的数值 cell。 |
| Hu et al., *Real-Time Tube MPC Applied to a 10-State Quadrotor Model*, ACC 2018 | 复核 Run168--170 对 Theorem 1、式(8)、Lemma 1 的全文记录 | tube-dependent nonlinearity bounder 必须覆盖 tube 内全部状态/扰动。 | 本轮只使用仓库已认证的竖直 actual-thrust residual graph，未复现 10-state RFIT。 |

## 准入判断

**作为最小实现门槛通过；作为创新命题不通过。** Hempel 已经覆盖 noisy-output fiber 共用输入和
逐多面体法向验证，Houska 已覆盖固定复杂度 information-set 表示。可实施的新增工作仅是把这些
义务可靠实例化到本项目的 packet edge、联合坐标和 control-dependent residual graph。

最强同条件基线是 Hempel 的 fiber-robust polyhedral condition，外加 Hu 式 tube-dependent
nonlinearity bounder。本轮只应回答“一个冻结 cell 的 oracle 是否能闭合”，不能声称新算法。
若输入越界、source domain 失效、任一 target normal 超界，或需要按隐藏 `eta`/未来 packet
结果选输入，则候选立即被推翻。通过后也必须继续到 mode 4 的 success/miss 未知分叉，才会
检验真正的共享输入难点。
