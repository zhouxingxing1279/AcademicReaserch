# Run 141 文献准入卡：竖直 observation-fiber 因果性差距

日期：2026-10-02。仓库起点为 Run 140 修正提交 `9dad151`；远端 `main` 为
`1c49659`。本轮只判断允许读取隐藏估计误差的 full-state vertex control 能否替代真实
observation-fiber control 作可实施性证书。

## 1. 本轮问题与最近邻

| 文献 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901`, [全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **全文重读 Section III-A--C，Definition 2、Theorem 1、式 (3)--(12)** | 对每个 noisy output 与已知 scheduling 只选一个输入，并对与该输出一致的全部状态和扰动保证不变；最坏状态支持是 output 的 PWA 函数，控制可在线或显式求解。 | full-state vertex control 只能作乐观上界；真实控制必须先对 observation fiber 取交。其 scheduling 外生可测，仍不能直接覆盖本项目的控制相关推力。 |
| Lucia, Ernesto, Castelan, *Set-theoretic output feedback control: a bilinear programming approach*, Automatica 2023, DOI `10.1016/j.automatica.2023.110861`, [作者预印本](https://users.encs.concordia.ca/~wlucia/files/STOutput2023.pdf) | **全文精读 Sections 2--5，Definitions 2--3、Propositions 1--2、Algorithm 1、式 (7)--(31)** | 用静态输出反馈增益和嵌套 robust one-step controllable sets 保证约束、递归可行性与有限步 UUB；满状态带噪情形可按当前测量选择更小集合，而 rank-deficient output 情形必须使用不依赖隐藏状态的保守切换。 | 输出反馈与 noisy/full-state 的不同信息权限已有明确近邻；本轮只能提供当前四旋翼合同的实例化差距，不能声称一般理论创新。 |
| Baras, Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, IEEE TAC 43(1), 1998, [作者全文](https://terpconnect.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf) | **沿用 Run 140 对 Section IV-A--B、Lemma 4、Theorems 9--11、15--16 的全文精读；本轮定向重读信息状态量词** | observation history 诱导的信息状态是一般 output-feedback robust game 的充分统计量。 | 当前只用 `(mode,d,z,bar u)` 的 policy 是有限保守类；单个纤维反例不能否定一般 history-dependent controller。 |
| Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for LPV Systems*, 2023, [arXiv:2309.06998](https://arxiv.org/abs/2309.06998) | **沿用 Run 139 对 Section III-C、Lemma 3、Problem 1、Section IV 的全文精读** | full-state RCI 使用 `forall state exists control forall disturbance`，vertex controls 可凸插值。 | 这是本轮非因果上界；若 vertex control 读取隐藏 `eta`，它不能升级为输出反馈证书。 |

检索覆盖 output-feedback controlled invariance、set-theoretic output feedback、imperfect
state information 与 robust RCI。至少两篇最近邻全文已核查正文、量词、证明与算法；不以
摘要判断首次性。

## 2. 严格差异与待验证命题

冻结 Run 140 竖直 success edge。令 `h=1/50`、位置校正增益 `L=9/2`，当前可见
`d=(0,0)`，隐藏 Run 136 mode-4 estimation-error zonotope 给出

```math
q=\eta_{p_z}+h\eta_{v_z}\in[-q_4,q_4],\qquad
q_4=1004143/7200000.
```

下一位置测量噪声为 `n in [-1/50,1/50]`。同一控制必须在 mode 4 的未知 miss/success
分叉前选定。竖直中心误差满足

```math
d_{v_z}^{+}=d_{v_z}+h\delta T\quad(\text{miss}),\qquad
d_{v_z}^{+}=d_{v_z}+h\delta T+L(q+n)\quad(\text{success}).
```

本轮只验证下面的严格 predecessor-slice 分离：在 success target
`|d_p^+|<=q_4+1/50, |d_v^+|<=13/20`、miss target
`d_p^+=0, |d_v^+|<=7/100` 及 correction bound `|delta T|<=3.57589375` 下，
允许读取 `q` 的 full-state policy 对整个 mode-4 fiber 可行，但任何只观察相同 `d=0`
的单一 causal control 都不可行。整个 mode-4 zonotope 的逐坐标支持还必须严格落在
hover 真值源域内，不能只检查达到 `q` 支持的两个见证点。

这不是 RCI 存在性命题。它只是一个必要的 solver negative control：后续 causal RCI
程序若接受该 fiber，量词或变量共享必然错误。

## 3. 推翻条件、比较基线与课题作用

若 `q_4` 不是 Run 136 mode-4 zonotope 在方向 `(eta_p+h eta_v)` 的精确支持；若所需
full-state correction 越过实际 correction box；若 miss 与 success 使用了不同当前控制；
或若固定 causal control 的不可能区间不严格分离，则候选失败。

最强比较基线是 Hempel 式 observation-fiber input intersection；full-state vertex RCI 仅是
乐观上界。该证书推进的是求解器语义和回归门槛，不直接改善控制性能、可行域或复杂度，
也不单独构成硕士课题贡献。

## 4. 准入结论

**通过实际参数绑定的精确因果性负对照；不通过 RCI 综合、一般不可行结论或创新声明。**

允许新增 exact-rational verifier、TDD 回归、理论说明和结果 artifact。verifier 必须显式
核查 miss 两个顶点、success 四个 `(q,n)` 顶点、correction/actual-input 盒和整个 source
fiber 的逐坐标支持。完成后下一轮仍须
求解非轴对齐 vertical causal RCI；不能把一条 fiber 的严格差距替代完整集合闭合。
