# Run 127 文献准入卡：539-generator Scott CZ 的终端 mRPI 审计

日期：2026-09-29。仓库基线：`main` 1c49659c；研究基线：`research/run126-scott-cz-baseline` c00d102（tree a215b46）。

## 最近邻与本轮实际阅读

| 文献 | 阅读层级与本轮定位 | 已解决内容及对本轮的约束 |
|---|---|---|
| Köhler, Müller, Allgöwer, *Robust output feedback model predictive control using online estimation bounds*, 2021，[作者全文](https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf) | **全文定向精读** pp. 5--6 的 Theorem 2 与 (15)--(17)，pp. 9--10 的 Assumption 7、Theorem 4 及递归可行性证明。 | 集合成员估计给出真值包含和有效误差界；递归可行性证明显式依赖 terminal ingredients，移位序列的最后一步由 Assumption 7 封闭。阶段约束通过不能替代终端集合条件。 |
| Mayne, Seron, Raković, *Robust model predictive control of constrained linear systems with bounded disturbances*, Automatica 41 (2005) 219--224，[DOI](https://doi.org/10.1016/j.automatica.2004.08.019) | 本轮核对书目信息、摘要及 Raković 公开讲义中 rigid-tube 局部动力学与 RPI 条件；**未取得原论文全文**。 | 固定反馈下误差集合须满足 `(A+BK)S \oplus W \subseteq S`。本轮只使用仓库已经独立构造并由有理数尾界核查的固定 mRPI，不从摘要补造定理细节。 |
| Dey, Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026，[arXiv:2605.23661](https://arxiv.org/abs/2605.23661) | 本轮核对引言、贡献和 terminal-set 更新定位；沿用 Run 123 对 Section IV、Algorithm 1、Theorem 2、Appendix IV 的全文记录，不宣称本轮重复通读。 | 在线估计界、tube 更新、备份计划与终端更新已有一般框架。这里不是新 adaptive-tube 方法，而是冻结实现是否满足其同类 terminal/shift 证明义务的审计。 |
| Scott, Raimondo, Marseglia, Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, 2016，[DOI](https://doi.org/10.1016/j.automatica.2016.02.036)，[作者全文](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) | 沿用 Run 126 对 Sections 3.1、4.1--4.3、Appendix Algorithm 1 与 (A.9)--(A.10) 的全文重读和可执行复现。 | lift-then-reduce 保证外包原 CZ，但不保证约减结果位于另一个指定 mRPI 内；终端包含必须单独认证。 |

Robbins 等 ACC 2026 的正文仍未取得，不据摘要作排除性判断。本轮不提出算法或首次性主张，故 Köhler 的全文足以开启“既有实现的证明义务审计”。

## 本轮问题、严格关系与最强基线

令 `R` 为 Run 126 的 539-generator Scott CZ，`W=D0 G[-1,1]`，

\[
S=\bigoplus_{i=0}^{\infty}F^iW,\qquad
E_N(R)=F^N R\oplus\bigoplus_{i=0}^{N-1}F^iW.
\]

固定 mRPI 满足

\[
h_S(q)=h_S(F^{N\mathsf T}q)+
\sum_{i=0}^{N-1}h_W(F^{i\mathsf T}q).
\]

因此 `R subseteq S` 足以推出 `E_N(R) subseteq S`；在本仓库 `F` 可逆时，两者实际等价，因为 `r=F^{N\mathsf T}q` 遍历所有方向。若找到方向 `r` 使 `h_R(r)>h_S(r)`，则 `q=F^{-N\mathsf T}r` 是终端集合的分离方向，且支持差相同。

最强同条件基线是未约减的 605-generator 精确 strip-as-CZ：其状态投影就是 Run 123 posterior，是 mRPI 有限冲激前缀的子集。Scott 外包只给 `C subseteq R`，不能传递 `R subseteq S`。

## 价值、证据标准与推翻条件

该审计直接决定“539 个生成元通过 300 个阶段查询”能否进入终端—移位—递归可行性链条。证据分级如下：

1. 任一方向的可靠正支持差即可**反例否定**包含；若计算基于浮点 CZ，则必须报告稳定裕量、求解残差和精度局限，不能冒充精确有理数证明。
2. 有限方向均通过只能是**数值观察**；证明包含需要完整的集合包含证书或等价的全方向证书。
3. 若 539-CZ 不包含于 `S`，则否定当前完整准入，下一步只允许把终端支持预算并入压缩规则；若无分离方向，也不能据此宣称递归可行。

## 准入判断

**通过既有 539-CZ 的终端包含/分离审计；不通过新算法或创新声明。** 允许实现最小复现器：搜索 `h_R-h_S` 的分离方向，用长有限和及 Run-120 的有理数 block-tail 上界交叉核查，并把终端方向映射残差写入结果。若没有严格、数值稳定的正间隔，则本轮只记录“未证”，不以采样通过代替数学证明。
