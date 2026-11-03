# Run190 文献准入卡：测量条件化 extreme-set family

日期：2026-10-27。远端基线为 Run189 `c24ae0a8`（tree `0a94d51b`）；远端 `main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026), 112661；arXiv:2307.04146 | **重读 §3.1--3.2、§6.1--6.5、Definition 7、式(56)--(57)及 Theorem 3 证明接口** | information ensemble 对任意紧集求交向下闭合；真正 extreme sets 是包含极大成员。§6.4 另定义有限的 extreme vertex polytopes，参数顶点可代表外部凸信息，但不必穷尽真正 extreme boundary。 | 必须明确区分“连续多个真正 extreme sets”和“两个人工参数顶点”；不得把端点数写成真实边界基数。 |
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, Automatica 163 (2024), 111543；arXiv:2208.12554 | **重读 §3.4--3.5、Lemma 1、Definition 7、Theorem 2 的 scalar/vertex-map证明** | 固定法向参数域为多面锥，配置域可退化到边界；固定配置时 facet offsets 与 vertex maps 线性关联。 | 六方向 offset segment 必须逐点落在 configuration cone；若斜 facets 退化，不得声称得到 regular six-facet `H/Omega`。 |
| Artstein--Rakovic, *Set invariance under output feedback: a set-dynamics approach*, IJSS 42 (2011), 539--555 | **仅核对作者公开摘要；正文未取得** | 以信息集集合的 set dynamics 讨论输出反馈不变性。 | 只作为历史最近邻线索；不据摘要引用定理或首次性。 |
| Valero et al., *Set-Based State Estimation: A Polytopic Approach*, IFAC World Congress (2020) | **核对全文 Introduction、§1.1及问题表示** | 固定复杂度多面体外包与 measurement-consistent state set 优化已有直接基线。 | “多面体与测量条带求交”不是创新；本轮只审计项目合同中的 exact local family。 |

## 严格差异、强基线与证伪条件

本轮不是新算法，而是 Run183 物理盒、Run187 measurement semantics 与 Run186 六方向模板的一次精确局部实例化。最强同条件基线是 Houska 的 polytopic information ensemble；本轮必须遵守其 downward-closure 和 extreme-set 语义。

候选 family 由真实可辨识测量中心产生，不引入任意 caps。若任一非空实际 posterior 不属于 family、不同中心的 maximal sets 可相互包含、或 tight six-offset map 不是一条 configured affine segment，则候选被推翻。即使通过，若其保留完整 velocity width，则不能声称消除 Run184 动力学环或降低闭环保守性。

## 准入判断

**通过“单 source mode 的 exact measurement-generated extreme family”；不通过“有限两个真正 extreme sets”、完整 `H/Omega`、图不变性或控制创新。** 允许实现精确有理数 checker；本轮不进入 15-mode/17-edge LP。
