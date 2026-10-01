# Run 130 文献准入卡：终端 witness 约束的非-Scott 单步约减

日期：2026-09-29。仓库起点为本地 Run 129 提交 `1d5e9bc`；远端 `main` 为 `1c49659`，远端最新研究分支为 Run 126 `c00d102`。本轮问题只针对冻结四状态合同、Run 123 的 605-generator 精确后验 `R_605` 与 602-generator 固定终端 mRPI 前缀 `S_602`。

## 1. 候选问题与判退条件

候选是把

\[
R_{605}\subseteq R_{\mathrm{red}}\subseteq S_{602}
\]

同时作为非-Scott 约减的硬约束，直接搜索少于 605 个 generators 的 `R_red`。原计划把“至少删除一列”作为成功标准，并希望绕开 Run 129 中 Scott 首次放大破坏已知终端包含映射的问题。

准入前预设的判退条件是：若最近邻已经明确研究“以包含为硬约束优化 reduced generators”，当前差异只剩 CZ equality 和第二个固定目标包含；或若直接形式仍需巨型稠密映射；或删列可由丢弃全部测量信息的退化解完成，则不实现。

## 2. 本轮实际精读的最近邻

| 文献 | 本轮实际阅读范围 | 已解决内容 | 与本轮关系 |
|---|---|---|---|
| Sadraddini, Tedrake, *Linear Encodings for Polytope Containment Problems*, expanded arXiv:1903.05214 | 全文版本；重点 Section V-B、Proposition 6 和式 (30) | 直接把 reduced zonotope 的生成元矩阵作为决策变量，在 outer containment 下最小化 Hausdorff 上界；约束含 `X=X_red Gamma_0`、`X_red=X Gamma_1+Delta`、行范数界。双线性等式导致非凸，作者用 projected sequential LP/交替法并需要初始化。 | “包含 witness 作为 generator reduction 硬约束”已经被明确提出；不是本项目的新机制。 |
| Kopetzki, Schürmann, Althoff, *Methods for Order Reduction of Zonotopes*, CDC 2017 | 全文；重点 Section III-D constrained optimization | 直接优化 reduced generator matrix `C`，以 `sum_j |C^{-1}G|_{ij} <= 1` 保证原 zonotope 被包含，并以 determinant/volume 为目标；用 `fmincon` interior-point 求非线性问题。 | 再次表明 containment-constrained outer reduction 是强基线；本轮不能把“非-Scott + 硬包含”称作创新。 |
| Raghuraman, Koeln, *Set operations and order reductions for constrained zonotopes*, Automatica 2022 | 全文；重点 Section 5、zonotope/CZ inner-approximation reduction | 以 Sadraddini--Tedrake 的 containment encoding 约束优化；CZ 通过 nullspace/AH-polytope 表示构造 LP，可删一个 generator 和一个 constraint 后再缩放。 | 方向是内近似，不能替代可靠 SMF posterior 的 outer enclosure；但证明“CZ order reduction + containment encoding”本身也已有明确先例。 |

稳定链接：Sadraddini--Tedrake [arXiv](https://arxiv.org/abs/1903.05214)；Kopetzki 等 [作者全文](https://mediatum.ub.tum.de/doc/1442501/1442501.pdf)；Raghuraman--Koeln [DOI](https://doi.org/10.1016/j.automatica.2022.110204) / [arXiv](https://arxiv.org/abs/2009.06039)。三篇均阅读正文，不是只读摘要。

## 3. 严格差异、直接推论与最强基线

本轮候选相对上述文献的严格差异只有：源集是带三条 equality 的 CZ，而且 reduced outer set 还必须被固定 `S_602` 包含。后一个条件可继续用 Sadraddini--Tedrake 型生成元映射编码；前一个条件可用 Run 129 的 equality-adjusted affine map 或一般 AH/CZ 编码。因此它是两个已知包含模块的 sandwich 组合，不自动构成新算法或新定理。

最强同条件比较至少包括：

1. 不压缩的精确 `R_605`，保留全部三次 measurement intersection 信息；
2. 固定 `S_602` / 固定 tube 基线；
3. Run 129 的 605→604 deterministic Scott 首步及其失败的 carried-map 证书；
4. Sadraddini--Tedrake Proposition 6 / Kopetzki Section III-D 的 containment-constrained outer reduction。

## 4. 两个决定性的止损检查

### 4.1 “至少删一列”存在退化真解

因为精确 posterior 的构造已知满足 `R_605 subseteq S_602`，直接取

\[
R_{\mathrm{red}}=S_{602}
\]

便同时满足 sandwich，并从 605 generators、3 条 equality 变成 602 generators、0 条 equality。这确实删除了三列，却等价于丢弃三条测量带来的全部后验信息，退化为固定 tube/mRPI-prefix 基线。因此“至少删除一列”不是有控制意义的成功标准。

任何非平凡候选还必须在相同模型、信息、硬约束和在线预算下，相对 `S_602` 证明至少一个控制相关量的严格改善，例如全部实际 tightening normals 上不劣且至少一条严格更紧、可行域严格扩大或认证闭环代价严格降低。仅有几何体积或删列数量不足。

### 4.2 直接 map 参数化仍然过大

若用 `G_red=YB` 搜索 604-generator 候选，仅 `B` 就有

\[
602\times604=363{,}608
\]

个连续条目；从 605 个源 coefficients 到 604 个 reduced coefficients 的 outer-inclusion map 又有

\[
604\times605=365{,}420
\]

个条目。两者合计至少 `729,028`，尚未计入三条 equality 的调整变量、绝对值线性化、dual multipliers 或双线性迭代状态。这是直接 map 参数化的规模下界/数量级检查，不是完整 CZ 优化模型的精确变量数；但已经排除“便宜在线单步替换”的解释。

## 5. 对课题链条的作用与可推翻条件

若该路线成立，它本应补上“可靠 posterior outer enclosure → 固定预算 → 终端包含”的缺口。实际文献和退化检查表明：只证明 sandwich 可行或删除列，并不能证明在线 posterior 信息降低了控制保守性，也不能提供新的 recursive-feasibility 机制。

能推翻本轮止损结论的结果必须同时给出：结构化、亚稠密 map 规模的单步算法；保留可靠 outer containment；保证进入 terminal/backup set；并在 Run 123 的真实 stage/input/terminal normals 上相对 `S_602` 有严格、可认证的控制收益。当前没有这样的证据。

## 6. 准入结论

**创新/实现准入：不通过。方向纠正准入：通过。**

- 不实现新的 witness-constrained optimizer，也不以通用非凸/巨型 LP 扫描 604→539。
- 关闭当前 post-hoc generator reduction 支线；Run 127--130 已分别排除固定终端遗漏、通用大证书、携证 Scott 首步和“删列即成功”的准入标准。
- 下一步转向完整 terminal/tube 架构：在线 posterior 只在有限时域提供可验证的控制相关 tightening，同时由独立 backup/adaptive terminal tube 负责 shifted feasibility；但必须先精读 Dey--Bhasin、Köhler/Ping 等近邻，不能把两层结构本身预先声明为创新。
