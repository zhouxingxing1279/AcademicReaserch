# Run 125：非零重定心终端包含的精确分离反例

日期：2026-09-28。文献准入见 [run125_literature_gate.md](run125_literature_gate.md)。远端核查：`main` 1c49659c；最近有效研究基线 `research/run124-recenter-compression` c2f6188；本轮分支 `research/run125-terminal-containment`。

## 1. 本轮唯一问题

Run 124 在全部 300 条阶段收紧上找到非零重定心

\[
d_0=(0.0017170128554,\;0.0017170109266,\;0.0014648487415,\;0.0017170113556)^T,
\]

但只剩终端义务。令三次位置条带更新后的 602 潜变量 posterior 为 `C`，冻结闭环为 `F=A-BK`，扰动为 `W=D0 G[-1,1]`，则自由 nominal 修正输入不改变误差递推，终端误差集仍为

\[
E_N(d_0)=F^N(C-d_0)\oplus R_N,
\qquad
R_N=\bigoplus_{j=0}^{N-1}F^jW.
\]

固定 Run-121 终端集是

\[
S=\bigoplus_{j=0}^{\infty}F^jW=R_N\oplus F^NS.
\]

因此只要找到方向 `r` 满足

\[
h_C(r)-r^Td_0-h_S(r)>0,
\]

由于精确有理数 `det(F)=0.6999615978 != 0`，可取 `q_N=F^{-NT}r`，并有精确恒等式

\[
h_{E_N}(q_N)-h_S(q_N)
=h_C(r)-r^Td_0-h_S(r)>0.
\]

这直接否定 `E_N(d0) subseteq S`。

## 2. 证书构造与可靠性边界

浮点搜索只提出方向

\[
r=(-0.13945649,-0.00417764,-0.39679891,-0.90724035)^T
\]

和一个 posterior latent witness。验证器随后把所有 binary64 数据按 `as_integer_ratio()` 解释为精确有理数，并执行：

1. 用精确 `F,G,D0` 重建预期有理数合同的 602 个生成元及三次测量条带的**历史 latent 顺序**；测试仅用来核对顺序。它不宣称与 NumPy binary64 数组逐位相同：最大生成元/测量系数差均为 `5.21e-17`，结果中明确列为诊断量，正式证书只在显式有理数合同上计算。
2. 将 LP witness 沿零点缩放至 `0.9999980644488757`；零点严格满足所有条带。精确重算后最大条带超额为 `-2.13e-17`，最大 box 超额为 `-1.94e-6`，故 witness 确实属于 `C`。
3. witness 给出 `h_C(r)` 的可靠**下界** `0.5034606187289715`；这不依赖浮点 LP 达到最优。
4. 复用 Run-120 的 `M=139` block contraction，对前 600 项精确求和并对无限尾作几何上界，得到 `h_S(r)` 的可靠**上界** `0.5034735472948262`。
5. `r^T d0=-0.0023856140067776872`。最终精确有理数差的十进制显示为

\[
0.5034606187289715-(-0.0023856140067777)-0.5034735472948262
=0.0023726854409230>0.
\]

比较符号直接在 `Fraction` 上判定；分子/分母分别约 16496/16505 bits，JSON 只记录位数和十进制显示。结果同时保存 602 维原始 witness、方向和 `d0` 的 `float.hex()`；`replay_archived_certificate()` 不调用优化器即可重建缩放、成员检查和严格间隔。

## 3. 结论与证据等级

- **精确有理数反例：** 实际 Run-124 binary64 非零重定心在冻结精确有理数模型下满足 `C-d0 not subseteq S`，并由上式推出 `E_N(d0) not subseteq S`。
- **因此否定：** “300 条阶段约束通过 + nominal 终点归零”不足以使该候选满足固定 mRPI 终端合同；Run-124 整体准入不是仅缺证明，而是该具体候选为假。
- **仍成立：** Run-124 的 300 行 H-template 外包含和列入方向支持认证；它可保留为固定复杂度压缩基线。
- **不外推：** 本反例不证明所有非零重定心都不可能，也不证明更换 terminal contract 后不可能。但继续调小该射线或增加阶段方向只会回到局部修补，不能形成硕士课题贡献，故停止该支线。
- **模型边界：** 只适用于冻结 Run-93/119 四状态线性合同，不是六自由度非线性四旋翼保证。

## 4. 文献准入后的方向纠正

Sadraddini–Tedrake 的 AH-in-AH 线性编码能给有限 mRPI 内近似的包含充分证书，但不可行不是反例；本轮已有严格分离，无须再解一个不完备的大 LP。Kouramas–Raković–Kerrigan–Allwright–Mayne 的缩放外 RPI 近似要求满维 C-set 扰动，而当前 `W` 是四维中的秩一线段；且外近似方向不能补原 mRPI 内包含。

本轮重新检索到 Robbins 等 ACC 2026 的 IEEE PDF 地址，但抓取返回 HTTP 418，仍未完成全文精读，故不据摘要断言 300 行模板优于其在线外包。

## 5. 实现、失败修正与复现

新增：

- `verification/check_run125_terminal_separation.py`
- `verification/test_run125_terminal_separation.py`
- `results/controller_direction_closure_20260928/run125_terminal_separation.json`
- `verification/check_run123_two_time_shift.py` 与对应测试增加 `ACADEMIC_RESEARCH_NO_WRITE=1` 执行路径，避免全量回归因 SLSQP 浮点末位差异改写历史 JSON。

测试先固定标量几何级数的 exact block-tail、二维有符号非正规系统的尾界上包、Run-123 latent 顺序、`q_N=F^{-NT}r` 的精确恒等式、实际候选严格分离及存档 witness 的无求解器重放。初版合同重建误把历史测量行按当前生成元重算；latent-order 对照测试按预期失败，随后修正为继承旧测量系数并追加零列。这一修正不改变最终严格反例。

复现命令：

```bash
python -m unittest verification.test_run125_terminal_separation -v
python verification/check_run125_terminal_separation.py
python -m unittest discover -s verification -p 'test_*.py' -v
python verification/check_run120_terminal_rpi_support.py
```

## 6. 论文级主线审视与下一唯一问题

非零重定心没有闭合终端，因此不能作为主线创新；300 行模板目前只解决固定方向安全压缩，也不足以单独构成课题。下一轮唯一问题：**取得并精读 Robbins 等 ACC 2026 全文的算法/复杂度/实验章节，在冻结 Run-119 相同信息、扰动、硬约束和实际在线预算下，定义并复现其 zonotope 外包/在线收紧强基线；若全文仍不可得，则明确未知项并先用 Scott 2016 安全 CZ 外包作可实现替代基线。** 不再继续 Run-124 重定心射线。
