# Run 128 文献准入卡：有限 mRPI 的 AH/CZ 包含证书是否可作在线准入

日期：2026-09-29。远端 `main` 为 1c49659c；远端最新研究分支为 `research/run126-scott-cz-baseline` c00d102；本轮从尚未推送的 Run 127 提交 df98eee（tree 9c7ceb3）继续。研究对象仍是冻结四状态合同，不外推到完整六自由度四旋翼。

## 最近邻与本轮实际阅读

| 文献 | 阅读层级与本轮定位 | 已解决内容及本轮约束 |
|---|---|---|
| Sadraddini, Tedrake, *Linear Encodings for Polytope Containment Problems*, CDC 2019，[DOI](https://doi.org/10.1109/CDC40024.2019.9029363)，[作者全文](https://groups.csail.mit.edu/robotics-center/public_papers/Sadraddini19.pdf) | **全文定向重读** Section III Theorem 1 与 (11)--(17)（pp. 3--4），Theorem 2；Section IV-A Theorem 3 与反例（pp. 5--6），Table I。 | Theorem 1 给 AH-in-AH 的线性充分证书；其 primitive inbody 假设为满维。Theorem 3 给 zonotope-in-zonotope 的仿射生成元映射充分证书。两者可行都能证明包含，但一般不是必要条件；论文给出真包含而 zonotope 证书失败的三维反例。故 LP 不可行不能作为 539--604 不包含的证据。 |
| Hellwig, Schäfer, Qian, Platzer, Althoff, *From Zonotopes to Proof Certificates: A Formal Pipeline for Safe Control Envelopes*, iFM 2025 / LNCS 16194 (2026)，[DOI](https://doi.org/10.1007/978-3-032-10794-7_13) | **全文定向精读** pp. 10--11 的 containment witness、残差裕量与 Theorem 3.5。 | 浮点 LP witness 不能直接当形式证明；可通过精确有理数 witness，或把等式残差与右逆范数纳入收缩裕量后再可靠复核。该工作强化了“必须归档并独立检查 witness”的要求，但没有消除本轮高维证书的变量规模。 |
| Kulmburg, Schäfer, Althoff, *Approximability of the Containment Problem for Zonotopes and Ellipsotopes*, IEEE TAC 70(12), 2025, 8104--8119，[DOI](https://doi.org/10.1109/TAC.2025.3583624) | 本轮核对期刊元数据、摘要和 arXiv 记录；**正文下载失败，未作全文结论**。 | 摘要表明其研究 Sadraddini--Tedrake 等包含松弛的近似质量；本轮不据摘要声称得到新的无损或低复杂度 CZ 包含判据。 |
| Froese et al., *Parameterized Hardness of Zonotope Containment and Neural Network Verification*, 2025 preprint，[全文](https://arxiv.org/pdf/2509.22849) | **全文定向阅读** Section 3.1、Theorem 3.1，以及复杂度结论。 | 固定物理维数下，纯 zonotope containment 可通过枚举 `O(n^(d-1))` 顶点判定；一般问题具有困难性。该结果不是 constrained-zonotope-in-zonotope 算法，只用于排除“任意高生成元包含必有便宜完整 LP”的预期。 |

Scott 2016 的 lift-then-reduce 外包性质、Köhler 等 2021 的 terminal/shift 证明义务和 Run 127 的严格分离证书继续作为已核查前提。本轮没有取得 Robbins 等 ACC 2026 在线收紧论文正文，不以其摘要作首次性判断。

## 问题、正确参数化与最强基线

令 Scott 链上的压缩 CZ 为

\[
R_m=\{G_m\xi:\|\xi\|_\infty\le 1,\ A_m\xi=b_m\},
\qquad m\in\{539,\ldots,605\}.
\]

有限 mRPI 内近似取

\[
S_{602}=Y[-1,1]^{602},\qquad
Y=[D_0G,FD_0G,\ldots,F^{601}D_0G]\subset S.
\]

未压缩的 605-generator 表示是 602 个扰动变量加 3 个测量噪声变量的精确 strip-as-CZ；其状态投影就是 `S_602` 与三条测量带的交，因此 `R_605 subseteq S_602` 由构造直接成立，是最强同条件基线。

不能把 CZ 的 primitive set `|xi|<=1, A xi=b` 直接代入 Theorem 1，因为它在 `R^m` 中不满维。正确用法是取 `xi=xi0+Nz`，其中 `N` 张成 `ker(A)`，再以

\[
P_x=\{z:Nz\le 1-\xi_0,\ -Nz\le 1+\xi_0\}
\]

作为满维 primitive，并令物理 AH 映射为 `G xi0 + GN z`。只要 equality slice 有相对内点，这一参数化满足论文假设。

也可不显式消元：寻找 `Gamma,beta,Q` 使

\[
G_m=Y\Gamma+QA_m,\qquad Y\beta=Qb_m,
\]

并逐行用 box-with-equalities 支持 LP 的正、负对偶约束认证 `|Gamma xi+beta|<=1`。这给出可靠的充分证书，但仍须求解与 Theorem 1 同阶的大 LP。

## 当前实例的证书规模

这里 `dim(x)=4`、等式数 `p=3`、目标生成元数 `M=602`。下表只计主要连续变量和线性约束；它不是求解时间的实测替代。

| 证书 | `m=539` | `m=605` | 结论 |
|---|---:|---:|---|
| Theorem 1，经 nullspace 参数化：变量 | 1,621,186 | 1,819,846 | 其中非负 `Lambda` 分别占 1,297,912 / 1,456,840 个变量 |
| Theorem 1：等式 + 主不等式 | 647,492 + 1,204 | 727,220 + 1,204 | 每个在线 CZ 都需重新生成/求解并复核 witness |
| 原坐标 CZ 对偶证书：变量 | 1,626,616 | 1,825,276 | 避免 nullspace，但没有改变数量级 |
| 忽略 CZ 等式的 Theorem 3 zonotope 外壳：变量 | 648,956 | 728,420 | 更小但更保守；不可行仍不否定真实 CZ 包含 |

Run 126 的整个 67 候选、300 方向阶段审计约为秒级基线；在没有实测求解前，不能声称上述百万变量 LP 的具体耗时，但其变量/约束规模已经与“每步在线 fixed-budget admission”目标不相容。压缩 CZ 随测量和降阶在线变化，不能把一个冻结 witness 离线复用到后续时刻。

## 严格差异、价值、反例与准入结论

本轮没有提出新包含算法。它核查的是 Run 127 指定的“用通用 AH/CZ 证书扫描 539--605”能否成为**可实现的在线控制接口**。结论分三层：

1. `m=605` 已由集合构造证明包含，无需 LP；
2. 对 `m<605`，通用证书可行可给充分证明，但证书不可行不能区分“真实不包含”和“编码保守”；
3. 百万变量级证书即使能离线解出，也不能在当前同预算比较中作为在线压缩准入规则。

推翻这一方向纠正需要：给出利用 Scott 消去结构、可随压缩增量更新的稀疏 witness，使每步认证复杂度与保留生成元近线性或可实测进入既定预算；单次离线大 LP 成功不足以推翻。

**准入判断：不通过“通用 AH/CZ 大 LP 扫描”实现门槛；通过方向纠正与复杂度审计；不作创新声明。** 本轮不实现巨型 LP，也不把 604 等候选的证书不可行冒充反例。下一步应研究“certificate-carrying reduction”：压缩时同时维护到 `S_602` 的稀疏系数映射及行预算，只允许能由结构化 witness 直接认证的消去；若任何非平凡消去都会破坏预算，再以可核查的结构反例关闭普通 Scott 路线。
