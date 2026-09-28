# Run 125 文献准入卡：非零重定心后的终端 mRPI 包含

日期：2026-09-28。仓库基线：`main` 1c49659c；研究基线：`research/run124-recenter-compression` c2f6188。

## 本轮实际阅读与最近邻

| 文献 | 阅读层级与本轮定位 | 已解决内容及对本轮的约束 |
|---|---|---|
| Sadraddini, Tedrake, *Linear Encodings for Polytope Containment Problems*, 2019, [arXiv:1903.05214](https://arxiv.org/abs/1903.05214) | **全文定向精读** Section III Theorems 1–2（pp. 3–5）、Section IV-A Theorem 3 与反例（pp. 5–6）、Table I。 | Theorem 1 已给出 AH-polytope-in-AH-polytope 的线性充分证书；CZ 可视为 AH-polytope。zonotope-in-zonotope 的仿射系数映射也是充分而非一般必要条件，论文给出真包含但证书不可行的三维反例。因此本轮可用它证明包含，却不能由 LP 不可行推出不包含。一般 AH-in-AH 包含的判定复杂度也排除了“任意高维表示都有便宜无损证书”的假设。 |
| Kouramas, Raković, Kerrigan, Allwright, Mayne, *On the Minimal Robust Positively Invariant Set for Linear Difference Inclusions*, CDC-ECC 2005, [公开全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc05/pdffiles/papers/1964.pdf) | **全文定向精读** Sections II–V（pp. 1–4），尤其 Assumption 1、Theorems 2–4 和 (16)–(25)。 | 给出有限 Minkowski 和的缩放外 RPI 近似及任意精度外逼近。但 Assumption 1 要求扰动集是含原点内点的 C-set，且核心条件为后继层 `R_s subseteq alpha W`。本仓库 `W=D0 G[-1,1]` 在四维中秩一、没有内点，通常 `F^sW` 也不与 `W` 共线；故不能直接套该定理替换 Run-121 的精确无限和。外近似即使可构造，也不能证明候选位于原 mRPI 内。 |
| Dey, Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026, [arXiv:2605.23661](https://arxiv.org/abs/2605.23661) | 继承 Run 123 对 Section IV、Algorithm 1、Theorem 2、Appendix IV 的全文核查；本轮只复用其终端/备份集合证明义务。 | 在线估计集和 tube 更新下的旧解移位、终端兼容与递归可行性已有一般框架；本轮只审计冻结四状态实例的终端集合接口，不提出新 adaptive-tube 结构。 |
| Scott, Raimondo, Marseglia, Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, 2016, [DOI](https://doi.org/10.1016/j.automatica.2016.02.036) | 继承 Run 124 对 Sections 3.1、4、5 的全文精读；本轮不重复通读。 | CZ 表示、测量求交和安全外包降阶均已有。这里的新增义务不是集合运算，而是重定心后终端误差集对固定 mRPI 的方向正确的内包含。 |

Robbins 等 ACC 2026 的在线 CZ 收紧全文仍未取得，本轮不据摘要对其作排除性判断；它不改变当前终端包含的基本证明方向。

## 本轮问题、严格差异与最强基线

Run 124 候选的终端误差集为

\[
E_N(d_0)=F^N(C-d_0)\oplus\bigoplus_{j=0}^{N-1}F^jW,
\qquad
S=\bigoplus_{j=0}^{\infty}F^jW.
\]

自由 nominal 修正输入只改变 nominal 轨迹，不改变该误差集合。由于 `F` 可逆，`E_N(d0) subseteq S` 与 `C-d0 subseteq S` 在支持函数反例搜索上等价：若存在方向 `r` 使

\[
h_C(r)-r^Td_0>h_S(r),
\]

则取 `q=F^{-NT}r` 即得到终端集合的严格分离方向。最强同条件基线是 Run 123 的 `d0=0`：完整有限冲激前缀 posterior 是 `S` 的子集，终端包含由构造直接继承。

Sadraddini–Tedrake 证书可把 `E_N(d0)` 放入任一有限内近似 `R_M=oplus_{j=0}^{M-1}F^jW subset S`；可行即为可靠充分证明。但证书不可行只能标作“不完备/未证”，不是反例。Raković 等的外 RPI 近似方向相反，且本合同不满足其满维扰动假设，不能用来补洞。

## 对课题链条的价值与推翻条件

该问题直接决定 Run 124 的非零重定心能否进入“终端—移位—递归可行性”链条，而非再增加局部方向。候选只在以下两种结果之一时结束：

1. 给出可执行的充分包含证书，并明确数值求解与可靠认证的分界；或
2. 找到方向 `r`、posterior 可行 witness 及精确有理数上下界，使上式严格为正，从而否定实际 Run-124 非零候选。

有限采样、若干控制方向通过、AH 充分 LP 不可行或把候选放入 mRPI 外近似，均不能宣称完成。

## 准入结论

**通过“实际候选的包含/分离审计”，不通过新算法或创新声明。** 允许实现最小验证器：先数值搜索分离方向，再以 posterior 原始可行点给出支持下界，并用 Run-120 的精确有理数 block-tail 给出 `h_S` 上界。若得到严格间隔，它是当前候选的反例而不是一般重定心理定理；若搜不到，只记录未决，并转向 Sadraddini–Tedrake 的有限内近似充分证书。
